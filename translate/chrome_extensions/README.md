# URL
- [デモページ(Github Pages)](https://shimajima-eiji.github.io/__Operation-Maintenance/translate/chrome_extensions)
- [GASリポジトリ](https://github.com/shimajima-eiji/--GAS_v5_Translate)

# 翻訳した記録と履歴を残す
PC版の翻訳機能っぽいUIでGASにcurlして履歴を保存する

- 翻訳UIはindex.html
- 履歴を残す機能はGAS
- 翻訳処理もGAS

# 事前設定
ファイルをcloneして`translate.js`の`SCRIPT_ID = ''`にGASのスクリプトIDを入れてください。<br />
入れたらそのまま実行できます。

詳細は当該リポジトリを見て欲しいのですが、forkした後のGASにも設定が必要です。

# 使い方
デモページの通り。<br />
デモページの動作をchrome extensions(ver3)でも実行できるようにしています。

# 注意
LanguageAPIは回数制限があります。<br />
勉強用やデバッグ程度であればおそらく問題はないと思いますが、やりたくなるのが「日本語のファイルを流し込んで翻訳したい」というようなシーン。<br />
特に会社で使いたくなったりする事はありますが、社用で使う場合はセキュリティ面も含めて考える必要があります。
