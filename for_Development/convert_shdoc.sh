#!/bin/sh

# 引数にファイルパスを受け取っていない場合は処理をしない
if [ ! -f "$1" ]
then
  echo "[Stop] Required 1 args.(file-path)"
  echo ""
  echo "[End $0]"
  exit 1
fi

echo "[Start ${0}]"
echo ""

write_flag="false"
source_file=$1
markdown_file="${source_file%.*}.md"

# 既にマークダウンファイルが存在する場合は削除しておく
if [ -f "${markdown_file}" ]
then
  rm ${markdown_file}
fi

# ファイルの行数を取得し、行数分ループする
for index in $(seq 1 $(sed -n '$=' ${source_file}))
do
  line="$(sed -n ${index}P ${source_file})"

  # READMEの書き込み開始地点を検出
  if [ "${write_flag}" = "false" -a -n "$(echo ${line} | grep '<<README')" ]
  then
    write_flag="true"
  
  # READMEの書き込み終了地点を検出
  elif [ "${write_flag}" = "true" -a -n "$(echo ${line} | grep 'README')" ]
  then
    write_flag="false"

  # 書き込み範囲内の場合、追記
  elif [ "${write_flag}" = "true" ]
  then
    # コード部分はエスケープのため、「#``」としているのでこれを正しく表示させる
    if [ "${line}" = '#``' ]
    then
      line='```'
    fi

    echo "${line}" >>${markdown_file}

  # 書き込み範囲外の場合、何もせず終了
  fi
done

echo "Convert [${source_file}] -> [${markdown_file}]"
echo ""
echo "[Complete $0]"
