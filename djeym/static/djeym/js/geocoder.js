/*
* Geocoder - For direct geocoding.
* Copyright (c) 2014 genkosta
* License MIT
*/

djeymYMaps.ready( init );

function init() {
  "use strict";

  // Add download indicator to the map.
  let html = "<div id=\"djeymModalLock\"><div id=\"djeymLoadIndicator\"></div></div>";
  document.getElementById( "djeymYMapsID" ).innerHTML = html;

  // Stop spin indication.
  function stopSpinIndication() {
    let modalLock = document.getElementById( "djeymModalLock" );
    setTimeout( function() {
      modalLock.style.opacity = 0;
      setTimeout( function() {
        modalLock.remove();
      }, 1200 );
    }, 1400 );
  }

  // CREATE A MAP (Создать карту) ------------------------------------------------------------------
  let Map = new djeymYMaps.Map( "djeymYMapsID", {
    center: [ 0, 0 ],
    zoom: 3,
    type: ( window.djeymTile === undefined ) ? window.djeymMapType : null,
    controls: window.djeymControls ? [ "zoomControl" ] : [ "default" ]
  }, {
    maxZoom: ( typeof window.djeymTile === "undefined" ) ? 23 : window.djeymTile.maxZoom,
    minZoom: ( typeof window.djeymTile === "undefined" ) ? 0 : window.djeymTile.minZoom,
    hasHint: false,
    hasBalloon: true
  } );

  // Enable search by organization.
  if ( window.djeymControls === false ) {
    Map.controls.get( "searchControl" ).options.set( "provider", "yandex#search" );
  }

  // Connect a third-party source of tiles.
  if ( typeof window.djeymTile !== "undefined" ) {
    Map.layers.add( new djeymYMaps.Layer(
      window.djeymSource(), {
        projection: djeymYMaps.projection.sphericalMercator
      } ) );

    if ( window.djeymTile.copyrights.length > 0 ) {
      Map.copyrights.add( window.djeymTile.copyrights );
    }
  }

  if ( window.djeymAddress.length > 0 ) {
    Map.events.once( "boundschange", function() {
      stopSpinIndication();
    } );

    djeymYMaps.geocode( window.djeymAddress, { results: 1 } ).then(
      function( res ) {
        let firstGeoObject = res.geoObjects.get( 0 );

        if ( typeof res.geoObjects.get( 0 ) === "undefined" ) {
          stopSpinIndication();
          return;
        }

        let bounds = firstGeoObject.properties.get( "boundedBy" );

        if ( typeof window.djeymMarker !== "undefined" ) {
          firstGeoObject.options.set( {
            hasHint: false,
            iconLayout: "default#image",
            iconImageHref: window.djeymMarker.iconImageHref,
            iconImageOffset: window.djeymMarker.iconImageOffset,
            iconImageSize: window.djeymMarker.iconImageSize
          } );
        } else {
          firstGeoObject.options.set( "preset", "islands#darkBlueDotIconWithCaption" );
          firstGeoObject.properties.set( "iconCaption", firstGeoObject.getAddressLine() );
        }
        Map.geoObjects.add( firstGeoObject );
        Map.setBounds( bounds, { checkZoomRange: true } );
      },
      function( err ) {
        console.error( err );
        stopSpinIndication();
      }
    );
  } else {
    stopSpinIndication();
  }
}
