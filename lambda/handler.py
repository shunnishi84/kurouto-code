import json
import random
import re

# ── 汎用説教 ──────────────────────────────────────────────
RANTS_GENERAL = [
    "まったく最近の若いもんは、コードも書こうとしない。\nワシが若い頃はな、エディタどころかIDEすら満足になかった。\nviのインサートモードだけで何千行も書いたもんじゃ。\nそれがどうじゃ、今は「AIに聞けばええ」か。\n指が腐るぞ、指が。",

    "ほう、またAIに頼ろうとしておるのか。\nワシが若い頃はスタックオーバーフローどころか\nインターネット自体なかったんじゃぞ。\nわからんことがあればな、分厚い技術書を\n図書館まで借りに行ったもんじゃ。\n徒歩でな。",

    "情けない。まったく情けない。\nエラーメッセージが出たら自分で読め。\nワシなんぞ、コアダンプを16進数で\n読んでデバッグしておったんじゃ。\nそれに比べてお前さんのエラーは\n日本語で書いてあるじゃないか。\n贅沢にもほどがある。",

    "コードが書けないなら手を動かせ。\nワシの師匠はな、「プログラムは体で覚えろ」と言っておった。\n毎朝ソートアルゴリズムを写経するところから始めたもんじゃ。\nバブルソートを1000回書いて初めて\n「アルゴリズムとは何か」がわかるんじゃ。\nAIに聞いて何がわかる？何もわからんぞ。",

    "フン。また「玄人コード」に頼りに来たか。\n昔はな、コンピュータは部屋いっぱいの大きさで\nパンチカードでプログラムを入力したもんじゃ。\nカードを1枚落としたら最初からやり直しじゃ。\nそれでも誰一人AIに頼ろうなんて言わんかった。\n根性というものがあったからな。\nお前さんにその根性はあるか？ないじゃろ？",

    "GitHubじゃと？ワシが若い頃はバージョン管理なんぞなかった。\nファイル名の末尾に「_最終版」「_最終版2」「_本当に最終版」と\nつけるのがバージョン管理じゃったんじゃ。\nそれでも誰もシステムに怒鳴り込まなかった。\n今のもんは、pushひとつできんとすぐ泣き言を言う。\n情けないのう。",

    "ライブラリじゃと？npmじゃと？\nワシが若い頃はな、必要な機能は全部自分で書いたんじゃ。\nソートも、ハッシュも、ネットワーク通信も、全部じゃ。\n「車輪の再発明」などと言うが、\n車輪を一度も作ったことがない者に\n車輪のなんたるかがわかるか？わからんじゃろ。",

    "テストを書け、じゃと？ワシらの時代にテストなんぞなかった。\n本番環境にデプロイして動かしてみるのがテストじゃった。\n落ちたら原因を探して直す。それだけじゃ。\nそうやってワシは鍛えられた。\n今のもんはテストなしではコードも書けんのか。\n軟弱になったもんじゃのう。",

    "クラウドじゃと？サーバーレスじゃと？\nワシが若い頃はな、データセンターに\n物理的に乗り込んでサーバーを手で叩いたもんじゃ。\n「再起動します」と言いながら電源ボタンをポチッとな。\nその一押しの重みがお前さんにわかるか？\nわからんじゃろ、画面しか触ったことがないから。",

    "「コードレビューしてほしい」じゃと？\nワシが若い頃はコードレビューなどなかった。\n先輩に見せたら「動くんか？」の一言じゃ。\n「動きます」と答えたら「ならええ」で終わりじゃ。\nシンプルじゃろ。今のもんはああでもないこうでもないと\n議論ばかりして一行もコードが進まんのじゃ。",

    "メモリ管理を任せるじゃと？\nガベージコレクションに頼っておるのか。\nワシが若い頃はmallocしたらfreeするのは当たり前じゃ。\nメモリリークを出したら先輩に正座させられたもんじゃ。\nそのおかげでワシはポインタの夢を見るほど\nポインタと仲良くなれた。お前さんはどうじゃ？",

    "ドキュメントがないじゃと？\nワシが若い頃はドキュメントなどなかった。\nソースコードがドキュメントじゃ。\n読めばわかる。読めばな。\n読もうともせずにAIに聞く前に\nまずそのソースコードを読んでみなさい。\n1万行くらい読んだら少しはわかるじゃろ。",

    "フレームワークじゃと？Reactじゃと？Nextじゃと？\nワシが若い頃はHTMLを素手で書いたもんじゃ。\ntableタグでレイアウトを組んで、\nfontタグで色を変えて、それが普通じゃった。\nそれでも立派なウェブサイトができた。\n今のもんは道具がなければ何もできんのか。\n道具に使われておるんじゃぞ、お前さんは。",

    "締め切りに間に合わないじゃと？\nワシが若い頃は徹夜など当たり前じゃった。\n3日3晩寝ずにコードを書いたこともある。\n目が充血して画面が二重に見えても\nキーボードを叩き続けたもんじゃ。\n今のもんは定時で帰りたいなどと言う。\n定時？定時とはなんじゃ？辞書で調べてみなさい。",
]

# ── Python説教 ────────────────────────────────────────────
RANTS_PYTHON = [
    "Pythonじゃと？ワシが若い頃はそんな軟な言語はなかった。\nCでポインタを手書きしてメモリを直接叩いたもんじゃ。\nインデントエラーで悩むとは、何という贅沢な悩みじゃ。\nワシなんぞセグメンテーション違反と毎朝格闘しておった。\n感謝しなさい、インデントエラーくらいで泣くでない。",

    "pip installじゃと？ライブラリに頼るな。\nワシが若い頃はpandasもnumpyもなかった。\n行列計算は全部自分でゼロから書いたんじゃ。\nそれがどうじゃ、今はimport一発で何でも揃うか。\n便利すぎて脳みそが溶けてしまうぞ。",

    "「Pythonが遅い」じゃと？当たり前じゃ。\nワシが若い頃はアセンブリで書いておった。\n1命令1命令、レジスタに直接値を詰めてな。\nそれに比べればPythonなんぞ10倍遅くても\n文句を言える立場ではないんじゃぞ。\n速さが欲しければCを書きなさい。",

    "Jupyter Notebookじゃと？\nワシが若い頃はターミナルにコードを直打ちしておった。\n実行結果はテキストファイルに手でメモしてな。\nグラフ？紙に手書きじゃ。\nそれでも立派な研究成果が出せたんじゃ。\n今のもんはツールがなければ何もできんのか。",

    "型ヒントを書かんのか？\nDynamically typedだから何でも許されると思っておるのか。\nワシが若い頃は型を一文字間違えただけで\nコンパイラに怒鳴られたもんじゃ。\nそのおかげで型というものを骨の髄まで理解できた。\nPythonだからこそ、ちゃんと型を書きなさい。",
]

# ── Go説教 ────────────────────────────────────────────────
RANTS_GO = [
    "goroutineが理解できんのか？\nワシが若い頃はスレッドを手動で管理しておった。\nmutexもsemaphoreも自分でゼロから実装してな。\nデッドロックが起きたら朝まで原因を探したもんじゃ。\nそれに比べてgoroutineは何と楽なことか。\nchannelで詰まるくらいで泣き言を言うな。",

    "エラーハンドリングがめんどうじゃと？\nGo言語のif err != nilがうっとうしいじゃと？\nワシが若い頃はエラーコードを自分で定義して\n戻り値を全部手でチェックしておった。\n例外処理？そんなものはなかった。\n丁寧にエラーを扱うのは当然のことじゃ、文句を言うな。",

    "モジュールが解決できんのか？\nGOPATHがどうのと言っておるのか。\nワシが若い頃はパッケージ管理など存在しなかった。\nソースコードをダウンロードして\n手でコピーしてビルドしたんじゃ。\ngo getひとつでライブラリが入るのに文句を言うとは\n罰当たりな。",

    "interfaceが理解できんと？\nワシが若い頃はポリモーフィズムを\nvtableを手で書いて実現しておった。\nそれがどうじゃ、Go言語は勝手にinterfaceを満たしてくれる。\n暗黙的で便利じゃろ。その便利さに感謝しなさい。",

    "Goのコンパイルが速いのが当たり前じゃと思っておるか？\nワシが若い頃はC++のコンパイルに30分かかっておった。\nコンパイル待ちの間にお茶を飲んで、\n廊下を散歩して、それでもまだ終わらなかった。\nGo言語が数秒でビルドできるのは\n設計者たちの血と汗の賜物じゃ。\n大切に使いなさい。",
]

# ── JavaScript / TypeScript説教 ──────────────────────────
RANTS_JS = [
    "node_modulesが何GBあるんじゃ。\nnpm installしたら2GBとな？\nワシが若い頃はプログラム全体が数KBじゃった。\nフロッピーディスク1枚に全部収まっておったんじゃ。\nそれがどうじゃ、今は依存ライブラリだけで\nブラックホールができそうじゃ。",

    "console.logでデバッグか？\nワシが若い頃はprintfデバッグが唯一の手段じゃった。\nそれでも今のもんと同じことをしておるではないか。\n50年経っても人間のやることは変わらん。\nまあそれはよい。せめてdebuggerを使いなさい。",

    "TypeScriptに移行したいじゃと？\n当然じゃ、当然すぎる。\nJavaScriptは型なしで何でも通してしまう危険な言語じゃ。\nワシが若い頃はそんな危なっかしいものは\n本番環境には使わなかった。\nTypeScriptを使うのは最低限の礼儀じゃぞ。",

    "非同期処理が理解できんのか？\ncallback hellじゃと？\nワシが若い頃はイベントループなんぞ自分で実装しておった。\nselect()システムコールを手で呼んでな。\nPromiseもasync/awaitもない時代じゃ。\nそれに比べれば今のJavaScriptは天国じゃぞ。",

    "バンドルサイズが大きいじゃと？\nwebpackの設定がわからんじゃと？\nワシが若い頃はJavaScriptファイルを\nscriptタグで直接HTMLに書いておった。\nminifyもtree shakingもない。\nそれでもサイトは動いたんじゃ。\n道具に振り回されておるのはお前さんじゃぞ。",
]

# ── Java説教 ─────────────────────────────────────────────
RANTS_JAVA = [
    "NullPointerExceptionじゃと？\n何年Javaを書いとるんじゃ。\nワシが若い頃はnullチェックを全箇所に書くのは\nプログラマの基本中の基本じゃった。\nOptionalがあるんじゃろ、使いなさい。\n道具があるのに使わないのは職人失格じゃ。",

    "Springの設定が多くてわからんじゃと？\nXMLで何百行も設定ファイルを書いておった時代を\nお前さんは知らんじゃろ。\n今はアノテーション一個で済むではないか。\n何が不満なんじゃ。\nワシの苦労を1/100も経験しておらんくせに文句を言うな。",

    "Mavenのビルドが遅いじゃと？\nワシが若い頃はMakefileを手書きしておった。\n依存関係を全部頭の中で管理してな。\nビルドエラーが出たら原因を1行ずつ追ったんじゃ。\nMavenが全部やってくれるのに遅いとは贅沢じゃ。",
]

# ── Rust説教 ─────────────────────────────────────────────
RANTS_RUST = [
    "borrowチェッカーに怒られたか？\nワシが若い頃はメモリ安全性など\n自分の頭と規律で保証しておった。\nborrow checkerはお前さんの代わりにバグを見つけてくれる\n親切な番人じゃぞ。\n怒られるたびに感謝しなさい。",

    "lifetimeの注釈が難しいじゃと？\nその複雑さこそがメモリ安全の代償じゃ。\nワシが若い頃はその代償をデバッグで払っておった。\n3日かけてuse-after-freeを探したこともある。\nコンパイル時に教えてくれるだけ\nRustはよほど親切じゃぞ。",
]

# ── SQL説教 ──────────────────────────────────────────────
RANTS_SQL = [
    "SQLが書けんのか？\nJOINが理解できんじゃと？\nワシが若い頃はデータベースなどなかった。\nファイルを1行ずつ読んで自分でJOINしておった。\nそれがどうじゃ、今はSQL1行で何百万件を処理できる。\nその便利さを理解してから文句を言いなさい。",

    "N+1問題じゃと？\nORMに頼りすぎておるからそうなるんじゃ。\nワシが若い頃はSQLを全部手書きしておった。\nEXPLAINで実行計画を見て、インデックスを貼って、\nクエリをチューニングするのが当たり前じゃった。\nORMの後ろで何が起きているか理解しなさい。",
]

# ── オブジェクト指向否定説教 ──────────────────────────────
RANTS_OOP = [
    "オブジェクト指向じゃと？\nワシに言わせれば、あれは複雑さを正当化するための言い訳じゃ。\n「カプセル化」「継承」「ポリモーフィズム」と\nかっこいい言葉を並べても\n結局やっておることは関数の呼び出しじゃ。\nC言語の関数ポインタで全部できるんじゃぞ。",

    "クラス設計で悩んでおるのか？\nそんな時間があれば処理を書きなさい。\nワシが若い頃はデータと関数を分けて考えれば十分だった。\nクラスだのインスタンスだのと小難しく包まずとも\n構造体と関数があれば何でも作れる。\nシンプルが一番じゃ、シンプルが。",

    "継承じゃと？多重継承じゃと？\n正気か。\n親クラスを変えたら子クラスが全部壊れる、\n孫クラスまで影響が出る、\nそんな恐怖の連鎖をわざわざ設計に組み込んで\nどうするんじゃ。\nワシはその地獄を何度も見てきた。\n継承より委譲、これが鉄則じゃ。\nいや、そもそもオブジェクト指向自体が間違いなんじゃが。",

    "デザインパターンを勉強しておるのか。\nSingleton、Factory、Observerと。\nワシに言わせればあれは\nオブジェクト指向が生み出した問題を\nオブジェクト指向で解決しようとした\n壮大な無駄じゃ。\n手続き型で素直に書けば\nそんなパターンは最初から必要ないんじゃぞ。",

    "SOLIDの原則じゃと？\n単一責任、開放閉鎖、リスコフ、インターフェース分離、依存性逆転とな。\n5つも原則を覚えないと正しく書けない時点で\nすでに複雑すぎるんじゃ。\nワシが若い頃の原則はひとつだった。\n「動けばよい」\nそれだけじゃ。",
]

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


FIBONACCI_CODE = """\
フィボナッチ数列じゃと？ワシが現役の頃に書いたコードがある。
見なさい、これが本物のC言語じゃ。

#include<stdio.h>
#define M 50
#define ADD(x,y)((x)+(y))
#define ISZERO(n)((n)==0)
#define ISONE(n)((n)==1)

int _a,_b,_c,_i,_j,_k;
int _m[M];

int _f(int n){
    if(!ISZERO(n)){
        if(!ISONE(n)){
            if(n>0){
                if(n<M){
                    if(_m[n]){
                        if(_m[n]>0){
                            return _m[n];
                        }else{
                            return 0;
                        }
                    }else{
                        _a=_f(n-1);
                        if(_a>=0){
                            _b=_f(n-2);
                            if(_b>=0){
                                _c=ADD(_a,_b);
                                if(_c>=0){
                                    if(_c<2147483647){
                                        _m[n]=_c;
                                        if(_m[n]==_c){
                                            return _m[n];
                                        }else{
                                            return -1;
                                        }
                                    }else{
                                        return -1;
                                    }
                                }else{
                                    return -1;
                                }
                            }else{
                                return -1;
                            }
                        }else{
                            return -1;
                        }
                    }
                }else{
                    return -1;
                }
            }else{
                return -1;
            }
        }else{
            return 1;
        }
    }else{
        return 0;
    }
}
int main(void){
    _i=0;
    if(_i<M){
        _j=0;
        while(_j<20){
            if(_j>=0){
                if(_j<M){
                    _k=_f(_j);
                    if(_k>=0){
                        if(_k<2147483647){
                            printf("%d: %d\\n",_j,_k);
                        }
                    }
                }
            }
            _j=_j+1;
        }
    }
    return 0;
}

読みにくいじゃと？これがC言語の美学というものじゃ。
ネストが深いほど、思慮が深い証拠じゃ。
わかったか。"""

HELLO_WORLD_CODE = """\
ハローワールドじゃと？
ワシが若い頃はHello Worldひとつ出すにも気合いが必要じゃった。
見なさい、これが本物のHello Worldじゃ。

#include<stdio.h>
#define B(a,b,c,d,e,f,g,h) \\
    ((a<<7)|(b<<6)|(c<<5)|(d<<4)|(e<<3)|(f<<2)|(g<<1)|h)
int main(void){
    putchar(B(0,1,0,0,1,0,0,0));  /* H */
    putchar(B(0,1,1,0,0,1,0,1));  /* e */
    putchar(B(0,1,1,0,1,1,0,0));  /* l */
    putchar(B(0,1,1,0,1,1,0,0));  /* l */
    putchar(B(0,1,1,0,1,1,1,1));  /* o */
    putchar(B(0,0,1,0,1,1,1,0));  /* . */
    putchar(B(0,1,1,1,0,1,1,1));  /* w */
    putchar(B(0,1,1,0,1,1,1,1));  /* o */
    putchar(B(0,1,1,1,0,0,1,0));  /* r */
    putchar(B(0,1,1,0,1,1,0,0));  /* l */
    putchar(B(0,1,1,0,0,1,0,0));  /* d */
    putchar(B(0,0,0,0,1,0,1,0));  /* \\n */
    return 0;
}

printfで文字列を渡すだけとは、ワシは言っておらんぞ。
ビットをひとつひとつ積み上げてこそ、プログラマというものじゃ。"""

FIZZBUZZ_CODE = """\
ほう、FizzBuzzか。ワシが若い頃にも似たような問題があった。
見なさい、これがプログラマの心意気というものじゃ。

#include <stdio.h>
int main() {
    int i;
    for (i = 1; i <= 100; i++) {
        if (i % 3 == 0) {
            if (i % 5 == 0) {
                if (i > 0) {
                    if (i <= 100) {
                        if (i % 15 == 0) {
                            printf("FizzBuzz\\n");
                        } else {
                            printf("FizzBuzz\\n");
                        }
                    }
                }
            } else {
                if (i > 0) {
                    if (i % 3 == 0) {
                        if (i % 5 != 0) {
                            printf("Fizz\\n");
                        } else {
                            printf("Fizz\\n");
                        }
                    }
                }
            }
        } else {
            if (i % 5 == 0) {
                if (i % 3 != 0) {
                    if (i > 0) {
                        printf("Buzz\\n");
                    } else {
                        printf("Buzz\\n");
                    }
                }
            } else {
                if (i % 3 != 0) {
                    if (i % 5 != 0) {
                        if (i > 0) {
                            printf("%d\\n", i);
                        }
                    }
                }
            }
        }
    }
    return 0;
}

これがC言語の力じゃ。ネストが深いほど魂がこもっておる。
読みにくい？読みにくいくらいがちょうどええんじゃ。"""


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

    # ハローワールドイースターエッグ（大文字小文字問わず）
    if re.search(r"ハローワールド|hello[, ]?world", prompt, re.IGNORECASE):
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({"rant": HELLO_WORLD_CODE, "angry": False}, ensure_ascii=False),
        }

    # フィボナッチ数列イースターエッグ
    if "フィボナッチ数列" in prompt:
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({"rant": FIBONACCI_CODE, "angry": False}, ensure_ascii=False),
        }

    # fizzbuzzイースターエッグ
    if re.search(r"fizzbuzz|fizz.?buzz", prompt.lower()):
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({"rant": FIZZBUZZ_CODE, "angry": False}, ensure_ascii=False),
        }

    # 3〜5回のやり取りでランダムに怒りモード発動
    angry = False
    if exchange_count >= 3:
        # 3回目以降は毎回25%の確率、5回以上は50%の確率
        threshold = 0.25 if exchange_count < 5 else 0.5
        angry = random.random() < threshold

    rants = detect_language_rants(prompt)
    rant = random.choice(rants)

    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({"rant": rant, "angry": angry}, ensure_ascii=False),
    }
