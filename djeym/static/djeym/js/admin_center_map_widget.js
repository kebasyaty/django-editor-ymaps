/*
* Admin panel.
* Load map for determine the center of the map.
* Copyright (c) 2014 kebasyaty
* License MIT
*/

window.djeymYMaps.ready( function() {
  'use strict';

  function roundNumber( num ) {
    return Math.round( parseFloat( num ) * 1000000 ) / 1000000;
  }

  let Placemark;
  const latitude = $( '#id_latitude' );
  const longitude = $( '#id_longitude' );
  const coordinates = [ roundNumber( latitude.val() ), roundNumber( longitude.val() ) ];
  let coords;

  // Change type field
  latitude.attr( 'type', 'number' );
  longitude.attr( 'type', 'number' );

  // Disable Slug field
  $( '#id_slug' ).attr( 'disabled', 'disabled' );

  // Create map
  const Map = new window.djeymYMaps.Map( 'id_center_map', {
    center: coordinates,
    zoom: $( 'select#id_zoom option:selected' ).val(),
    controls: [ 'default', 'routeButtonControl' ]
  } );
  Map.cursors.push( 'arrow' );

  // Enable search by organization. (Включить поиск по организациям.)
  Map.controls.get( 'searchControl' ).options.set( 'provider', 'yandex#search' );

  if ( Map ) { //
    // Change the zoom
    $( '#id_zoom' ).on( 'change', function() {
      Map.setZoom( $( 'select#id_zoom option:selected' ).val() );
    } );

    // Add event on Map - Change the zoom
    Map.events.add( 'boundschange', function( e ) {
      $( 'select#id_zoom option[value="' + e.get( 'target' ).getZoom() + '"]' )
        .prop( 'selected', true );
    } );

    // Create placemark
    Placemark = new window.djeymYMaps.Placemark( Map.getCenter(), {
      hintContent: '',
      balloonContent: ''
    }, {
      iconLayout: 'default#image',
      iconImageHref: '/static/djeym/img/center.svg',
      iconImageSize: [ 32, 60 ],
      iconImageOffset: [ -16, -60 ],
      draggable: true
    } );

    // Add event on Placemark - Drag Placemark
    Placemark.events.add( 'drag', function( e ) {
      coords = e.get( 'target' ).geometry.getCoordinates();
      latitude.val( roundNumber( coords[ 0 ] ) );
      longitude.val( roundNumber( coords[ 1 ] ) );
    } );

    // Add event on Map - Click the mouse
    Map.events.add( 'click', function( e ) {
      coords = e.get( 'coords' );
      Placemark.geometry.setCoordinates( coords );
      latitude.val( roundNumber( coords[ 0 ] ) );
      longitude.val( roundNumber( coords[ 1 ] ) );
    } );

    // Add Placemark on Map
    Map.geoObjects.add( Placemark );

    // Change the position of Placemark on Map through the coordinate fields.
    // (Изменить положение метки на карте по полям координат.)
    $( '#id_latitude, #id_longitude' ).on( 'keyup', function() {
      const latNum = latitude.val() * 1;
      const logNum = longitude.val() * 1;
      const regex = /^-?\d+(\.\d+)?$/;

      if ( regex.test( latNum ) && regex.test( logNum ) ) {
        Placemark.geometry.setCoordinates( [ roundNumber( latNum ), roundNumber( logNum ) ] );
      }
    } );
  }
} );
