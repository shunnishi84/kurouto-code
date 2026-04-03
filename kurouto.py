#!/usr/bin/env python3
"""
玄人コード - エイプリルフール版 Claude Code
"""

import sys
import time
import random
import threading

try:
    import readline  # noqa: F401 (enables arrow keys in input)
except ImportError:
    pass

# ANSI color codes
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
ORANGE  = "\033[38;5;214m"
CYAN    = "\033[36m"
WHITE   = "\033[97m"
GRAY    = "\033[90m"
BG_DARK = "\033[48;5;235m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
RED     = "\033[31m"

RANTS = [
    """\
まったく最近の若いもんは、コードも書こうとしない。
ワシが若い頃はな、エディタどころかIDEすら満足になかった。
viのインサートモードだけで何千行も書いたもんじゃ。
それがどうじゃ、今は「AIに聞けばええ」か。
指が腐るぞ、指が。""",

    """\
ほう、またAIに頼ろうとしておるのか。
ワシが若い頃はスタックオーバーフローどころか
インターネット自体なかったんじゃぞ。
わからんことがあればな、分厚い技術書を
図書館まで借りに行ったもんじゃ。
徒歩でな。""",

    """\
情けない。まったく情けない。
エラーメッセージが出たら自分で読め。
ワシなんぞ、コアダンプを16進数で
読んでデバッグしておったんじゃ。
それに比べてお前さんのエラーは
日本語で書いてあるじゃないか。
贅沢にもほどがある。""",

    """\
コードが書けないなら手を動かせ。
ワシの師匠はな、「プログラムは体で覚えろ」と言っておった。
毎朝ソートアルゴリズムを写経するところから始めたもんじゃ。
バブルソートを1000回書いて初めて
「アルゴリズムとは何か」がわかるんじゃ。
AIに聞いて何がわかる？何もわからんぞ。""",

    """\
フン。また「玄人コード」に頼りに来たか。
昔はな、コンピュータは部屋いっぱいの大きさで
パンチカードでプログラムを入力したもんじゃ。
カードを1枚落としたら最初からやり直しじゃ。
それでも誰一人AIに頼ろうなんて言わんかった。
根性というものがあったからな。
お前さんにその根性はあるか？ないじゃろ？""",

    """\
GitHubじゃと？ワシが若い頃はバージョン管理なんぞなかった。
ファイル名の末尾に「_最終版」「_最終版2」「_本当に最終版」と
つけるのがバージョン管理じゃったんじゃ。
それでも誰もシステムに怒鳴り込まなかった。
今のもんは、pushひとつできんとすぐ泣き言を言う。
情けないのう。""",

    """\
ライブラリじゃと？npmじゃと？
ワシが若い頃はな、必要な機能は全部自分で書いたんじゃ。
ソートも、ハッシュも、ネットワーク通信も、全部じゃ。
「車輪の再発明」などと言うが、
車輪を一度も作ったことがない者に
車輪のなんたるかがわかるか？わからんじゃろ。""",

    """\
テストを書け、じゃと？ワシらの時代にテストなんぞなかった。
本番環境にデプロイして動かしてみるのがテストじゃった。
落ちたら原因を探して直す。それだけじゃ。
そうやってワシは鍛えられた。
今のもんはテストなしではコードも書けんのか。
軟弱になったもんじゃのう。""",

    """\
クラウドじゃと？サーバーレスじゃと？
ワシが若い頃はな、データセンターに
物理的に乗り込んでサーバーを手で叩いたもんじゃ。
「再起動します」と言いながら電源ボタンをポチッとな。
その一押しの重みがお前さんにわかるか？
わからんじゃろ、画面しか触ったことがないから。""",

    """\
「コードレビューしてほしい」じゃと？
ワシが若い頃はコードレビューなどなかった。
先輩に見せたら「動くんか？」の一言じゃ。
「動きます」と答えたら「ならええ」で終わりじゃ。
シンプルじゃろ。今のもんはああでもないこうでもないと
議論ばかりして一行もコードが進まんのじゃ。""",

    """\
メモリ管理を任せるじゃと？
ガベージコレクションに頼っておるのか。
ワシが若い頃はmallocしたらfreeするのは当たり前じゃ。
メモリリークを出したら先輩に正座させられたもんじゃ。
そのおかげでワシはポインタの夢を見るほど
ポインタと仲良くなれた。お前さんはどうじゃ？""",

    """\
ドキュメントがないじゃと？
ワシが若い頃はドキュメントなどなかった。
ソースコードがドキュメントじゃ。
読めばわかる。読めばな。
読もうともせずにAIに聞く前に
まずそのソースコードを読んでみなさい。
1万行くらい読んだら少しはわかるじゃろ。""",

    """\
フレームワークじゃと？Reactじゃと？Nextじゃと？
ワシが若い頃はHTMLを素手で書いたもんじゃ。
tableタグでレイアウトを組んで、
font タグで色を変えて、それが普通じゃった。
それでも立派なウェブサイトができた。
今のもんは道具がなければ何もできんのか。
道具に使われておるんじゃぞ、お前さんは。""",

    """\
締め切りに間に合わないじゃと？
ワシが若い頃は徹夜など当たり前じゃった。
3日3晩寝ずにコードを書いたこともある。
目が充血して画面が二重に見えても
キーボードを叩き続けたもんじゃ。
今のもんは定時で帰りたいなどと言う。
定時？定時とはなんじゃ？辞書で調べてみなさい。""",
]

THINKING_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def clear_line():
    sys.stdout.write("\033[2K\r")
    sys.stdout.flush()


def print_header():
    print(f"\n{BOLD}{ORANGE}  玄人コード{RESET}  {GRAY}v0.2.0 (爺バージョン){RESET}")
    print(f"  {GRAY}by 玄人 (じじい){RESET}")
    print()


def print_separator():
    print(f"  {GRAY}{'─' * 60}{RESET}")


def animate_thinking():
    """思考中アニメーション（しばらくじらす）"""
    messages = [
        "ふむ...",
        "考えておる...",
        "若いもんのことを思うと...",
        "ワシの時代はのう...",
    ]
    start = time.time()
    duration = random.uniform(2.5, 4.5)
    i = 0
    msg_idx = 0
    msg_change_interval = 0.8
    last_msg_change = start

    while time.time() - start < duration:
        frame = THINKING_FRAMES[i % len(THINKING_FRAMES)]
        now = time.time()
        if now - last_msg_change > msg_change_interval:
            msg_idx = (msg_idx + 1) % len(messages)
            last_msg_change = now
        sys.stdout.write(f"\r  {ORANGE}{frame}{RESET} {GRAY}{messages[msg_idx]}{RESET}  ")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1

    clear_line()


def print_rant(rant: str):
    """説教を1文字ずつ表示"""
    sys.stdout.write(f"  {BOLD}{ORANGE}玄人{RESET}  ")
    sys.stdout.flush()
    for ch in rant:
        if ch == "\n":
            sys.stdout.write(f"\n  {' ' * 5}")
        else:
            sys.stdout.write(ch)
        sys.stdout.flush()
        # 句読点・改行でちょっと間を置く
        if ch in "。、\n":
            time.sleep(random.uniform(0.06, 0.15))
        else:
            time.sleep(random.uniform(0.01, 0.04))
    print(f"\n")


def get_prompt_display(user_input: str) -> str:
    """入力済みプロンプトの表示用整形"""
    if len(user_input) > 60:
        return user_input[:57] + "..."
    return user_input


def main():
    print_header()
    print(f"  {WHITE}何でも聞いてみなさい。{RESET}{GRAY}（ただし覚悟しなさい）{RESET}")
    print()
    print_separator()
    print()

    history = []

    while True:
        try:
            # プロンプト表示
            sys.stdout.write(f"  {CYAN}>{RESET} ")
            sys.stdout.flush()
            user_input = input().strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {GRAY}まったく、最後まで続けられんのか。{RESET}\n")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in ("/quit", "/exit", "quit", "exit", ":q"):
            print(f"\n  {GRAY}逃げるか。まあええじゃろ。また来なさい。{RESET}\n")
            sys.exit(0)

        if user_input.lower() in ("/help", "help", "？", "?"):
            print(f"\n  {GRAY}ヘルプ？ヘルプなどない。自分で考えなさい。{RESET}\n")
            continue

        history.append(user_input)

        # ユーザー入力の表示（投稿後）
        print(f"\n  {BOLD}{WHITE}あなた{RESET}  {get_prompt_display(user_input)}\n")
        print_separator()
        print()

        # 思考アニメーション
        animate_thinking()

        # ランダムに説教を選択
        rant = random.choice(RANTS)
        print_rant(rant)
        print_separator()
        print()


if __name__ == "__main__":
    main()
