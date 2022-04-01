#!/bin/sh
echo "| ファイル名 | MD5 | SHA256 |"
echo "| -------- | --- | ------ |"

path="."  # フルパスが欲しい場合、$(pwd)
for file in $(find "${path}")
do
  md5_sum=$(md5 ${file} | cut -d' ' -f4)
  sha256_sum=$(shasum -a 256 ${file} | cut -d' ' -f1)
  echo "| ${file} | ${md5_sum} | ${sha256_sum} |"
done
