#!/bin/sh
# need: `brew install imagemagick`

for file in $(find $(dirname $0) -name "*.png")
do
  webp=${file%.*}.webp
  if [ -f "${webp}" ]
  then
   continue
  fi

  resize="${file%.*}_resize.${file##*.}"
  convert "$file" -resize "1024"x"768" -sharpen 1 "${resize}"
  cwebp ${resize} -o "${webp}"
  rm "${resize}"
done
