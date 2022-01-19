'''
# パラメータ
python translate_path.py
* 1: エンドポイント
* 2: 翻訳したいファイル

日本語から英語に翻訳する事に特化している。

# 使用パッケージ
pip install requests
pip install pathlib
pip install git+https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api
pip install googletrans==4.0.0-rc1

# 実行例
```
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/translate/translate_path.py >run.py
python run.py (エンドポイント) (ファイルパス)
```

'''

from pathlib import Path # pip install pathlib
import sys
import requests  # pip install requests
import json
from googletrans import Translator  # pip install (git+https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api or googletrans==4.0.0-rc1)

# (ディレクトリ走査のみ)ファイルを書き出すパターン
def export_pattern(file):
  return Path(str(file.parent) + "/" + file.stem + "_en" + file.suffix)

# 処理対象となるファイルパターン
def include_pattern(file):
  # ファイル名が.や_などから始まらないもの
  # 拡張子はtxtかmd
  return Path(file.suffix) in ['.txt', '.md'] and not file.name[0] in ['.', '_']

# コンソールからjqコマンドで加工できるようにする
def return_json(json_value):
  return json.dumps(json_value, ensure_ascii=False)

# GASを使って翻訳する
def translate_gas(endpoint, text):
  headers = {
    'Content-Type': 'application/json',
  }
  body = json.dumps({
    "text": text,
    "source": "ja",
    "target": "en",
    "by": "translate_path.py"
  })

  response = requests.post(endpoint, headers=headers, data=body)
  return response.json()

# Google-Transを使って翻訳する
def translate_googletrans(str_line):
  # Translatorの設定
  try:
    tr = Translator(service_urls=['translate.googleapis.com'])
    return tr.translate(str_line, src="ja", dest="en").text
  except Exception as e:
    tr = Translator()
    return tr.translate(str_line, src="ja", dest="en").text

# 取得したデータを出力する
def create_file(file, data):
  with export_pattern(file).open('w') as f:
    for translated in data:
      f.write(translated)

# 受け取ったファイルを翻訳する
def translate_file(file, endpoint, export_flag = False):
  # この場合はロジックを見直す
  if not file.is_file() or not file.exists():
    return {"result": False, "message": "[Stop] Illigal error!"}

  # 処理対象外となるファイルはスキップ
  if not include_pattern(file):
    return

  # 翻訳済みのファイルか、既に翻訳しているファイルの場合はスキップ
  if file.stem[-3:] == '_en' or file.stem[-3:] == '_ja' or export_pattern(file).is_file():
    return {"result": False, "message": "[SKIP] existed translate file."}

  with file.open(mode='r') as f:
    data = translate_gas(endpoint, f.readlines())

  source_flag = False
  # data['translate']と歩調を合わせるため、enumerate
  for index, line in enumerate(data['text']):
    str_line = line.strip()

    # ソースコード判定
    if str_line == '```':
      source_flag = not source_flag
      data['translate'][index] = line
      continue

    # 改行やソースコードは翻訳しない
    elif source_flag or str_line == '':
      data['translate'][index] = line
      continue

    # hタグは翻訳後おかしくなるのでGoogle Transを使用
    elif str_line[0] == '#' and str_line[1] == ' ' or data['translate'][index].strip() == '':
      # result = tr.translate(text=str_line, src="ja", dest="en")
      data['translate'][index] = translate_googletrans(str_line) + "\n"

    # GASで翻訳に失敗している場合はGoogleTransで再翻訳する
    elif data['translate'][index].strip() == '' and str_line.strip() == '':
      data['translate'][index] = translate_googletrans(str_line) + "\n"

    # リストを変換すると'--'に置き換えられるので手動で差し戻す
    tmp = data['translate'][index].strip()
    if tmp[0] == '-' and tmp[1] == '-':
      data['translate'][index] = data['translate'][index].replace('--', '- ')

  # ディレクトリサーチ（マルチプロセッシング）の場合はファイルを作る
  if export_flag:
    create_file(file, data['translate'])

  return data

def search_dir(dir_path):
  # この場合はロジックを見直す
  if not dir_path.is_dir() or not dir_path.exists():
    return {"result": False, "message": "[Stop] Illigal error!"}

  # dir_pathはdir確定
  for result in dir_path.iterdir():
    # .gitや_configを除外
    if result.name[0] in ['.', '_']:
      continue

    # ディレクトリの場合、再起処理
    if result.is_dir():
      search_dir(result)
      continue

    # ファイルの場合、見つけた順番に処理する
    if translate_file(result, ENDPOINT, True).result:
      file_count+=1

# multiprocessingを使うため、実行処理の書き方を変える事はできない
if __name__ == "__main__":
  # 引数がなければ実行しない
  if len(sys.argv) <= 2:
    print(return_json({"result": False, "error": "[STOP] Required (*endpoint) (*path)"}))
    quit()

  ENDPOINT = sys.argv[1]

  # パスが存在しない場合は実行しない
  path = Path(sys.argv[2])
  if not Path(path).exists():
    print(return_json({"result": False, "error": "[STOP] {path} is not file or directory."}))
    quit()

  file_count=0
  # ディレクトリの場合は並列処理させる
  if path.is_dir():
    search_dir(path)

  # ファイルの場合は単一処理させる
  if path.is_file():
    print(return_json(translate_file(path, ENDPOINT)))
    file_count+=1

  print('[COMPLETE] translate_path.py: 翻訳したファイル数')
  print(file_count)
