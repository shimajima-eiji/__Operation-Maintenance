import os
import copy
import re
import shutil
from PIL import Image, ImageDraw, ImageFont  # pip pillow
from pathlib import Path  # pip pathlib
import sys
from box import Box  # pip python-box
import math

"""
# 環境構築
```
pip install pillow pathlib python-box
```

# 使い方
```
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_github/workflows/convert_webp.py >convert_webp.py
python convert_webp.py (パス) (上書きフラグ)
rm convert_webp.py
```

# パラメータ
パス(カレント): 検索対象とするファイル・ディレクトリパス。サブディレクトリも参照する
上書きフラグ(False): 引数があれば変換済みファイルを再変換する

# 開発者向け情報: エラーパターン
本来であれば、以下の方法でも問題はなかった。

```
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_github/workflows/convert_webp.py | python
```

curlで実行してみたところ、Path.globでエラーになった。
そのため、curlでファイルを格納した上で実施するとこの問題は解消される。
原因が特定できていないが、ファイルパスが影響する可能性が高い。

差し替えるなら、該当箇所に以下を差し込む。

```
if(__file__ == "<stdin>"):
    quit()
```

同様に、処理に失敗したらデッドロックするため、マルチプロセスは廃止

# FYI
- class Color: https://www.nomuramath.com/kv8wr0mp/
- def watermark: https://remotestance.com/blog/2834/
- const ROTATE: https://qiita.com/Klein/items/a04cf1a6c94d6f03846e
"""

# マルチプロセスで__mp_main__から実行されるので、これを回避するため必須
if __name__ != "__main__":
    quit()


class __Color:

    @classmethod
    def __print(this, code, message): return f'\033[{code}m{message}\033[39m'
    # デバッグ時は、returnをprintにする。printから呼び出して使う想定
    # print(f"Color.red('テスト')白文字")

    @classmethod
    def black(this, message): return this.__print(30, message)
    @classmethod
    def red(this, message): return this.__print(31, message)
    @classmethod
    def green(this, message): return this.__print(32, message)
    @classmethod
    def yellow(this, message): return this.__print(33, message)
    @classmethod
    def blue(this, message): return this.__print(34, message)
    @classmethod
    def magenta(this, message): return this.__print(35, message)
    @classmethod
    def cyan(this, message): return this.__print(36, message)
    @classmethod
    def white(this, message): return this.__print(37, message)
    @classmethod
    def default(this, message): return this.__print(39, message)


def __watermark(base):
    # テキストを描画する画像オブジェクトを作成します。
    # ※後ほど45度回転させたとき、元の画像と同じ大きさにしておくと隙間ができてしまいます。
    #  その隙間をなくすために拡大します。
    PARAMETER = Box({
        "url": 'https://nomuraya.tk',

        # IMAGES.text用の設定情報
        "text": {
            "mode": 'RGBA',
            "square": (base.width * 3, base.height * 3),
            "rbga": (255, 255, 255, 0),
            "angle": 30,
        },

        # IMAGES.draw用の設定情報
        "draw": {
            "color": (255, 255, 255),  # 文字色
            "opacity": 20,  # 文字の透明度
        },


        "watermark": {
            "margin": {
                "x": 1.5,  # ウォーターマークの横幅の倍率
                "y": 3,   # ウォーターマークの縦幅の倍率
            },
        },
    })

    # ウォーターマークの元画像を生成する
    # imageオブジェクトを生成する
    WATERMARK_IMAGES = Box({})
    WATERMARK_IMAGES.text = Image.new(PARAMETER.text.mode,
                                      PARAMETER.text.square, PARAMETER.text.rbga)
    WATERMARK_IMAGES.draw = ImageDraw.Draw(WATERMARK_IMAGES.text)

    # 文字の横幅、縦幅を取得し、マージン幅を確定する
    textsize = WATERMARK_IMAGES.draw.textsize(PARAMETER.url)
    PARAMETER.watermark.margin.x *= int(textsize[0])
    PARAMETER.watermark.margin.y *= int(textsize[1])

    position = Box({})
    # 画像内にウォーターマークをループして書き込む
    # x座標とy座標を取得し、順番にテキストを描画する
    for x_loop in range(math.floor(WATERMARK_IMAGES.text.width / PARAMETER.watermark.margin.x)):
        position.x = x_loop * PARAMETER.watermark.margin.x

        for y_loop in range(math.floor(WATERMARK_IMAGES.text.height / PARAMETER.watermark.margin.y)):
            position.y = y_loop * PARAMETER.watermark.margin.y
            square = (position.x, position.y)

            # テキストを描画します。
            WATERMARK_IMAGES.draw.text(
                square,
                PARAMETER.url,
                fill=PARAMETER.draw.color + (PARAMETER.draw.opacity,)
            )

    # 作成したウォーターマーク画像を回転
    WATERMARK_IMAGES.text = WATERMARK_IMAGES.text.rotate(PARAMETER.text.angle)

    """
    # トリミング位置の算出
    拡大したウォーターマーク画像 - 元画像 の結果を半分にした位置から
    # 例
    `(100 - 50) / 2 = 25〜75  # 元画像50が取得できる`
    """
    # ウォーターマークは拡大しているので、元の画像サイズでトリミングする
    left = math.floor((WATERMARK_IMAGES.text.width - base.width) / 2)
    right = left + base.width
    top = math.floor((WATERMARK_IMAGES.text.height - base.height) / 2)
    bottom = top + base.height
    WATERMARK_IMAGES.text = WATERMARK_IMAGES.text.crop(
        # ４隅の情報を１つの引数にするため、まとめて渡す
        (left, top, right, bottom)
    )

    # 画像オブジェクトを重ねます。
    return Image.alpha_composite(base, WATERMARK_IMAGES.text)


ROTATE = {
    1: lambda img: img,
    # 左右反転
    2: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
    # 180度回転
    3: lambda img: img.transpose(Image.ROTATE_180),
    # 上下反転
    4: lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
    # 左右反転＆反時計回りに90度回転
    5: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Pillow.ROTATE_90),
    # 反時計回りに270度回転
    6: lambda img: img.transpose(Image.ROTATE_270),
    # 左右反転＆反時計回りに270度回転
    7: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Pillow.ROTATE_270),
    # 反時計回りに90度回転
    8: lambda img: img.transpose(Image.ROTATE_90),
}


def __create_image(path, base=None, to=None):
    if(base is None):
        base = Path(f"{path.parent}/base/{path.name}")
    if(to is None):
        to = Path(f"{path.parent}/webp/{path.stem}/{path.stem}.webp")
    origin = Path(f"{path.parent}/origin/{path.stem}/{path.name}")
    icon = Path(f"{path.parent}/icon/{path.stem}/{path.stem}.ico")

    # 同一ディレクトリにwebpが存在する場合はやらない
    if(path.with_suffix(".webp").is_file()
        # 変換済みのファイルが存在する場合はやらない
        or base.is_file()
        or to.is_file()
        or origin.is_file()
        or icon.is_file()
       ):
        return False

    print(f"[Run] {path}")

    image = Image.open(path)

    # Exifを削除するため新しく画像を生成する。見た目を変えないため元画像から情報をコピー。
    webp = Image.new(image.mode, image.size).convert('RGBA')
    webp.putdata(image.getdata())

    # リサイズ時に縦画像を横に変換してしまうため、回転処理を入れる。
    # 回転処理は元画像のexif情報から取得する
    try:
        exif = image._getexif()

        # exifが取れた時は回転させる
        if not exif is None:
            orientation = exif.get(0x112, 1)
            webp = ROTATE[orientation](webp)

    except:
        print(f"[Skip] Can't clear exif.: {path}")

    # ウォーターマークを入れる
    if path.parent.name != "nomark":
        webp = __watermark(webp)

    # webpに変換して保存する
    def save(image, path, *trash, to=None, tag=""):
        if(len(tag) > 0):
            tag = f"_{tag}"

        # jpegを変換する際に必要。pngに影響がないのでそのまま採用する
        image.convert('RGB').save(path.with_stem(f"{path.stem}{tag}"),
                                  None, quality=95, optimize=True)

        if(to is not None):
            image.convert('RGB').save(to.with_stem(f"{to.stem}{tag}"),
                                      None, quality=95, optimize=True)

    origin.parent.mkdir(parents=True, exist_ok=True)
    to.parent.mkdir(parents=True, exist_ok=True)
    save(webp, origin, to=to)

    # 適切なサイズにリサイズする
    def resize(base, width, height, tag, origin, to=None):
        image = copy.deepcopy(base)

        # 縦画像の場合は比率を入れ替える
        if(image.width < image.height):
            width, height = height, width

        # 指定サイズに満たない場合はやらない
        if(image.width < width and image.height < height):
            return

        # アイコンなのに正方形じゃない場合もやらない
        if("con" in tag and image.width != image.height):
            return

        image.thumbnail(size=(width, height))
        save(image, origin, to=to, tag=tag)

    # いくつかの画像パターンに合わせて作成する
    # 画面サイズ
    # 16:9
    resize(webp, 1920, 1080, "fullHD", origin, to)
    resize(webp, 1280, 720, "HDTV", origin, to)

    # 4:3
    resize(webp, 1280, 960, "QXGA", origin, to)
    resize(webp, 1024, 768, "XGA", origin, to)
    resize(webp, 800, 600, "SVGA", origin, to)
    resize(webp, 480, 360, "VGA", origin, to)
    resize(webp, 360, 240, "QVGA", origin, to)

    # 1:1 アイコン
    icon.parent.mkdir(parents=True, exist_ok=True)
    resize(webp, 512, 512, "icon_large", icon)
    resize(webp, 256, 256, "icon", icon)
    resize(webp, 128, 128, "icon_small", icon)
    resize(webp, 64, 64, "icon_mini", icon)
    resize(webp, 16, 16, "favicon", icon)

    # wordpress
    resize(webp, 938, 939, "blog_940", origin, to)
    resize(webp, 720, 721, "blog_720", origin, to)
    print(f"[{__Color.green('Success')}] {path} -> {to}")

    base.parent.mkdir(exist_ok=True)
    print(f"ファイル移動 {path} / {base}")
    shutil.move(path, base)


def __main(path):
    # 画像生成
    try:
        __create_image(path)

    except:
        print(f"[Skip] Can't convert.: {path}")

    return True


def retry(path):
    """
    再変換フラグがONの場合のみ実施する。baseディレクトリにあるファイルは、初回変換時はbaseディレクトリの上で実施されているので、パスを初回変換時に合わせる
    """
    if(path.with_suffix(".webp").is_file()):
        # print("同一ディレクトリ")
        base = path
        to = path.with_suffix(".webp")
        __create_image(path, base, to)
        # print(f"同一ディレクトリのケース {path}")
        # os.rmdir(base.parent)

    elif(path.parent.name == "base" and Path(path.parent.parent / "webp" / path.stem / path.with_suffix(".webp").name).is_file()):
        # print("現行フォーマット")
        base = path
        path = Path(path.parent.parent / path.name)
        to = Path(path.parent.parent / "webp" /
                  path.stem / path.with_suffix(".webp").name)
        shutil.move(base, path)
        __create_image(path, base, to)
        # print(f"新フォーマットのケース {base} / {path}")
        shutil.move(path, base)

    elif(path.parent.name == "base" and Path(path.parent.parent / "webp" / path.with_suffix(".webp").name).is_file()):
        # print("旧フォーマット")
        base = path
        path = Path(path.parent.parent / path.name)
        to = Path(path.parent.parent / "webp" / path.with_suffix(".webp").name)
        shutil.move(base, path)
        __create_image(path, base, to)

        # print(f"旧フォーマットのケース（エラーになる） {base} / {path}")


# 引数処理
# `curl | python`で実施した場合、else時はカレントディレクトリを返す
filename = "curl script" if sys.argv[0] == "" else sys.argv[0]
# 引数があればそれを、なければこのファイルと同じディレクトリを走査
path = Path((sys.argv[1]) if len(sys.argv) > 1 else ".")
# 引数があれば上書きする
retry_flag = len(sys.argv) > 2
_f = retry if(retry_flag) else __main

print(f"[{__Color.blue('Start')}: {filename}]")
print()

# パスが画像ファイルならピンポイントに変換
execute_suffix = [".jpg", ".JPG", ".jpeg", "JPEG",
                  ".png", ".PNG", ".bmp", ".BMP"]
if(path.is_file() and path.suffix in execute_suffix):
    __main(path)

# パスがディレクトリなら以下ファイルを検索する。
elif(path.is_dir()):
    print(f"[{__Color.white('Information')}] ディレクトリサーチ: {path.resolve()}")

    # 画像ファイル以外と、baseディレクトリのファイルは除外する。
    # 既に変換されているかサーチして処理するのが手間だったので、convert内で実施している
    result = [
        _f(file) for file in path.glob('**/*')
        # 画像拡張子でなければやらない
        if re.search(f"/*({'|'.join(execute_suffix)})", str(file))

        # 変換済みのファイルを格納したディレクトリは対象外
        if file.parent.name != "base" or retry_flag
        if file.parent.name != "origin"
        if file.parent.parent.name != "origin"
        if file.parent.name != "icon"
        if file.parent.parent.name != "icon"
    ]
    if len(result) > 0:
        print(f"[{__Color.white('Information')}] ディレクトリパスは既に変換済みか、ファイルが存在しない]")

# 画像ではないファイルか、ファイルでもディレクトリでもない場合
else:
    print(f"[{__Color.yellow('Skip')}] 不正なパス: {path}")

print()
print(f"[{__Color.blue('End')}: {filename}]")
