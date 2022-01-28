# Related Services
- https://github.com/shimajima-eiji/- GAS_v5_Translate

# File introduction
File name | Usage | Required tools | Where to use |
| -------------------- | ---- | --- | --- |
| translate_curl.py | Translate a single character | GAS Endpoint (Get) ||
| translates_curl.py | Translate multiple characters together | GAS Endpoint (Post) ||
| translate_google.py | Translate one character | googletrans (pip) | Not used from a logging point of view |
| translates_google.py | Translate multiple characters at once | googletrans (pip) | Not used from a logging point of view |
| translate_path.py | File search and batch conversion | GAS and googletrans (API restriction avoidance) ||

I don't use `translate.sh`

# Google-translate
- `pip install git + https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api`
- `pip install googletrans == 4.0.0-rc1`

It can be executed by either.
Be careful when changing the package to be installed because the script description is different.

```
from googletrans import Translator  # pip install (git+https://github.com/alainrouillon/py-googletrans@feature/enhance-use-of-direct-api or googletrans==4.0.0-rc1)

tr = Translator(service_urls=['translate.googleapis.com'])  # git
tr = Translator()  # 4.0.0-rc1
```
