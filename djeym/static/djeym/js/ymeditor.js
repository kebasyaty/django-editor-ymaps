/*
* DjEYM
* Yandex Map Editor.
* https://github.com/genkosta/django-editor-ymaps
* Copyright (c) 2014 genkosta
* License MIT
*/

djeymYMaps.ready( init );

function init() {
  "use strict";

  // GLOBAL VARIABLES (Глобальные переменные) ------------------------------------------------------

  let Map,
    globalButtonShowPanel,
    globalTemp,
    globalImageOfHelp,
    globalObjMngPlacemark,
    globalObjMngPolyline,
    globalObjMngPolygon,
    globalHeatmap,
    globalHeatPoints;
  let globalMinHeightContextMenu = 480;

  // Default color for colorPicker plugin.
  // (Цвет по умолчанию для плагина colorPicker.)
  const GLOBAL_DEFAULT_COLOR = "#1e98ff";
  const GLOBAL_MAX_WIDTH_LINE = 25;
  const GLOBAL_BOXIOS_SIZE = "middle";
  const GLOBAL_DEFAULTS_YMAPS_COLORS = [
    "82cdff", "1e98ff", "177bc9", "0e4779",
    "56db40", "1bad03", "97a100", "595959",
    "b3b3b3", "f371d1", "b51eff", "793d0e",
    "ffcc00", "ff931e", "e6761b", "ed4543"
  ];

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

  // FUNCTIONS -------------------------------------------------------------------------------------

  // Get content for Balloon.
  function getBalloonContent( geoObjectType, classIcon, textHeader, footerType ) {
    footerType = ( footerType ) ? "__" + footerType : "";
    return {
      contentHeader: "<div id=\"djeymModalLock\"><div id=\"djeymLoadIndicator\"></div></div>" +
                "<div class=\"djeym__balloon__content-header\">" +
                "<i class=\"" + classIcon + " m-r-10 font-blue\"></i>" + textHeader + "</div>",
      contentBody: "<div class=\"djeym__balloon__content-body\">" +
                $( "#id_hidden_" + geoObjectType + "__content" ).html() +
                "<div id=\"id_bat_save\"></div></div>",
      contentFooter: "<div class=\"djeym__balloon__content-footer\">" +
                $( "#id_hidden_" + geoObjectType + footerType + "__footer" ).html() +
                "<div id=\"djeymSignLoaded\"></div>" + "</div>"
    };
  }

  // Get item of category or subcategory.
  // (Получить элемент категории или подкатегории.)
  function getItemCategory( inputType, key, categoryID, globalTemp, isSubmark ) {
    key = +key;

    let checked = ( inputType === "radio" ) ?
      key === categoryID : $.inArray( key, categoryID ) > -1;
    let icon = globalTemp[ key ][ 1 ];
    let title = globalTemp[ key ][ 0 ];
    let $hiddenButtonsCategory = isSubmark ?
      $( "#id_hidden_buttons_subcategory" ).clone() : $( "#id_hidden_buttons_category" ).clone();
    let $input = $hiddenButtonsCategory.find( "input" );

    $input.val( key );
    $hiddenButtonsCategory.find( ".boxios-ios-icon-display" ).html( icon );
    $hiddenButtonsCategory.find( ".boxios-ios-label-text" ).text( title );

    if ( checked ) {
      $input.attr( "checked", "checked" );
    }

    return $hiddenButtonsCategory.html();
  }

  // Hide the color palette modal.
  // (Скрыть цветовую палитру.)
  function hideColorPaletteModal() {
    $( document ).off( "mousedown", $.fn.colorPicker.checkMouse );
    $( ".colorPicker-palette" ).hide();
  }

  // Button Load Indicator - Save.
  // (Индикатор загрузки для кнопки - Сохранить.)
  function startBtnLoadIndicator( $btn ) {
    $btn.html( "<i class=\"fas fa-sync-alt fa-spin\"></i>" );
  }
  function stopBtnLoadIndicator( $btn ) {
    setTimeout( function() {
      $btn.html( "<i class=\"fas fa-save\"></i>" );
    }, 500 );
  }

  // Opening and closing of the Accordion.
  // (Открытие и закрытие Аккордеона.)
  function djeymAccordion() {
    let acc = document.getElementsByClassName( "djeym_accordion" );

    for ( let idx = 0; idx < acc.length; idx++ ) {
      acc[ idx ].addEventListener( "click", function() {
        this.classList.toggle( "active" );
        let panel = this.nextElementSibling;

        if ( panel.style.display === "block" ) {
          panel.style.display = "none";
        } else {
          panel.style.display = "block";
        }
      } );
    }
  }

  // Wait for the content to load into the Balloon and update the information for the presets.
  // (Дождаться загрузки контента в Balloon и обновить информацию для пресетов.)
  let globalTimerID1;
  let globalTimerID2;
  let globalTimerID3;
  let globalTimerID4;
  function waitLoadContent() {
    globalTimerID4 = setTimeout( function() {
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
        globalTimerID3 = setTimeout( function() {
          waitLoadContent();
        }, 100 );
      } else {
        $( ".djeymUpdateInfoPreset" ).each( function() {
          $( this ).trigger( "click" );
        } );
        let modalLock = document.getElementById( "djeymModalLock" );
        if ( modalLock !== null ) {
          globalTimerID2 = setTimeout( function() {
            globalTimerID1 = setTimeout( function() {
              modalLock.remove();
            }, 600 );
            modalLock.style.opacity = 0;
          }, 200 );
        }
      }
    }, 500 );
  }

  // CUSTOMIZE PLUGINS (Настройка плагинов) --------------------------------------------------------

  // colorPicker - Default colors (Цвета по умолчанию)
  $.fn.colorPicker.defaults.colors = [
    "FFFFFF", "F08080", "CD5C5C", "FF0000", "FF1493", "C71585",
    "800080", "F0E68C", "BDB76B", "6A5ACD", "483D8B", "3CB371",
    "2E8B57", "9ACD32", "008000", "808000", "20B2AA", "008B8B",
    "00BFFF", "F4A460", "CD853F", "A52A2A", "708090", "34495e",
    "999966", "333333"
  ].concat( GLOBAL_DEFAULTS_YMAPS_COLORS );

  // EDITOR PANEL (Панель редактора) ---------------------------------------------------------------

  // Close panel.
  // (Закрыть панель.)
  $( "#id_djeym_sidenav .djeym-closebtn" ).on( "click", function( event ) {
    event.stopPropagation();
    document.getElementById( "id_djeym_sidenav" ).style.left = "-360px";
  } );

  // Open menu tab.
  // (Открыть вкладку меню.)
  $( ".djeym-matrix-menu__btn" ).on( "click", function( event ) {
    event.stopPropagation();

    let $this = $( this );
    let tabIDName = $this.data( "id_name" );

    if ( !$this.hasClass( "djeym_tab_active" ) ) {
      $( ".djeym-matrix-menu__btn" ).removeClass( "djeym_tab_active" );
      $this.addClass( "djeym_tab_active" );
      $( ".djeym-tab-item" ).hide();
      document.getElementById( tabIDName ).style.display = "block";
    }
  } );

  // CUSTOM LAYOUTS --------------------------------------------------------------------------------

  // Custom layout for Balloon.
  // (Кастомный макет для Балуна.)
  let customBalloonContentLayout = djeymYMaps.templateLayoutFactory.createClass(
    "<div class=\"position-relative hight-100\">" +
    "<div id=\"djeymModalLock\"><div id=\"djeymLoadIndicator\"></div></div>" +
    "<div class=\"djeym_ballon_header\">{{ properties.balloonContentHeader|raw }}</div>" +
    "<div class=\"djeym_ballon_body\">{{ properties.balloonContentBody|raw }}</div>" +
    "<div class=\"djeym_ballon_footer\">{{ properties.balloonContentFooter|raw }}</div></div>"
  );

  // Custom layout for Balloon.
  // (Кастомный макет для Балуна.)
  let customBalloonContextMenuLayout = djeymYMaps.templateLayoutFactory.createClass(
    "<div class=\"djeym_ballon_header\">{{ properties.balloonContentHeader|raw }}</div>" +
    "<div class=\"djeym_ballon_body\">{{ properties.balloonContentBody|raw }}</div>" +
    "<div class=\"djeym_ballon_footer\">{{ properties.balloonContentFooter|raw }}</div>" +
    "<div id=\"djeymSignLoaded\"></div>"
  );

  // Custom layout for content cluster icons.
  // (Кастомный макет для контента иконки кластера.)
  let customIconContentLayoutForCluster = djeymYMaps.templateLayoutFactory.createClass(
    "<div class=\"djeym_cluster_icon_content\"><span style=\"background-color:" +
    window.djeymClusterIconContentBgColor + ";color:" +
    window.djeymClusterIconContentTxtColor +
    ";\">$[properties.geoObjects.length]</span></div>"
  );

  // CREATE A MAP (Создать карту) ------------------------------------------------------------------
  Map = new djeymYMaps.Map( "djeymYMapsID", {
    center: window.djeymCenterMap,
    zoom: window.djeymZoomMap,
    type: ( typeof window.djeymTile === "undefined" ) ? window.djeymMapType : null,
    controls: window.djeymControls
  }, {
    maxZoom: ( typeof window.djeymTile === "undefined" ) ? 23 : window.djeymTile.maxZoom,
    minZoom: ( typeof window.djeymTile === "undefined" ) ? 0 : window.djeymTile.minZoom,
    geoObjectHasBalloon: true,
    hasHint: false,
    geoObjectBalloonMinWidth: 322,
    geoObjectBalloonMaxWidth: 342,
    geoObjectBalloonMinHeight: window.djeymBalloonMinHeight,
    geoObjectBalloonPanelMaxMapArea: 0,
    geoObjectOpenBalloonOnClick: true,
    geoObjectBalloonContentLayout: customBalloonContextMenuLayout
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
  // (Включить поиск по организациям.)
  if ( window.djeymControls.includes( "searchControl" ) &&
       window.djeymSearchProvider ) {
    Map.controls.get( "searchControl" ).options.set( "provider", "yandex#search" );
  }

  // Connect a third-party source of tiles.
  // (Подключить сторонний источник тайлов.)
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
  // (Настройки тепловой карты.)
  if ( window.djeymHeatmap ) {
    djeymYMaps.modules.require( [ "Heatmap" ], function( Heatmap ) {
      globalHeatPoints = {
        type: "FeatureCollection",
        features: []
      };
      globalHeatmap = new Heatmap( globalHeatPoints, {
        radius: parseInt( $( "#id_djeym_heatmap_radius" ).val() ),
        dissipating: $( "#id_djeym_heatmap_dissipating" ).is( ":checked" ),
        opacity: parseFloat( $( "#id_djeym_heatmap_opacity" ).val() ),
        intensityOfMidpoint: parseFloat( $( "#id_djeym_heatmap_intensity" ).val() ),
        gradient: {
          0.1: $( "#id_djeym_heatmap_gradient_color1" ).val(),
          0.2: $( "#id_djeym_heatmap_gradient_color2" ).val(),
          0.7: $( "#id_djeym_heatmap_gradient_color3" ).val(),
          1.0: $( "#id_djeym_heatmap_gradient_color4" ).val()
        }
      } );
      globalHeatmap.setMap( Map );
    } );

    $( "#id_djeym_heatmap_radius" ).on( "input", function() {
      globalHeatmap.options.set( "radius", parseInt( $( this ).val() ) );
    } );

    $( "#id_djeym_heatmap_dissipating" ).on( "change", function() {
      globalHeatmap.options.set( "dissipating", $( this ).is( ":checked" ) );
    } );

    $( "#id_djeym_heatmap_opacity" ).on( "input", function() {
      globalHeatmap.options.set( "opacity", parseFloat( $( this ).val() ) );
    } );

    $( "#id_djeym_heatmap_intensity" ).on( "input", function() {
      globalHeatmap.options.set( "intensityOfMidpoint", parseFloat( $( this ).val() ) );
    } );

    $( ".djeym_heatmap_gradient_color" ).on( "change", function() {
      globalHeatmap.options.set( "gradient", {
        0.1: $( "#id_djeym_heatmap_gradient_color1" ).val(),
        0.2: $( "#id_djeym_heatmap_gradient_color2" ).val(),
        0.7: $( "#id_djeym_heatmap_gradient_color3" ).val(),
        1.0: $( "#id_djeym_heatmap_gradient_color4" ).val()
      } );
    } );
  }

  // CREATE CUSTOM CONTROLS ------------------------------------------------------------------------
  // (Создание кастомных элементов управления)

  // Create Button - Show Panel.
  // (Создать кнопку - Показать панель редактора.)
  globalButtonShowPanel = new djeymYMaps.control.Button( {
    data: {
      image: window.djeymRoundTheme ?
        "/static/djeym/img/round_open_panel.svg" : "/static/djeym/img/open_panel.svg"
    },
    options: {
      size: "small",
      selectOnClick: false,
      maxWidth: 28
    }
  } );
  globalButtonShowPanel.events.add( "click", function() { //
    // Open panel. (Открыть панель.)
    document.getElementById( "id_djeym_sidenav" ).style.left = "0";
  } );

  // ADD EVENTS TO THE MAP (Добавить события на карту) ---------------------------------------------

  // Start the movement of the map and resize the map.
  // (Начало движения карты и изменение размера карты.)
  Map.events.add( [ "actionbegin", "sizechange" ], function() { //
    // Hide the color palette modal. (Скрыть цветовую палитру.)
    hideColorPaletteModal();
  } );

  // Opening the balloon on the map.
  // (Открытие балуна на карте. )
  Map.events.add( "balloonopen", function() { //
    // Update Info Preset.
    // (Обновить информацию пресета.)
    clearTimeout( globalTimerID1 );
    clearTimeout( globalTimerID2 );
    clearTimeout( globalTimerID3 );
    clearTimeout( globalTimerID4 );
    waitLoadContent();
  } );

  // Update preset information in the balloon-panel.
  // (Обновить информацию пресета в балун-панеле.)
  $( document ).on(
    "click",
    "ymaps:regex(class, .*-cluster-tabs__menu-item.*), " +
    "ymaps:regex(class, .*-cluster-carousel__pager-item.*), " +
    "ymaps:regex(class, .*-cluster-carousel__nav.*)",
    function( event ) {
      event.stopPropagation();
      clearTimeout( globalTimerID1 );
      clearTimeout( globalTimerID2 );
      clearTimeout( globalTimerID3 );
      clearTimeout( globalTimerID4 );
      waitLoadContent();
    } );

  // When closing the balun, clean the content elements.
  // (При закрытии балуна, чистим элементы контента.)
  Map.events.add( "balloonclose", function() { //
    // Hide the color palette modal. (Скрыть цветовую палитру.)
    hideColorPaletteModal();

    // Cleaning Balloon content. (Очистить контент Балуна.)
    $( ".djeym__balloon__content-header, " +
       ".djeym__balloon__content-body, " +
       ".djeym__balloon__content-footer" ).remove();
  } );

  // Menu - Select and create a geo-object.
  // (Меню - Выбор и создание геообъекта.)
  Map.events.add( "click", function( mapEvent ) {
    let coords = mapEvent.get( "coords" );

    Map.balloon.close();
    Map.balloon.open( coords,
      getBalloonContent(
        "action_menu",
        "fas fa-check",
        gettext( "Select an object" ) )
      , {
        minHeight: 100,
        maxWidth: 205
      }
    );

    // Launch Action Menu (Запуск меню действий)
    function launchActionMenu() { //
      // Check on the card for unfinished objects.
      // (Проверить на карте наличие незавершенных объектов.)
      let creatNewGeoObject = true;

      Map.geoObjects.each( function( context ) {
        if ( context.properties.get( "isEdit" ) ) {
          creatNewGeoObject = false;
          return false;
        }
      } );

      if ( !creatNewGeoObject ) {
        Map.balloon.close();
        swal( {
          title: gettext( "The map has an unfinished geoobject." ),
          showCloseButton: true
        } );
      }

      // Add Placemark (Добавить метку)
      $( ".djeym__balloon__content-body .djeym_add_placemark" )
        .on( "click", function( event ) {
          event.stopPropagation();
          djeymContextMenuPlacemark( mapEvent, true, coords );
        } );

      // Add Polyline (Добавить маршрут)
      $( ".djeym__balloon__content-body .djeym_add_polyline" )
        .on( "click", function( event ) {
          event.stopPropagation();
          djeymContextMenuPolyline( mapEvent, true, coords );
        } );

      // Add Polygon (Добавить территорию)
      $( ".djeym__balloon__content-body .djeym_add_polygon" )
        .on( "click", function( event ) {
          event.stopPropagation();
          djeymContextMenuPolygon( mapEvent, true, coords );
        } );

      // Add Heat Point. (Добавить тепловую точку.)
      $( ".djeym__balloon__content-body .djeym_add_heat_point" )
        .on( "click", function( event ) {
          event.stopPropagation();
          djeymHeatPoint( mapEvent, true, coords );
        } );
    }

    // Waiting for balun loading (Ожидание загрузки балуна)
    function waitLoadBalloon() {
      if ( !$( "div" ).is( ".djeym__balloon__content-body #id_bat_save" ) ) {
        setTimeout( function() {
          waitLoadBalloon();
        }, 100 );
      } else {
        launchActionMenu();
      }
    }

    waitLoadBalloon();
  } );

  // HEAT POINT (Settings) -------------------------------------------------------------------------
  function djeymHeatPoint( objEvent, mode, coords ) { //
    // mode=true (create object); mode=false (context menu).

    // Features (Характеристики)
    let pk = 0;
    let Coordinates = coords;

    // Properties (Свойства)
    let title = "";
    let weight = 0;

    // Menu on Balloon
    let iconTitleMenu = ( mode ) ? "fas fa-plus" : "fas fa-cog";
    let titleMenu = ( mode ) ? gettext( "Add Heat point" ) : gettext( "Heat point settings" );
    let menuTargetAction = ( mode ) ? "create" : "context";

    // Balloon size
    let minHeight = 260;
    let minWidth = 240;
    let maxWidth = 250;

    // Pre-close any open Balloon.
    // (Предварительно закрываем любой открытый балун.)
    Map.balloon.close();

    // Display settings in the balloon.
    // (Выводим настройки в балун.)
    Map.balloon.open( Coordinates,
      getBalloonContent( "heatpoint",
        iconTitleMenu,
        titleMenu,
        menuTargetAction )
      , {
        minHeight: minHeight,
        minWidth: minWidth,
        maxWidth: maxWidth
      }
    );

    // Run the functionality.
    // (Запуск функционала.)
    function runFunctional() {
      let $title = $( ".djeym__balloon__content-body #id_djeym_heatpoint_title" );
      let $weight = $( ".djeym__balloon__content-body #id_djeym_heatpoint_weight" );

      $title.val( title );
      $weight.val( weight );

      $title.on( "change", function() {
        title = $( this ).val();
      } );

      $weight.on( "change", function() {
        weight = $( this ).val();
      } );

      // Button - Save.
      // (Кнопка - Сохранить.)
      $( ".djeym__balloon__content-body .saveHeatPoint" ).on( "click", function( event ) {
        event.stopPropagation();

        // Fill in the form (Заполнить форму)
        $( "#id_title" ).val( title );
        $( "#id_weight" ).val( weight );
        $( "#id_coordinates" ).val( JSON.stringify( Coordinates ) );
        $( "#id_pk" ).val( pk );
        $( "#id_geo_type" ).val( "heatpoint" );

        // Add an action type in the form
        // (Добавить тип действия в форме)
        $( "#id_action" ).val( "save" );

        // Submit Form (Отправить форму)
        $( "#id_form_geoobjects" ).trigger( "submit" );

        // Actions after a successful save.
        // Действия после удачного сохранения.
        $( ".djeym__balloon__content-body #id_bat_save" ).on( "click", function( event ) {
          event.stopPropagation();
          Map.balloon.close();
        } );
      } );

      // Button - Cancel.
      // (Кнопка - Отменить.)
      $( ".djeym__balloon__content-body .cancelHeatPoint" ).on( "click", function( event ) {
        event.stopPropagation();
        Map.balloon.close();
      } );

      // Button - Help.
      // (Кнопка - Помощь.)
      $( ".djeym__balloon__content-body .helpHeatPoint" ).on( "click", function( event ) {
        event.stopPropagation();
        let iconHTML = "<i class=\"fas fa-info-circle m-r-10 font-dark-blue font-14\"></i>";
        let textHTML = gettext( "Due to the features of the plugin, to edit or delete a " +
                                "heat point, go to the admin panel - YANDEX MAPS / Heat Points." );
        textHTML = "<div class=\"font-14\">" + textHTML + "</div>";
        swal( {
          html: iconHTML + textHTML,
          showCloseButton: true
        } );
      } );
    }

    // Waiting for balloon loading.
    // (Ждем загрузку балуна.)
    function waitLoadBalloon() {
      if ( !$( "div" ).is( ".djeym__balloon__content-body #id_bat_save" ) ) {
        setTimeout( function() {
          waitLoadBalloon();
        }, 100 );
      } else {
        runFunctional();
      }
    }

    waitLoadBalloon();
  }

  // PLACEMARK (Settings) --------------------------------------------------------------------------
  function djeymContextMenuPlacemark( objEvent, mode, coords ) { //
    // mode=true (create object); mode=false (context menu).

    if ( !mode ) {
      try {
        objEvent.properties.get( "isEdit" );
      } catch ( err ) { //
        // Check on the card for unfinished objects.
        // (Проверить на карте наличие незавершенных объектов.)
        let creatNewGeoObject = true;

        Map.geoObjects.each( function( context ) {
          if ( context.properties.get( "isEdit" ) ) {
            creatNewGeoObject = false;
            return false;
          }
        } );

        if ( !creatNewGeoObject ) {
          Map.balloon.close();
          swal( {
            title: gettext( "The map has an unfinished geoobject." ),
            showCloseButton: true
          } );
          return;
        }

        // Republish object for editing.
        // (Переиздать объект для возможности редактировать.)
        let iconName = objEvent.properties.iconName;
        let tmpObj = new djeymYMaps.GeoObject( {
          geometry: {
            type: "Point",
            coordinates: objEvent.geometry.coordinates
          },
          properties: {
            isEdit: true,
            balloonContentHeader: objEvent.properties.balloonContentHeader,
            balloonContentBody: objEvent.properties.balloonContentBody,
            balloonContentFooter: objEvent.properties.balloonContentFooter,
            id: objEvent.properties.id,
            categoryID: objEvent.properties.categoryID,
            subCategoryIDs: objEvent.properties.subCategoryIDs,
            iconName: iconName
          }
        }, {
          draggable: true,
          iconLayout: "default#image",
          iconImageHref: objEvent.options.iconImageHref,
          iconImageSize: objEvent.options.iconImageSize,
          iconImageOffset: objEvent.options.iconImageOffset
        } );

        globalObjMngPlacemark.remove( objEvent );
        objEvent = tmpObj;
        Map.geoObjects.add( objEvent );

        objEvent.events.add( "contextmenu", function( event ) {
          djeymContextMenuPlacemark( event.get( "target" ), false, event.get( "coords" ) );
        } );
      }
    }

    // Properties (Свойства)
    let balloonContentHeader = ( mode ) ? "" : objEvent.properties.get( "balloonContentHeader" );
    let balloonContentBody = ( mode ) ? "" : objEvent.properties.get( "balloonContentBody" );
    let balloonContentFooter = ( mode ) ? "" : objEvent.properties.get( "balloonContentFooter" );
    let pk = ( mode ) ? 0 : objEvent.properties.get( "id" );
    let categoryID = ( mode ) ? 0 : objEvent.properties.get( "categoryID" );
    let subCategoryIDs = ( mode ) ? new Array( 1 ) : objEvent.properties.get( "subCategoryIDs" );
    let iconName = ( mode ) ? $( "#id_djeym_matrix_icons td" ).eq( 0 ).data( "icon_name" ) :
      objEvent.properties.get( "iconName" );

    // Coordinates (Координаты)
    let Coordinates = ( mode ) ? coords : objEvent.geometry.getCoordinates();

    // URL address of custom icon. (URL-адрес пользовательского значка.)
    let imgSrc = ( mode ) ? $( "#id_djeym_matrix_icons td" ).eq( 0 ).data( "icon_url" ) :
      objEvent.options.get( "iconImageHref" );

    // Menu on Balloon
    let iconTitleMenu = ( mode ) ? "fas fa-plus" : "fas fa-cog";
    let titleMenu = ( mode ) ? gettext( "Add marker" ) : gettext( "Marker settings" );
    let menuTargetAction = ( mode ) ? "create" : "context";

    // Balloon size
    let minHeight = 300;
    let maxWidth = 250;

    // Pre-close any open Balloon.
    // (Предварительно закрываем любой открытый балун.)
    Map.balloon.close();

    // Define a group of buttons. (Определяем группу кнопок.)
    if ( mode ) {
      $( ".buttons-create-new-placemark" ).show();
      $( ".buttons-context-menu-placemark" ).hide();
    } else {
      $( ".buttons-create-new-placemark" ).hide();
      $( ".buttons-context-menu-placemark" ).show();
    }

    // Display settings in the balloon.
    // (Выводим настройки в балун.)
    Map.balloon.open( Coordinates,
      getBalloonContent( "placemark",
        iconTitleMenu,
        titleMenu,
        menuTargetAction )
      , {
        minHeight: minHeight,
        maxWidth: maxWidth
      }
    );

    // Run the functionality (Запуск функционала)
    function runFunctional() { //
      // Help
      $( ".djeym__balloon__content-body #id_djeym_help" )
        .on( "click", function( event ) {
          event.stopPropagation();
          let iconHTML = "<i class=\"fas fa-info-circle m-r-10 font-dark-blue font-14\"></i>";
          let imgHTML = "<img src=\"" + globalImageOfHelp + "\" width=\"50%\" alt=\"Help\">";
          let textHTML1 = gettext( "Open the editor panel and select the desired icon." );
          let textHTML2 = gettext( "If you need to change the position of the marker - " +
                                   "Close the context menu, move the marker, again open the " +
                                   "context menu (right click on the object) and save result." );

          textHTML1 = "<div class=\"font-14\">" + textHTML1 + "</div><hr>";
          textHTML2 = "<div class=\"font-14\">" + textHTML2 + "</div><hr>";

          swal( {
            html: ( mode ) ? iconHTML + textHTML1 + imgHTML : iconHTML + textHTML2 + imgHTML,
            showCloseButton: true
          } );
        } );

      // Marker Icon
      let $icon = $( ".djeym__balloon__content-body #id_icon" );

      // Show icon in balloon.
      $icon.attr( "src", imgSrc );

      // Select and replace icon. (Выбор и смена иконки.)
      $( "#id_djeym_matrix_icons td" ).on( "click", function( event ) {
        event.stopPropagation();

        let $this = $( this );
        let iconURL = $this.data( "icon_url" );

        iconName = $this.data( "icon_name" );
        $icon.attr( "src", iconURL );

        if ( !mode ) {
          objEvent.properties.set( "iconName", iconName );
          objEvent.options.set( {
            iconImageHref: iconURL,
            iconImageSize: eval( $this.data( "icon_size" ) ),
            iconImageOffset: eval( $this.data( "icon_offset" ) )
          } );
        }
      } );

      // Open select of category. (Открыть выбор коллекции.)
      $( ".djeym__balloon__content-body #id_select_category" ).on( "click", function( event ) {
        event.stopPropagation();

        let itemsSelectCategory = "<div id=\"id_popup_select_category\">";
        let $radioButtonsCategory;
        let $checkboxButtonsSubCategory;

        globalTemp = window.djeymCategories.placemarks;
        itemsSelectCategory += "<fieldset><legend class=\"legend_btn_style\">" +
                    gettext( "Categories" ) + "</legend>";

        for ( let key in globalTemp ) {
          if ( globalTemp.hasOwnProperty( key ) ) {
            itemsSelectCategory += getItemCategory(
              "radio", key, categoryID, globalTemp );
          }
        }
        itemsSelectCategory += "</fieldset>";

        globalTemp = window.djeymCategories.submarks;
        itemsSelectCategory += "<fieldset class=\"m-t-20\"><legend class=\"legend_btn_style\">" +
                    gettext( "Subcategories" ) + "</legend>";

        for ( let key in globalTemp ) {
          if ( globalTemp.hasOwnProperty( key ) ) {
            itemsSelectCategory += getItemCategory(
              "checkbox", key, subCategoryIDs, globalTemp, true );
          }
        }
        itemsSelectCategory += "</fieldset></div>";

        if ( /input/.test( itemsSelectCategory ) ) {
          swal( {
            title: gettext( "Select a category" ),
            html: itemsSelectCategory,
            showCloseButton: true,
            onOpen: () => {
              $( "#id_popup_select_category .radio_buttons_category" )
                .boxiosRadio( { size: GLOBAL_BOXIOS_SIZE } );
              $( "#id_popup_select_category .checkbox_buttons_subcategory" )
                .boxiosCheckbox( { size: GLOBAL_BOXIOS_SIZE } );
            }

          } ).then( function( result ) {
            if ( result.value ) {
              $radioButtonsCategory = $( "#id_popup_select_category " +
                                        ".radio_buttons_category:checked" );
              $checkboxButtonsSubCategory = $( "#id_popup_select_category " +
                                              ".checkbox_buttons_subcategory:checked" );

              if ( $radioButtonsCategory.length !== 0 ) {
                categoryID = parseInt( $radioButtonsCategory.val() );
                if ( !mode ) {
                  objEvent.properties.set( "categoryID", categoryID );
                }
              }

              if ( $checkboxButtonsSubCategory.length !== 0 ) {
                let subID;
                subCategoryIDs = new Array( 1 );

                $checkboxButtonsSubCategory.each( function() {
                  subID = parseInt( $( this ).val() );

                  if ( typeof subCategoryIDs[ 0 ] !== "undefined" ) {
                    subCategoryIDs.push( subID );
                    if ( !mode ) {
                      objEvent.properties.set( "subCategoryIDs", subCategoryIDs );
                    }
                  } else {
                    subCategoryIDs[ 0 ] = subID;
                    if ( !mode ) {
                      objEvent.properties.set( "subCategoryIDs", subCategoryIDs );
                    }
                  }
                } );
              } else {
                subCategoryIDs = [];
                if ( !mode ) {
                  objEvent.properties.set( "subCategoryIDs", subCategoryIDs );
                }
              }
            }

            $( "#id_popup_select_category" ).remove();
          } );
        } else {
          swal( {
            type: "info",
            title: gettext( "There are no categories for markers." ),
            text: gettext( "Add a category in the admin panel." ),
            showCloseButton: true
          } );
        }
      } );

      // Button - Add, Save.
      // (Кнопка - Добавить, Сохранить.)
      $( ".djeym__balloon__content-body .savePlacemark" )
        .on( "click", function( event ) {
          event.stopPropagation();

          if ( balloonContentHeader.length === 0 ) {
            swal( {
              type: "warning",
              title: gettext( "Give a name to the marker" ),
              html: $( ".djeym-warning-add-geo-object-name" ).html(),
              showCloseButton: true
            } );
            return;
          } else if ( categoryID === 0 ) {
            swal( {
              type: "warning",
              title: gettext( "Select a category" ),
              html: $( ".djeym-warning-select-category" ).html(),
              showCloseButton: true
            } );
            return;
          }

          // Fill in the form (Заполнить форму)
          $( "#id_icon_name" ).val( iconName );
          $( "#id_header" ).val( balloonContentHeader );
          $( "#id_body" ).val( balloonContentBody );
          $( "#id_footer" ).val( balloonContentFooter );
          $( "#id_coordinates" ).val( JSON.stringify( Coordinates ) );
          $( "#id_pk" ).val( pk );
          $( "#id_category" ).val( categoryID );
          $( "#id_geo_type" ).val( "placemark" );

          let $subcategories = $( "#id_subcategories" );
          $subcategories.find( "option" ).remove();
          for ( let idx = 0; idx < subCategoryIDs.length; idx++ ) {
            $subcategories.append( "<option selected value=\"" +
            subCategoryIDs[ idx ] + "\"></option>" );
          }

          // Add an action type in the form
          // (Добавить тип действия в форме)
          $( "#id_action" ).val( "save" );

          // Submit Form (Отправить форму)
          $( "#id_form_geoobjects" ).trigger( "submit" );
        } );

      // Actions after a successful save or update.
      // Действия после удачного сохранения или обновления.
      $( ".djeym__balloon__content-body #id_bat_save" ).on( "click", function( event ) {
        event.stopPropagation();

        if ( !mode ) {
          Map.geoObjects.remove( objEvent );
        }

        Map.balloon.close();
      } );

      if ( !mode ) { //
        // Button - Delete (Кнопка - Удалить)
        $( ".djeym__balloon__content-body .delPlacemark" )
          .on( "click", function( event ) {
            event.stopPropagation();

            swal( {
              type: "warning",
              html: "<div class=\"font-dark-red font-24\">" +
                gettext( "Confirm object deletion!" ) + "</div>",
              showCloseButton: true,
              showCancelButton: true
            } ).then( ( result ) => {
              if ( result.value ) {
                $( "#id_pk" ).val( pk );
                $( "#id_geo_type" ).val( "placemark" );
                $( "#id_action" ).val( "delete" );
                $( "#id_form_geoobjects" ).trigger( "submit" );
                Map.geoObjects.remove( objEvent );
                Map.balloon.close();
              }
            } );
          } );
      }

      // Button - Cancel (Кнопка - Отменить)
      $( ".djeym__balloon__content-body .cancelPlacemark" ).on( "click", function( event ) {
        event.stopPropagation();

        if ( pk > 0 ) {
          $( "#id_pk" ).val( pk );
          $( "#id_geo_type" ).val( "placemark" );
          $( "#id_action" ).val( "reload" );

          Map.geoObjects.remove( objEvent );

          $( "#id_form_geoobjects" ).trigger( "submit" );
        }

        Map.balloon.close();
      } );

      // CKEditor - Add context to the editor field.
      // CKEditor - Добавить контекст в поле редактора.
      $( ".djeym__balloon__content-body .djeym_text_content" ).on( "click", function( event ) {
        event.stopPropagation();

        let $ckeditor;
        let targetVarName = $( this ).data( "target_var_name" );
        let titlePopup = "";
        let iconHTML = "<i class=\"fas fa-info-circle m-r-10 font-dark-blue font-12\"></i>";
        let hintHTML = gettext( "Image width is automatically optimized to <b>322</b> pixels." );

        hintHTML = "<span class=\"font-gray-666 font-12\">" + hintHTML + "</span><br>";

        switch ( targetVarName ) {
          case "balloonContentHeader":
            titlePopup = gettext( "Place name" );
            break;
          case "balloonContentBody":
            titlePopup = gettext( "Details" );
            break;
          case "balloonContentFooter":
            titlePopup = gettext( "Footer" );
            break;
        }

        swal( {
          html: "<div>" + titlePopup + "</div>" + iconHTML + hintHTML,
          showCloseButton: true,
          showCancelButton: true,
          onOpen: () => {
            $ckeditor = $( ".swal2-textarea" );
            $ckeditor.ckeditor( $( "#id_ckeditor_textarea" ).data( "config" ) );

            switch ( targetVarName ) {
              case "balloonContentHeader":
                $ckeditor.val( balloonContentHeader );
                break;
              case "balloonContentBody":
                $ckeditor.val( balloonContentBody );
                break;
              case "balloonContentFooter":
                $ckeditor.val( balloonContentFooter );
                break;
            }

            window.runCKEditorResizeImage();
          }
        } ).then( ( result ) => {
          if ( result.value ) {
            switch ( targetVarName ) {
              case "balloonContentHeader":
                balloonContentHeader = $ckeditor.val();
                if ( !mode ) {
                  objEvent.properties.set( "balloonContentHeader", balloonContentHeader );
                }
                break;
              case "balloonContentBody":
                balloonContentBody = $ckeditor.val();
                if ( !mode ) {
                  objEvent.properties.set( "balloonContentBody", balloonContentBody );
                }
                break;
              case "balloonContentFooter":
                balloonContentFooter = $ckeditor.val();
                if ( !mode ) {
                  objEvent.properties.set( "balloonContentFooter", balloonContentFooter );
                }
                break;
            }
          }
          $( document ).off( "click", "a.cke_dialog_tab_selected" );
          $ckeditor.ckeditor().editor.destroy();
          $ckeditor.remove();
        } );
      } );
    }

    // Waiting for balloon loading.
    // (Ждем загрузку балуна.)
    function waitLoadBalloon() {
      if ( !$( "div" ).is( ".djeym__balloon__content-body #id_bat_save" ) ) {
        setTimeout( function() {
          waitLoadBalloon();
        }, 100 );
      } else {
        runFunctional();
      }
    }

    waitLoadBalloon();
  }

  // POLYLINE (Settings) ---------------------------------------------------------------------------

  function djeymContextMenuPolyline( objEvent, mode, coords ) { //
    // mode=true (create object); mode=false (context menu).

    if ( !mode ) {
      try {
        objEvent.properties.get( "isEdit" );
      } catch ( err ) { //
        // Check on the card for unfinished objects.
        // (Проверить на карте наличие незавершенных объектов.)
        let creatNewGeoObject = true;

        Map.geoObjects.each( function( context ) {
          if ( context.properties.get( "isEdit" ) ) {
            creatNewGeoObject = false;
            return false;
          }
        } );

        if ( !creatNewGeoObject ) {
          Map.balloon.close();
          swal( {
            title: gettext( "The map has an unfinished geoobject." ),
            showCloseButton: true
          } );
          return;
        }

        // Republish object for editing.
        // (Переиздать объект для возможности редактировать.)
        let tmpObj = new djeymYMaps.GeoObject( {
          geometry: {
            type: "LineString",
            coordinates: objEvent.geometry.coordinates
          },
          properties: {
            isEdit: true,
            balloonContentHeader: objEvent.properties.balloonContentHeader,
            balloonContentBody: objEvent.properties.balloonContentBody,
            balloonContentFooter: objEvent.properties.balloonContentFooter,
            id: objEvent.properties.id,
            categoryID: objEvent.properties.categoryID
          }
        }, {
          draggable: true,
          strokeWidth: objEvent.options.strokeWidth,
          strokeColor: objEvent.options.strokeColor,
          strokeOpacity: objEvent.options.strokeOpacity
        } );

        globalObjMngPolyline.remove( objEvent );
        objEvent = tmpObj;
        Map.geoObjects.add( objEvent );

        objEvent.events.add( "contextmenu", function( event ) {
          djeymContextMenuPolyline( event.get( "target" ), false, event.get( "coords" ) );
        } );
      }
    }

    // Properties (Свойства)
    let balloonContentHeader = ( mode ) ? "" : objEvent.properties.get( "balloonContentHeader" );
    let balloonContentBody = ( mode ) ? "" : objEvent.properties.get( "balloonContentBody" );
    let balloonContentFooter = ( mode ) ? "" : objEvent.properties.get( "balloonContentFooter" );
    let pk = ( mode ) ? 0 : objEvent.properties.get( "id" );
    let categoryID = ( mode ) ? 0 : objEvent.properties.get( "categoryID" );

    // Options (Опции)
    let strokeWidth = ( mode ) ? 5 : objEvent.options.get( "strokeWidth" );
    let strokeColor = ( mode ) ? GLOBAL_DEFAULT_COLOR : objEvent.options.get( "strokeColor" );
    let strokeOpacity = ( mode ) ? 0.9 : parseFloat( objEvent.options.get( "strokeOpacity" ) );

    // Coordinates (Координаты)
    let Coordinates = ( mode ) ? [] : objEvent.geometry.getCoordinates();
    let iconTitleMenu = ( mode ) ? "fas fa-plus" : "fas fa-cog";
    let titleMenu = ( mode ) ? gettext( "Add route" ) : gettext( "Route settings" );
    let menuTargetAction = ( mode ) ? "create" : "context";

    // Balloon size
    let minHeight = 350;
    let maxWidth = 270;

    // Pre-close any open Balloon. (Предварительно закрываем любой открытый балун.)
    Map.balloon.close();

    if ( mode ) {
      $( ".buttons-create-new-polyline" ).show();
      $( ".buttons-context-menu-polyline" ).hide();
    } else {
      $( ".buttons-create-new-polyline" ).hide();
      $( ".buttons-context-menu-polyline" ).show();
    }

    // Display settings in the balloon.
    // (Выводим настройки в балун.)
    Map.balloon.open( coords,
      getBalloonContent( "polyline",
        iconTitleMenu,
        titleMenu,
        menuTargetAction )
      , {
        minHeight: minHeight,
        maxWidth: maxWidth
      }
    );

    // Run the functionality (Запуск функционала)
    function runFunctional() {
      let $colorLine = $( ".djeym__balloon__content-body #id_color_line" );

      // Help
      $( ".djeym__balloon__content-body #id_djeym_help" )
        .on( "click", function( event ) {
          event.stopPropagation();
          let iconHTML = "<i class=\"fas fa-info-circle m-r-10 font-dark-blue font-14\"></i>";
          let imgHTML = "<img src=\"" + globalImageOfHelp + "\" width=\"50%\" alt=\"Help\">";
          let textHTML = gettext( "After the button [ <b>+</b> ], click the left mouse " +
                                  "button on the map and create a route. Open the context " +
                                  "menu again (right-click on the object) and save the result." );

          textHTML = "<div class=\"font-14\">" + textHTML + "</div><hr>";

          swal( {
            html: ( mode ) ? iconHTML + textHTML + imgHTML : imgHTML,
            showCloseButton: true
          } );
        } );

      // Connecting a plugin to choose a color
      // (Подключение плагина для выбора цвета)
      $colorLine.colorPicker( {
        pickerDefault: strokeColor
      } );

      // Temporarily apply color to the line while editing.
      // (Временное применение цвета к линии, во время редактирования.)
      $colorLine.on( "change", function() {
        if ( mode ) {
          strokeColor = $( this ).val();
        } else {
          strokeColor = $( this ).val();
          objEvent.options.set( "strokeColor", strokeColor );
        }
      } );

      // Slider - Width line (Толщина линии)
      $( function() {
        let $sliderWidthLine = $( ".djeym__balloon__content-body #id_slider_width_line" );

        $sliderWidthLine.boxiosRange( {
          min: 1,
          max: GLOBAL_MAX_WIDTH_LINE,
          value: strokeWidth
        } );

        $sliderWidthLine.on( "input", function() {
          if ( mode ) {
            strokeWidth = parseInt( $( this ).val() );
          } else {
            strokeWidth = parseInt( $( this ).val() );
            objEvent.options.set( "strokeWidth", strokeWidth );
          }
        } );
      } );

      // Slider - Opacity of line (Прозрачность линии)
      $( function() {
        let $sliderOpacityLine = $( ".djeym__balloon__content-body #id_slider_opacity_line" );
        $sliderOpacityLine.boxiosRange( {
          width: "50%",
          min: 0,
          max: 1,
          step: 0.1,
          value: strokeOpacity
        } );
        $sliderOpacityLine.on( "input", function() {
          if ( mode ) {
            strokeOpacity = parseFloat( $( this ).val() );
          } else {
            strokeOpacity = parseFloat( $( this ).val() );
            objEvent.options.set( "strokeOpacity", strokeOpacity );
          }
        } );
      } );

      // Open selection category (Открыть выбор коллекции)
      $( ".djeym__balloon__content-body #id_select_category" ).on( "click", function( event ) {
        event.stopPropagation();

        let itemsSelectCategory = "<div id=\"id_popup_select_category\">";
        let $radioButtonsCategory;

        globalTemp = window.djeymCategories.polylines;

        for ( let key in globalTemp ) {
          if ( globalTemp.hasOwnProperty( key ) ) {
            itemsSelectCategory += getItemCategory(
              "radio", key, categoryID, globalTemp );
          }
        }
        itemsSelectCategory += "</div>";

        if ( /input/.test( itemsSelectCategory ) ) {
          swal( {
            title: gettext( "Select a category" ),
            html: itemsSelectCategory,
            showCloseButton: true,
            onOpen: () => {
              $( "#id_popup_select_category .radio_buttons_category" )
                .boxiosRadio( { size: GLOBAL_BOXIOS_SIZE } );
            }
          } ).then( function( result ) {
            if ( result.value ) {
              $radioButtonsCategory = $( "#id_popup_select_category " +
                                        ".radio_buttons_category:checked" );

              if ( $radioButtonsCategory.length ) {
                categoryID = parseInt( $radioButtonsCategory.val() );
                if ( !mode ) {
                  objEvent.properties.set( "categoryID", categoryID );
                }
              }
            }

            $( "#id_popup_select_category" ).remove();
          } );
        } else {
          swal( {
            type: "info",
            title: gettext( "There are no categories for routes." ),
            text: gettext( "Add a category in the admin panel." ),
            showCloseButton: true
          } );
        }
      } );

      // Button - Add, Edit.  (Кнопка - Добавить, Редактировать.)
      $( ".djeym__balloon__content-body .editPolyline" )
        .on( "click", function( event ) {
          event.stopPropagation();

          if ( mode ) {
            if ( balloonContentHeader.length === 0 ) {
              swal( {
                type: "warning",
                title: gettext( "Give a name for the route" ),
                html: $( ".djeym-warning-add-geo-object-name" ).html(),
                showCloseButton: true
              } );
              return;
            } else if ( categoryID === 0 ) {
              swal( {
                type: "warning",
                title: gettext( "Select a category" ),
                html: $( ".djeym-warning-select-category" ).html(),
                showCloseButton: true
              } );
              return;
            }

            let Polyline = new djeymYMaps.GeoObject( {
              geometry: {
                type: "LineString",
                coordinates: Coordinates
              },
              properties: {
                isEdit: true,
                balloonContentHeader: balloonContentHeader,
                balloonContentBody: balloonContentBody,
                balloonContentFooter: balloonContentFooter,
                id: pk,
                categoryID: categoryID
              }
            }, {
              draggable: true,
              strokeWidth: strokeWidth,
              strokeColor: strokeColor,
              strokeOpacity: strokeOpacity
            } );

            Polyline.events.add( "contextmenu", function( event ) {
              djeymContextMenuPolyline( event.get( "target" ), false, event.get( "coords" ) );
            } );

            Map.geoObjects.add( Polyline );
            Polyline.editor.startEditing();
            Polyline.editor.startDrawing();
          } else {
            objEvent.editor.startEditing();
            objEvent.editor.startDrawing();
          }

          Map.balloon.close();
        } );

      // Button - Cancel (Кнопка - Отменить)
      $( ".djeym__balloon__content-body .cancelPolyline" ).on( "click", function( event ) {
        event.stopPropagation();

        if ( pk > 0 ) {
          $( "#id_pk" ).val( pk );
          $( "#id_geo_type" ).val( "polyline" );
          $( "#id_action" ).val( "reload" );

          Map.geoObjects.remove( objEvent );

          $( "#id_form_geoobjects" ).trigger( "submit" );
        }

        Map.balloon.close();
      } );

      // Buttons for the context menu.
      // (Кнопки для контекстного меню.)
      if ( !mode ) { //
        // Button - Save (Кнопка - Сохранить)
        $( ".djeym__balloon__content-body .savePolyline" )
          .on( "click", function( event ) {
            event.stopPropagation();

            if ( balloonContentHeader.length === 0 ) {
              swal( {
                type: "warning",
                title: gettext( "Give a name for the route" ),
                html: $( ".djeym-warning-add-geo-object-name" ).html(),
                showCloseButton: true
              } );
              return;
            } else if ( categoryID === 0 ) {
              swal( {
                type: "warning",
                title: gettext( "Select a category" ),
                html: $( ".djeym-warning-select-category" ).html(),
                showCloseButton: true
              } );
              return;
            }

            // Fill in the form (Заполнить форму)
            $( "#id_header" ).val( balloonContentHeader );
            $( "#id_body" ).val( balloonContentBody );
            $( "#id_footer" ).val( balloonContentFooter );
            $( "#id_stroke_width" ).val( strokeWidth );
            $( "#id_stroke_color" ).val( strokeColor );
            $( "#id_stroke_opacity" ).val( strokeOpacity );
            $( "#id_coordinates" ).val( JSON.stringify( Coordinates ) );
            $( "#id_pk" ).val( pk );
            $( "#id_category" ).val( categoryID );
            $( "#id_geo_type" ).val( "polyline" );
            $( "#id_action" ).val( "save" );

            // Submit the form (Отправляем форму)
            $( "#id_form_geoobjects" ).trigger( "submit" );
          } );

        // Actions after a successful save or update.
        // (Действия после удачного сохранения или обновления.)
        $( ".djeym__balloon__content-body #id_bat_save" ).on( "click", function( event ) {
          event.stopPropagation();

          Map.geoObjects.remove( objEvent );
          Map.balloon.close();
        } );

        // Button - Delete (Кнопка - Удалить)
        $( ".djeym__balloon__content-body .delPolyline" ).on( "click", function( event ) {
          event.stopPropagation();

          swal( {
            type: "warning",
            html: "<div class=\"font-dark-red font-24\">" +
                  gettext( "Confirm object deletion!" ) + "</div>",
            showCloseButton: true,
            showCancelButton: true
          } ).then( ( result ) => {
            if ( result.value ) {
              if ( pk > 0 ) {
                $( "#id_pk" ).val( pk );
                $( "#id_geo_type" ).val( "polyline" );
                $( "#id_action" ).val( "delete" );

                $( "#id_form_geoobjects" ).trigger( "submit" );
              }

              Map.geoObjects.remove( objEvent );
              Map.balloon.close();
            }
          } );
        } );
      }

      // CKEditor - Add context to the editor field.
      // CKEditor - Добавить контекст в поле редактора.
      $( ".djeym__balloon__content-body .djeym_text_content" )
        .on( "click", function( event ) {
          event.stopPropagation();
          let $ckeditor;
          let targetVarName = $( this ).data( "target_var_name" );
          let titlePopup = "";
          let iconHTML = "<i class=\"fas fa-info-circle m-r-10 font-dark-blue font-12\"></i>";
          let hintHTML = gettext( "Image width is automatically optimized to <b>322</b> pixels." );

          hintHTML = "<span class=\"font-gray-666 font-12\">" + hintHTML + "</span><br>";

          switch ( targetVarName ) {
            case "balloonContentHeader":
              titlePopup = gettext( "Route name" );
              break;
            case "balloonContentBody":
              titlePopup = gettext( "Details" );
              break;
            case "balloonContentFooter":
              titlePopup = gettext( "Footer" );
              break;
          }

          swal( {
            html: "<div>" + titlePopup + "</div>" + iconHTML + hintHTML,
            showCloseButton: true,
            showCancelButton: true,
            onOpen: () => {
              $ckeditor = $( ".swal2-textarea" );
              $ckeditor.ckeditor( $( "#id_ckeditor_textarea" ).data( "config" ) );

              switch ( targetVarName ) {
                case "balloonContentHeader":
                  $ckeditor.val( balloonContentHeader );
                  break;
                case "balloonContentBody":
                  $ckeditor.val( balloonContentBody );
                  break;
                case "balloonContentFooter":
                  $ckeditor.val( balloonContentFooter );
                  break;
              }

              window.runCKEditorResizeImage();
            }
          } ).then( ( result ) => {
            if ( result.value ) {
              switch ( targetVarName ) {
                case "balloonContentHeader":
                  balloonContentHeader = $ckeditor.val();
                  if ( !mode ) {
                    objEvent.properties.set( "balloonContentHeader", balloonContentHeader );
                  }
                  break;
                case "balloonContentBody":
                  balloonContentBody = $ckeditor.val();
                  if ( !mode ) {
                    objEvent.properties.set( "balloonContentBody", balloonContentBody );
                  }
                  break;
                case "balloonContentFooter":
                  balloonContentFooter = $ckeditor.val();
                  if ( !mode ) {
                    objEvent.properties.set( "balloonContentFooter", balloonContentFooter );
                  }
                  break;
              }
            }
            $( document ).off( "click", "a.cke_dialog_tab_selected" );
            $ckeditor.ckeditor().editor.destroy();
            $ckeditor.remove();
          } );
        } );
    }

    // Waiting for balloon loading.
    // (Ждем загрузку балуна.)
    function waitLoadBalloon() {
      if ( !$( "div" ).is( ".djeym__balloon__content-body #id_bat_save" ) ) {
        setTimeout( function() {
          waitLoadBalloon();
        }, 100 );
      } else {
        runFunctional();
      }
    }

    waitLoadBalloon();
  }

  // POLYGON (Settings) ----------------------------------------------------------------------------

  function djeymContextMenuPolygon( objEvent, mode, coords ) { //
    // mode=true (create object); mode=false (context menu).

    if ( !mode ) {
      try {
        objEvent.properties.get( "isEdit" );
      } catch ( err ) { //
        // Check on the card for unfinished objects.
        // (Проверить на карте наличие незавершенных объектов.)
        let creatNewGeoObject = true;

        Map.geoObjects.each( function( context ) {
          if ( context.properties.get( "isEdit" ) ) {
            creatNewGeoObject = false;
            return false;
          }
        } );

        if ( !creatNewGeoObject ) {
          Map.balloon.close();
          swal( {
            title: gettext( "The map has an unfinished geoobject." ),
            showCloseButton: true
          } );
          return;
        }

        // Republish object for editing.
        // (Переиздать объект для возможности редактировать.)
        let tmpObj = new djeymYMaps.GeoObject( {
          geometry: {
            type: "Polygon",
            coordinates: objEvent.geometry.coordinates
          },
          properties: {
            isEdit: true,
            balloonContentHeader: objEvent.properties.balloonContentHeader,
            balloonContentBody: objEvent.properties.balloonContentBody,
            balloonContentFooter: objEvent.properties.balloonContentFooter,
            id: objEvent.properties.id,
            categoryID: objEvent.properties.categoryID
          }
        }, {
          draggable: true,
          strokeWidth: objEvent.options.strokeWidth,
          strokeColor: objEvent.options.strokeColor,
          strokeOpacity: objEvent.options.strokeOpacity,
          fillColor: objEvent.options.fillColor,
          fillOpacity: objEvent.options.fillOpacity
        } );

        globalObjMngPolygon.remove( objEvent );
        objEvent = tmpObj;
        Map.geoObjects.add( objEvent );

        objEvent.events.add( "contextmenu", function( event ) {
          djeymContextMenuPolygon( event.get( "target" ), false, event.get( "coords" ) );
        } );
      }
    }

    // Properties (Свойства)
    let balloonContentHeader = ( mode ) ? "" : objEvent.properties.get( "balloonContentHeader" );
    let balloonContentBody = ( mode ) ? "" : objEvent.properties.get( "balloonContentBody" );
    let balloonContentFooter = ( mode ) ? "" : objEvent.properties.get( "balloonContentFooter" );
    let pk = ( mode ) ? 0 : objEvent.properties.get( "id" );
    let categoryID = ( mode ) ? 0 : objEvent.properties.get( "categoryID" );

    // Options (Опции)
    let strokeWidth = ( mode ) ? 2 : objEvent.options.get( "strokeWidth" );
    let strokeColor = ( mode ) ? GLOBAL_DEFAULT_COLOR : objEvent.options.get( "strokeColor" );
    let strokeOpacity = ( mode ) ? 0.9 : objEvent.options.get( "strokeOpacity" );
    let fillColor = ( mode ) ? GLOBAL_DEFAULT_COLOR : objEvent.options.get( "fillColor" );
    let fillOpacity = ( mode ) ? 0.9 : objEvent.options.get( "fillOpacity" );

    // Coordinates (Координаты)
    let Coordinates = ( mode ) ? [] : objEvent.geometry.getCoordinates();
    let iconTitleMenu = ( mode ) ? "fas fa-plus" : "fas fa-cog";
    let titleMenu = ( mode ) ? gettext( "Add territory" ) : gettext( "Territory settings" );
    let menuTargetAction = ( mode ) ? "create" : "context";

    // Balloon size
    let minHeight = ( window.djeymAreaCalculation ) ?
      globalMinHeightContextMenu : globalMinHeightContextMenu - 20;
    let maxWidth = 270;

    // Pre-close any open Balloon. (Предварительно закрываем любой открытый балун.)
    Map.balloon.close();

    if ( mode ) {
      $( ".buttons-create-new-polygon" ).show();
      $( ".buttons-context-menu-polygon" ).hide();
    } else {
      $( ".buttons-create-new-polygon" ).hide();
      $( ".buttons-context-menu-polygon" ).show();
    }

    // Display settings in the balloon.
    // (Выводим настройки в балун.)
    Map.balloon.open( coords,
      getBalloonContent(
        "polygon",
        iconTitleMenu,
        titleMenu,
        menuTargetAction )
      , {
        minHeight: minHeight,
        maxWidth: maxWidth
      }
    );

    // Run the functionality (Запуск функционала)
    function runFunctional() {
      let $colorLine = $( ".djeym__balloon__content-body #id_color_line" );
      let $colorFill = $( ".djeym__balloon__content-body #id_color_fill" );

      // Help
      $( ".djeym__balloon__content-body #id_djeym_help" )
        .on( "click", function( event ) {
          event.stopPropagation();
          let iconHTML = "<i class=\"fas fa-info-circle m-r-10 font-dark-blue font-14\"></i>";
          let imgHTML = "<img src=\"" + globalImageOfHelp + "\" width=\"50%\" alt=\"Help\">";
          let textHTML = gettext( "After the button [ <b>+</b> ], " +
                                  "click the left mouse button on the map and mark the " +
                                  "territory. Open the context menu again " +
                                  "(right-click on the object) and save the result." );

          textHTML = "<div class=\"font-14\">" + textHTML + "</div><hr>";

          swal( {
            html: ( mode ) ? iconHTML + textHTML + imgHTML : imgHTML,
            showCloseButton: true
          } );
        } );

      // Area Calculate.
      // (Рассчитать площадь.)
      if ( !mode && window.djeymAreaCalculation ) {
        djeymYMaps.modules.require( [ "util.calculateArea" ], function( calculateArea ) {
          let area = calculateArea( objEvent );

          // If the area exceeds 1,000,000 m², then we bring it to km².
          // (Если площадь превышает 1 000 000 м², то приводим ее к км².)
          if ( area <= 1e6 ) {
            area += " м²";
          } else {
            area = ( area / 1e6 ).toFixed( 3 ) + " км²";
          }
          $( ".djeym__balloon__content-body #id_djeym_result_calculate_area" ).text( area );
        } );
      }

      // Connecting the plugin to select colors.
      // (Подключение плагина для выбора цвета.)
      $colorLine.colorPicker( { pickerDefault: strokeColor } );
      $colorFill.colorPicker( { pickerDefault: fillColor } );

      // Temporarily applying color to a line when editing.
      // Временное применение цвета к линии, при редактировании.
      $colorLine.on( "change", function() {
        if ( mode ) {
          strokeColor = $( this ).val();
        } else {
          strokeColor = $( this ).val();
          objEvent.options.set( "strokeColor", strokeColor );
        }
      } );

      // Temporarily apply a fill color to a polygon when editing.
      // Временное применение цвета заливки к многоугольнику при редактировании.
      $colorFill.on( "change", function() {
        if ( mode ) {
          fillColor = $( this ).val();
        } else {
          fillColor = $( this ).val();
          objEvent.options.set( "fillColor", $( this ).val() );
        }
      } );

      // Slider - Width line (Толщина линии)
      $( function() {
        let $sliderWidthLine = $( ".djeym__balloon__content-body #id_slider_width_line" );

        $sliderWidthLine.boxiosRange( {
          min: 1,
          max: GLOBAL_MAX_WIDTH_LINE,
          value: strokeWidth
        } );

        $sliderWidthLine.on( "input", function() {
          if ( mode ) {
            strokeWidth = parseInt( $( this ).val() );
          } else {
            strokeWidth = parseInt( $( this ).val() );
            objEvent.options.set( "strokeWidth", strokeWidth );
          }
        } );
      } );

      // Slider - Opacity of line (Прозрачность линии)
      $( function() {
        let $sliderOpacityLine = $( ".djeym__balloon__content-body #id_slider_opacity_line" );

        $sliderOpacityLine.boxiosRange( {
          width: "50%",
          min: 0,
          max: 1,
          step: 0.1,
          value: strokeOpacity
        } );

        $sliderOpacityLine.on( "input", function() {
          if ( mode ) {
            strokeOpacity = parseFloat( $( this ).val() );
          } else {
            strokeOpacity = parseFloat( $( this ).val() );
            objEvent.options.set( "strokeOpacity", strokeOpacity );
          }
        } );
      } );

      // Slider - Opacity fill (Прозрачность заливки)
      $( function() {
        let $sliderOpacityFill = $( ".djeym__balloon__content-body #id_slider_opacity_fill" );

        $sliderOpacityFill.boxiosRange( {
          width: "50%",
          min: 0,
          max: 1,
          step: 0.1,
          value: fillOpacity
        } );

        $sliderOpacityFill.on( "input", function() {
          if ( mode ) {
            fillOpacity = parseFloat( $( this ).val() );
          } else {
            fillOpacity = parseFloat( $( this ).val() );
            objEvent.options.set( "fillOpacity", fillOpacity );
          }
        } );
      } );

      // Open selection category (Открыть выбор коллекции)
      $( ".djeym__balloon__content-body #id_select_category" )
        .on( "click", function( event ) {
          event.stopPropagation();
          let itemsSelectCategory = "<div id=\"id_popup_select_category\">";
          let $radioButtonsCategory;

          globalTemp = window.djeymCategories.polygons;

          for ( let key in globalTemp ) {
            if ( globalTemp.hasOwnProperty( key ) ) {
              itemsSelectCategory += getItemCategory( "radio",
                key, categoryID, globalTemp );
            }
          }
          itemsSelectCategory += "</div>";

          if ( /input/.test( itemsSelectCategory ) ) {
            swal( {
              title: gettext( "Select a category" ),
              html: itemsSelectCategory,
              showCloseButton: true,
              onOpen: () => {
                $( "#id_popup_select_category .radio_buttons_category" )
                  .boxiosRadio( { size: GLOBAL_BOXIOS_SIZE } );
              }
            } ).then( function( result ) {
              if ( result.value ) {
                $radioButtonsCategory = $( "#id_popup_select_category " +
                                          ".radio_buttons_category:checked" );

                if ( $radioButtonsCategory.length !== 0 ) {
                  categoryID = parseInt( $radioButtonsCategory.val() );
                  if ( !mode ) {
                    objEvent.properties.set( "categoryID", categoryID );
                  }
                }
              }

              $( "#id_popup_select_category" ).remove();
            } );
          } else {
            swal( {
              type: "info",
              title: gettext( "There are no categories for territories." ),
              text: gettext( "Add a category in the admin panel." ),
              showCloseButton: true
            } );
          }
        } );

      // Button - Add, Edit. (Кнопка - Добавить, Редактировать.)
      $( ".djeym__balloon__content-body .editPolygon" )
        .on( "click", function( event ) {
          event.stopPropagation();

          if ( mode ) {
            if ( balloonContentHeader.length === 0 ) {
              swal( {
                type: "warning",
                title: gettext( "Give a name to the territory." ),
                html: $( ".djeym-warning-add-geo-object-name" ).html(),
                showCloseButton: true
              } );
              return;
            } else if ( categoryID === 0 ) {
              swal( {
                type: "warning",
                title: gettext( "Select a category" ),
                html: $( ".djeym-warning-select-category" ).html(),
                showCloseButton: true
              } );
              return;
            }

            let Polygon = new djeymYMaps.GeoObject( {
              geometry: {
                type: "Polygon",
                coordinates: Coordinates
              },
              properties: {
                isEdit: true,
                balloonContentHeader: balloonContentHeader,
                balloonContentBody: balloonContentBody,
                balloonContentFooter: balloonContentFooter,
                id: pk,
                categoryID: categoryID
              }
            }, {
              draggable: true,
              strokeWidth: strokeWidth,
              strokeColor: strokeColor,
              strokeOpacity: strokeOpacity,
              fillColor: fillColor,
              fillOpacity: fillOpacity
            } );

            Polygon.events.add( "contextmenu", function( event ) {
              djeymContextMenuPolygon( event.get( "target" ), false, event.get( "coords" ) );
            } );

            Map.geoObjects.add( Polygon );
            Polygon.editor.startEditing();
            Polygon.editor.startDrawing();
          } else {
            objEvent.editor.startEditing();
            objEvent.editor.startDrawing();
          }

          Map.balloon.close();
        } );

      // Button - Cancel (Кнопка - Отменить)
      $( ".djeym__balloon__content-body .cancelPolygon" ).on( "click", function( event ) {
        event.stopPropagation();

        if ( pk > 0 ) {
          $( "#id_pk" ).val( pk );
          $( "#id_geo_type" ).val( "polygon" );
          $( "#id_action" ).val( "reload" );

          Map.geoObjects.remove( objEvent );

          $( "#id_form_geoobjects" ).trigger( "submit" );
        }

        Map.balloon.close();
      } );

      // Buttons for the context menu.
      // (Кнопки для контекстного меню.)
      if ( !mode ) { //
        // Button - Save (Кнопка - Сохранить)
        $( ".djeym__balloon__content-body .savePolygon" ).on( "click", function( event ) {
          event.stopPropagation();

          if ( balloonContentHeader.length === 0 ) {
            swal( {
              type: "warning",
              title: gettext( "Give a name to the territory." ),
              html: $( ".djeym-warning-add-geo-object-name" ).html(),
              showCloseButton: true
            } );
            return;
          } else if ( categoryID === 0 ) {
            swal( {
              type: "warning",
              title: gettext( "Select a category" ),
              html: $( ".djeym-warning-select-category" ).html(),
              showCloseButton: true
            } );
            return;
          }

          $( "#id_header" ).val( balloonContentHeader );
          $( "#id_body" ).val( balloonContentBody );
          $( "#id_footer" ).val( balloonContentFooter );
          $( "#id_stroke_width" ).val( strokeWidth );
          $( "#id_stroke_color" ).val( strokeColor );
          $( "#id_stroke_opacity" ).val( strokeOpacity );
          $( "#id_fill_color" ).val( fillColor );
          $( "#id_fill_opacity" ).val( fillOpacity );
          $( "#id_coordinates" ).val( JSON.stringify( Coordinates ) );
          $( "#id_pk" ).val( pk );
          $( "#id_category" ).val( categoryID );
          $( "#id_geo_type" ).val( "polygon" );
          $( "#id_action" ).val( "save" );

          // Submit the form (Отправляем форму)
          $( "#id_form_geoobjects" ).trigger( "submit" );
        } );

        // Actions after a successful save or update.
        // Действия после удачного сохранения или обновления.
        $( ".djeym__balloon__content-body #id_bat_save" ).on( "click", function( event ) {
          event.stopPropagation();
          Map.geoObjects.remove( objEvent );
          Map.balloon.close();
        } );

        // Button - Delete (Кнопка - Удалить)
        $( ".djeym__balloon__content-body .delPolygon" ).on( "click", function( event ) {
          event.stopPropagation();

          swal( {
            type: "warning",
            html: "<div class=\"font-dark-red font-24\">" +
                  gettext( "Confirm object deletion!" ) + "</div>",
            showCloseButton: true,
            showCancelButton: true
          } ).then( ( result ) => {
            if ( result.value ) {
              if ( pk > 0 ) {
                $( "#id_pk" ).val( pk );
                $( "#id_geo_type" ).val( "polygon" );
                $( "#id_action" ).val( "delete" );
                $( "#id_form_geoobjects" ).trigger( "submit" );
              }

              Map.geoObjects.remove( objEvent );
              Map.balloon.close();
            }
          } );
        } );
      }

      // CKEditor - Add context to the editor field.
      // CKEditor - Добавить контекст в поле редактора.
      $( ".djeym__balloon__content-body .djeym_text_content" ).on( "click", function( event ) {
        event.stopPropagation();
        let $ckeditor;
        let targetVarName = $( this ).data( "target_var_name" );
        let titlePopup = "";
        let iconHTML = "<i class=\"fas fa-info-circle m-r-10 font-dark-blue font-12\"></i>";
        let hintHTML = gettext( "Image width is automatically optimized to <b>322</b> pixels." );

        hintHTML = "<span class=\"font-gray-666 font-12\">" + hintHTML + "</span><br>";

        switch ( targetVarName ) {
          case "balloonContentHeader":
            titlePopup = gettext( "Territory name" );
            break;
          case "balloonContentBody":
            titlePopup = gettext( "Details" );
            break;
          case "balloonContentFooter":
            titlePopup = gettext( "Footer" );
            break;
        }

        swal( {
          html: "<div>" + titlePopup + "</div>" + iconHTML + hintHTML,
          showCloseButton: true,
          showCancelButton: true,
          onOpen: () => {
            $ckeditor = $( ".swal2-textarea" );
            $ckeditor.ckeditor( $( "#id_ckeditor_textarea" ).data( "config" ) );

            switch ( targetVarName ) {
              case "balloonContentHeader":
                $ckeditor.val( balloonContentHeader );
                break;
              case "balloonContentBody":
                $ckeditor.val( balloonContentBody );
                break;
              case "balloonContentFooter":
                $ckeditor.val( balloonContentFooter );
                break;
            }

            window.runCKEditorResizeImage();
          }
        } ).then( ( result ) => {
          if ( result.value ) {
            switch ( targetVarName ) {
              case "balloonContentHeader":
                balloonContentHeader = $ckeditor.val();
                if ( !mode ) {
                  objEvent.properties.set( "balloonContentHeader", balloonContentHeader );
                }
                break;
              case "balloonContentBody":
                balloonContentBody = $ckeditor.val();
                if ( !mode ) {
                  objEvent.properties.set( "balloonContentBody", balloonContentBody );
                }
                break;
              case "balloonContentFooter":
                balloonContentFooter = $ckeditor.val();
                if ( !mode ) {
                  objEvent.properties.set( "balloonContentFooter", balloonContentFooter );
                }
                break;
            }
          }
          $( document ).off( "click", "a.cke_dialog_tab_selected" );
          $ckeditor.ckeditor().editor.destroy();
          $ckeditor.remove();
        } );
      } );
    }

    // Waiting for balloon loading.
    // (Ждем загрузку балуна.)
    function waitLoadBalloon() {
      if ( !$( "div" ).is( ".djeym__balloon__content-body #id_bat_save" ) ) {
        setTimeout( function() {
          waitLoadBalloon();
        }, 100 );
      } else {
        runFunctional();
      }
    }

    waitLoadBalloon();
  }

  // CREATE OBJECT MANAGERS ------------------------------------------------------------------------

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
    clusterize: window.djeymClusteringEdit,
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

  // Transfer the data of geo objects from the manager to the context menu.
  // (Передать данные geoобъектов из менеджера в контекстное меню.)
  function transferToContextMenu( geoObjectType, geoObject, coords ) {
    let pk = geoObject.properties.id;

    $.get( "/djeym/ajax-balloon-content/",
      { objID: pk, objType: geoObjectType, presetsBool: false }
    ).done( function( data ) {
      geoObject.properties.balloonContentHeader = data.header;
      geoObject.properties.balloonContentBody = data.body;
      geoObject.properties.balloonContentFooter = data.footer
        .replace( /<div id="djeymSignLoaded">.*<\/div>/g, "" );

      switch ( geoObjectType ) {
        case "Point":
          djeymContextMenuPlacemark( geoObject, false, coords );
          break;
        case "LineString":
          djeymContextMenuPolyline( geoObject, false, coords );
          break;
        case "Polygon":
          djeymContextMenuPolygon( geoObject, false, coords );
          break;
      }
    } ).fail( function( jqxhr, textStatus, error ) {
      let err = textStatus + ", " + error;
      console.log( "Request Failed: " + err );
    } );
  }

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

  // Transfer object from manager to map for editing.
  // (Перевести объект из менеджера на карту для редактирования.)
  globalObjMngPlacemark.objects.events.add( "contextmenu", function( event ) {
    let objectId = event.get( "objectId" );
    let geoObject = globalObjMngPlacemark.objects.getById( objectId );
    transferToContextMenu( geoObject.geometry.type, geoObject, event.get( "coords" ) );
  } );
  globalObjMngPolyline.objects.events.add( "contextmenu", function( event ) {
    let objectId = event.get( "objectId" );
    let geoObject = globalObjMngPolyline.objects.getById( objectId );
    transferToContextMenu( geoObject.geometry.type, geoObject, event.get( "coords" ) );
  } );
  globalObjMngPolygon.objects.events.add( "contextmenu", function( event ) {
    let objectId = event.get( "objectId" );
    let geoObject = globalObjMngPolygon.objects.getById( objectId );
    transferToContextMenu( geoObject.geometry.type, geoObject, event.get( "coords" ) );
  } );

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

  // Reload editor page. (Перезагрузить страницу редактора.)
  function reloadEditorPage() {
    swal( {
      type: "info",
      html: gettext( "The editor page will automatically reload for full completion." ),
      showCloseButton: true
    } ).then( ( result ) => {
      if ( result.value ) { location.reload( true ); }
    } );
  }

  // Saving and updating geo-objects.
  // (Сохранение и обновление геообъектов.)
  $( "#id_form_geoobjects" ).on( "submit", function( event ) {
    event.preventDefault();
    let $form = $( this );
    let url = $form.attr( "action" );
    let dataForm = $form.serialize();

    $.post( url, dataForm )
      .done( function( data ) {
        if ( data.length > 0 ) {
          let geoType = $( "#id_geo_type" ).val();

          $( ".djeym__balloon__content-body #id_bat_save" ).trigger( "click" );

          switch ( geoType ) {
            case "heatpoint":
              addHeatPoints( data );
              break;
            case "placemark":
              addPlacemarkTypeObjects( data );
              break;
            case "polyline":
              addPolylineTypeObjects( data );
              break;
            case "polygon":
              addPolygonTypeObjects( data );
              break;
          }
        }
      } )
      .fail( function( jqxhr, textStatus, error ) {
        errorProcessing( jqxhr, textStatus, error );
      } );
  } );

  // Tile source change.
  // (Смена источника тайлов.)
  $( ".djeym_select_tile_sources" ).on( "input", function() {
    let $this = $( this );
    let url = "/djeym/ajax-tile-source-change/";
    let dataForm = {
      csrfmiddlewaretoken: $( "input[name=\"csrfmiddlewaretoken\"" ).val(),
      map_id: window.djeymMapID,
      tile_id: $this.data( "tile-id" )
    };

    $.post( url, dataForm )
      .done( function( data ) {
        reloadEditorPage();
      } )
      .fail( function( jqxhr, textStatus, error ) {
        errorProcessing( jqxhr, textStatus, error );
      } );
  } );

  // Update selection of map controls.
  // (Обновить выбор элементов управления картой.)
  $( "#djeymMapControlsForm" ).on( "submit", function( event ) {
    event.preventDefault();
    let $form = $( this );
    let url = $form.attr( "action" );
    let dataForm = $form.serialize();
    let $btn = $form.find( "button[type=\"submit\"]" );

    startBtnLoadIndicator( $btn );

    $.post( url, dataForm )
      .done( function( data ) {
        stopBtnLoadIndicator( $btn );
        reloadEditorPage();
      } )
      .fail( function( jqxhr, textStatus, error ) {
        stopBtnLoadIndicator( $btn );
        errorProcessing( jqxhr, textStatus, error );
      } );
  } );

  // Save Heatmap settings.
  // (Сохранить настройки тепловой карты.)
  $( "#heatmapSettingsForm" ).on( "submit", function( event ) {
    event.preventDefault();
    let $form = $( this );
    let url = $form.attr( "action" );
    let dataForm = $form.serialize();
    let $btn = $form.find( "button[type=\"submit\"]" );

    startBtnLoadIndicator( $btn );

    $.post( url, dataForm )
      .done( function( data ) {
        stopBtnLoadIndicator( $btn );
      } )
      .fail( function( jqxhr, textStatus, error ) {
        stopBtnLoadIndicator( $btn );
        errorProcessing( jqxhr, textStatus, error );
      } );
  } );

  // Activate Heatmap.
  // (Активировать Тепловую карту.)
  $( "#id_djeym_activate_heatmap" ).on( "change", function( event ) {
    let url = "/djeym/ajax-activate-heatmap/";
    let heatmap = $( this ).is( ":checked" );
    let dataForm = {
      csrfmiddlewaretoken: $( "input[name=\"csrfmiddlewaretoken\"" ).val(),
      mapID: window.djeymMapID,
      heatmap: heatmap ? "True" : "False"
    };

    $.post( url, dataForm )
      .done( function( data ) {
        reloadEditorPage();
      } )
      .fail( function( jqxhr, textStatus, error ) {
        errorProcessing( jqxhr, textStatus, error );
      } );
  } );

  // Heatmap, reset to default settings.
  // (Тепловая карта, сброс к настройкам по умолчанию.)
  $( "#id_djeym_heatmap_undo_settings" ).on( "click", function( event ) {
    event.stopPropagation();

    let url = "/djeym/ajax-heatmap-undo-settings/";
    let dataForm = {
      csrfmiddlewaretoken: $( "input[name=\"csrfmiddlewaretoken\"" ).val(),
      map_id: window.djeymMapID
    };

    swal( {
      type: "info",
      html: gettext( "Confirm reset to default settings!" ),
      showCloseButton: true,
      showCancelButton: true
    } ).then( ( result ) => {
      if ( result.value ) {
        $.post( url, dataForm )
          .done( function( data ) {
            globalHeatmap.options.set( {
              radius: data.radius,
              dissipating: data.dissipating,
              opacity: data.opacity,
              intensityOfMidpoint: data.intensityOfMidpoint,
              gradient: {
                0.1: data.gradient_color1,
                0.2: data.gradient_color2,
                0.7: data.gradient_color3,
                1.0: data.gradient_color4
              } } );

            let $gradientColor1 = $( "#id_djeym_heatmap_gradient_color1" );
            let $gradientColor2 = $( "#id_djeym_heatmap_gradient_color2" );
            let $gradientColor3 = $( "#id_djeym_heatmap_gradient_color3" );
            let $gradientColor4 = $( "#id_djeym_heatmap_gradient_color4" );

            $gradientColor1.parent().find( ".colorPicker-picker" ).remove();
            $gradientColor1.val( data.gradient_color1 );
            $gradientColor1.colorPicker();

            $gradientColor2.parent().find( ".colorPicker-picker" ).remove();
            $gradientColor2.val( data.gradient_color2 );
            $gradientColor2.colorPicker();

            $gradientColor3.parent().find( ".colorPicker-picker" ).remove();
            $gradientColor3.val( data.gradient_color3 );
            $gradientColor3.colorPicker();

            $gradientColor4.parent().find( ".colorPicker-picker" ).remove();
            $gradientColor4.val( data.gradient_color4 );
            $gradientColor4.colorPicker();

            $( "#id_djeym_heatmap_radius" ).val( data.radius ).trigger( "input" );
            $( "#id_djeym_heatmap_opacity" ).val( data.opacity ).trigger( "input" );
            $( "#id_djeym_heatmap_intensity" ).val( data.intensityOfMidpoint ).trigger( "input" );

            if ( $( "#id_djeym_heatmap_dissipating" ).is( ":checked" ) ) {
              $( "#id_djeym_heatmap_dissipating" ).parent().parent().trigger( "click" );
            }
          } )
          .fail( function( jqxhr, textStatus, error ) {
            errorProcessing( jqxhr, textStatus, error );
          } );
      }
    } );
  } );

  // Update Preset settings.
  // (Обновить настройки Пресета.)
  $( document ).on( "submit", ".djeym_update_preset_settings_form", function( event ) {
    event.preventDefault();
    let $form = $( this );
    let url = $form.attr( "action" );
    let dataForm = $form.serialize();
    let $btn = $form.find( "button[type=\"submit\"]" );

    startBtnLoadIndicator( $btn );

    $.post( url, dataForm )
      .done( function( data ) {
        setTimeout( function() {
          $( ".boxios-checkbox_preset" ).off( "change" );
          $( "#id_djeym_presets" ).html( data.html );
          $( ".boxios-checkbox_preset" ).boxiosCheckbox( { size: "small" } );

          // Corrections for Firefox.
          if ( navigator.userAgent.toLowerCase().indexOf( "firefox" ) > -1 ) {
            $( ".djeym-button" ).css( "padding", "3px 20px" );
          }
          djeymAccordion();
        }, 1000 );
      } )
      .fail( function( jqxhr, textStatus, error ) {
        stopBtnLoadIndicator( $btn );
        errorProcessing( jqxhr, textStatus, error );
      } );
  } );

  // Update General Settings.
  // (Обновить общие настройки.)
  $( "#djeymGeneralSettingsForm" ).on( "submit", function( event ) {
    event.preventDefault();
    let $form = $( this );
    let url = $form.attr( "action" );
    let dataForm = $form.serialize();
    let $btn = $form.find( "button[type=\"submit\"]" );

    startBtnLoadIndicator( $btn );

    $.post( url, dataForm )
      .done( function( data ) {
        stopBtnLoadIndicator( $btn );
        reloadEditorPage();
      } )
      .fail( function( jqxhr, textStatus, error ) {
        stopBtnLoadIndicator( $btn );
        errorProcessing( jqxhr, textStatus, error );
      } );
  } );

  // Change the download indicator.
  // (Изменить индикатор загрузки.)
  $( "#id_djeym_button_change_load_indicator" ).on( "click", function( event ) {
    event.stopPropagation();
    let $btn = $( this );
    let slug = $( ".boxios-radio-load_indicator:checked" ).val();
    let size = $( ".boxios-radio-load_indicator_size:checked" ).val();
    let speed = $( "#id_djeym_animation_speed" ).val();
    let animation = $( ".boxios-checkbox_disable_loading_indicator_animation" ).prop( "checked" );
    let url = "/djeym/ajax-load-indicator-change/";
    let dataForm = {
      csrfmiddlewaretoken: $( "input[name=\"csrfmiddlewaretoken\"" ).val(),
      map_id: window.djeymMapID,
      slug: slug,
      size: size,
      speed: speed,
      animation: animation ? "True" : "False"
    };

    startBtnLoadIndicator( $btn );

    $.post( url, dataForm )
      .done( function( data ) {
        stopBtnLoadIndicator( $btn );
        reloadEditorPage();
      } )
      .fail( function( jqxhr, textStatus, error ) {
        stopBtnLoadIndicator( $btn );
        errorProcessing( jqxhr, textStatus, error );
      } );
  } );

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

    function panelActivation() {
      $( ".djeym_content_matrix_icons" ).show( "fast", function() {
        let $lastRow = $( "#id_djeym_matrix_icons tr" ).eq( -1 );
        if ( $lastRow.find( "td" ).length === 0 ) {
          $lastRow.remove();
        }
      } );

      // boxiOS - Filters by categories
      $( ".djeym_content_category" ).show( "fast", function() {
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
      } );

      $( ".djeym_content_tile_sources" ).show( "fast", function() {
        $( ".djeym_select_tile_sources" ).boxiosRadio( { size: GLOBAL_BOXIOS_SIZE } );
      } );

      $( ".djeym_content_map_controls" ).show( "fast", function() {
        $( ".boxios-checkbox_map_controls" ).boxiosRadio( { size: GLOBAL_BOXIOS_SIZE } );
        $( ".boxios-radio_cluster_balloon_layout" ).boxiosRadio( { size: "small" } );
        $( ".djeym-general-settings-color" ).colorPicker();
      } );

      $( ".djeym_content_heatmap" ).show( "fast", function() {
        $( ".djeym_heatmap_gradient_color" ).colorPicker();
        $( ".boxios-checkbox_heatmap" ).boxiosRadio( { size: GLOBAL_BOXIOS_SIZE } );
        $( "#id_djeym_heatmap_opacity, #id_djeym_heatmap_intensity, #id_djeym_heatmap_radius" )
          .boxiosRange();
      } );

      $( ".djeym_content_about" ).show();

      $( ".djeym_content_presets" ).show( "fast", function() {
        $( ".boxios-checkbox_preset" ).boxiosCheckbox( { size: "small" } );
        djeymAccordion();
      } );

      $( ".djeym_content_load_indicators" ).show( "fast", function() {
        $( ".boxios-radio-load_indicator, .boxios-checkbox_disable_loading_indicator_animation" )
          .boxiosRadio( { size: GLOBAL_BOXIOS_SIZE } );
        $( ".boxios-radio-load_indicator_size" ).boxiosRadio( { size: "small" } );
        $( "#id_djeym_animation_speed" ).boxiosRange();
      } );

      // Load image for help
      // (Загрузить изображение для справки)
      globalImageOfHelp = new Image().src = "/static/djeym/img/help.png";

      // Corrections for Firefox.
      if ( navigator.userAgent.toLowerCase().indexOf( "firefox" ) > -1 ) { //
        // $( ".legend_btn_style, .boxios-ios-label-text" ).css( "font-size", "12px" );
        $( ".djeym-button" ).css( "padding", "3px 20px" );

        // $( ".djeym-button > div" ).css( { fontSize: "12px", fontWeight: 600 } );
        globalMinHeightContextMenu += 40;
      }

      // Open the panel. (Открыть панель.)
      setTimeout( function() {
        let sidenav = document.getElementById( "id_djeym_sidenav" );

        if ( sidenav.style.left !== "0" ) {
          sidenav.style.left = "0";
        }
      }, 500 );

      // Add button «Show Panel» on map.
      // (Добавить кнопку «Показать панель» на карте.)
      setTimeout( function() {
        Map.controls.add( globalButtonShowPanel, { position: { left: "10px", top: "59px" } } );
      }, 1000 );
    }
  }, 3000 );
}
