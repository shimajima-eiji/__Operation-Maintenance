#!/bin/sh
### curl -sf   | sh -s -- (ログファイル) (以降、コマンド。""で囲ってもOK)
### @param
###   $1 : log path
###   $2-: Recommend: command

default_path=~/logs/upsert_result_$(date "+%Y%m%d_%H%M%S").log
log_path=$1

if [ $# -eq 0 ]
then
  log_path="${default_path}"
fi

# ルートを指定できないようにする
if [ "$(dirname ${log_path})" = "/" ]
then
  log_path="${default_path}"
fi

# 指定したパスがディレクトリもしくはシンボリックリンクだった場合はデフォルトパス
if [ -d "${log_path}" -o -L "${log_path}" ]
then
  log_path="${default_path}"
fi
  
# 親ディレクトリが存在しない場合は、先にディレクトリを作成する。
create_directory() {
  if [ ! -d "$(dirname $1)" ]
  then
    mkdir -p "$(dirname $1)"
  fi
}

create_directory "${log_file}"
# 重複以外の何らかの理由で親ディレクトリ作成に失敗したらデフォルトパスを使用する
if [ ! "$?" = "0" ]
then
  log_path="${default_path}"
  create_directory "${log_file}"
fi

# 実行コマンドが引数にあれば

echo "[Command]: ${@:2}" >>${log_path}
echo >>${log_path}
# 出力先のパスを渡すために出力。
# 取得する場合は`| tail -n 1`が確実
echo "${log_path}"
