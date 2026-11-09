# 第4章　質問集を作って、最初の点数を測る

本の第4章を終えた時点のファイルです。本のコードの枠の上の「サンプルコード　ch04/…」は、このフォルダーのファイルを指します。このフォルダーには、それまでの章で使ったファイルもすべて入っています。

この章でできるようになること:

- 質問集の 30 問（うち点数に入れるのは 29 問）でナレッジを検索し、正しい文書が何位に来たかを数えられる

## この章での使い方

コマンドは、Windows は PowerShell、Mac はターミナルで実行します。サンプルコードはホームのフォルダーに `dify-rag-accuracy-samples-main` として展開し、作業用のフォルダー（`sp_sync`・`evaluate`・`report`）もホームのフォルダーに作ってある前提です（[リポジトリのトップ](../README.md)の「フォルダーの置き場所」）。環境変数は、トップの README の「毎回の入力を省く（おすすめ）」のとおりに保存しておくと、PowerShell やターミナルを開き直すたびに設定し直す必要がありません。

1. ホームのフォルダーに `evaluate` フォルダーを作り、このフォルダーの `evaluate.py` をコピーします。

2. `evaluate` フォルダーに移動して実行します。パッケージは、第3章で `sp_sync` の仮想環境にインストールしたものを使います。環境変数 `DIFY_URL`・`DIFY_DATASET_ID`・`DIFY_API_KEY` は、第3章で設定した値です。第3章の後で環境変数を保存していれば、そのまま実行できます。保存していないときは、PowerShell かターミナルを開き直すたびに、第3章の手順3のうち、この3行（Windows は `PYTHONIOENCODING` の行も）を設定し直します。

   Windows（PowerShell）:

   ```text
   cd $HOME\evaluate
   ..\sp_sync\.venv\Scripts\python.exe evaluate.py ..\dify-rag-accuracy-samples-main\data\質問集.csv 結果_第4章.csv
   ```

   Mac（ターミナル）:

   ```text
   cd ~/evaluate
   ../sp_sync/.venv/bin/python evaluate.py ../dify-rag-accuracy-samples-main/data/質問集.csv 結果_第4章.csv
   ```

## うまくいったかの確かめ方

- 数秒で 29 問の検索が終わり、最後に点数が表示される
- `evaluate` フォルダーに `結果_第4章.csv` ができ、1問ごとに正しい文書の順位が書かれている

動作しないときは、本の第4章の「うまくいかないとき」を見てください。

<details>
<summary>第3章からの変更（追加・変更したファイル 1 個）</summary>

- 追加: [`evaluate.py`](evaluate.py)

</details>

← [ch03](../ch03)　｜　[一覧](../README.md)　｜　[ch05](../ch05) →
