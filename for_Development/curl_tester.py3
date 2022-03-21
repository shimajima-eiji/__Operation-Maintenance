"""
curlで動いているかどうかを調べるためのテスター
```
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_Development/curl_tester.py3 | python
```
"""
import sys
try:
  from pathlib import Path
  print(__file__)
  print(__file__ == "<stdin>")
  print(sys.argv[0])
  print(__name__)
  print(Path(__file__).cwd())
  path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).cwd()
  print(path)
  [print(f"パス: {p}\n") for p in path.glob("**/*")]
except Error:
  print("pathlibのインポートエラー")

# `curl -sf (これ) | python`を実施すると、カレントディレクトリになる
# なお、`__file__`は`<stdin>`が表示される
