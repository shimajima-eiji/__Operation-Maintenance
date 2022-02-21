#!/bin/sh
# git configを初回設定するためのコード群
# 引数があればそちらを優先し、なければ環境変数から取得する
git_user=${1:-${git_user}}
git_email=${2:-${git_emal}}

git config --global user.user ${git_user}
git config --global user.email ${git_email}
