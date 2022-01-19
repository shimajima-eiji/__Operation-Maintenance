'''
pip install git+https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api
pip install googletrans==4.0.0-rc1
'''
from googletrans import Translator

try {
  tr = Translator()
} catch {
  tr = Translator(service_urls=['translate.googleapis.com'])
}
print(tr.translate("テスト", src="ja", dest="en").text)
# 翻訳されたtestが表示されれば成功
