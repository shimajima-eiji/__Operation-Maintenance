#!/bin/sh

: <<README
# optimize_images.sh
## 使い方
#``
curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_github/workflows/optimize_images.sh >./__optimize_images.sh
source ./__optimize_images.sh
rm ./__optimize_images.sh
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
  source "${devtool}"
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
既にwebpが存在する場合はスキップ
__main__
current="$(dirname $0)"
convert_to="${current}/webp"

for file in $(find "${current}" -maxdepth 1 -name "*.png" -or -name "*.jpg" -or -name "*.jpeg")
do
  webp="${convert_to}/${file%.*}.webp"
  # 既に変換されているファイルはやらない
  if [ -f "${webp}" ]
  then
    __skip "$(__green ${file}): already webp."
    continue
  fi

  convert_from="${current}/base"
  mkdir -p "${convert_from}"
  mkdir -p "${convert_to}"
  convert_file "${file}" "${webp}" "${convert_from}" &
done
wait

__end "$0"
