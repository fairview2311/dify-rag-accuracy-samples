#!/bin/bash
export TENANT_ID="テナント ID"
export CLIENT_ID="クライアント ID"
export TEAM_ID="チームの ID"
export FOLDERS="規程,手順,過去の問い合わせ"
export DIFY_URL="http://localhost"
export DIFY_DATASET_ID="ナレッジの ID"
export DIFY_API_KEY="dataset-で始まるキー"
cd "$(dirname "$0")"
echo "=== $(date '+%Y-%m-%d %H:%M:%S')" >> sync.log
.venv/bin/python sp_sync.py >> sync.log 2>&1
