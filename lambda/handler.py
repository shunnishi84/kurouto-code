import json
import random
import re

from rants import (
    RANTS_GENERAL,
    RANTS_PYTHON,
    RANTS_GO,
    RANTS_JS,
    RANTS_JAVA,
    RANTS_RUST,
    RANTS_SQL,
    RANTS_OOP,
    FIBONACCI_CODE,
    HELLO_WORLD_CODE,
    FIZZBUZZ_CODE,
)

# ── 言語キーワードマッピング ──────────────────────────────
LANG_PATTERNS = [
    (r"オブジェクト指向|oop\b|クラス設計|継承|ポリモーフィズム|カプセル化|デザインパターン|solid原則|singleton|dependency.inject|抽象クラス|インターフェース.*実装", RANTS_OOP),
    (r"python|pip|pandas|numpy|django|flask|pytorch|tensorflow|jupyter|\.py\b|def |lambda |print\(", RANTS_PYTHON),
    (r"golang|goroutine|go言語|\bgo\b.*\bfunc\b|\bchan\b|\bdefer\b|\.go\b|go mod|go get", RANTS_GO),
    (r"javascript|typescript|node\.?js|npm |react|vue|angular|\.js\b|\.ts\b|console\.log|async/await|webpack|babel", RANTS_JS),
    (r"java\b|spring|maven|gradle|\.java\b|nullpointer|@autowired|pom\.xml", RANTS_JAVA),
    (r"rust|cargo|ownership|borrow|lifetime|\.rs\b|rustc|tokio", RANTS_RUST),
    (r"\bsql\b|mysql|postgresql|sqlite|select.*from|join.*on|n\+1|orm\b|クエリ", RANTS_SQL),
]

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


def detect_language_rants(prompt: str):
    """プロンプトから言語を検出して該当説教リストを返す。なければ汎用を返す。"""
    lower = prompt.lower()
    for pattern, rants in LANG_PATTERNS:
        if re.search(pattern, lower):
            return rants
    return RANTS_GENERAL


def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": HEADERS, "body": ""}

    body = {}
    try:
        body = json.loads(event.get("body") or "{}")
    except Exception:
        pass

    prompt = body.get("prompt", "")
    exchange_count = int(body.get("exchange_count", 0))

    # ── イースターエッグ ──
    if re.search(r"ハローワールド|hello[, ]?world", prompt, re.IGNORECASE):
        return _ok(HELLO_WORLD_CODE, angry=False)

    if "フィボナッチ数列" in prompt:
        return _ok(FIBONACCI_CODE, angry=False)

    if re.search(r"fizzbuzz|fizz.?buzz", prompt.lower()):
        return _ok(FIZZBUZZ_CODE, angry=False)

    # ── 怒りモード（3回以降ランダム発動）──
    angry = False
    if exchange_count >= 3:
        threshold = 0.25 if exchange_count < 5 else 0.5
        angry = random.random() < threshold

    rant = random.choice(detect_language_rants(prompt))
    return _ok(rant, angry=angry)


def _ok(rant: str, angry: bool):
    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({"rant": rant, "angry": angry}, ensure_ascii=False),
    }
