#!/bin/bash
# @param
# [*]$1: git clone path
# $2: repository url(https/ssh)

update_file=dummy

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

for now_day in $(seq 0 380)  # 当日を含めるので0からカウントし、Webから見た時に全て反映させるのに380日分が必要
do
  if [ "$(uname)" = "Darwin" ]
  then
    message="dummy update: $(date -v -${now_day}d +"%Y/%m/%d")"
  else
    message="dummy update: $(date -d "-${now_day} days" "+%Y/%m/%d")"
  fi
  echo "${message}" >${update_file}

  git add ${update_file}  # -aをコミットに使うと`git add`は要らないが、念の為ファイルを指定する
  if [ "$(uname)" = "Darwin" ]
  then
    git commit -m "${message}" --date="$(date -v -${now_day}d)"
  else
    git commit -m "${message}" --date="$(date -d "-${now_day} days")"
  fi

  echo "${now_day} / 366: ${message}"  # debug
  echo ""
done
git push

# cloneしてきた場合は削除
if [ "${clone_flag}" = "true" ]
then
  cd ..
  rm -rf ${git_clone_path}
fi
