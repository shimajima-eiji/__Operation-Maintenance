#!/bin/sh
### 要準備
### 予めwikiとwiki用のリポジトリを作成しておく

### 使い方
### curl -sf https://raw.githubusercontent.com/shimajima-eiji/Settings_Environment/main/for_github/wiki_contribute.sh | sh -s -- リポジトリ ユーザー

# 引数処理
repository=$1
user=${2:-shimajima-eiji}

# リポジトリが未入力の場合、中断
if [ -z "${repository}" ]
then
  echo "[Stop]Required arg1: [repository name]"
  exit 1
fi

# 紛らわしいので名付けをしておく
clone_directory=${repository}.wiki
wiki_repository=https://github.com/${user}/${clone_directory}.git
contribute_repository=https://github.com/${user}/__${repository}_wiki.git

# 後でディレクトリを削除するためにcloneしたか判定する
clone_flag=false
if [ ! -d "${repository}.wiki" ]
then
  git clone ${wiki_repository}  

  # 失敗したら処理を中断する
  if [ "$?" -ne 0 ]
  then
    echo "[Stop]Failed git clone ${wiki_repository}"
    rm -rf "${wiki_repository}"
    exit 1
  fi
fi

cd "${clone_directory}"
git pull
git push --mirror "${contribute_repository}"

if [ "$?" -ne 0 ]
then
  echo "[ERROR]Failed git push --mirror ${contribute_repository}"
  exit 1
fi

if [ "${clone_flag}" = true ]
then
  rm -rf "${clone_directory}"
  echo "[INFO]Remove cloned directory : ${clone_directory}"
fi

echo "[COMPLETE]wiki_contribute.sh."
