/**
 * 定義
 */
const GAS_ID = "(https://github.com/shimajima-eiji/--GAS_v5_Translate をpullしたプロジェクトのデプロイURL)"

const endpoint = `https://script.google.com/macros/s/${GAS_ID}/exec`
let __getEBI = (id) => document.getElementById(id);
let source = __getEBI('source')
let target = __getEBI('target')
let clear = __getEBI('clear')
let convert = __getEBI('convert')
let from = __getEBI('convert_from')
let to = __getEBI('convert_to')

/**
 * 実行
 */

// [TODO] 日本語・英語以外の追加。HTML側も追記する
source.addEventListener("change", () => {
  let value = (source.value == "ja") ? 0 : 1;
  target.options[value].selected = true;
});

// 消去ボタン
clear.addEventListener("click", () => from.value = '');

// 変換ボタン
convert.addEventListener("click", async () => {
  // 翻訳できるまで待機中メッセージを表示
  to.placeholder = '翻訳中…';

  // 可変部分はtextだけなので、雛形を作っておく
  const fix_url = `${endpoint}?source=${source.value}&target=${target.value}&by=自分で拡張機能を使った&text=`

  // forEachを非同期処理するが、一番最後の処理だけ実施させるため上限値を設定
  let results = []
  let values = from.value.split('\n')

  values.forEach(async (word, index) => {
    const response = await fetch(`${fix_url}${word}`);
    let result = await response.json();

    // 非同期だが順番があるのでarray.pushにせず、indexで管理する
    results[index] = result.translate;
    // 最後の処理の時だけ処理させる
    if (results.length == values.length)
      to.value = results.join('\n');
  });
});

(async () => {
  const response = await fetch(`${endpoint}?extension=true`);
  let result = await response.json();

  from.placeholder = "ここに翻訳したい文字を入力";
  if (result == null) {
    to.placeholder = "ここに翻訳された文字を表示";
    return;
  }

  from.value = result.text;
  to.value = result.translate;
})();
