# 玄人コード

> エイプリルフール版 Claude Code — どんな質問にもじじいが説教で答えるジョークアプリ

## 概要

Claude Code の UI を模したターミナル風チャットアプリです。  
プロンプトを送信すると、AIの代わりに「玄人（じじい）」が説教を返します。  
Python / Go / JavaScript など言語別の説教や、FizzBuzz・フィボナッチ数列などのイースターエッグも搭載しています。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| フロントエンド | HTML / CSS / Vanilla JS（S3 静的ホスティング） |
| バックエンド | Python 3.12 / AWS Lambda / API Gateway (HTTP API) |
| CDN / HTTPS | Amazon CloudFront |
| インフラ | AWS（Lambda・API Gateway・S3・CloudFront） |
| CI/CD | GitHub Actions |

## ディレクトリ構成

```
.
├── frontend/          # S3にホスティングする静的ファイル
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── lambda/            # AWS Lambda 関数
│   ├── handler.py
│   └── rants/         # 説教テキスト定義
│       ├── general.py
│       ├── python.py
│       ├── go.py
│       ├── javascript.py
│       ├── java.py
│       ├── rust.py
│       ├── sql.py
│       ├── oop.py
│       └── easter_eggs.py
├── kurouto.py         # CLIで動かすスタンドアロン版
└── .github/
    └── workflows/
        └── deployment.yml
```

## 各ディレクトリの詳細

- [frontend/README.md](frontend/README.md) — フロントエンド詳細
- [lambda/README.md](lambda/README.md) — バックエンド詳細
