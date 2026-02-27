/*
* Admin panel.
* Load map for checking icon offset.
* Copyright (c) 2014 kebasyaty
* License MIT
*/

window.djeymYMaps.ready( function() {
  'use strict';

  const sizeWidth = $( '.field-size_width .readonly' ).text();
  const sizeHeight = $( '.field-size_height .readonly' ).text();

  if ( sizeWidth > 0 && sizeHeight > 0 ) {
    let standardPlacemark;
    let testPlacemark;
    const offsetX = $( '#id_offset_x' );
    const offsetY = $( '#id_offset_y' );

    // Display hint for map.
    $( '.field-check_icon_offset, .hint_check_icon_offset' ).show();

    // Create Map
    const Map = new window.djeymYMaps.Map( 'id_check_icon_offset_map', {
      center: [ 0, 0 ],
      zoom: 3,
      type: 'yandex#satellite',
      controls: []
    }, {
      maxZoom: 12,
      minZoom: 0
    } );

    if ( Map ) { //
      // Create Standard Placemark
      standardPlacemark = new window.djeymYMaps.Placemark( Map.getCenter(), {}, {
        iconLayout: 'default#image',
        iconImageHref: '/static/djeym/img/offset.svg',
        iconImageSize: [ 38, 60 ],
        iconImageOffset: [ -19, 0 ],
        hasBalloon: false,
        hasHint: false,
        zIndex: 2
      } );

      // Create Test Placemark
      testPlacemark = new window.djeymYMaps.Placemark( Map.getCenter(), {}, {
        iconLayout: 'default#image',
        iconImageHref: $( '.file-upload a' ).attr( 'href' ),
        iconImageSize: [ +sizeWidth, +sizeHeight ],
        iconImageOffset: [ +offsetX.val(), +offsetY.val() ],
        hasBalloon: false,
        hasHint: false,
        zIndex: 1
      } );

      // Add Placemarks on Map
      Map.geoObjects.add( standardPlacemark );
      Map.geoObjects.add( testPlacemark );

      // Change the position of Placemark on Map through the offset fields.
      $( '#id_offset_x, #id_offset_y' ).on( 'keyup mouseup', function( event ) {
        event.preventDefault ? event.preventDefault() : ( event.returnValue = false );
        testPlacemark.options.set(
          { iconImageOffset: [ +offsetX.val(), +offsetY.val() ] } );
      } );

      $( '#id_offset_x' ).on( 'mousewheel', function( event ) {
        event.preventDefault ? event.preventDefault() : ( event.returnValue = false );
        let num;
        if ( event.deltaY === 1 ) {
          num = +offsetX.val() + 0.1;
          num = num.toFixed( 1 );
        } else {
          num = +offsetX.val() - 0.1;
          num = num.toFixed( 1 );
        }
        offsetX.val( num );
        testPlacemark.options.set(
          { iconImageOffset: [ num, +offsetY.val() ] } );
      } );

      $( '#id_offset_y' ).on( 'mousewheel', function( event ) {
        event.preventDefault ? event.preventDefault() : ( event.returnValue = false );
        let num;
        if ( event.deltaY === 1 ) {
          num = +offsetY.val() - 0.1;
          num = num.toFixed( 1 );
        } else {
          num = +offsetY.val() + 0.1;
          num = num.toFixed( 1 );
        }
        offsetY.val( num );
        testPlacemark.options.set(
          { iconImageOffset: [ +offsetX.val(), num ] } );
      } );

      // Add buttons for touch screen.
      // (Добавить кнопки для сенсорного экрана.)
      offsetX.after( '<div id="id_offset_x_right_btn" class="marker_offset_btn">' +
                '<img src="/static/djeym/img/arrow_right.svg" alt="Plus"></div>' );
      offsetX.after( '<div id="id_offset_x_left_btn" class="marker_offset_btn">' +
                '<img src="/static/djeym/img/arrow_left.svg" alt="Minus"></div>' );
      offsetY.after( '<div id="id_offset_y_down_btn" class="marker_offset_btn">' +
                '<img src="/static/djeym/img/arrow_down.svg" alt="Minus"></div>' );
      offsetY.after( '<div id="id_offset_y_up_btn" class="marker_offset_btn">' +
                '<img src="/static/djeym/img/arrow_up.svg" alt="Plus"></div>' );

      $( '#id_offset_x_right_btn' ).on( 'click', function( event ) {
        event.preventDefault ? event.preventDefault() : ( event.returnValue = false );
        const num = ( +offsetX.val() + 0.1 ).toFixed( 1 );
        offsetX.val( num );
        testPlacemark.options.set(
          { iconImageOffset: [ num, +offsetY.val() ] } );
      } );
      $( '#id_offset_x_left_btn' ).on( 'click', function( event ) {
        event.preventDefault ? event.preventDefault() : ( event.returnValue = false );
        let num = ( +offsetX.val() - 0.1 ).toFixed( 1 );
        num = ( num < 0 ) ? num : 0;
        offsetX.val( num );
        testPlacemark.options.set(
          { iconImageOffset: [ num, +offsetY.val() ] } );
      } );
      $( '#id_offset_y_down_btn' ).on( 'click', function( event ) {
        event.preventDefault ? event.preventDefault() : ( event.returnValue = false );
        const num = ( +offsetY.val() + 0.1 ).toFixed( 1 );
        offsetY.val( num );
        testPlacemark.options.set(
          { iconImageOffset: [ +offsetX.val(), num ] } );
      } );
      $( '#id_offset_y_up_btn' ).on( 'click', function( event ) {
        event.preventDefault ? event.preventDefault() : ( event.returnValue = false );
        let num = ( +offsetY.val() - 0.1 ).toFixed( 1 );
        num = ( num < 0 ) ? num : 0;
        offsetY.val( num );
        testPlacemark.options.set(
          { iconImageOffset: [ +offsetX.val(), num ] } );
      } );
    }
  }
} );
