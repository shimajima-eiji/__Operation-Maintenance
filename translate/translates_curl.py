# python3を想定。python2では動かない
'''
# 使い方
python translates_curl.py
* -e --endpoint: エンドポイント
  -s --source(ja): 翻訳元
  -t --target(en): 翻訳先
オプションを指定しない引数は全て翻訳される。順不同

英和翻訳をしたいなら-s en -t jaとする
言語を指定すれば英語や日本語以外でも翻訳できる
'''

import requests  # need pip install
from json import dumps
from argparse import ArgumentParser

# エンドポイントオプション引数に対応。endpointは必須
parser = ArgumentParser()
parser.add_argument('values', nargs='*')
parser.add_argument('-e', '--endpoint', type=str,
                        required = True,
                        help='APIのエンドポイント(GASを想定)を指定します')
parser.add_argument('-s', '--source', type=str,
                        default='ja',
                        help='翻訳したい文字の言語を指定します')
parser.add_argument('-t', '--target', type=str,
                        default='en',
                        help='文字をどの言語に翻訳するか指定します')
args = parser.parse_args()

text = args.values
ENDPOINT = args.endpoint
source = args.source
target = args.target

# 引数から入力を受け取って翻訳したファイルを作成する
def translates():
  headers = {
    'Content-Type': 'application/json',
  }

  body = dumps({
    "text": text,
    "source": source,
    "target": target,
    "by": "translates.py"
  })
  result = requests.post(ENDPOINT, headers=headers, data=body).json()
  result['text'] = text
  return result

print(dumps(translates(), ensure_ascii=False))
