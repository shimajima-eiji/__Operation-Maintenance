#!/bin/sh
### 元々は.wiki.gitリポジトリをコントリビューションするために作成
### GithubActionsで実行すると権限周りで失敗するので、手動実施
### 最近は--GAS_v5_Templateを自分でforkっぽい事をするために利用

copy_from_repository=$1
copy_mirror_repository=$2

git clone https://github.com/shimajima-eiji/${copy_from_repository}.git
git push --mirror https://github.com/shimajima-eiji/${copy_mirror_repository}.git
