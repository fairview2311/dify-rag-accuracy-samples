"""SharePoint（Teams のチームのファイル）の Word・Excel・CSV を、Dify のナレッジに同期する。

- 新しいファイルは追加し、更新されたファイルは置き換え、無くなったファイルは削除する
- 前回の同期の状態は sync_state_<ナレッジ ID の先頭8文字>.json に保存する（ファイルの更新日時で変更を判断する）
- SharePoint の「状態」の列を、Dify のメタデータ「状態」に反映する（列が空なら「有効」）
- SharePoint のファイルのリンクを、Dify のメタデータ「出典」に反映する
- Microsoft 365 へのサインインはデバイス コード（初回だけ。トークンは token_cache.json に保存する）
"""
import csv
import io
import json
import os
import pathlib
import re

import docx
import msal
import openpyxl
import requests

TENANT_ID = os.environ["TENANT_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]
TEAM_ID = os.environ["TEAM_ID"]
FOLDERS = os.environ.get("FOLDERS", "規程").split(",")
DIFY_URL = os.environ.get("DIFY_URL", "http://localhost")
DATASET_ID = os.environ["DIFY_DATASET_ID"]
DIFY_KEY = os.environ["DIFY_API_KEY"]

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "token_cache.json"
STATE = HERE / f"sync_state_{DATASET_ID[:8]}.json"
GRAPH = "https://graph.microsoft.com/v1.0"
EXTS = (".docx", ".xlsx", ".csv")


def graph_token() -> str:
    cache = msal.SerializableTokenCache()
    if CACHE.exists():
        cache.deserialize(CACHE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=cache
    )
    scopes = ["Files.Read.All", "Sites.Read.All"]
    accounts = app.get_accounts()
    result = app.acquire_token_silent(scopes, account=accounts[0]) if accounts else None
    if not result:
        flow = app.initiate_device_flow(scopes=scopes)
        print(flow["message"], flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if cache.has_state_changed:
        CACHE.write_text(cache.serialize())
    return result["access_token"]


def to_text(name: str, data: bytes) -> str:
    if name.endswith(".docx"):
        doc = docx.Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    if name.endswith(".xlsx"):
        lines = []
        book = openpyxl.load_workbook(io.BytesIO(data), data_only=True)
        for ws in book.worksheets:
            for row in ws.iter_rows(values_only=True):
                cells = [str(c) for c in row if c is not None]
                if cells:
                    lines.append("\t".join(cells))
        return "\n".join(lines)
    rows = csv.reader(io.StringIO(data.decode("utf-8-sig")))
    return "\n".join("\t".join(r) for r in rows if r)


def list_files(gh: dict) -> list:
    files = []
    for folder in FOLDERS:
        url = (f"{GRAPH}/groups/{TEAM_ID}/drive/root:/{folder}:/children"
               "?$select=id,name,lastModifiedDateTime,webUrl&$expand=listItem($expand=fields)")
        items = requests.get(url, headers=gh, timeout=30).json()["value"]
        files += [f for f in items if f["name"].endswith(EXTS)]
    return files


def column(f: dict, name: str) -> str:
    fields = f["listItem"]["fields"]
    for key, value in fields.items():
        if re.sub(r"_x([0-9a-f]{4})_", lambda m: chr(int(m.group(1), 16)), key) == name:
            return value
    return ""


def field(dh: dict, name: str) -> str:
    url = f"{DIFY_URL}/v1/datasets/{DATASET_ID}/metadata"
    for m in requests.get(url, headers=dh, timeout=30).json()["doc_metadata"]:
        if m["name"] == name:
            return m["id"]
    r = requests.post(url, headers=dh, json={"type": "string", "name": name}, timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def main() -> None:
    gh = {"Authorization": f"Bearer {graph_token()}"}
    dh = {"Authorization": f"Bearer {DIFY_KEY}"}
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    files = list_files(gh)
    status_id = field(dh, "状態")
    url_id = field(dh, "出典")

    seen = set()
    for f in files:
        seen.add(f["name"])
        old = state.get(f["name"])
        status = column(f, "状態") or "有効"
        if (old and old["modified"] == f["lastModifiedDateTime"] and old.get("status") == status
                and old.get("url") == f["webUrl"]):
            continue
        url = f"{GRAPH}/groups/{TEAM_ID}/drive/items/{f['id']}/content"
        data = requests.get(url, headers=gh, timeout=60).content
        text = f"出典: {f['webUrl']}\n\n" + to_text(f["name"], data)
        body = {"name": f["name"], "text": text, "indexing_technique": "high_quality",
                "process_rule": {"mode": "automatic"}}
        base = f"{DIFY_URL}/v1/datasets/{DATASET_ID}"
        if old:
            r = requests.post(f"{base}/documents/{old['document_id']}/update-by-text",
                              headers=dh, json=body, timeout=60)
            action = "更新"
        else:
            r = requests.post(f"{base}/document/create-by-text", headers=dh, json=body, timeout=60)
            action = "追加"
        r.raise_for_status()
        doc_id = r.json()["document"]["id"]
        meta = {"document_id": doc_id, "metadata_list": [
            {"id": status_id, "name": "状態", "value": status},
            {"id": url_id, "name": "出典", "value": f["webUrl"]},
        ]}
        requests.post(f"{base}/documents/metadata", headers=dh, json={"operation_data": [meta]},
                      timeout=30).raise_for_status()
        state[f["name"]] = {"modified": f["lastModifiedDateTime"], "document_id": doc_id,
                            "status": status, "url": f["webUrl"]}
        print(f"{action}: {f['name']}（状態: {status}）")

    for name in [n for n in state if n not in seen]:
        requests.delete(f"{DIFY_URL}/v1/datasets/{DATASET_ID}/documents/{state[name]['document_id']}",
                        headers=dh, timeout=30)
        del state[name]
        print(f"削除: {name}")

    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1))
    print(f"同期しました（SharePoint のファイル {len(files)} 本）")


if __name__ == "__main__":
    main()
