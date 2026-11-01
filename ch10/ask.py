"""質問集の質問を、Dify のチャットフロー（Web アプリと同じアプリ）に聞き、答えを数える。

使い方: python ask.py 質問集.csv 答え.csv
- 環境変数 DIFY_URL・DIFY_APP_KEY（アプリの API キー。app- で始まる）を使う
- 「答えに入る語」が答えに入っていれば「正しい」、総務部に送った答えなら「総務部へ」と数える
- 答えの無い質問は、総務部に送れば正しい扱い。総務部に送ると、Teams のチャネルにも投稿される
"""
import csv
import os
import sys

import requests

DIFY_URL = os.environ.get("DIFY_URL", "http://localhost")
APP_KEY = os.environ["DIFY_APP_KEY"]
SENT = "総務部の Teams のチャネルに送りました"


def ask(query: str) -> str:
    r = requests.post(f"{DIFY_URL}/v1/chat-messages", headers={"Authorization": f"Bearer {APP_KEY}"},
                      json={"inputs": {}, "query": query, "response_mode": "blocking", "user": "ask-py"},
                      timeout=120)
    r.raise_for_status()
    return r.json()["answer"]


def main() -> None:
    src, out = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    right = sent = 0
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["質問", "答えに入る語", "判定", "答え"])
        for row in rows:
            answer = ask(row["質問"])
            word = row["答えに入る語"].replace(",", "")
            if SENT in answer:
                sent += 1
                result = "総務部へ（正しい）" if not row["正しい根拠の文書"] else "総務部へ（答えがあるのに）"
            elif word in answer.replace(",", ""):
                right += 1
                result = "正しい"
            else:
                result = "違う"
            w.writerow([row["質問"], row["答えに入る語"], result, answer])
            print(f"{result}: {row['質問']}")
    print(f"質問 {len(rows)} 問: 正しい答え {right} 問・総務部へ {sent} 問")


if __name__ == "__main__":
    main()
