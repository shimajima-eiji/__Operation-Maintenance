# coding: [encoding]

### curlで動いているかどうかを調べるためのテスター
### curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/curl_tester.py | python
try:
  # python2
  print __file__
except Error:
  # python3
  print(__file__)
  
