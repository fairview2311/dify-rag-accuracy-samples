# 第6章　古い版と過去の問い合わせを、検索の対象から外す

本の第6章を終えた時点のファイルです。本のコードの枠の上の「サンプルコード　ch06/…」は、このフォルダーのファイルを指します。このフォルダーには、それまでの章で使ったファイルもすべて入っています。

この章でできるようになること:

- 同期のときに、文書の「状態」（有効・廃止・参考）をナレッジのメタデータに書き込める
- `STATUS` を「有効」にして測ると、旧版や過去の問い合わせを除いて検索できる

## この章での使い方

コマンドは、Windows は PowerShell、Mac はターミナルで実行します。サンプルコードはホームのフォルダーに `dify-rag-accuracy-samples-main` として展開し、作業用のフォルダー（`sp_sync`・`evaluate`・`report`）もホームのフォルダーに作ってある前提です（[リポジトリのトップ](../README.md)の「フォルダーの置き場所」）。環境変数は、トップの README の「毎回の入力を省く（おすすめ）」のとおりに保存しておくと、PowerShell やターミナルを開き直すたびに設定し直す必要がありません。

1. このフォルダーの `sp_sync.py` を、ホームの `sp_sync` フォルダーにコピーして上書きします（本の5つの直しを済ませたファイルです）。続けて、`sp_sync` フォルダーで `sp_sync.py` を実行し直します。1回目は 20 本すべてが「更新」になり、それぞれの状態が表示されます。

2. このフォルダーの `evaluate.py` を、ホームの `evaluate` フォルダーにコピーして上書きします。`STATUS` を空のまま測り、続けて「有効」にして測ります。

   Windows（PowerShell）:

   ```text
   cd $HOME\evaluate
   ..\sp_sync\.venv\Scripts\python.exe evaluate.py ..\dify-rag-accuracy-samples-main\data\質問集.csv 結果_第6章_前.csv
   $env:STATUS = "有効"
   ..\sp_sync\.venv\Scripts\python.exe evaluate.py ..\dify-rag-accuracy-samples-main\data\質問集.csv 結果_第6章_後.csv
   ```

   Mac（ターミナル）:

   ```text
   cd ~/evaluate
   ../sp_sync/.venv/bin/python evaluate.py ../dify-rag-accuracy-samples-main/data/質問集.csv 結果_第6章_前.csv
   export STATUS="有効"
   ../sp_sync/.venv/bin/python evaluate.py ../dify-rag-accuracy-samples-main/data/質問集.csv 結果_第6章_後.csv
   ```

## うまくいったかの確かめ方

- `結果_第6章_後.csv` の点数が、`結果_第6章_前.csv` より上がる

動作しないときは、本の第6章の「うまくいかないとき」を見てください。

<details>
<summary>第5章からの変更（追加・変更したファイル 2 個）</summary>

- 変更: [`evaluate.py`](evaluate.py)
- 変更: [`sp_sync.py`](sp_sync.py)

</details>

← [ch05](../ch05)　｜　[一覧](../README.md)　｜　[ch07](../ch07) →
