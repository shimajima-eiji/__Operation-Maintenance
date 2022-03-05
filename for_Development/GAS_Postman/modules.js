// 定義ブロック。複数箇所で使っているものは管理のため集約
let getEBI = (id) => document.getElementById(id);
let gas = (gas_id) => {
  return (gas_id.substr(0, 4) == "http") ? gas_id : `https://script.google.com/macros/s/${gas_id}/exec`;
}
/**
 * fetch関数
 * @param
 * - method(String): GET/POST
 * - endpoint(String): GAS ID
 * - params(JSON): 送信するパラメータ
 * 
 * @returns
 * - JSON: GET=出力結果 / POST={}
 */
let run_fetch = async (method, endpoint, params) => {
  let result = {};

  // post時は第二引数にオプションを付与する。GASの仕様で値を受け取ることはできない。(GAS側でpostした値を処理する事はできる)
  // Ref: https://qiita.com/khidaka/items/ebf770591100b1eb0eff
  // Ref: https://www.sambaiz.net/article/319/
  if (method == "post") {
    let request = await fetch(endpoint, {
      method: "post",
      body: JSON.stringify(params),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
    });
    result = await request.json();

    // get時はURLにパラメータを追記し、resultに格納する
  } else {
    if (params) endpoint = `${endpoint}?${new URLSearchParams(params)}`
    let request = await fetch(endpoint);
    result = await request.json();
  }
  return result;
}

/**
 * パラメーターフォーム
 * キー列とバリュー列のinput要素を作る
 * @param
 * - key(String)
 * - value(String)
 * 
 * @return
 * none
 */
let add_param = (key, value) => {
  // 追加するキーと値を設定できるようにする。最後に改行を入れる
  parameters.appendChild(document.createElement('input'));
  if (key) parameters.lastChild.value = key
  parameters.appendChild(document.createElement('input'));
  if (value) parameters.lastChild.value = value
  parameters.appendChild(document.createElement('br'));
}

let remove_param = () => {
  // 値が入っていたら確認画面を出す。キャンセルされたら処理しない
  if (
    (parameters.lastChild.previousSibling.value  // value
      || parameters.lastChild.previousSibling.previousSibling.value  // key
    )
    && !window.confirm("データが存在しますが、本当に削除して良いですか？\n（削除後は復元できないので、誤って削除した場合は再投入してください）")
  ) return;

  // key, value, brを削除
  parameters.removeChild(parameters.lastChild);
  parameters.removeChild(parameters.lastChild);
  parameters.removeChild(parameters.lastChild);
}

/**
 * saveとsubmitで使用
 * parametersの要素を全取得
 * @param
 * - 引数を受け取って使う事を想定していない（再起処理用）
 * @return
 *   JSONS String
 */
let set_param = (target = parameters.firstChild, body) => {
  // targetは必ずbrの要素になっているので、次の要素にkey,valueが入っている
  if (!target.nextSibling || !target.nextSibling.value || !target.nextSibling.nextSibling.value)
    // 次の要素が見つからなければ生成した値を返す
    return (body) ? body : undefined

  // keyとvalueを取得して次の要素を渡す
  // JSONの場合
  if (!body) body = {}
  body[target.nextSibling.value] = target.nextSibling.nextSibling.value;

  // JSONS Stringの場合。使っていないのでコメントアウト中
  // if(!body) body = []
  // body.push({[target.nextSibling.value]: target.nextSibling.nextSibling.value});

  return set_param(target.nextSibling.nextSibling.nextSibling, body);
}