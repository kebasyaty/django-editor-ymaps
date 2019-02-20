/*
* Import/Export - Icon Collection.
* Import/Export - Source tile layer.
*/

$( document ).ready( function() {
  "use strict";

  $( "#changelist .actions" ).css( "margin-top", "20px" );

  // Start function of spin indication
  let TIMEOUT_SPIN_INDICATION;
  function startSpinIndication() {
    $( "#id_modal_lock" ).show();
    TIMEOUT_SPIN_INDICATION = setTimeout( function() {
      if ( $( "#id_modal_lock" ).css( "display" ) !== "none" ) {
        stopSpinIndication();
      }
    }, 30000 );
  }

  // Stop function of spin indication
  function stopSpinIndication() {
    let $modalLock = $( "#id_modal_lock" );
    $modalLock.css( "opacity", "0" );
    setTimeout( function() {
      $modalLock.hide().css( "opacity", ".85" );
      clearTimeout( TIMEOUT_SPIN_INDICATION );
    }, 1000 );
  }

  function sandFormAjax( url, formData ) {
    $.ajax( {
      type: "POST",
      url: url,
      data: formData,
      processData: false,
      contentType: false
    } )
      .done( function( data ) {
        if ( data.successfully ) {
          location.reload( true );
          stopSpinIndication();
        }
      } )
      .fail( function( jqxhr, textStatus, error ) {
        let err = textStatus + ", " + error;
        let errDetail = "";

        stopSpinIndication();

        if ( jqxhr.responseJSON !== undefined &&
          jqxhr.responseJSON.hasOwnProperty( "detail" ) ) {
          errDetail = jqxhr.responseJSON.detail;
        }

        if ( errDetail.length !== 0 ) {
          console.log( "Request Failed: " + err + " - " + errDetail );
          alert( ( "Request Failed: " + err + " - " + errDetail ) );
        } else {
          console.log( "Request Failed: " + err );
          alert( "Request Failed: " + err );
        }
      } );
  }

  if ( $( "a" ).is( "#id_import_icon_collection" ) ) { //
    // Import file Icon Collection.
    $( "#id_import_file_icon_collection" ).on( "change", function() {
      let url = $( "#id_import_icon_collection" ).data( "import-url" );
      let collectionFile = $( this )[ 0 ].files[ 0 ];
      let csrftoken = $( "input[name=\"csrfmiddlewaretoken\"" ).val();
      let formData = new FormData();

      formData.append( "csrfmiddlewaretoken", csrftoken );
      formData.append( "collection", collectionFile );

      startSpinIndication();
      sandFormAjax( url, formData );
    } );
  } else if ( $( "a" ).is( "#id_import_tile_source" ) ) { //
    if ( ( $( "table#result_list tr" ).length - 1 ) > 0 ) {
      $( "#id_export_tile_source" ).show();
    }

    // Import file with sources of tile layers.
    $( "#id_import_file_tile_source" ).on( "change", function() {
      let url = $( "#id_import_tile_source" ).data( "import-url" );
      let sourcesFile = $( this )[ 0 ].files[ 0 ];
      let csrftoken = $( "input[name=\"csrfmiddlewaretoken\"" ).val();
      let formData = new FormData();

      formData.append( "csrfmiddlewaretoken", csrftoken );
      formData.append( "sources", sourcesFile );

      startSpinIndication();
      sandFormAjax( url, formData );
    } );
  }

  if ( $( "input" ).is( "#id_site" ) ) {
    let $site = $( "#id_site" );
    if ( $site.val().length > 0 ) {
      let url = $site.val();
      let btn = "<div class=\"tile_go_to_website_btn\"><a href=\"" + url +
                "\" target=\"_blank\" rel=\"nofollow\">" +
                "<img src=\"/static/djeym/img/arrow_right.svg\" alt=\"Button\"></a></div>";
      $site.after( btn );
    }
  }
} );
