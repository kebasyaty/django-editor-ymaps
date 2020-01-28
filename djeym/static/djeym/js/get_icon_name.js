/*
* Get Icon name.
* Copyright (c) 2014 kebasyaty
* License MIT
*/

$( document ).ready( function() {
  'use strict';

  $( '#id_svg' ).on( 'change', function() {
    const img = $( this )[ 0 ].files[ 0 ];
    const imgName = img.name.split( '.' ).slice( 0, -1 ).join( '.' );
    $( '#id_title' ).val( imgName );
  } );
} );
