"""質問集の質問を Dify のナレッジで検索し、正しい文書が何位に来たかを数える。

使い方: python evaluate.py 質問集.csv 結果.csv
- 環境変数 DIFY_URL・DIFY_DATASET_ID・DIFY_API_KEY を使う
- 検索の設定はナレッジの「検索設定」のまま（ナレッジの画面で変えた設定がそのまま測れる）
- 正しい根拠の文書が空の質問（答えが規程に無い質問）は、点数に入れない
"""
import csv
import os
import sys

import requests

DIFY_URL = os.environ.get("DIFY_URL", "http://localhost")
DATASET_ID = os.environ["DIFY_DATASET_ID"]
DIFY_KEY = os.environ["DIFY_API_KEY"]


def search(query: str) -> list:
    url = f"{DIFY_URL}/v1/datasets/{DATASET_ID}/retrieve"
    r = requests.post(url, headers={"Authorization": f"Bearer {DIFY_KEY}"},
                      json={"query": query}, timeout=60)
    r.raise_for_status()
    names = []
    for rec in r.json()["records"]:
        name = rec["segment"]["document"]["name"].rsplit(".", 1)[0]
        if name not in names:
            names.append(name)
    return names


def main() -> None:
    src, out = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    top1 = top3 = total = 0
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["質問", "正しい文書", "順位", "1位の文書"])
        for row in rows:
            want = row["正しい根拠の文書"].split("/")[-1]
            if not want:
                continue
            total += 1
            names = search(row["質問"])
            rank = names.index(want) + 1 if want in names else 0
            top1 += rank == 1
            top3 += 1 <= rank <= 3
            w.writerow([row["質問"], want, rank or "圏外", names[0] if names else ""])
    print(f"質問 {total} 問: 1位 {top1} 問・3位以内 {top3} 問")


if __name__ == "__main__":
    main()
