# 第13章　毎月の効果をまとめて、上司に報告する

本の第13章を終えた時点のファイルです。本のコードの枠の上の「サンプルコード　ch13/…」は、このフォルダーのファイルを指します。このフォルダーには、それまでの章で使ったファイルもすべて入っています。

この章でできるようになること:

- 毎月の件数を、総務部のチームの Excel「社内業務AIの月次の件数.xlsx」に記録し、上司への報告のメールにできる

## この章での使い方

コマンドは、Windows は PowerShell、Mac はターミナルで実行します。サンプルコードはホームのフォルダーに `dify-rag-accuracy-samples-main` として展開し、作業用のフォルダー（`sp_sync`・`evaluate`・`report`）もホームのフォルダーに作ってある前提です（[リポジトリのトップ](../README.md)の「フォルダーの置き場所」）。環境変数は、トップの README の「毎回の入力を省く（おすすめ）」のとおりに保存しておくと、PowerShell やターミナルを開き直すたびに設定し直す必要がありません。

1. ホームのフォルダーに `report` フォルダーを作り、このフォルダーの `find_ids.py` をコピーします。

2. `report` フォルダーで実行し、Excel のファイルの ID とサイトの ID を調べます。環境変数 `TENANT_ID`・`CLIENT_ID`・`TEAM_ID` は第3章の値です。

   Windows（PowerShell）:

   ```text
   cd $HOME\report
   ..\sp_sync\.venv\Scripts\python.exe find_ids.py
   ```

   Mac（ターミナル）:

   ```text
   cd ~/report
   ../sp_sync/.venv/bin/python find_ids.py
   ```

3. このフォルダーの `monthly_report.yml` を、テキストエディターで開きます。`value: ファイルの ID` と `value: サイトの ID` の2か所を、表示された値に書き換えて上書き保存します。サイトの ID は、値の前後を `'` で囲みます。

4. Dify の「スタジオ」の［作成］→［アプリをインポート］で `monthly_report.yml` を読み込み、公開します。Excel 365・Markdownエクスポーター・Outlook のプラグインを使います。

## うまくいったかの確かめ方

- `find_ids.py` が「ファイルの ID」と「サイトの ID」を表示する
- Web アプリで実行すると、Excel に1か月分の行が追加され、報告の下書きができる

動作しないときは、本の第13章の「うまくいかないとき」を見てください。

<details>
<summary>第12章からの変更（追加・変更したファイル 2 個）</summary>

- 追加: [`find_ids.py`](find_ids.py)
- 追加: [`monthly_report.yml`](monthly_report.yml)

</details>

← [ch12](../ch12)　｜　[一覧](../README.md)　｜　[ch14](../ch14) →
