#!/bin/sh
### need `apt install translate-shell`
### curl -sf https://raw.githubusercontent.com/shimajima-eiji/Settings_Environment/main/for_WSL/translate.sh | sh -s "(変換したいファイルパス)"
### .gitや.githubディレクトリなど、隠しファイルは対象にしない。
### 実運用時は出力を捨てた方が使いやすいかもしれない。

# transコマンドが使えなければやらない
if [ -z "$(which trans)" ]
then
  echo "[Stop] not found 'trans(translate-shell)'"
  exit 1
fi

# ディレクトリパスを引数に指定されていない場合はやらない
arg=$1
if ! [ -d "${arg}" -o -f "${arg}" ]
then
  echo "[Stop] Require arg. or arg isn't file or directory. ${arg}"
  exit 1
fi

source_arg=$2
target_arg=$3

# API制限を回避する
wait () {
  # FYI:
  # - https://qiita.com/eggplants/items/f3de713add0bb4f0548f
  # - https://webbibouroku.com/Blog/Article/linux-rand
  sleep "$(($(od -An -tu2 -N2 /dev/urandom | tr -d ' ')%5))"
}

# [Hint] 変換したファイルや行数が知りたい場合は、ファイル行数からカウントすべき
run () {
  echo  # メッセージを見やすくするため、改行する
  arg=$1
  source_arg=$2
  target_arg=$3

  # バイナリファイルは変換できないのでスキップ
  if [ -n "$(file --mime ${arg} | grep 'charset=binary')" ]
  then
    echo "[Skip] File is binary: ${arg}"
    return 1
  fi

  # ログファイルは対象にしない
  if [ "${arg##*.}" = "log" ]
  then
    echo "[Skip] File is exclude extension[.log]: ${arg}"
    return 1
  fi

  # ファイル名が「_」から始まる場合は対象にしない
  if [ "$(basename "${arg}" | cut -c1 )" = "_" ]
  then
    echo "[Skip] Filename is exclude pattern[_]: ${arg}"
    return 1
  fi

  # 対象ファイルが、過去に変換のために作成したものである場合はスキップ
  if [ -n "$(echo ${arg} | grep '_en.md')" -o -n "$(echo ${arg} | grep '_ja.md')" ]
  then
    echo "[Skip] translated file: ${arg}"
    echo "[Hint] '(name)_ja.md' and '(name)_en.md' is translate file."
    return 1
  fi

  #  既に変換済みのファイルの場合はスキップする（更新時は変換ファイルを手動削除すること）
  transen_file="${arg%.*}_en.md"
  transja_file="${arg%.*}_ja.md"
  if [ -f "${transen_file}" -o -f "${transja_file}" ]
  then
    echo "[Skip] Already translate: ${transen_file} or ${transja_file}"
    echo "[Hint] Case: updated ${arg}. 'rm (${transen_file} or ${transja_file})' after push."
    return 1
  fi

  # 翻訳する言語が決まっている場合は判定しない
  if [ -n "${source_arg}" -a -n "${target_arg}" ]
  then
    source=${source_arg}
    target=${target_arg}
    transfile="${arg%.*}_${target_arg}.md"

  else
    # 言語検出。ファイルの一行目を取得する。
    # ここでは基本的に日本語に変換するが、入力が日本語だったり、言語を検出できない場合は英語にする
    target="ja"
    source="en"
    result="$(trans -b :${target} "$(head -n 1 "${arg}")" 2>/dev/null)"
    transfile="${transja_file}"

    if [ "$(head -n 1 "${arg}")" = "${result}" -o -n "$(echo "${result}" | grep 'Did you mean: ')" ]
    then
      target="en"
      source="ja"

      transfile="${transen_file}"
    fi
  fi

  # ファイルから全ての行を抽出して変換する。
  echo
  echo "[INFO] Run translate(${target}): ${arg} -> ${transfile}"

  # 初期設定
  row_count=0
  source_flag='false'
  curl_log="$(pwd)/curl_gas.log"
  source ~/.env  # GAS_TRANSLATE_ENDPOINTを呼び出す
  curl_py="curl_translate.py"

  # jqコマンドが使えるならGASに問い合わせてみる
  if [ "$(which jq)" -a -n "${GAS_TRANSLATE_ENDPOINT}" ]
  then
    curl -sf https://raw.githubusercontent.com/shimajima-eiji/__Settings_Environment/main/for_WSL/translate_curl.py >${curl_py}
  fi

  # ファイル走査
  while read line
  do
    row_count=$((row_count+1))

    # 改行ではない場合
    if [ -n "${line}" ]
    then

      # markdownのソースコード表記は、フラグを入れ替えて```を追記
      if [ "${line}" = '```' ]
      then
        if [ "${source_flag}" = 'true' ]
        then
          source_flag='false'

        else
          source_flag='true'

        fi
        echo "${line}" >>${transfile}
        echo "[TRANSLATE PROGRESS] ${row_count}: ${line}"

      # ソースコードの場合は翻訳しない
      elif [ "${source_flag}" = 'true' ]
      then
        echo "${line}" >>${transfile}
        echo "[TRANSLATE PROGRESS] ${row_count}: ${line}"

      # ソースコードではない場合は翻訳する
      else
        # pyをcurlしているならGASを優先する
        if [ -f "${curl_py}" ]
        then
          python "${curl_py}" "${GAS_TRANSLATE_ENDPOINT}?text=${line}&source=${source}&target=${target}" "${curl_log}"

          # curlが成功した時はTranslate-GASの結果を入れる。2>/dev/nullは${curl_log}が存在しなかった場合にエラーメッセージを吐くため
          if [ -f "${curl_log}" -a "$(cat ${curl_log} 2>/dev/null | jq .result)" = "true" ]
          then
            translate_line="$(cat ${curl_log} | jq .translate)"
            echo "${translate_line}" >>${transfile}
            echo "[TRANSLATE PROGRESS] ${row_count}: ${line} -> ${translate_line}"

          # curlに失敗した場合は、translate-shellを使う
          else
            translate_line="$(trans -b ${source}:${target} "${line}" 2>/dev/null)"
            echo "${translate_line}" >>${transfile}
            echo "[TRANSLATE PROGRESS] ${row_count}: ${line} -> ${translate_line}"
            wait  # API制限に引っかかるので、待機時間を入れる
          fi

        # jqが使えない場合は、translate-shellを使う
        else
          translate_line="$(trans -b ${source}:${target} "${line}" 2>/dev/null)"
          echo "${translate_line}" >>${transfile}
          echo "[TRANSLATE PROGRESS] ${row_count}: ${line} -> ${translate_line}"
          wait  # API制限に引っかかるので、待機時間を入れる
        fi
      fi

    # 改行の場合
    else
      echo >>${transfile}
      echo "[TRANSLATE PROGRESS] ${row_count}:"
    fi
  done <"${arg}"

  # GASを使っている場合ｊは不要なファイルが残るので削除
  if [ -f "${curl_log}" ]
  then
    rm ${curl_log}
  fi
  # GASを使っている場合ｊは不要なファイルが残るので削除
  if [ -f "${curl_py}" ]
  then
    rm ${curl_py}
  fi

  echo "[COMPLETE] Done ${arg} -> ${transfile}"
  echo
  return 0
}

count=0  # 変換したファイル数をカウント
find_file () {
  arg="$1"
  source_arg=$2
  target_arg=$3

  # 変数がファイルなら変換処理
  if [ -f "${arg}" ]
  then
    run "${arg}" "${source_arg}" "${target_arg}"

    if [ $? -eq 0 ]
    then
      count=$((count+1))
    fi

  # 変数がファイル以外ならディレクトリを移動してサーチする
  else
    cd "${arg}"

    for path in *
    do
      find_file "${path}" "${source_arg}" "${target_arg}"
    done
    cd ..
    echo
  fi
}

find_file "${arg}" "${source_arg}" "${target_arg}"
echo "[COMPLETE] translate files:"
echo ${count}
