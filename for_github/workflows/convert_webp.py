from multiprocessing import Pool
import re
import shutil
from PIL import Image
from pathlib import Path
import sys
import os

"""
FYI: https: // www.nomuramath.com/kv8wr0mp/
"""


class Color:

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


def convert(path):
    webp = Path(path.parent / "webp" / (path.stem + ".webp"))
    if(path.with_suffix(".webp").is_file() or webp.is_file()):
        return

    print(f"[Run] {path}")
    base = Path(path.parent / "base" / path.name)
    base.parent.mkdir(exist_ok=True)
    webp.parent.mkdir(exist_ok=True)

    # 画像データやサイズ情報を取得
    img = Image.open(path)

    # 新しく画像を生成してExifを削除し、webpに変換する
    new_img = Image.new(img.mode, img.size).convert('RGB')
    new_img.putdata(img.getdata())
    new_img.thumbnail(size=(720, 640))
    new_img.save(webp, 'webp')

    shutil.move(path, base)
    print(f"[{Color.green('Success')}] {path} -> {webp}")


# マルチプロセスで__mp_main__から実行されるので、これを回避するため必須
if __name__ == "__main__":
    print(f"[{Color.blue('Start')}: {sys.argv[0]}]")
    print()

    p = Pool(os.cpu_count())

    path = Path(sys.argv[1]) if(len(sys.argv) > 1) else Path(__file__).parent
    if(path.is_file()):
        convert(path)
    elif(path.is_dir()):
        [p.map(convert, [p for p in path.glob(
            '**/*') if re.search('/*\.(jpg|jpeg|png|gif|bmp)', str(p)) if str(p.parent) != "base"])]

    print()
    print(f"[{Color.blue('End')}: {sys.argv[0]}]")
