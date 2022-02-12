/**
 * 以下ファイルを先に読み込まれている想定
 * define.js
 * modules.js
 */

/* 初期画面作成 */
(async () => {
  const response = await run_fetch("get", LOAD_SCRIPT, set_param());

  // gas_id
  webhook.value = response[0].gas_id;

  // method
  getEBI("post").checked = (response[1].method == "post") ? true : false
  console.log(response[2].parameter)

  // parameter
  try {
    const params = JSON.parse(response[2].parameter)
    Object.keys(params).forEach(key => add_param(key, params[key]));
  } catch (e) {

  }
})();

/* ボタン制御 */
getEBI("add").addEventListener("click", () => add_param());  // 追加
getEBI("remove").addEventListener("click", remove_param);    // 削除
getEBI("save").addEventListener("click", () => run_fetch(    // 保存
  "post",
  LOAD_SCRIPT,
  {
    gas_id: webhook.value,
    method: document.methods.method.value,
    parameter: JSON.stringify(set_param()),
  }
))
getEBI("submit").addEventListener("click", async () =>       // 送信
{
  const SCRIPT_ID = webhook.value;
  if (!SCRIPT_ID) return;

  const response = await run_fetch(document.methods.method.value, SCRIPT_ID, set_param());
  getEBI("result").innerText = JSON.stringify(response);                        // result
});
