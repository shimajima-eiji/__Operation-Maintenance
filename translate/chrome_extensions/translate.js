function language ( object )
{
  let value = ( object.value == "ja" ) ? 0 : 1;
  document.getElementById( 'target' ).options[ value ].selected = true;
}

document.getElementById( 'clear' ).addEventListener( "click", () =>
{
  document.getElementById( 'convert_from' ).value = '';
} );

document.getElementById( 'convert' ).addEventListener( "click", () =>
{
  let get_value = ( id ) => document.getElementById( id ).value;
  let text = get_value( "convert_from" );
  let source = get_value( "source" );
  let target = get_value( "target" );

  const SCRIPT_ID = 'AKfycbzX_fawOiQ-7ZKfbBlVc_3GM5YSDrStUJ5oASwt_Gt7VuzQciSLT8WTA426Vhxxiq3NOg'  // https://github.com/shimajima-eiji/--GAS_v5_Translate をpullしたプロジェクトのデプロイURLを指定
  const endpoint = 'https://script.google.com/macros/s/' + SCRIPT_ID + '/exec'
  let url = endpoint + "?text=" + text + "&source=" + source + "&target=" + target

  const request = new XMLHttpRequest();
  request.open( 'GET', url, true );
  request.responseType = 'json';

  request.onload = function ()
  {
    var data = this.response;
    document.getElementById( 'convert_to' ).value = data.translate;
  };

  request.send();
} );
