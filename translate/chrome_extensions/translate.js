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
  const fix_url = `${endpoint}?source=${source.value}&target=${target.value}&by=Operation-Maintenanceで使用&text=${from.value.split('\n').join('&text=')}`
  const response = await fetch(fix_url);
  let result = await response.json();
  to.value = result.translates.join('\n');
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
