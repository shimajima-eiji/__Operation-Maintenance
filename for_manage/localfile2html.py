from pathlib import Path
import sys

"""
# README.md
## 引数
- current_directory(current path): ファイル走査をするディレクトリ。後述の構成を想定している
- output_path(output.html): 結果を出力するファイル。.mdを作る

## 使い方
```
curl https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_manage/localfile2html.py > localfile2html.py
python localfile2html.py (走査するパス) （結果の出力先）
```

## ゲームファイルのディレクトリ構成
windowsを想定しているのでフォルダーと表記しておくが、ディレクトリと同じ。

```
.
├── カテゴリー
│   ├── タイトル
│   │   ├── 判別ファイル(saveフォルダやsetup.exeなど)
│   │   └── window
│   ├── タイトル
... ... ...
├── カテゴリー
│   ├── タイトル
... ... ...
├── 任意（本スクリプトで扱わない）
│   ├── カテゴリー
│   │   ├── タイトル
... ... ... 
```

### 注意事項
- 追記処理をしているので、カテゴリは重複してよい
- ゲームタイトルが重複している場合、スクリプトが最初に発見したディレクトリを採用する
- ファイル走査部分(78行目for文)で細かい分岐条件を追加していく

"""

# 引数処理
current_directory = Path(sys.argv[1] if len(sys.argv) > 1 and Path(
    sys.argv[1]).is_dir() else Path().cwd())
output_path = Path(sys.argv[2] if len(sys.argv) > 2 else "output.html")

output_path.parent.mkdir(parents=True, exist_ok=True)

# データクレンジング
games = []
categories = []
for path in current_directory.glob("**"):
    # 隠しディレクトリが含まれているパターンのディレクトリパスは除外
    # ディレクトリ名を走査し、"."で始まり2文字以上存在する場合を検出
    if(any([p[:1] == "." and len(p) > 1 for p in str(path).split("/")])):
        continue

    # 「既に確認済みのタイトル名」をパスから見つけた場合は除外
    if(any([Path(p).name in games for p in str(path).split("/")])):
        continue

    # PRGMV(www/save)。後述が当たるのでなくてもいいかもしれない
    if(path.name == "save" and path.parent.name == "www"):
        # print(path.parent.name)
        games.append(path.parent.parent.name)
        categories.append(path.parent.parent.parent.name)
        continue

    # RPGMV(www)。findの仕様上、先にこちらが当たる
    if(path.name == "www"):
        # print(path.parent.parent.name, path)
        games.append(path.parent.name)
        categories.append(path.parent.parent.name)
        continue

    # 多くのタイトルが該当する
    if(path.name == "save" or path.name == "Save"):
        # print(path.parent.name)
        games.append(path.parent.name)
        categories.append(path.parent.parent.name)
        continue

    # フォルダ管理をしていない（カレント直下にsaveファイルを置いている）タイトルの場合、ファイル走査
    for p in path.glob("*"):
        # 「既に確認済みのタイトル名」をパスから見つけた場合は除外
        if(any([file in games for file in str(p).split("/")])):
            continue

        # Mac用(app形式)はフォルダ扱いなので、先行して処理する
        if(p.is_dir() and p.suffix == ".app"):
            games.append(p.parent.name)
            categories.append(p.parent.parent.name)
            continue

        # ファイルではない場合は除外
        if(not p.is_file()):
            continue

        # RPGVXAce or PRGMV
        if(p.suffix == ".rvdata" or p.suffix == ".rvdata2" or p.suffix == ".rpgsave"):
            games.append(p.parent.name)
            categories.append(p.parent.parent.name)
            continue

        # PRGMVとPRGVXAceは上記で登録できるはずなので、以降の判定はしない
        if(any([file == "RPGMV" for file in str(p).split("/")])
           or any([file == "RPGVXAce" for file in str(p).split("/")])):
            continue

        # 多くの作品で採用されている拡張子
        if(p.suffix == ".sav" or p.suffix == ".SAV"):
            if(
                not "sav" in p.parent.name
                and not "Sav" in p.parent.name
                and not "SAV" in p.parent.name
            ):
                games.append(p.parent.name)
                categories.append(p.parent.parent.name)
                continue

            games.append(p.parent.parent.name)
            categories.append(p.parent.parent.parent.name)
            continue

        # saveファイルをAppDataやMyDocumentなどに格納している場合は、ゲームエンジンのパターンから推測する
        if(p.name == "setup.exe"           # 汎用
           or p.name == "uninstall.exe"    # 汎用
           or p.name == "Uninstall.exe"    # 汎用
           or p.name == "UnityPlayer.dll"  # Unity
           or p.name == "data.xp3"         # 吉里吉里
           ):
            games.append(p.parent.name)
            categories.append(p.parent.parent.name)
            continue

        # その他、経験に基づいて除外するパターン
        # ここに来る場合でも結果的にgamesに登録されている場合があるが、先に登録対象外のファイルを走査し、その後登録対象ファイルを走査すると可能性があるので扱いに注意
        # print(p, games)

    if(path.name in games):
        continue

    # print(path)

# 構築
html = [f"<tr><td>{categories[i]}</td><td>{g}</td></tr>" for i,
        g in enumerate(games)]
markdown = [f"|{categories[i]}|{g}|" for i,
            g in enumerate(games)]

with output_path.open(mode="w") as f:
    f.write(
        f"<table><tr><th>カテゴリー</th><th>タイトル</th></tr>{''.join(html)}</table>")

with output_path.with_suffix(".md").open(mode="w") as f:
    f.write("|カテゴリー|タイトル|\n|---|---|\n" + '\n'.join(markdown))
