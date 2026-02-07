/*
* Replacing the icon for a custom marker.
* Copyright (c) 2014 kebasyaty
* License MIT
*/

$( document ).ready( function() {
  'use strict';
  if ( $( 'form' ).is( '#placemark_form' ) ) {
    const mapID = $( '#id_ymap option:selected' ).val();

    if ( mapID ) {
      const slugIcon = $( '#id_icon_slug' );

      $.get( '/djeym/ajax-upload-icon-collection/', {
        mapID: mapID
      } )
        .done( function( data ) { //
          // Add button
          slugIcon.after( '<span class="view_icon change_slug_icon" title="' +
                            window.gettext( 'Icon replacement' ) + '">' +
                          '<span class="mdi mdi-map-marker-multiple"></span></span>' );

          // Add Icon list
          slugIcon.after( '<div class="icon_list_wrap">' +
                          '<div class="icon_list_wrap__top_block">' +
                          '<span class="mdi mdi-close icon_list_wrap__close"></span></div>' +
                          '<div class="icon_list_wrap__center_block"></div></div>' );

          const centerBlock = $( '.icon_list_wrap__center_block' );
          data.iconCollection.forEach( item => {
            centerBlock.append( '<div class="icon_list_wrap__icon" data-slug="' +
                                  item.slug + '" ' +
                               'style="background-image: url(' + item.url + ');"></div>' );
          } );

          // Open icon list
          $( document ).on( 'click', '.change_slug_icon', function() {
            $( '.change_slug_icon' ).hide();
            $( '.icon_list_wrap' ).css( 'display', 'inline-block' );
          } );

          // Close icon list
          $( document ).on( 'click', '.icon_list_wrap__close', function() {
            $( '.icon_list_wrap' ).hide();
            $( '.change_slug_icon' ).show();
          } );

          // Apply selected icon
          $( document ).on( 'click', '.icon_list_wrap__icon', function() {
            $( '#id_icon_slug' ).val( $( this ).data( 'slug' ) );
            $( '.icon_list_wrap' ).hide();
            $( '.change_slug_icon' ).show();
          } );
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
    }
  }
} );
