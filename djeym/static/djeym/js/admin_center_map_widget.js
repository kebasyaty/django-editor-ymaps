/*
* Admin panel.
* Load map for determine the center of the map.
* (Панель администратора. Загрузить карту для определения центра карты.)
* Copyright (c) 2014 genkosta
* License MIT
*/

djeymYMaps.ready( function() {
  "use strict";

  let Map;

  let Placemark;

  let latitude = $( "#id_latitude" );

  let longitude = $( "#id_longitude" );

  let coordinates = [ latitude.val(), longitude.val() ];

  let coords;

  // Create map
  Map = new djeymYMaps.Map( "id_center_map", {
    center: coordinates,
    zoom: $( "select#id_zoom option:selected" ).val(),
    controls: [ "default", "routeButtonControl" ]
  } );

  // Enable search by organization. (Включить поиск по организациям.)
  Map.controls.get( "searchControl" ).options.set( "provider", "yandex#search" );

  if ( Map ) { //
    // Change the zoom
    $( "#id_zoom" ).on( "change", function() {
      Map.setZoom( $( "select#id_zoom option:selected" ).val() );
    } );

    // Add event on Map - Change the zoom
    Map.events.add( "boundschange", function( e ) {
      $( "select#id_zoom option[value=\"" + e.get( "target" ).getZoom() + "\"]" )
        .prop( "selected", true );
    } );

    // Create placemark
    Placemark = new djeymYMaps.Placemark( Map.getCenter(), {
      hintContent: "",
      balloonContent: ""
    }, {
      iconLayout: "default#image",
      iconImageHref: "/static/djeym/img/flag.svg",
      iconImageSize: [ 60, 60 ],
      iconImageOffset: [ -18.7, -53 ],
      draggable: true
    } );

    // Add event on Placemark - Drag Placemark
    Placemark.events.add( "drag", function( e ) {
      coords = e.get( "target" ).geometry.getCoordinates();
      latitude.val( coords[ 0 ] );
      longitude.val( coords[ 1 ] );
    } );

    // Add event on Map - Click the mouse
    Map.events.add( "click", function( e ) {
      coords = e.get( "coords" );
      Placemark.geometry.setCoordinates( coords );
      latitude.val( coords[ 0 ] );
      longitude.val( coords[ 1 ] );
    } );

    // Add Placemark on Map
    Map.geoObjects.add( Placemark );

    // Change the position of Placemark on Map through the coordinate fields.
    // (Изменить положение метки на карте по полям координат.)
    $( "#id_latitude, #id_longitude" ).on( "keyup", function() {
      let latNum = latitude.val() * 1;

      let logNum = longitude.val() * 1;

      if ( isNaN( latNum ) || isNaN( logNum ) ) {
        alert( "The coordinate value is not a number.\nЗначение координат не является числом." );
      } else {
        Placemark.geometry.setCoordinates( [ latNum, logNum ] );
      }
    } );
  }
} );
