#!/bin/sh
# need: `brew install imagemagick webp`

if [ ! "$(type -t __check_setup_develop_code)" = "function" ]
then
  curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_Development/setup_develop-code.sh >./setup_develop-code.sh
  source ./setup_develop-code.sh
  rm ./setup_develop-code.sh
fi

__start "$0"

convert_file() {
  file=$1
  webp=$2
  resize="${file%.*}_resize.${file##*.}"
  convert "$file" -resize "1024"x"768" -sharpen 1 "${resize}"
  cwebp ${resize} -o "${webp}"
  rm "${resize}"

  __success "${file} -> ${webp}"
}

for file in $(find $(dirname $0) -name "*.png" -or -name "*.jpg" -or -name "*.jpeg")
do
  webp=${file%.*}.webp
  if [ -f "${webp}" ]
  then
    __skip "$((__green ${file})): already webp."
    continue
  fi

  convert_file "${file}" "${webp}" &
done
wait

__end "$0"
