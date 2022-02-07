const obj = document.getElementById( "words" );
const view = document.getElementById( "view" );

let count = () => view.value = obj.value.length;
obj.addEventListener( "keydown", () => count() );
obj.addEventListener( "keyup", () => count() );
