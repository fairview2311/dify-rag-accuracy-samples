"""総務部のチームのファイルに、月次の記録の Excel を置き、ワークフローに書く2つの ID を表示する。

使い方: python find_ids.py
- 第3章の環境変数 TENANT_ID・CLIENT_ID・TEAM_ID と、sp_sync フォルダーの token_cache.json を使う
- 「社内業務AIの月次の件数.xlsx」がまだ無ければ、見出しの行だけの Excel を作って置く
"""
import io
import os
import pathlib

import msal
import openpyxl
import requests

TENANT_ID = os.environ["TENANT_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]
TEAM_ID = os.environ["TEAM_ID"]
CACHE = pathlib.Path(__file__).parent.parent / "sp_sync" / "token_cache.json"
GROUP = f"https://graph.microsoft.com/v1.0/groups/{TEAM_ID}"
NAME = "社内業務AIの月次の件数.xlsx"
HEAD = ["月", "規程の質問", "総務部へ回した質問", "返信の下書き（回）", "申請の確認（回）",
        "改定のお知らせ（回）", "受け入れの資料（回）"]


def token() -> str:
    cache = msal.SerializableTokenCache()
    if CACHE.exists():
        cache.deserialize(CACHE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=cache
    )
    scopes = ["Files.ReadWrite.All", "Sites.Read.All"]
    accounts = app.get_accounts()
    result = app.acquire_token_silent(scopes, account=accounts[0]) if accounts else None
    if not result:
        flow = app.initiate_device_flow(scopes=scopes)
        print(flow["message"], flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if cache.has_state_changed:
        CACHE.write_text(cache.serialize())
    return result["access_token"]


def main() -> None:
    h = {"Authorization": f"Bearer {token()}"}
    r = requests.get(f"{GROUP}/drive/root:/{NAME}", headers=h, timeout=30)
    if r.status_code == 404:
        wb = openpyxl.Workbook()
        wb.active.title = "月次"
        wb.active.append(HEAD)
        buf = io.BytesIO()
        wb.save(buf)
        r = requests.put(f"{GROUP}/drive/root:/{NAME}:/content", data=buf.getvalue(), timeout=60,
                         headers={**h, "Content-Type": "application/octet-stream"})
        print(f"{NAME} を作りました")
    r.raise_for_status()
    site = requests.get(f"{GROUP}/sites/root?$select=id", headers=h, timeout=30).json()
    print(f"ファイルの ID: {r.json()['id']}")
    print(f"サイトの ID: {site['id']}")


if __name__ == "__main__":
    main()
