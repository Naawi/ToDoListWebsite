var initialise = () => {
    console.log('initialise called');
    $( 'input[name="text"]' ).keypress( () => {
        $( '.has-error' ).hide();
    } );
};
console.log('list.js loaded');