window.Superlists = {}; //namespace
window.Superlists.initialise = () => {
    $( 'input[name="text"]' ).keypress( () => {
        $( '.has-error' ).hide();
    } );
};