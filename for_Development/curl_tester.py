# -*- coding: utf-8 -*-
import sys

"""
curlで動いているかどうかを調べるためのテスター
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/curl_tester.py | python
"""

if sys.version_info.major == 2:
  print __file__
elif sys.version_info.major == 3:
  print(__file__)
