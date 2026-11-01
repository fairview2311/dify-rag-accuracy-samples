# 第3章　SharePoint の規程と手順書を取り込む

本の第3章を終えた時点のファイルです。本のコードの枠の上の「サンプルコード　ch03/…」は、このフォルダーのファイルを指します。このフォルダーには、それまでの章で使ったファイルもすべて入っています。

この章でできるようになること:

- SharePoint の規程と手順書（20 本）を、Dify のナレッジに同期できる
- SharePoint の文書を書き換えると、同期し直したときにその文書だけが更新される
- 毎朝 7 時に、同期が自動で実行される

## この章での使い方

コマンドは、Windows は PowerShell、Mac はターミナルで実行します。サンプルコードはホームのフォルダーに `dify-rag-accuracy-samples-main` として展開し、作業用のフォルダー（`sp_sync`・`evaluate`・`report`）もホームのフォルダーに作ってある前提です（[リポジトリのトップ](../README.md)の「フォルダーの置き場所」）。環境変数は、トップの README の「毎回の入力を省く（おすすめ）」のとおりに保存しておくと、PowerShell やターミナルを開き直すたびに設定し直す必要がありません。

1. ホームのフォルダーに作業用のフォルダー `sp_sync` を作り、このフォルダーの `sp_sync.py` をコピーします。

2. `sp_sync` フォルダーに移動し、Python の仮想環境を作って、4つのパッケージをインストールします。Python は 3.12 以降を使います。

   Windows（PowerShell）:

   ```text
   cd $HOME\sp_sync
   py -m venv .venv
   .venv\Scripts\python.exe -m pip install msal python-docx openpyxl requests
   ```

   Mac（ターミナル）:

   ```text
   cd ~/sp_sync
   python3 -m venv .venv
   .venv/bin/python -m pip install msal python-docx openpyxl requests
   ```

3. 7つの値を環境変数に設定して、同期を実行します。日本語の所は、`"` の中を自分の値に置き換えます。値の調べ方は本の第3章の「スクリプトに渡す値を調べる」にあります。初めて実行すると、サインインの案内が表示されるので、本の図3-14・図3-15 のとおりにサインインします。

   Windows（PowerShell）:

   ```text
   $env:TENANT_ID = "テナント ID"
   $env:CLIENT_ID = "クライアント ID"
   $env:TEAM_ID = "チームの ID"
   $env:FOLDERS = "規程,手順,過去の問い合わせ"
   $env:DIFY_URL = "http://localhost"
   $env:DIFY_DATASET_ID = "ナレッジの ID"
   $env:DIFY_API_KEY = "dataset-で始まるキー"
   $env:PYTHONIOENCODING = "utf-8"
   .venv\Scripts\python.exe sp_sync.py
   ```

   Mac（ターミナル）:

   ```text
   export TENANT_ID="テナント ID"
   export CLIENT_ID="クライアント ID"
   export TEAM_ID="チームの ID"
   export FOLDERS="規程,手順,過去の問い合わせ"
   export DIFY_URL="http://localhost"
   export DIFY_DATASET_ID="ナレッジの ID"
   export DIFY_API_KEY="dataset-で始まるキー"
   .venv/bin/python sp_sync.py
   ```

4. 毎朝の自動実行に使うファイルを、`sp_sync` フォルダーにコピーします。Windows は `run_sync.ps1`、Mac は `run_sync.sh` です。ファイルの中の日本語の値を、手順3と同じ値に書き換えて保存します。Windows のメモ帳では、［エンコード］で「UTF-8 (BOM 付き)」を選んで保存します。

5. Windows はタスク スケジューラに、Mac は launchd に登録します。Mac は、`com.example.sp-sync.plist` の `/Users/you/sp_sync` の `you` を自分のユーザー名に置き換えて、`~/Library/LaunchAgents` に置きます。`chmod 700 run_sync.sh` で `run_sync.sh` を実行できるようにしておきます。登録のコマンドは本の第3章の「毎朝自動で同期する」にあります。

6. これで、`run_sync.ps1`（Mac は `run_sync.sh`）に7つの値がそろいました。トップの README の「毎回の入力を省く（おすすめ）」のコマンドを1回実行して、環境変数を保存しておきます。第4章からは、PowerShell やターミナルを開き直しても、値を設定し直す必要がありません。

## うまくいったかの確かめ方

- 1回目の同期の最後に「同期しました（SharePoint のファイル 20 本）」と表示される
- Dify の「社内規程と手順書」のナレッジに、20 本の文書が「利用可能」で並ぶ
- 自動実行を試しに1回動かすと、`sp_sync` フォルダーの `sync.log` に「同期しました」の行が書かれる
- `token_cache.json`（サインインの情報）はパスワードと同じ扱いにします。共有のフォルダーや Git に置かないでください

動作しないときは、本の第3章の「うまくいかないとき」を見てください。

<details>
<summary>このフォルダーのファイル</summary>

第3章で作る同期のスクリプトと、毎朝の自動実行のファイルです。`run_sync.ps1` は Windows、`run_sync.sh` と `com.example.sp-sync.plist` は Mac で使います。

</details>

[一覧](../README.md)　｜　[ch04](../ch04) →
