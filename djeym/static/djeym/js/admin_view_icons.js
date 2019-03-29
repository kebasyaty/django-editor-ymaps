/*
* View icons on admin panel.
* Copyright (c) 2014 genkosta
* License MIT
*/

$( document ).ready( function() {
  "use strict";

  // Add support Regex.
  jQuery.expr[ ":" ].regex = function( elem, index, match ) {
    let matchParams = match[ 3 ].split( "," );
    let validLabels = /^(data|css):/;
    let attr = {
      method: matchParams[ 0 ].match( validLabels ) ?
        matchParams[ 0 ].split( ":" )[ 0 ] : "attr",
      property: matchParams.shift().replace( validLabels, "" )
    };
    let regexFlags = "ig";
    let regex = new RegExp( matchParams.join( "" ).replace( /^\s+|\s+$/g, "" ), regexFlags );
    return regex.test( jQuery( elem )[ attr.method ]( attr.property ) );
  };

  function ajaxGetIcon( ajaxURL, $image, objID ) {
    if ( parseInt( objID ) ) {
      $.getJSON( ajaxURL, { obj_id: objID } )
        .done( function( data ) {
          $image.attr( "src", data.url ).show();
        } )
        .fail( function( jqxhr, textStatus, error ) {
          let err = textStatus + ", " + error;
          let errDetail = "";

          if ( jqxhr.responseJSON !== undefined &&
                        jqxhr.responseJSON.hasOwnProperty( "detail" ) ) {
            errDetail = jqxhr.responseJSON.detail;
          }

          if ( errDetail.length !== 0 ) {
            console.log( "Request Failed: " + err + " - " + errDetail );
          } else {
            console.log( "Request Failed: " + err );
          }
        } );
    } else {
      $image.hide();
    }
  }

  let idForm = $( "form" ).eq( 0 ).attr( "id" );

  if ( /^category/.test( idForm ) || /^subcategory/.test( idForm ) || /^map/.test( idForm ) ) {
    let $icon = $( "#id_category_icon, input:regex(id, ^id_presets-.*-icon)" );

    $icon.each( function() {
      let $this = $( this );
      $this.after( "<span class=\"view_icon\">" + $this.val() + "</span>" );
    } );

    $icon.on( "keyup mouseup mouseout", function( event ) {
      let $this = $( this );
      $this.parent().find( ".view_icon" ).html( $this.val() );
    } );
  }

  if ( /^map_form/.test( idForm ) ) {
    let $iconCluster = $( "#id_icon_cluster" );
    let clusterIconID = $iconCluster.find( "option:selected" ).val();
    let ajaxClusterIconURL = "/djeym/ajax-cluster-icon/";

    let $iconCollection = $( "#id_icon_collection" );
    let ajaxExampleIconURL = "/djeym/ajax-collection-example-icon/";
    let collectionIconID = $iconCollection.find( "option:selected" ).val();

    let $tileSource = $( "#id_tile" );
    let tileSourceID = $tileSource.find( "option:selected" ).val();
    let ajaxTileSourceURL = "/djeym/ajax-tile-screenshot/";

    let $iconLoadIndicator = $( "#id_load_indicator" );
    let loadIndicatorIconID = $iconLoadIndicator.find( "option:selected" ).val();
    let ajaxLoadIndicatorIconURL = "/djeym/ajax-load-indicator-icon/";

    let $imageClusterIcon;
    let $imageExampleIcon;
    let $imageTile;
    let $imageLoadIndicator;

    // If there is no cluster or collection, hide the "Edit Map" button.
    // (Если нет кластера или коллекции, скрыть кнопку "Редактировать карту".)
    if ( $( "#id_icon_cluster option:selected" ).val().length === 0 ||
      $( "#id_icon_collection option:selected" ).val().length === 0 ) {
      $( ".editing_map_link" ).hide();
    }

    // Ajax, load custom cluster icon - Map.
    $iconCluster.parent().addClass( "custom_cluster_icon_wrapper" ).append(
      "<img src=\"\" id=\"id_custom_cluster_icon\" alt=\"Cluster Icon\">"
    );
    $imageClusterIcon = $( "#id_custom_cluster_icon" );
    ajaxGetIcon( ajaxClusterIconURL, $imageClusterIcon, clusterIconID );
    $iconCluster.on( "change", function( event ) {
      clusterIconID = $( this ).find( "option:selected" ).val();
      ajaxGetIcon( ajaxClusterIconURL, $imageClusterIcon, clusterIconID );
    } );

    /* Ajax - Load example icon from collection. */
    $iconCollection.parent().addClass( "icon_collection_wrapper" ).append(
      "<img src=\"\" id=\"id_collection_example_icon\" alt=\"Example Icon\">"
    );
    $imageExampleIcon = $( "#id_collection_example_icon" );
    ajaxGetIcon( ajaxExampleIconURL, $imageExampleIcon, collectionIconID );
    $iconCollection.on( "change", function( event ) {
      collectionIconID = $( this ).find( "option:selected" ).val();
      ajaxGetIcon( ajaxExampleIconURL, $imageExampleIcon, collectionIconID );
    } );

    /* Ajax - Upload a screenshot of the tile. */
    $tileSource.parent().addClass( "tile_screenshot_wrapper" ).append(
      "<img src=\"\" id=\"id_tile_screenshot\" alt=\"Screenshot\">"
    );
    $imageTile = $( "#id_tile_screenshot" );

    if ( tileSourceID.length > 0 ) {
      ajaxGetIcon( ajaxTileSourceURL, $imageTile, tileSourceID );
    } else {
      $imageTile.attr( "src", "/static/djeym/img/default_tile.png" ).show();
    }

    $tileSource.on( "change", function( event ) {
      tileSourceID = $( this ).find( "option:selected" ).val();
      if ( tileSourceID.length > 0 ) {
        ajaxGetIcon( ajaxTileSourceURL, $imageTile, tileSourceID );
      } else {
        $imageTile.attr( "src", "/static/djeym/img/default_tile.png" ).show();
      }
    } );

    // Ajax, load - Icon of load indicator for Map.
    $iconLoadIndicator.parent().addClass( "load_indicator_icon_wrapper" ).append(
      "<img src=\"\" id=\"id_icon_load_indicator\" alt=\"Icon\">"
    );
    $imageLoadIndicator = $( "#id_icon_load_indicator" );
    ajaxGetIcon( ajaxLoadIndicatorIconURL, $imageLoadIndicator, loadIndicatorIconID );
    $iconLoadIndicator.on( "change", function( event ) {
      loadIndicatorIconID = $( this ).find( "option:selected" ).val();
      ajaxGetIcon( ajaxLoadIndicatorIconURL, $imageLoadIndicator, loadIndicatorIconID );
    } );
  }
} );
