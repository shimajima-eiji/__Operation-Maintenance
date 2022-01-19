# 関連サービス
- https://github.com/shimajima-eiji/--GAS_v5_Translate

# ファイル紹介
|ファイル名            |用途|必要ツール|使用場所|
|--------------------|----|---|---|
|translate_curl.py   |一つの文字を翻訳する|GASエンドポイント(Get)||
|translates_curl.py  |複数の文字をまとめて翻訳する|GASエンドポイント(Post)||
|translate_google.py |一つの文字を翻訳する|googletrans(pip)|ロギングの観点から使わない|
|translates_google.py |複数の文字をまとめて翻訳する|googletrans(pip)|ロギングの観点から使わない|
|translate_path.py   |ファイルサーチして一括で変換する|GASとgoogletrans(API制限回避)||

`translate.sh`は使っていない

# Google-Translate
- `pip install git+https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api`
- `pip install googletrans==4.0.0-rc1`

のどちらかで実行できる。
スクリプトの記述が異なるため、インストールするパッケージの変更時は要注意。

```
from googletrans import Translator  # pip install (git+https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api or googletrans==4.0.0-rc1)

tr = Translator(service_urls=['translate.googleapis.com'])  # git
tr = Translator()  # 4.0.0-rc1
```
