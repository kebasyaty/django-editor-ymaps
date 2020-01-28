/*
* Upload icons to admin panel.
* Copyright (c) 2014 kebasyaty
* License MIT
*/

$( document ).ready( function() {
  'use strict';

  // jQuery - Support Regex.
  $.expr[ ':' ].regex = function( elem, index, match ) {
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

  // Ajax
  function ajaxGetIcon( ajaxURL, $image, objID ) {
    if ( parseInt( objID ) ) {
      $.getJSON( ajaxURL, { obj_id: objID } )
        .done( function( data ) {
          $image.attr( 'src', data.url ).show();
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
          } else {
            console.log( 'Request Failed: ' + err );
          }
        } );
    } else {
      $image.hide();
    }
  }

  if ( $( 'form' ).is( '#map_form' ) ) { //
    /*
    Icons for Presets, Categories and Subcategories.
    ------------------------------------------------------------------------------------------------
    */
    const textObjs = '#id_category_icon, input:regex(id, ^id_presets-.+-icon),' +
                     'input:regex(id, ^id_categories_placemark-.+-category_icon),' +
                     'input:regex(id, ^id_subcategories_placemark-.+-category_icon),' +
                     'input:regex(id, ^id_categories_polyline-.+-category_icon),' +
                     'input:regex(id, ^id_subcategories_polyline-.+-category_icon),' +
                     'input:regex(id, ^id_categories_polygon-.+-category_icon),' +
                     'input:regex(id, ^id_subcategories_polygon-.+-category_icon)';
    const $icon = $( textObjs );

    $icon.each( function() {
      const $this = $( this );
      const id = $this.attr( 'id' );
      if ( !/^id_presets-/.test( id ) ) {
        $this.after( '<br><a href="https://materialdesignicons.com/" target="_blank" ' +
        'rel="nofollow noreferrer noopener">MaterialDesignIcons.com</a>' );
      }
      $this.after( '<span class="view_icon"><span class="mdi ' + $this.val() + '"></span></span>' );
    } );

    $( document ).on( 'keyup mouseup mouseout', textObjs, function() {
      const $this = $( this );
      if ( $this.val().length > 0 ) {
        if ( !/^mdi-/.test( $this.val() ) ) {
          $this.val( 'mdi-' + $this.val() );
        }
        $this.parent().find( '.view_icon' ).html( '<span class="mdi ' + $this.val() + '"></span>' );
      }
    } );

    $( document ).on( 'click', '.add-row a', function() {
      const $icon = $( textObjs );
      $icon.each( function() {
        const $this = $( this );
        if ( $this.parent().find( '.view_icon' ) === undefined ) {
          $this.after( '<span class="view_icon"></span>' );
        }
      } );
    } );

    /*
    Icons for Clusters, Icon Collections, Tile Sources and Upload Indicators.
    ------------------------------------------------------------------------------------------------
    */
    const $iconCluster = $( '#id_icon_cluster' );
    let clusterIconID = $iconCluster.find( 'option:selected' ).val();
    const ajaxClusterIconURL = '/djeym/ajax-cluster-icon/';

    const $iconCollection = $( '#id_icon_collection' );
    const ajaxExampleIconURL = '/djeym/ajax-collection-example-icon/';
    let collectionIconID = $iconCollection.find( 'option:selected' ).val();

    const $tileSource = $( '#id_tile' );
    let tileSourceID = $tileSource.find( 'option:selected' ).val();
    const ajaxTileSourceURL = '/djeym/ajax-tile-screenshot/';

    const $iconLoadIndicator = $( '#id_load_indicator' );
    let loadIndicatorIconID = $iconLoadIndicator.find( 'option:selected' ).val();
    const ajaxLoadIndicatorIconURL = '/djeym/ajax-load-indicator-icon/';

    /* If there is no cluster or collection, hide the "Edit Map" button.
       (Если нет кластера или коллекции, скрыть кнопку "Редактировать карту".) */
    if ( $( '#id_icon_cluster option:selected' ).val().length === 0 ||
      $( '#id_icon_collection option:selected' ).val().length === 0 ) {
      $( '.editing_map_link' ).hide();
    }

    // Upload custom cluster icon - Map.
    $iconCluster.parent().addClass( 'custom_cluster_icon_wrapper' ).append(
      '<img src="" id="id_custom_cluster_icon" alt="Cluster Icon">'
    );
    const $imageClusterIcon = $( '#id_custom_cluster_icon' );
    ajaxGetIcon( ajaxClusterIconURL, $imageClusterIcon, clusterIconID );
    $iconCluster.on( 'change', function() {
      clusterIconID = $( this ).find( 'option:selected' ).val();
      ajaxGetIcon( ajaxClusterIconURL, $imageClusterIcon, clusterIconID );
    } );

    // Upload example icon from collection.
    $iconCollection.parent().addClass( 'icon_collection_wrapper' ).append(
      '<img src="" id="id_collection_example_icon" alt="Example Icon">'
    );
    const $imageExampleIcon = $( '#id_collection_example_icon' );
    ajaxGetIcon( ajaxExampleIconURL, $imageExampleIcon, collectionIconID );
    $iconCollection.on( 'change', function() {
      collectionIconID = $( this ).find( 'option:selected' ).val();
      ajaxGetIcon( ajaxExampleIconURL, $imageExampleIcon, collectionIconID );
    } );

    // Upload a screenshot of the tile.
    $tileSource.parent().addClass( 'tile_screenshot_wrapper' ).append(
      '<img src="" id="id_tile_screenshot" alt="Screenshot">'
    );
    const $imageTile = $( '#id_tile_screenshot' );

    if ( tileSourceID.length > 0 ) {
      ajaxGetIcon( ajaxTileSourceURL, $imageTile, tileSourceID );
    } else {
      $imageTile.attr( 'src', '/static/djeym/img/default_tile.png' ).show();
    }

    $tileSource.on( 'change', function() {
      tileSourceID = $( this ).find( 'option:selected' ).val();
      if ( tileSourceID.length > 0 ) {
        ajaxGetIcon( ajaxTileSourceURL, $imageTile, tileSourceID );
      } else {
        $imageTile.attr( 'src', '/static/djeym/img/default_tile.png' ).show();
      }
    } );

    // Upload icon of load indicator for Map.
    $iconLoadIndicator.parent().addClass( 'load_indicator_icon_wrapper' ).append(
      '<img src="" id="id_icon_load_indicator" alt="Icon">'
    );
    const $imageLoadIndicator = $( '#id_icon_load_indicator' );
    ajaxGetIcon( ajaxLoadIndicatorIconURL, $imageLoadIndicator, loadIndicatorIconID );
    $iconLoadIndicator.on( 'change', function() {
      loadIndicatorIconID = $( this ).find( 'option:selected' ).val();
      ajaxGetIcon( ajaxLoadIndicatorIconURL, $imageLoadIndicator, loadIndicatorIconID );
    } );
  }
} );
