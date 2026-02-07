/*
* Ban user if vandalism is to be prevented.
* Copyright (c) 2014 kebasyaty
* License MIT
*/

$( document ).ready( function() {
  'use strict';

  if ( $( 'form' ).is( '#placemark_form' ) ) {
    const mapID = $( '#id_ymap option:selected' ).val();

    if ( mapID ) {
      const inputUserIP = $( '#id_user_ip' );
      const csrftoken = $( 'input[name="csrfmiddlewaretoken"' ).val();
      inputUserIP.after( '<span class="view_icon block_ip" title="' +
                       window.gettext( 'Block IP' ) + '">' +
                       '<span class="mdi mdi-cancel"></span></span>' );

      $( document ).on( 'click', '.block_ip', function() {
        const ip = inputUserIP.val();
        $.post( '/djeym/ajax-block-ip-address/', {
          ip: ip,
          csrfmiddlewaretoken: csrftoken
        } )
          .done( function() {
            alert( ip + ' --> ' + window.gettext( 'Added to the list of blocked IPs.' ) );
          } )
          .fail( function( jqxhr, textStatus, error ) {
            const err = textStatus + ', ' + error;
            let errDetail = '';

            if ( jqxhr.responseJSON !== undefined &&
                      jqxhr.responseJSON.detail !== undefined ) {
              errDetail = jqxhr.responseJSON.detail;
            }

            if ( errDetail.length !== 0 ) {
              console.log( 'Request Failed: ' + err + ' - ' + errDetail );
              alert( errDetail.replace( /<.*?>/g, '' ) );
            } else {
              console.log( 'Request Failed: ' + err );
            }
          } );
      } );
    }
  }
} );
