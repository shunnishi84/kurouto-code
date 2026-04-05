# バックエンド（Lambda）

## 概要

AWS Lambda + API Gateway (HTTP API) で構成されるサーバーレスバックエンドです。  
フロントエンドからのリクエストを受け取り、プロンプトの内容に応じた説教テキストをランダムに返します。

## 技術スタック

| 技術 | 用途 |
|---|---|
| Python 3.12 | Lambda ランタイム |
| AWS Lambda | サーバーレス関数実行 |
| API Gateway (HTTP API) | REST エンドポイント・CORS 管理 |

## ファイル構成

```
lambda/
├── handler.py         # Lambda ハンドラー（エントリーポイント）
└── rants/             # 説教テキスト定義パッケージ
    ├── __init__.py    # 全モジュールの re-export
    ├── general.py     # 汎用説教（14パターン）
    ├── python.py      # Python 関連説教（5パターン）
    ├── go.py          # Go 言語関連説教（5パターン）
    ├── javascript.py  # JavaScript / TypeScript 関連説教（5パターン）
    ├── java.py        # Java 関連説教（3パターン）
    ├── rust.py        # Rust 関連説教（2パターン）
    ├── sql.py         # SQL 関連説教（2パターン）
    ├── oop.py         # オブジェクト指向否定説教（5パターン）
    └── easter_eggs.py # イースターエッグ用コード（FizzBuzz・フィボナッチ・Hello World）
```

## API 仕様

### `POST /rant`

プロンプトを受け取り、説教テキストを返します。

**リクエストボディ**

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `prompt` | string | ✅ | ユーザーの入力テキスト |
| `exchange_count` | number | | やり取り回数（怒りモード判定に使用） |

**レスポンスボディ**

| フィールド | 型 | 説明 |
|---|---|---|
| `rant` | string | 説教テキスト |
| `angry` | boolean | 怒りモード発動フラグ |

## ロジック詳細

### 言語検知

`handler.py` の `LANG_PATTERNS` に正規表現とランツリストのペアを定義しています。  
プロンプトを小文字化して順番に照合し、最初にヒットした言語の説教リストを使用します。  
どれにもヒットしない場合は `RANTS_GENERAL` にフォールバックします。

### イースターエッグ

以下のキーワードが含まれる場合、専用の C 言語コードを返します。

| キーワード | 内容 |
|---|---|
| `ハローワールド` / `hello world` など | ビットシフトで `Hello.world` を出力するコード |
| `フィボナッチ数列` | 深いネストのメモ化再帰コード |
| `fizzbuzz` / `fizz buzz` | 無駄にネストした FizzBuzz コード |

### 怒りモード

`exchange_count >= 3` のとき、一定確率で `angry: true` を返します。

| やり取り回数 | 発動確率 |
|---|---|
| 3〜4 回 | 25% |
| 5 回以上 | 50% |

## デプロイ

GitHub Actions（`.github/workflows/deployment.yml`）により、`main` ブランチへのプッシュ時に自動デプロイされます。
