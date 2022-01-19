'''
# 使用パッケージ
pip install git+https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api
pip install googletrans==4.0.0-rc1

# 実行例
```
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_Development/googletrans_test.py | python
```
'''

from googletrans import Translator
from json import dumps

try:
  tr = Translator(service_urls=['translate.googleapis.com'])
except Exception as e:
  tr = Translator()

print(dumps(tr.translate("テスト", src="ja", dest="en"), ensure_ascii=False))
# 翻訳されたtestが表示されれば成功
