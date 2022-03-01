"""
curlで動いているかどうかを調べるためのテスター
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/curl_tester.py3 | python
"""
from pathlib import Path
print(Path(__file__).cwd())
