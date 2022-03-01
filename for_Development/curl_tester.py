# -*- coding: utf-8 -*-
"""
curlで動いているかどうかを調べるためのテスター
```
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/curl_tester.py | python
```
"""
try:
  from pathlib import Path
  print Path(__file__).cwd()
except Error:
  print "pathlibのインポートエラー"

# `curl -sf (これ) | python`を実施すると、カレントディレクトリになる
# なお、`__file__`は`<stdin>`が表示される
