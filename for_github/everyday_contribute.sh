#!/bin/sh
# @param
# [*]$1: git clone path
# $2: repository url(https/ssh)
#
# eg: curl -sf https://raw.githubusercontent.com/shimajima-eiji/Settings_Environment/main/for_github/everyday_contribute.sh | sh -s -- README https://github.com/shimajima-eiji/README

update_file="dummy"

stop_flag=false
if [ -n "$1" ]
then
  git_clone_path=$1
else
  echo "[stop] Require argument: path(git clone directory)"
  stop_flag=true
fi

# git_clone_url=${2:}
if [ -n "$2" ]
then
  git_clone_url=$2
fi

# 指定したディレクトリが存在しない
if [ ! -d "${git_clone_path}" ]
then

  # リポジトリ.gitを指定している場合はcloneする
  if [ -n "${git_clone_url}" ]
  then
    git clone ${git_clone_url} ${git_clone_path}
    clone_flag=true

    # git cloneが失敗した場合は中断する
    if [ ! "$?" = 0 ]
    then
      echo "[stop] failed command: [git clone ${git_clone_url} ${git_clone_path}]"
      stop_flag=true
    fi

  # リポジトリ.gitを指定していない場合は中断する
  else
    echo "[stop] not found: ${git_clone_path}"
    echo "Hint: add argument [git clone url]. git clone [argu2:url] [argu1:path]"
    stop_flag=true
  fi
fi

# 前提の処理に失敗していた場合は中断する
if [ "${stop_flag}" = "true" ]
then
  exit 1
fi

cd ${git_clone_path}

# ファイルを差し替えてアップロード
today=$(date "+%Y/%m/%d")
echo "dummy update: $today" >$update_file
git add $update_file
git commit -m "dummy update: $today"
git push

# cloneしてきた場合は削除
if [ "${clone_flag}" = "true" ]
then
  cd ..
  rm -rf ${git_clone_path}
fi
