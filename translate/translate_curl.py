"""
# 引数
python translate_curl.py
* 1: エンドポイント
* 2: 翻訳したいテキスト
  3: 翻訳元
  4: 翻訳先

英和翻訳をしたいなら(URL) (テキスト) en jaとする
言語を指定すれば英語や日本語以外でも翻訳できる

# 使用パッケージ
- requests
- pathlib

# 実行例
```
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/translate/translate_curl.py >run.py
python run.py (エンドポイント) (翻訳したいテキスト)
```

"""

import requests  # need pip
import sys
from json import dumps

args = sys.argv
# 引数はエンドポイント・文字列が必須
if len(args) <= 2:
    print(dumps(
        {"result": False, "error": "[STOP] Required (*endpoint) (*text) (source:2) (target:2)"}, ensure_ascii=False))
    quit()

gas_id = args[1]
text = args[2]
source = "ja" if (len(args) <= 3) else args[3]
target = "en" if (len(args) <= 4) else args[4]
ENDPOINT = f"https://script.google.com/macros/s/{gas_id}/exec?text={text}&source={source}&target={target}&by=translate_curl.py"

result = requests.get(ENDPOINT).json()
result['text'] = text
print(dumps(result, ensure_ascii=False))
