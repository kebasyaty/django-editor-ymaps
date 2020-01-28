/*
* Import/Export - Icon Collection and Source tile layer.
* Copyright (c) 2014 kebasyaty
* License MIT
*/

$( document ).ready( function() {
  'use strict';

  $( '#changelist .actions' ).css( 'margin-top', '20px' );

  // Start load indication
  let TIMEOUT_SPIN_INDICATION;
  function startLoadIndication() {
    $( '#djeymModalLock' ).show().find( '#djeymLoadIndicator' ).addClass( 'djeym-load-indicator' );
    TIMEOUT_SPIN_INDICATION = setTimeout( function() {
      if ( $( '#djeymModalLock' ).css( 'display' ) !== 'none' ) {
        stopLoadIndication();
      }
    }, 30000 );
  }

  // Stop load indication
  function stopLoadIndication() {
    const $modalLock = $( '#djeymModalLock' );
    $modalLock.css( 'opacity', '0' );
    setTimeout( function() {
      $modalLock.find( '#djeymLoadIndicator' ).removeClass( 'djeym-load-indicator' );
      $modalLock.hide().css( 'opacity', '.85' );
      clearTimeout( TIMEOUT_SPIN_INDICATION );
    }, 1000 );
  }

  function sandFormAjax( url, formData ) {
    $.ajax( {
      type: 'POST',
      url: url,
      data: formData,
      processData: false,
      contentType: false
    } )
      .done( function() {
        stopLoadIndication();
        document.location.reload( true );
      } )
      .fail( function( jqxhr, textStatus, error ) {
        const err = textStatus + ', ' + error;
        let errDetail = '';

        stopLoadIndication();

        if ( jqxhr.responseJSON !== undefined &&
          jqxhr.responseJSON.detail !== undefined ) {
          errDetail = jqxhr.responseJSON.detail;
        }

        if ( errDetail.length !== 0 ) {
          console.log( 'Request Failed: ' + err + ' - ' + errDetail );
          alert( ( 'Request Failed: ' + err + ' - ' + errDetail ) );
        } else {
          console.log( 'Request Failed: ' + err );
          alert( 'Request Failed: ' + err );
        }
      } );
  }

  if ( $( 'a' ).is( '#id_import_icon_collection' ) ) { //
    // Import file Icon Collection.
    $( '#id_import_file_icon_collection' ).on( 'change', function() {
      const url = $( '#id_import_icon_collection' ).data( 'import-url' );
      const collectionFile = $( this )[ 0 ].files[ 0 ];
      const csrftoken = $( 'input[name="csrfmiddlewaretoken"' ).val();
      const formData = new FormData();

      formData.append( 'csrfmiddlewaretoken', csrftoken );
      formData.append( 'collection', collectionFile );

      startLoadIndication();
      sandFormAjax( url, formData );
    } );
  } else if ( $( 'a' ).is( '#id_import_tile_source' ) ) { //
    if ( ( $( 'table#result_list tr' ).length - 1 ) > 0 ) {
      $( '#id_export_tile_source' ).show();
    }

    // Import file with sources of tile layers.
    $( '#id_import_file_tile_source' ).on( 'change', function() {
      const url = $( '#id_import_tile_source' ).data( 'import-url' );
      const sourcesFile = $( this )[ 0 ].files[ 0 ];
      const csrftoken = $( 'input[name="csrfmiddlewaretoken"' ).val();
      const formData = new FormData();

      formData.append( 'csrfmiddlewaretoken', csrftoken );
      formData.append( 'sources', sourcesFile );

      startLoadIndication();
      sandFormAjax( url, formData );
    } );
  }

  if ( $( 'input' ).is( '#id_site' ) ) {
    const $site = $( '#id_site' );
    if ( $site.val().length > 0 ) {
      const url = $site.val();
      const btn = '<div class="tile_go_to_website_btn"><a href="' + url +
        '" target="_blank" rel="nofollow noreferrer noopener">' +
        '<img src="/static/djeym/img/arrow_right.svg" alt="Button"></a></div>';
      $site.after( btn );
    }
  }
} );
