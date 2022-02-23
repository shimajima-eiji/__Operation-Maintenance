#!/bin/sh

: <<README
# setup_develop-code.sh
## 使い方
当該コード内に以下を入れておく

#``
if [ ! "$(type -t __check_setup_develop_code)" = "function" ]
then
  curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Operation-Maintenance/main/for_Development/setup_develop-code.sh >./setup_develop-code.sh
  source ./setup_develop-code.sh
  rm ./setup_develop-code.sh
fi
#``

## 解説
- shebangは意識する必要はないが、./setup_develop-code.shで/bin/shが実行できるように指定しておく
- 敢えて白色を指定するシーンが思いつかないので、関数ではなく定数とする。なくてもいい

## 参考
- [シェルスクリプトのechoで”問題なく”色をつける(bash他対応)](https://qiita.com/ko1nksm/items/095bdb8f0eca6d327233)

## READMEバージョン
2022.02.21

README

# 判定ロジック用。変更しない
__check_setup_develop_code() {
  echo "version: 2022.02.24"
}

# 定義
__color="\033"
__white="${__color}[37m"
__print() {
  printf "${__color}$1${@:2}${__white}"
}

# 使用したいカラーコードは以下に追加する
__red() {
  __print "[31m" "$@"
}

__green() {
  __print "[32m" "$@"
}

__blue() {
  __print "[34m" "$@"
}

__yellow() {
  __print "[33m" "$@"
}

## よく使うカラーコードを利用するパターンを登録しておく
__start() {
  echo "[$(__blue Start): $1]"
  echo ""
}

__skip() {
  echo "[$(__yellow Skip)] $1"
}

__end() {
  echo ""
  echo "[$(__blue End: ): $1]"
  exit 0
}

__success() {
  echo "[$(__green Success)] $1"
}

# 実行シェルをシバンで強制したい場合
__search_shell() {
  if [ $# -lt 1 ]
  then
    echo "[$(__red Stop): $(__blue __search_shell)] Required 1 args.(path)"
    exit 1
  fi

  # Macの場合
  if [ $(uname) = "Darwin" ]
  then
    run_shell="$(ps $$ | awk 'NR==2 {print $5}' | awk -F/ '{print $NF}')"

  # スクリプト側が対応していないケースを想定して、手入力も許可する
  else
    run_shell=$2
  
  fi
  shebang="$(head -1 $1 | awk -F/ '{print $NF}')"

  if [ ! "${run_shell}" = "${shebang}" ]
  then
    echo "[$(__red Stop): $(__blue __search_shell)] Required command: [ $(__blue ./${1}) ]"
    exit
  fi
}
