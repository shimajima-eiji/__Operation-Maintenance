document.getElementById( 'source' ).addEventListener( "change", () =>
{
  let value = ( document.getElementById( 'source' ).value == "ja" ) ? 0 : 1;
  document.getElementById( 'target' ).options[ value ].selected = true;
} );

document.getElementById( 'clear' ).addEventListener( "click", () =>
{
  document.getElementById( 'convert_from' ).value = '';
} );

document.getElementById( 'convert' ).addEventListener( "click", () =>
{
  document.getElementById( 'convert_to' ).placeholder = '翻訳中…';
  let get_value = ( id ) => document.getElementById( id ).value;
  let text = get_value( "convert_from" );
  let source = get_value( "source" );
  let target = get_value( "target" );

  const SCRIPT_ID = 'AKfycbzX_fawOiQ-7ZKfbBlVc_3GM5YSDrStUJ5oASwt_Gt7VuzQciSLT8WTA426Vhxxiq3NOg'  // https://github.com/shimajima-eiji/--GAS_v5_Translate をpullしたプロジェクトのデプロイURLを指定
  const endpoint = 'https://script.google.com/macros/s/' + SCRIPT_ID + '/exec'

  let add = ( text ) =>
  {
    let object = document.getElementById( 'convert_to' );
    object.value = object.value + text + '\n';
  }
  document.getElementById( 'convert_to' ).value = '';
  text.split( '\n' ).forEach( ( word ) =>
  {
    let parameter = "?text=" + word + "&source=" + source + "&target=" + target;
    let url = endpoint + parameter;

    let request = new XMLHttpRequest();
    request.open( 'GET', url + "&by=Github Pages(Chrome Extensions)", true );
    request.responseType = 'json';

    // アロー関数にしたら怒られるのでこのままで
    request.onload = function ()
    {
      add( this.response.translate );
    };
    request.send();
  } );

} );

function setup ()
{
  const SCRIPT_ID = 'AKfycbzX_fawOiQ-7ZKfbBlVc_3GM5YSDrStUJ5oASwt_Gt7VuzQciSLT8WTA426Vhxxiq3NOg'  // https://github.com/shimajima-eiji/--GAS_v5_Translate をpullしたプロジェクトのデプロイURLを指定
  const endpoint = 'https://script.google.com/macros/s/' + SCRIPT_ID + '/exec?extension=true'

  let request = new XMLHttpRequest();
  request.open( 'GET', endpoint, true );
  request.responseType = 'json';
  request.onload = function ()
  {
    document.getElementById( 'convert_from' ).value = this.response.text;
    document.getElementById( 'convert_to' ).value = this.response.translate
  };
  request.send();
}
setup();
