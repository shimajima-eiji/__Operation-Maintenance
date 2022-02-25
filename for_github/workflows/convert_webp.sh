#!/bin/sh

: <<README
# convert_webp.sh
## 使い方
#``
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_github/workflows/convert_webp.sh >./__convert_webp.sh
source ./__convert_webp.sh
rm ./__convert_webp.sh
#``

## 前提
以下がインストールされている必要がある

- imagemagick
- webp(cwebp)

## 解説
拡張子を「.command」に変えると、Macでもスクリプトが動くように作っている

## READMEバージョン
2022.02.21

README

# 開発ツールをインストール
if [ ! "$(type -t __check_setup_develop_code)" = "function" ]
then
  devtool="./__setup_develop-code.sh"
  curl -sf "https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_Development/setup_develop-code.sh" >"${devtool}"
  . "${devtool}"
  rm "${devtool}"
fi
# インストールに失敗していたら、以下の実行に失敗してしまう

__start "$0"

: <<convert_file
## 用途
マルチスレッド化のため、変換部分を切り出す
リサイズした後にwebpに変換する

## パラメータ
$1はfindで取得した結果なのでファイルチェックは不要
$2は存在しないwebpパスなのでファイルチェックは不要
$3はファイルの存在を気にせず強制的に書き換える運用にする
convert_file
convert_file() {
  file=$1
  webp=$2
  move=$3

  width="720"   #px
  height="540"  #px
  resize="${file%.*}_resize.${file##*.}"

  convert "${file}" -resize "${width}"x"${height}" -sharpen 1 "${resize}"
  cwebp ${resize} -o "${webp}"
  rm "${resize}"
  mv "${file}" "${move}/$(basename ${file})"

  __success "${file} -> ${webp}"
}

: <<__main__
pngとjpgをwebpに変換する
パスがディレクトリの場合、元ファイルはbaseディレクトリへ、webpファイルはwebpディレクトリに移動する
既にwebpに変換している場合はスキップ
__main__
path=${1:-$(dirname $0)}

# パスがファイルなら、そのファイルだけ変換
# ディレクトリの場合と違って、webpファイルがあっても上書きする
if [ -f "${path}" ]
then
  # 拡張子がpng, jpgでなければやらない
  extension=${path##*.}
  if [ ! "${extension}" = "png" ] && [ ! "${extension}" = "jpg" ] && [ ! "${extension}" = "jpeg" ]
  then
    __skip "Not supported extension: [${extension}]"
    __end $0
  fi

  current="$(dirname ${path})"
  webp="${current}/$(basename ${path%.*}.webp)"
  convert_file "${path}" "${webp}" "${current}"
  exit 0

# パスがファイルでもディレクトリでもない場合はスキップ
elif [ ! -d "${path}" ]
then
  __skip "Not found: [${path}]"
  __end "$0"
fi

# パスがディレクトリの場合、ファイルサーチ
# baseディレクトリのファイルは対象外とする
# ファイルの場合と違って、webpファイルが存在していた場合はスキップ
for file in $(find "${path}" -name "*.png" -or -name "*.jpg" -or -name "*.jpeg" -not -name "*/base/*")
do
  # baseディレクトリに移動したファイルは、変換をしているはずなので除外する
  current="$(dirname ${file})"
  [ "$(basename ${current})" = "base" ] && continue

  # webpファイルが同一ディレクトリ内に存在していれば変換をしているはずなので除外する
  # ファイルを変換した後で、ディレクトリを指定しているケースを想定
  webp="${file%.*}.webp"
  if [ -f "${webp}" ]
  then
    __skip "$(__green ${file}): already webp."
    continue
  fi

  convert_to="${current}/webp"
  webp="${convert_to}/$(basename ${file%.*}.webp)"

  # webpディレクトリに存在しているファイル名は変換済みなので除外する
  # ディレクトリ指定後にもう一度ディレクトリを指定したケースを想定
  if [ -f "${webp}" ]
  then
    __skip "$(__green ${file}): already webp."
    continue
  fi

  # 以下、変換実施。baseとwebpディレクトリを作成する
  convert_from="${current}/base"
  mkdir -p "${convert_from}"
  mkdir -p "${convert_to}"
  convert_file "${file}" "${webp}" "${convert_from}" &
done
wait

__end "$0"
