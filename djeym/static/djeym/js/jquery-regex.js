/*
* Example: 'input:regex(id, ^id_name-.+-part_of_the_name)'
*/
$( document ).ready( function() {
  'use strict';

  // jQuery - Support Regex.
  window.$.expr[ ':' ].regex = function( elem, index, match ) {
    const matchParams = match[ 3 ].split( ',' );
    const validLabels = /^(data|css):/;
    const attr = {
      method: matchParams[ 0 ].match( validLabels ) ?
        matchParams[ 0 ].split( ':' )[ 0 ] : 'attr',
      property: matchParams.shift().replace( validLabels, '' )
    };
    const regexFlags = 'ig';
    const regex = new RegExp( matchParams.join( '' ).replace( /^\s+|\s+$/g, '' ), regexFlags );
    return regex.test( $( elem )[ attr.method ]( attr.property ) );
  };
} );
