/*
* DjEYM
* Create Yandex Map for the site page.
* Copyright (c) 2014 genkosta
* License MIT
*/

djeymYMaps.ready( init );

function init() {
  "use strict";

  // GLOBAL VARIABLES ------------------------------------------------------------------------------
  let Map,
    globalButtonShowPanel,
    globalTemp,
    globalObjMngPlacemark,
    globalObjMngPolyline,
    globalObjMngPolygon,
    globalHeatmap,
    globalHeatPoints;

  const GLOBAL_BOXIOS_SIZE = "middle";

  // FUNCTIONS -------------------------------------------------------------------------------------

  // Wait for the content to load into the Balloon and update the information for the presets.
  // (Дождаться загрузки контента в Balloon и обновить информацию для пресетов.)
  let globalRestartID1;
  let globalRestartID2;
  let globalRestartID3;
  let globalRestartID4;
  function waitLoadContent() {
    globalRestartID4 = setTimeout( function() {
      let loadIndicator = document.getElementById( "djeymLoadIndicator" );

      if ( loadIndicator === null ) { return; }

      loadIndicator.style.display = "block";

      let $images = $( "ymaps:regex(class, .*-balloon__content) img" );
      let imgLoaded = false;
      let counter = 0;

      if ( $images.length === 0 ) {
        imgLoaded = true;
      } else {
        $images.each( function() {
          if ( this.complete ) { counter++; }
        } );
        if ( counter === $images.length ) { imgLoaded = true; }
      }

      if ( !$( "div" ).is( "#djeymSignLoaded" ) || !imgLoaded ) {
        globalRestartID3 = setTimeout( function() {
          waitLoadContent();
        }, 100 );
      } else {
        $( ".djeymUpdateInfoPreset" ).each( function() {
          $( this ).trigger( "click" );
        } );
        let modalLock = document.getElementById( "djeymModalLock" );
        if ( modalLock !== null ) {
          globalRestartID2 = setTimeout( function() {
            globalRestartID1 = setTimeout( function() {
              modalLock.remove();
            }, 600 );
            modalLock.style.opacity = 0;
          }, 200 );
        }
      }
    }, 500 );
  }

  // jQuery ----------------------------------------------------------------------------------------

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

  // CREATE A MAP ----------------------------------------------------------------------------------
  Map = new djeymYMaps.Map( "djeymYMapsID", {
    center: window.djeymCenterMap,
    zoom: window.djeymZoomMap,
    type: ( typeof window.djeymTile === "undefined" ) ? window.djeymMapType : null,
    controls: window.djeymControls
  }, {
    maxZoom: ( typeof window.djeymTile === "undefined" ) ? 23 : window.djeymTile.maxZoom,
    minZoom: ( typeof window.djeymTile === "undefined" ) ? 0 : window.djeymTile.minZoom,
    hasHint: false
  } );

  if ( Map.getType() === null ) {
    Map.controls.get( "typeSelector" ).options.set( "visible", false );
  }

  if ( window.djeymRoundTheme ) {
    globalTemp = window.djeymControls.length;
    for ( let idx = 0; idx < globalTemp; idx++ ) {
      switch ( window.djeymControls[ idx ] ) {
        case "geolocationControl":
          Map.controls.get( "geolocationControl" ).options.set( {
            size: "small"
          } );
          break;
        case "searchControl":
          Map.controls.get( "searchControl" ).options.set( {
            size: "small"
          } );
          break;
        case "routeButtonControl":
          Map.controls.get( "routeButtonControl" ).options.set( {
            size: "small"
          } );
          break;
        case "trafficControl":
          Map.controls.get( "trafficControl" ).options.set( {
            size: "small"
          } );
          break;
        case "typeSelector":
          Map.controls.get( "typeSelector" ).options.set( {
            size: "small"
          } );
          break;
        case "fullscreenControl":
          Map.controls.get( "fullscreenControl" ).options.set( {
            size: "small"
          } );
          break;
        case "zoomControl":
          Map.controls.get( "zoomControl" ).options.set( {
            size: "small"
          } );
          break;
        case "rulerControl":
          Map.controls.get( "rulerControl" ).options.set( {
            size: "small"
          } );
          break;
      }
    }
  }

  // Enable search by organization.
  if ( window.djeymControls.includes( "searchControl" ) &&
       window.djeymSearchProvider ) {
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

  // Heatmap settings.
  if ( window.djeymHeatmap ) {
    djeymYMaps.modules.require( [ "Heatmap" ], function( Heatmap ) {
      globalHeatPoints = {
        type: "FeatureCollection",
        features: []
      };
      globalHeatmap = new Heatmap( globalHeatPoints, {
        radius: window.djeymHeatmapRadius,
        dissipating: window.djeymHeatmapDissipating,
        opacity: window.djeymHeatmapOpacity,
        intensityOfMidpoint: window.djeymHeatmapIntensity,
        gradient: {
          0.1: window.djeymHeatmapGradientColor1,
          0.2: window.djeymHeatmapGradientColor2,
          0.7: window.djeymHeatmapGradientColor3,
          1.0: window.djeymHeatmapGradientColor4
        }
      } );
      globalHeatmap.setMap( Map );
    } );
  }

  // CREATE CUSTOM CONTROLS ------------------------------------------------------------------------

  // Create Button - Show Panel.
  if ( !window.djeymDisableSitePanel ) {
    globalButtonShowPanel = new djeymYMaps.control.Button( {
      data: {
        image: "/static/djeym/img/front_open_panel.svg"
      },
      options: {
        size: "small",
        selectOnClick: false,
        maxWidth: 28
      }
    } );
    globalButtonShowPanel.events.add( "click", function() { //
    // Open panel.
      document.getElementById( "id_djeym_sidenav" ).style.left = "0";
    } );
  }

  // ADD EVENTS TO THE MAP (Добавить события на карту) ---------------------------------------------

  // Opening the balloon on the map.
  // (Открытие балуна на карте. )
  Map.events.add( "balloonopen", function() { //
    // Update Info Preset.
    // (Обновить информацию пресета.)
    clearTimeout( globalRestartID1 );
    clearTimeout( globalRestartID2 );
    clearTimeout( globalRestartID3 );
    clearTimeout( globalRestartID4 );
    waitLoadContent();
  } );

  // Update preset information in the balloon-panel.
  // (Обновить информацию пресета в балун-панель.)
  $( document ).on(
    "click",
    "ymaps:regex(class, .*-cluster-tabs__menu-item.*), " +
    "ymaps:regex(class, .*-cluster-carousel__pager-item.*), " +
    "ymaps:regex(class, .*-cluster-carousel__nav.*)",
    function( event ) {
      event.stopPropagation();
      clearTimeout( globalRestartID1 );
      clearTimeout( globalRestartID2 );
      clearTimeout( globalRestartID3 );
      clearTimeout( globalRestartID4 );
      waitLoadContent();
    } );

  // ADD PANEL TO MAP ------------------------------------------------------------------------------
  ( function() {
    let $tempSidenav = $( "#id_djeym_temp_sidenav" );
    $( "#djeymYMapsID" ).append( $tempSidenav.html() );
    $tempSidenav.remove();
    let $matrixMenuBtn = $( ".djeym-matrix-menu__btn" );
    if ( $matrixMenuBtn.length === 1 ) { $matrixMenuBtn.eq( 0 ).hide(); }
    $( ".djeym-tab-item" ).eq( 0 ).addClass( "djeym_tab_active" ).show();
  } )();

  // CREATE OBJECT MANAGERS ------------------------------------------------------------------------

  // Custom layout for Balloon.
  // (Кастомный макет для Балуна.)
  let customBalloonContentLayout = djeymYMaps.templateLayoutFactory.createClass(
    "<div class=\"position-relative hight-100\">" +
    "<div id=\"djeymModalLock\"><div id=\"djeymLoadIndicator\"></div></div>" +
    "<div class=\"djeym_ballon_header\">{{ properties.balloonContentHeader|raw }}</div>" +
    "<div class=\"djeym_ballon_body\">{{ properties.balloonContentBody|raw }}</div>" +
    "<div class=\"djeym_ballon_footer\">{{ properties.balloonContentFooter|raw }}</div></div>"
  );

  // Custom layout for content cluster icons.
  // (Кастомный макет для контента иконки кластера.)
  let customIconContentLayoutForCluster = djeymYMaps.templateLayoutFactory.createClass(
    "<div class=\"djeym_cluster_icon_content\"><span style=\"background-color:" +
    window.djeymClusterIconContentBgColor + ";color:" +
    window.djeymClusterIconContentTxtColor +
    ";\">$[properties.geoObjects.length]</span></div>"
  );

  let geoObjectBalloonOptions = {
    geoObjectHasBalloon: true,
    geoObjectHasHint: false,
    geoObjectBalloonMinWidth: 322,
    geoObjectBalloonMaxWidth: 342,
    geoObjectBalloonMinHeight: window.djeymBalloonMinHeight,
    geoObjectBalloonPanelMaxMapArea: 0,
    geoObjectBalloonContentLayout: customBalloonContentLayout,
    geoObjectOpenBalloonOnClick: false
  };

  let objMngPlacemarkOptions = {
    clusterize: window.djeymClusteringSite,
    clusterHasBalloon: true,
    clusterHasHint: false,
    clusterIconContentLayout: window.djeymClusterIconContent ?
      customIconContentLayoutForCluster : null,
    clusterBalloonItemContentLayout: customBalloonContentLayout,
    clusterDisableClickZoom: true,
    clusterOpenBalloonOnClick: false,
    showInAlphabeticalOrder: false,
    clusterBalloonPanelMaxMapArea: 0,
    clusterMaxZoom: Map.options.get( "maxZoom" ),
    clusterBalloonContentLayout: window.djeymClusterLayout,
    clusterIcons: [ {
      href: window.djeymCluster[ 0 ],
      size: window.djeymCluster[ 1 ],
      offset: window.djeymCluster[ 2 ],
      shape: {
        type: "Circle",
        coordinates: [ 0, 0 ],
        radius: parseInt( Math.min.apply( null, window.djeymCluster[ 1 ] ) / 2 )
      }
    } ]
  };

  Object.assign( objMngPlacemarkOptions, geoObjectBalloonOptions );

  // Create a manager for Placemarks.
  // (Создать менеджер для меток.)
  globalObjMngPlacemark = new djeymYMaps.ObjectManager( objMngPlacemarkOptions );

  // Create a manager for Polylines.
  // (Создать менеджер для полилиний.)
  globalObjMngPolyline = new djeymYMaps.ObjectManager( geoObjectBalloonOptions );

  // Create a manager for Polygons.
  // (Создать менеджер для полигонов.)
  globalObjMngPolygon = new djeymYMaps.ObjectManager( geoObjectBalloonOptions );

  // Clear content of geo-object.
  // (Очистить содержимое геообъекта.)
  function clearContentGeoObject( geoObject ) {
    geoObject.properties.balloonContentHeader = "";
    geoObject.properties.balloonContentBody = "";
    geoObject.properties.balloonContentFooter = "";
    return geoObject;
  }

  // Balloon switching to mode Panel.
  // (Переключение инфо-окна в режим панели)
  function djeymBalloonPanel() {
    let $window = $( window );
    let actualWidth = $window.width();
    let actualHeight = $window.height();
    let $ymap = $( "#djeymYMapsID" );
    let mapWidth = $ymap.width();
    let mapHeight = $ymap.height();

    if ( mapWidth < actualWidth ) { actualWidth = mapWidth; }
    if ( mapHeight < actualHeight ) { actualHeight = mapHeight; }

    Map.balloon.close();
    if ( actualWidth < 768 || actualHeight < 400 ) {
      globalObjMngPlacemark.clusters.options.set( "balloonPanelMaxMapArea", "Infinity" );
      globalObjMngPlacemark.objects.options.set( "balloonPanelMaxMapArea", "Infinity" );
      globalObjMngPolyline.objects.options.set( "balloonPanelMaxMapArea", "Infinity" );
      globalObjMngPolygon.objects.options.set( "balloonPanelMaxMapArea", "Infinity" );
    } else {
      globalObjMngPlacemark.clusters.options.set( "balloonPanelMaxMapArea", 0 );
      globalObjMngPlacemark.objects.options.set( "balloonPanelMaxMapArea", 0 );
      globalObjMngPolyline.objects.options.set( "balloonPanelMaxMapArea", 0 );
      globalObjMngPolygon.objects.options.set( "balloonPanelMaxMapArea", 0 );
    }
  }
  $( window ).on( "resize", function() { djeymBalloonPanel(); } );
  djeymBalloonPanel();

  // Ajax, load content for (Cluster) balloonContent - Header, Body and Footer.
  // (Ajax, загрузить контент для (Кластер) balloonContent - Header, Body и Footer.)
  globalObjMngPlacemark.clusters.events.add( "click", function( event ) {
    Map.balloon.close( true );

    let objectId = event.get( "objectId" );
    let cluster = globalObjMngPlacemark.clusters.getById( objectId );
    let geoObjects = cluster.properties.geoObjects;
    let countObjs = geoObjects.length;
    let ids = [];

    for ( let idx = 0; idx < countObjs; idx++ ) {
      ids.push( geoObjects[ idx ].properties.id );
    }

    for ( let idx = 0; idx < countObjs; idx++ ) {
      globalObjMngPlacemark.clusters.balloon.setData( clearContentGeoObject( geoObjects[ idx ] ) );
    }

    setTimeout( function() {
      globalObjMngPlacemark.clusters.balloon.open( objectId );
    }, 100 );

    $.get( "/djeym/ajax-balloon-content/", {
      ids: JSON.stringify( ids ),
      objType: "Point",
      presetsBool: true
    } ).done( function( data ) {
      for ( let idx = 0, marker, content; idx < countObjs; idx++ ) {
        marker = geoObjects[ idx ];
        content = data[ marker.properties.id ];
        marker.properties.balloonContentHeader = content.header;
        marker.properties.balloonContentBody = content.body;
        marker.properties.balloonContentFooter = content.footer;
      }
      $( "ymaps:regex(class, .*-cluster-tabs__menu-item.*)" ).eq( 0 ).trigger( "click" );
    } ).fail( function( jqxhr, textStatus, error ) {
      let err = textStatus + ", " + error;
      console.log( "Request Failed: " + err );
    } );
  } );

  // Ajax, load content for balloonContent - Header, Body and Footer.
  // (Ajax, загрузить контент для balloonContent - Header, Body и Footer.)
  function ajaxGetBalloonContent( geoObjectType, geoObject ) {
    Map.balloon.close( true );

    setTimeout( function() {
      if ( geoObjectType === "Point" ) {
        globalObjMngPlacemark.objects.balloon.open( geoObject.id );
      } else if ( geoObjectType === "LineString" ) {
        globalObjMngPolyline.objects.balloon.open( geoObject.id );
      } else if ( geoObjectType === "Polygon" ) {
        globalObjMngPolygon.objects.balloon.open( geoObject.id );
      }
    }, 100 );

    $.get( "/djeym/ajax-balloon-content/",
      { objID: geoObject.properties.id,
        objType: geoObjectType,
        presetsBool: true }
    ).done( function( data ) {
      geoObject.properties.balloonContentHeader = data.header;
      geoObject.properties.balloonContentBody = data.body;
      geoObject.properties.balloonContentFooter = data.footer;

      if ( geoObjectType === "Point" ) { //
        globalObjMngPlacemark.objects.balloon.setData( geoObject );
      } else if ( geoObjectType === "LineString" ) { //
        globalObjMngPolyline.objects.balloon.setData( geoObject );
      } else if ( geoObjectType === "Polygon" ) { //
        globalObjMngPolygon.objects.balloon.setData( geoObject );
      }
    } ).fail( function( jqxhr, textStatus, error ) {
      let err = textStatus + ", " + error;
      console.log( "Request Failed: " + err );
    } );
  }

  // Ajax, load content for balloonContent - Header, Body and Footer.
  // (Ajax, загрузить контент для balloonContent - Header, Body и Footer.)
  globalObjMngPlacemark.objects.events.add( "click", function( event ) {
    let objectId = event.get( "objectId" );
    let geoObject = globalObjMngPlacemark.objects.getById( objectId );
    geoObject = clearContentGeoObject( geoObject );
    ajaxGetBalloonContent( geoObject.geometry.type, geoObject );
  } );
  globalObjMngPolyline.objects.events.add( "click", function( event ) {
    let objectId = event.get( "objectId" );
    let geoObject = globalObjMngPolyline.objects.getById( objectId );
    geoObject = clearContentGeoObject( geoObject );
    ajaxGetBalloonContent( geoObject.geometry.type, geoObject );
  } );
  globalObjMngPolygon.objects.events.add( "click", function( event ) {
    let objectId = event.get( "objectId" );
    let geoObject = globalObjMngPolygon.objects.getById( objectId );
    geoObject = clearContentGeoObject( geoObject );
    ajaxGetBalloonContent( geoObject.geometry.type, geoObject );
  } );

  // Filter by Categories and Subcategories of placemarks.
  // (Фильтр по категориям и подкатегориям меток.)
  $( ".filter-by-category-placemarks, .filter-by-category-submarks" ).on( "change", function() {
    let subcategoriesIDs = [];
    let categoriesIDs = [];
    let countSubcategories;

    $( ".filter-by-category-submarks:checked" ).each( function( idx, elem ) {
      subcategoriesIDs.push( +$( elem ).val() );
    } );

    $( ".filter-by-category-placemarks:checked" ).each( function( idx, elem ) {
      categoriesIDs.push( +$( elem ).val() );
    } );

    countSubcategories = subcategoriesIDs.length;

    if ( subcategoriesIDs.length !== 0 ) {
      let tmpIDs;
      globalObjMngPlacemark.setFilter( function( object ) {
        tmpIDs = object.properties.subCategoryIDs;
        return categoriesIDs.includes( object.properties.categoryID ) &&
          tmpIDs.filter( num => subcategoriesIDs.includes( num ) ).length ===
          countSubcategories;
      } );
    } else {
      globalObjMngPlacemark.setFilter( function( object ) {
        return categoriesIDs.includes( object.properties.categoryID );
      } );
    }
  } );

  // Filter by Category routes.
  // (Фильтр по категориям маршрутов.)
  $( ".filter-by-category-polylines" ).on( "change", function() {
    let categoriesIDs = [];

    $( ".filter-by-category-polylines:checked" ).each( function( idx, elem ) {
      categoriesIDs.push( +$( elem ).val() );
    } );

    globalObjMngPolyline.setFilter( function( object ) {
      return categoriesIDs.includes( object.properties.categoryID );
    } );
  } );

  // Filter by category of territory.
  // (Фильтр по категориям территорий.)
  $( ".filter-by-category-polygons" ).on( "change", function() {
    let categoriesIDs = [];

    $( ".filter-by-category-polygons:checked" ).each( function( idx, elem ) {
      categoriesIDs.push( +$( elem ).val() );
    } );

    globalObjMngPolygon.setFilter( function( object ) {
      return categoriesIDs.includes( object.properties.categoryID );
    } );
  } );

  // Add object manager to map.
  // (Добавить менеджер объектов на карту.)
  Map.geoObjects.add( globalObjMngPlacemark );
  Map.geoObjects.add( globalObjMngPolyline );
  Map.geoObjects.add( globalObjMngPolygon );

  // FUNCTIONS - ADD GEO-OBJECTS -------------------------------------------------------------------
  // (Функции - Добавить геообъекты.)

  // Add Placemarks
  function addPlacemarkTypeObjects( geoObjects ) {
    globalObjMngPlacemark.add( {
      type: "FeatureCollection",
      features: geoObjects
    } );
  }

  // Add Heat Points
  function addHeatPoints( geoObjects ) {
    if ( window.djeymHeatmap ) {
      globalHeatPoints.features.push( geoObjects );
      globalHeatmap.setData( globalHeatPoints );
    }
  }

  // Add Polylines
  function addPolylineTypeObjects( geoObjects ) {
    globalObjMngPolyline.add( {
      type: "FeatureCollection",
      features: geoObjects
    } );
  }

  // Add Polygons
  function addPolygonTypeObjects( geoObjects ) {
    globalObjMngPolygon.add( {
      type: "FeatureCollection",
      features: geoObjects
    } );
  }

  // AJAX ------------------------------------------------------------------------------------------

  // Error processing. (Обработка ошибок.)
  function errorProcessing( jqxhr, textStatus, error ) {
    let err = textStatus + ", " + error;
    let errDetail = "";

    if ( jqxhr.responseJSON !== undefined &&
                jqxhr.responseJSON.hasOwnProperty( "detail" ) ) {
      errDetail = jqxhr.responseJSON.detail;

      swal( {
        type: "warning",
        html: errDetail,
        showCloseButton: true
      } );
    }

    if ( errDetail.length !== 0 ) {
      console.log( "Request Failed: " + err + " - " + errDetail );
    } else {
      console.log( "Request Failed: " + err );
    }
  }

  // FINAL STEPS -----------------------------------------------------------------------------------

  setTimeout( function() { //
    // Load Placemarks.
    // (Загрузить метки.)
    function loadPlacemarkGeoObjects( offset ) {
      $.getJSON( "/djeym/ajax-get-geo-objects-placemark/",
        { map_id: window.djeymMapID, offset: offset } )
        .done( function( data ) {
          if ( data.length > 0 ) {
            addPlacemarkTypeObjects( data );
            offset += 1000;
            loadPlacemarkGeoObjects( offset );
          } else {
            loadHeatPoints( 0 );
          }
        } )
        .fail( function( jqxhr, textStatus, error ) {
          errorProcessing( jqxhr, textStatus, error );
        } );
    }
    loadPlacemarkGeoObjects( 0 );

    // Loading Thermal points.
    // (Загрузить Тепловые точки.)
    function loadHeatPoints( offset ) {
      $.getJSON( "/djeym/ajax-get-heat-points/",
        { map_id: window.djeymMapID, offset: offset } )
        .done( function( data ) {
          if ( data.length > 0 ) {
            addHeatPoints( data );
            offset += 1000;
            loadHeatPoints( offset );
          } else {
            loadPolylineGeoObjects( 0 );
          }
        } )
        .fail( function( jqxhr, textStatus, error ) {
          errorProcessing( jqxhr, textStatus, error );
        } );
    }

    // Load Polylines.
    // (Загрузить полилинии.)
    function loadPolylineGeoObjects( offset ) {
      $.getJSON( "/djeym/ajax-get-geo-objects-polyline/",
        { map_id: window.djeymMapID, offset: offset } )
        .done( function( data ) {
          if ( data.length > 0 ) {
            addPolylineTypeObjects( data );
            offset += 500;
            loadPolylineGeoObjects( offset );
          } else {
            loadPolygonGeoObjects( 0 );
          }
        } )
        .fail( function( jqxhr, textStatus, error ) {
          errorProcessing( jqxhr, textStatus, error );
        } );
    }

    // Load Polygons.
    // (Загрузить полигоны.)
    function loadPolygonGeoObjects( offset ) {
      $.getJSON( "/djeym/ajax-get-geo-objects-polygon/",
        { map_id: window.djeymMapID, offset: offset } )
        .done( function( data ) {
          if ( data.length > 0 ) {
            addPolygonTypeObjects( data );
            offset += 500;
            loadPolygonGeoObjects( offset );
          } else {
            panelActivation();
          }
        } )
        .fail( function( jqxhr, textStatus, error ) {
          errorProcessing( jqxhr, textStatus, error );
        } );
    }

    function panelActivation() { //
      // Close panel.
      $( "#id_djeym_sidenav .djeym-closebtn" ).on( "click", function( event ) {
        document.getElementById( "id_djeym_sidenav" ).style.left = "-360px";
      } );

      // Open menu tab.
      $( ".djeym-matrix-menu__btn" ).on( "click", function( event ) {
        let $this = $( this );
        let tabIDName = $this.data( "id_name" );

        if ( !$this.hasClass( "djeym_tab_active" ) ) {
          $( ".djeym-matrix-menu__btn" ).removeClass( "djeym_tab_active" );
          $this.addClass( "djeym_tab_active" );
          $( ".djeym-tab-item" ).hide();
          document.getElementById( tabIDName ).style.display = "block";
        }
      } );

      // boxiOS - Filters by categories
      ( function() {
        let $this;

        $( ".filter-by-category-placemarks" ).each( function() {
          $this = $( this );
          $this.boxiosCheckbox( {
            size: GLOBAL_BOXIOS_SIZE, jackColor: $this.data( "jack_color" ) } );
        } );

        $( ".filter-by-category-submarks" ).each( function() {
          $this = $( this );
          $this.boxiosCheckbox( {
            size: GLOBAL_BOXIOS_SIZE, jackColor: $this.data( "jack_color" ) } );
        } );

        $( ".filter-by-category-polylines" ).each( function() {
          $this = $( this );
          $this.boxiosCheckbox( {
            size: GLOBAL_BOXIOS_SIZE, jackColor: $this.data( "jack_color" ) } );
        } );

        $( ".filter-by-category-polygons" ).each( function() {
          $this = $( this );
          $this.boxiosCheckbox( {
            size: GLOBAL_BOXIOS_SIZE, jackColor: $this.data( "jack_color" ) } );
        } );
      } )();

      // Corrections for Firefox.
      if ( navigator.userAgent.toLowerCase().indexOf( "firefox" ) > -1 ) { //
        // $( ".legend_btn_style, .boxios-ios-label-text" ).css( "font-weight", "600" );
        $( ".djeym-button" ).css( "padding", "3px 20px" );
      }

      // Open the panel.
      /*
      let sidenav = document.getElementById( "id_djeym_sidenav" );
      if ( sidenav.style.left !== "0" ) { sidenav.style.left = "0"; }
      */

      // Add button «Show Panel» on map.
      if ( !window.djeymDisableSitePanel ) {
        setTimeout( function() {
          Map.controls.add( globalButtonShowPanel, { position: { left: "10px", top: "59px" } } );
        }, 500 );
      }
    }
  }, 2000 );
}
