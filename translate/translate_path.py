"""
# 引数
python translate_path.py
* 1: エンドポイント
* 2: 翻訳したいファイル

日本語から英語に翻訳する事に特化している。

# 使用パッケージ
- requests
- pathlib

# 実行例
```
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/translate/translate_path.py >run.py
python run.py (エンドポイント)
```

"""

from pathlib import Path  # pip install pathlib
import sys
import requests  # pip install requests

"""
定義
"""


def create_body(text, path):
    """
    curl用のリクエストボディテンプレート
    """
    return {
        "text": text,
        "source": "ja",
        "target": "en",
        "by": f"[translate.py] {str(path)}"
    }


"""
関数
"""


def curl(text, path):
    """
    cleansingのサブルーチン
    """
    global GAS_ID
    endpoint = f"https://script.google.com/macros/s/{GAS_ID}/exec"

    try:
        return requests.get(endpoint, params=create_body(
            text.encode("utf-8"), path)).json()["translate"]
    except:
        return text


def cleansing(word, source, skip, path):
    """
    テキスト（行）をクレンジングする
    translateのサブルーチン
    """
    if(
        skip
        or source
        or len(word) == 0

        # 最初の文字が#や-から始まるケースはエラーになるため、エスケープする
        or word[0] in ["#", "-"]

        # URLは翻訳する必要がないのでスキップ
        or word[:7] == "http://"
        or word[:8] == "https://"
    ):
        return word

    # テーブル内を一括変換してしまうので切り分ける
    if(word[0] == "|"):
        return "|".join([cleansing(table, False, False, path) for table in word.split("|")])

    # 文中にコードが含まれる場合は翻訳しないように制御
    if("`" in word):
        return "`".join([cleansing(w, index % 2 == 1, False, path) for index, w in enumerate(word.split("`"))])

    return curl(word, path)


def translate(text, path):
    """
    翻訳処理
    execute_fileのサブルーチン
    """
    global skip
    source = False

    # codeタグの開始/終了
    if text == "```":
        skip = not skip

    if len(text) > 0 and text[-1] == "`":
        source = True

    return " ".join([cleansing(split, skip, source, path)
                     for split in text.strip().split(" ")])


def execute_file(path):
    """
    ファイル読み込み・書き込み
    """
    with path.open(mode='r') as ja:
        with (path.parent / path.with_name(path.stem + "_en" + path.suffix)).open(mode="w") as en:
            [en.write(translated + "\n") for translated in [translate(
                line.strip(), path) for line in ja.readlines()]]


def check_file(path):
    """
    条件処理用
    既に翻訳済み(_en)のファイルが存在したり、翻訳済みのファイルは除外する
    """
    return path.stem[-3:] != "_en" and not Path(f"{path.parent}/{path.stem}_en.md").is_file()


if __name__ == "__main__":
    if(len(sys.argv) < 2 or sys.argv[1][:7] == "http://" or sys.argv[1][:8] == "https://"):
        print(f"[Stop translate_path.py] Required args(curl URL)")
        quit()

    GAS_ID = sys.argv[1]
    skip = False

    # 入力値が存在するパスなら採用、それ以外の場合はカレントパスを採用
    path = Path(sys.argv[2]) if len(sys.argv) > 2 and (Path(
        sys.argv[2]).is_dir() or Path(sys.argv[2]).is_file()) else Path(__file__).parent

    if(path.is_file() and check_file(path)):
        execute_file(path)

    # 存在しないパスやファイルを指定しても件数なしで処理される
    [execute_file(result) for result in Path(
        path).glob("**/*.md") if(check_file(result))]
