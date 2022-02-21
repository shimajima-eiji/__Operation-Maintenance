#!/bin/sh
. ~/.env  # ここではGITHUB_REPO_TOKENの変数を参照するため、.envには以下を記述しておく
# GITHUB_REPO_TOKEN=パスワード

#--- 適宜変更すること
user=(user)
file=CHANGELOG.md
tmpfile=tmp
#--- 変更箇所はここまで

# チェックロジック
stop_flag=false  # 処理を継続するか判断するためのフラグ。立ったら中断
# 必要なコマンド（パッケージ）の確認
if [ -z "$(which github_changelog_generator)" ]
then
  echo "[stop] Require github_changelog_generator.(`which github_changelog_generator: https://github.com/github-changelog-generator/github-changelog-generator`)"
  stop_flag=true
fi

if [ -z "$(which github_changelog_generator)" ]
then
  echo "[stop] Require github_changelog_generator.(`which github_changelog_generator: https://github.com/github-changelog-generator/github-changelog-generator`)"
  stop_flag=true
fi

if [ -z "$(git config user.name)" ]
then
  echo "[stop] Required `git config user.name.`"
  stop_flag=true
fi

if [ -z "$(git config user.email)" ]
then
  echo "[stop] Required `git config user.email.`"
  stop_flag=true
fi

# 処理を中断する条件にあたった場合は中断させる
if [ ${stop_flag} = true ]
then
  exit 1
fi

# リポジトリについては、引数で変更できるようにしておく
if [ -z "$1" ]
then
  echo "[stop] Require repository"
  stop_flag=true
else
  repository=$1
fi

# .envがない、GITHUB_REPO_TOKENが設定されていない場合はユーザーに入力させる
if [ -z "${GITHUB_REPO_TOKEN}" ]
then
  read -p "[input] github token(required permission repo):" GITHUB_REPO_TOKEN
fi

github_changelog_generator -u ${user} -p ${repository} -t ${GITHUB_REPO_TOKEN} --issues-label "### 終了・または先送りしたissue" --header-label "# 日付順" --unreleased-label "指定なし" -o ${file}
github-changes -o ${user} -r ${repository} -k ${GITHUB_REPO_TOKEN} --use-commit-body -main -t "タグ別" -z Asia/Tokyo -m "YYYY年M月D日" -n "最終更新" -a -f ${tmpfile}

# 上記github-changesで失敗した場合は古いブランチ(master)の可能性があるので再試行する
if [ ! -f "${file}" ]
then
  github-changes -o ${user} -r ${repository} -k ${GITHUB_REPO_TOKEN} -b master --use-commit-body -t "タグ別" -z Asia/Tokyo -m "YYYY年M月D日" -n "最終更新" -a -f ${tmpfile}
fi

if [ -f "${file}" ]
then
  cat ${tmpfile} >>${file}
  rm ${tmpfile}
fi

git add ${file}
git commit -m "update: ${file}"
git tag "$(date '+v%Y/%m/%d')"
git push --tags
