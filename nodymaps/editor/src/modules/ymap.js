/*
 * The module for working with the map.
 */

import i18n from "@/locales/i18n.js";

export default {
  namespaced: true,
  state: {
    Map: null,
    mapID: window.djeymMapID,
    mapCenter: [0, 0],
    mapZoom: 0,
    cluster: [],
    globalHeatmap: null,
    globalHeatPoints: null,
    globalObjMngPlacemark: null,
    globalObjMngPolyline: null,
    globalObjMngPolygon: null,
    editableGeoObject: null, // Current editable Geo Object.
  },
  getters: {},
  mutations: {
    // Set Map.
    setMap(state, obj) {
      state.Map = obj;
    },
    // Refresh current editable Geo Object.
    setEditableGeoObject(state, obj) {
      state.editableGeoObject = obj;
    },
  },
  actions: {
    // Ajax -  Set settings.
    actionSetFromAjax({ state }, payload) {
      state.mapCenter = payload.mapCenter;
      state.mapZoom = payload.mapZoom;
      state.cluster = payload.cluster;
    },
    // Add Placemarks to manager.
    addPlacemarkTypeObjects({ state }, geoObjects) {
      state.globalObjMngPlacemark.add({
        type: "FeatureCollection",
        features: geoObjects,
      });
    },
    // Add Heat Points to manager.
    addHeatPoints({ state, rootState }, geoObjects) {
      if (rootState.heatmap.controls.panel1.isActive) {
        state.globalHeatPoints.features.push(geoObjects);
        state.globalHeatmap.setData(state.globalHeatPoints);
      }
    },
    // Add Polylines to manager.
    addPolylineTypeObjects({ state }, geoObjects) {
      state.globalObjMngPolyline.add({
        type: "FeatureCollection",
        features: geoObjects,
      });
    },
    // Add Polygons to manager.
    addPolygonTypeObjects({ state }, geoObjects) {
      state.globalObjMngPolygon.add({
        type: "FeatureCollection",
        features: geoObjects,
      });
    },
    // Find current  editable Geo-object.
    findEditableGeoObject({ state, commit }) {
      if (state.editableGeoObject !== null) {
        state.Map.setBounds(state.editableGeoObject.geometry.getBounds(), {
          duration: 1000,
          zoomMargin: 2,
        }).then(
          () => {
            if (state.editableGeoObject.geometry.getType() === "Point") {
              let maxZoom = state.Map.options.get("maxZoom");
              maxZoom = maxZoom > 16 ? 16 : maxZoom;
              state.Map.setZoom(maxZoom, {
                duration: 1000,
              });
            }
          },
          () => {
            // If failed to show the specified region.
            commit("modals/alertSnackbarShow", i18n.t("message.129"), {
              root: true,
            });
          },
          this,
        );
      }
    },
    // Create a map.
    createYMap({ state, commit, dispatch, rootState }) {
      let Map;

      const mapControls = rootState.mapControls;
      const isSearchByOrganization = mapControls.controls[2].isActive;
      const isTypeSelector =
        mapControls.activeControls.includes("typeSelector");
      const activeControls = mapControls.activeControls.filter(
        (title) => title !== "typeSelector",
      );

      const generalSettings = rootState.generalSettings;
      const isRoundTheme = generalSettings.controls.panel1_69[0].isActive;

      const currentTile = rootState.tileSources.currentTile;
      const randomTileUrl =
        currentTile !== null
          ? // eslint-disable-next-line no-new-func
            new Function("return " + currentTile.randomTileUrl)
          : null;

      const heatmapControls = rootState.heatmap.controls;

      // UPLOAD INDICATOR --------------------------------------------------------------------------
      let spinTimers = [];
      function waitLoadContent() {
        // wait upload content to Balloon
        spinTimers[3] = setTimeout(() => {
          const loadIndicator = document.getElementById("djeymLoadIndicator");

          if (loadIndicator === null) {
            return;
          }

          loadIndicator.style.display = "block";

          const $images = window.$(
            "ymaps:regex(class, .*-balloon__content) img",
          );
          let imgLoaded = false;
          let counter = 0;

          if ($images.length === 0) {
            imgLoaded = true;
          } else {
            $images.each((idx, elem) => {
              if (elem.complete) {
                counter++;
              }
            });
            if (counter === $images.length) {
              imgLoaded = true;
            }
          }

          if (!imgLoaded) {
            spinTimers[2] = setTimeout(() => {
              waitLoadContent();
            }, 100);
          } else {
            window.$(".djeymUpdateInfoPreset").each((idx, elem) => {
              window.$(elem).trigger("click");
            });
            const modalLock = document.getElementById("djeymModalLock");
            if (modalLock !== null) {
              spinTimers[1] = setTimeout(() => {
                spinTimers[0] = setTimeout(() => {
                  modalLock.remove();
                }, 600);
                modalLock.style.opacity = 0;
              }, 200);
            }
          }
        }, 500);
      }

      // CUSTOM LAYOUTS ----------------------------------------------------------------------------
      // Custom layout for Balloon.
      const customBalloonContentLayout =
        window.djeymYMaps.templateLayoutFactory.createClass(
          '<div class="djeym-pos-relative djeym-fill-hight">' +
            '<div id="djeymModalLock"><div id="djeymLoadIndicator"></div></div>' +
            '<div class="djeym_ballon_header">{{ properties.balloonContentHeader|raw }}</div>' +
            '<div class="djeym_ballon_body">{{ properties.balloonContentBody|raw }}</div>' +
            '<div class="djeym_ballon_footer">{{ properties.balloonContentFooter|raw }}</div></div>',
        );
      // Custom Balloon layout for editable.
      const customBalloonContentLayoutForEditable =
        window.djeymYMaps.templateLayoutFactory.createClass(
          '<div class="red--text text--darken-2 mb-3">' +
            '<span class="mdi mdi-tooltip-edit mdi-24px"></span>' +
            '<span class="subtitle-1 ml-1" style="position:relative;top:-4px;">' +
            i18n.t("message.108") +
            "</span></div>" +
            '<div class="djeym_ballon_header">{{ properties.balloonContentHeader|raw }}</div>' +
            '<div class="djeym_ballon_body">{{ properties.balloonContentBody|raw }}</div>' +
            '<div class="djeym_ballon_footer">{{ properties.balloonContentFooter|raw }}</div>',
        );
      // Custom layout for icon of Cluster.
      const customLayoutForClusterIcon =
        window.djeymYMaps.templateLayoutFactory.createClass(
          '<div class="djeym_layout_cluster_icon"><span style="background-color:' +
            generalSettings.colorBackgroundCountObjects +
            ";color:" +
            generalSettings.textColorCountObjects +
            ';">$[properties.geoObjects.length]</span></div>',
        );

      // CREATE A MAP ------------------------------------------------------------------------------
      Map = new window.djeymYMaps.Map(
        "djeymYMapsID",
        {
          center: state.mapCenter,
          zoom: state.mapZoom,
          type: null,
          controls: isRoundTheme ? [] : activeControls,
        },
        {
          minZoom: currentTile !== null ? currentTile.minZoom : 0,
          maxZoom: currentTile !== null ? currentTile.maxZoom : 23,
          geoObjectHasBalloon: true,
          hasHint: false,
          geoObjectBalloonMinWidth: 322,
          geoObjectBalloonMaxWidth: 342,
          geoObjectBalloonMinHeight: window.djeymBalloonMinHeight,
          geoObjectBalloonPanelMaxMapArea: 0,
          geoObjectOpenBalloonOnClick: true,
          geoObjectBalloonContentLayout: customBalloonContentLayoutForEditable,
        },
      );
      Map.cursors.push("arrow");
      commit("setMap", Map);

      // Add map types.
      if (isTypeSelector) {
        // Add map types to TypeSelector.
        let typeSelector;
        if (isRoundTheme) {
          typeSelector = new window.djeymYMaps.control.TypeSelector({
            options: {
              layout: "round#listBoxLayout",
              size: "small",
              float: "none",
              position: {
                bottom: "40px",
                left: "10px",
              },
            },
          });
        } else {
          typeSelector = new window.djeymYMaps.control.TypeSelector();
          typeSelector.options.set(
            "panoramasItemMode",
            generalSettings.controls.panel1_69[1].isActive
              ? "ifMercator"
              : "off",
          );
        }
        typeSelector.addMapType("yandex#map", 2);
        typeSelector.addMapType("yandex#satellite", 3);
        typeSelector.addMapType("yandex#hybrid", 4);
        // Create a map type for the current tile.
        if (currentTile !== null) {
          let currentTilLayer = function () {
            let layer = new window.djeymYMaps.Layer(randomTileUrl(), {
              projection: window.djeymYMaps.projection.sphericalMercator,
            });
            // Copyright.
            layer.getCopyrights = function () {
              return window.djeymYMaps.vow.resolve(currentTile.copyrights);
            };
            // The range of available sizes.
            layer.getZoomRange = function () {
              return window.djeymYMaps.vow.resolve([
                currentTile.minZoom,
                currentTile.maxZoom,
              ]);
            };
            return layer;
          };
          // Add a layer to the storage.
          window.djeymYMaps.layer.storage.add("tile#aerial", currentTilLayer);
          // Create map types.
          let currentTilMapType = new window.djeymYMaps.MapType(
            currentTile.title,
            ["tile#aerial"],
          );
          // Add map types in storage.
          window.djeymYMaps.mapType.storage.add(
            "tile#current",
            currentTilMapType,
          );
          typeSelector.addMapType("tile#current", 1);
          // Use custom current map type.
          Map.controls.add(typeSelector);
          Map.setType("tile#current", { checkZoomRange: true });
        } else {
          // Use default map type.
          Map.controls.add(typeSelector);
          Map.setType("yandex#map");
        }
      } else {
        if (currentTile !== null) {
          // Connect a third-party source of tiles.
          Map.layers.add(
            new window.djeymYMaps.Layer(randomTileUrl(), {
              projection: window.djeymYMaps.projection.sphericalMercator,
            }),
          );
          // Add Copyrights.
          Map.copyrights.add(currentTile.copyrights);
        } else {
          // Use default map type.
          Map.setType("yandex#map");
        }
      }

      // Use round theme for controls.
      if (isRoundTheme) {
        if (activeControls.includes("geolocationControl")) {
          let geolocationControl =
            new window.djeymYMaps.control.GeolocationControl({
              options: {
                layout: "round#buttonLayout",
                floatIndex: 4,
                size: "small",
              },
            });
          Map.controls.add(geolocationControl);
        }
        if (activeControls.includes("routeButtonControl")) {
          let customRouteButton = new window.djeymYMaps.control.Button({
            data: {
              iconType: "routes",
            },
            options: {
              layout: "round#buttonLayout",
              floatIndex: 2,
              size: "small",
            },
          });
          Map.controls.add(customRouteButton);
          Map.controls.add("routePanelControl", {
            visible: false,
            showHeader: true,
            floatIndex: 1,
            float: "left",
            top: "auto",
            right: "auto",
            bottom: "auto",
            left: "auto",
          });
          let routePanelControl = Map.controls.get("routePanelControl");
          customRouteButton.events.add("press", () => {
            if (routePanelControl.options.get("visible")) {
              routePanelControl.options.set("visible", false);
              routePanelControl.routePanel.state.set("fromEnabled", false);
            } else {
              routePanelControl.options.set("visible", true);
              routePanelControl.routePanel.state.set("fromEnabled", true);
            }
          });
        }
        if (activeControls.includes("searchControl")) {
          let searchControl = new window.djeymYMaps.control.SearchControl({
            options: {
              size: "small",
              float: "none",
              position: {
                top: -40,
              },
            },
          });
          let customSearchControl = new window.djeymYMaps.control.Button({
            data: {
              iconType: "loupe",
            },
            options: {
              layout: "round#buttonLayout",
              size: "small",
              floatIndex: 3,
              selectOnClick: false,
              float: "left",
            },
          });
          customSearchControl.events.add("press", () => {
            window
              .$(
                "ymaps:regex(class, ymaps-.+-float-button-icon_icon_magnifier)",
              )
              .trigger("click");
          });
          Map.controls.add(searchControl);
          Map.controls.add(customSearchControl);
        }
        if (activeControls.includes("trafficControl")) {
          let trafficControl = new window.djeymYMaps.control.TrafficControl({
            options: {
              visible: false,
            },
          });

          let customTrafficControl = new window.djeymYMaps.control.Button({
            data: {
              iconType: "traffic",
            },
            options: {
              layout: "round#buttonLayout",
              floatIndex: 1,
              size: "small",
              float: "right",
            },
          });
          customTrafficControl.events.add("press", () => {
            if (trafficControl.isTrafficShown()) {
              trafficControl.hideTraffic();
            } else {
              trafficControl.showTraffic();
            }
          });
          Map.controls.add(trafficControl);
          Map.controls.add(customTrafficControl);
        }
        if (activeControls.includes("fullscreenControl")) {
          let fullscreenControl =
            new window.djeymYMaps.control.FullscreenControl({
              data: {
                iconType: "expand",
              },
              options: {
                layout: "round#buttonLayout",
                size: "small",
                floatIndex: 2,
                selectOnClick: false,
              },
            });
          fullscreenControl.events.add("press", () => {
            if (!fullscreenControl.isSelected()) {
              Map.container.enterFullscreen();
            } else {
              Map.container.exitFullscreen();
            }
          });
          Map.container.events.add("fullscreenenter", () => {
            fullscreenControl.data.set({ iconType: "collapse" });
            fullscreenControl.select();
          });
          Map.container.events.add("fullscreenexit", () => {
            fullscreenControl.data.set({ iconType: "expand" });
            fullscreenControl.deselect();
          });
          Map.controls.add(fullscreenControl);
        }
        if (activeControls.includes("zoomControl")) {
          let zoomControl = new window.djeymYMaps.control.ZoomControl({
            options: {
              layout: "round#zoomLayout",
              size: "small",
            },
          });
          Map.controls.add(zoomControl);
        }
        if (activeControls.includes("rulerControl")) {
          let rulerControl = new window.djeymYMaps.control.RulerControl({
            options: {
              layout: "round#rulerLayout",
              size: "small",
              position: {
                bottom: "40px",
                right: "10px",
              },
            },
          });
          Map.controls.add(rulerControl);
        }
      } else {
        // Enable search by organization.
        if (
          activeControls.includes("searchControl") &&
          isSearchByOrganization
        ) {
          Map.controls
            .get("searchControl")
            .options.set("provider", "yandex#search");
        }
      }

      // Set up a heatmap.
      if (heatmapControls.panel1.isActive) {
        window.djeymYMaps.modules.require(["Heatmap"], (Heatmap) => {
          state.globalHeatPoints = {
            type: "FeatureCollection",
            features: [],
          };
          state.globalHeatmap = new Heatmap(state.globalHeatPoints, {
            radius: heatmapControls.panel2.radius,
            dissipating: heatmapControls.panel2.dissipating,
            opacity: heatmapControls.panel2.opacity,
            intensityOfMidpoint: heatmapControls.panel2.intensity,
            gradient: {
              0.1: heatmapControls.panel2.gradient.color1,
              0.2: heatmapControls.panel2.gradient.color2,
              0.7: heatmapControls.panel2.gradient.color3,
              1.0: heatmapControls.panel2.gradient.color4,
            },
          });
          state.globalHeatmap.setMap(Map);
        });
      }

      // ADD EVENTS TO THE MAP ---------------------------------------------------------------------
      // Open Balloon - Run Preset
      Map.events.add("balloonopen", () => {
        for (let idx = 0, len = spinTimers.length; idx < len; idx++) {
          clearTimeout(spinTimers[idx]);
        }
        waitLoadContent();
      });
      // Restart Preset
      window
        .$(document)
        .on(
          "click",
          "ymaps:regex(class, .*-cluster-tabs__menu-item.*), " +
            "ymaps:regex(class, .*-cluster-carousel__pager-item.*), " +
            "ymaps:regex(class, .*-cluster-carousel__nav.*)",
          (event) => {
            event.stopPropagation();
            for (let idx = 0, len = spinTimers.length; idx < len; idx++) {
              clearTimeout(spinTimers[idx]);
            }
            waitLoadContent();
          },
        );

      // Menu popup - Select geo-type and create new object.
      Map.events.add("click", (mapEvent) => {
        const coords = mapEvent.get("coords");
        Map.balloon.close();
        /* Cancel the action if the map has an editable geo object.
           (Отменяем действие, если на карте редактируемый геообъект.) */
        if (state.editableGeoObject !== null) {
          commit(
            "modals/messageDialogShow",
            {
              status: "accent",
              title: i18n.t("message.85"),
              text: i18n.t("message.41"),
              cancelBtn: true,
              okBtn: false,
              actionBtnCancel: () => {
                commit("modals/messageDialogClose", null, { root: true });
              },
              actionBtnOk: null,
            },
            { root: true },
          );
          return;
        }
        commit("dialogCreate/setLatitude", coords[0], { root: true });
        commit("dialogCreate/setLongitude", coords[1], { root: true });
        commit(
          "modals/controlsDialogShow",
          {
            title: i18n.t("message.93"),
            text: "",
            cancelBtn: true,
            saveBtn: false,
            componentMenu: true,
            actionBtnSave: null,
            actionBtnCancel: () => {
              commit("modals/controlsDialogClose", null, { root: true });
            },
          },
          { root: true },
        );
      });

      // CREATE MANAGERS GEO OBJECTS ---------------------------------------------------------------
      const geoObjectBalloonOptions = {
        geoObjectHasBalloon: true,
        geoObjectHasHint: false,
        geoObjectBalloonMinWidth: 322,
        geoObjectBalloonMaxWidth: 342,
        geoObjectBalloonMinHeight: window.djeymBalloonMinHeight,
        geoObjectBalloonPanelMaxMapArea: 0,
        geoObjectBalloonContentLayout: customBalloonContentLayout,
        geoObjectOpenBalloonOnClick: false,
      };

      const clusterRadius = parseInt(
        Math.min.apply(null, state.cluster.size) / 2,
      );
      const objMngPlacemarkOptions = {
        clusterize: generalSettings.controls.panel2_70[0].isActive,
        clusterHasBalloon: true,
        clusterHasHint: false,
        clusterIconContentLayout: generalSettings.controls.panel1_69[3].isActive
          ? customLayoutForClusterIcon
          : null,
        clusterBalloonItemContentLayout: customBalloonContentLayout,
        clusterDisableClickZoom: true,
        clusterOpenBalloonOnClick: false,
        showInAlphabeticalOrder: false,
        clusterBalloonPanelMaxMapArea: 0,
        clusterMaxZoom: Map.options.get("maxZoom"),
        gridSize: 128,
        margin: clusterRadius + 2,
        clusterBalloonContentLayout:
          generalSettings.controls.panel1_69[2].layout,
        clusterIcons: [
          {
            href: state.cluster.url,
            size: state.cluster.size,
            offset: state.cluster.offset,
            shape: {
              type: "Circle",
              coordinates: [0, 0],
              radius: clusterRadius,
            },
          },
        ],
      };

      Object.assign(objMngPlacemarkOptions, geoObjectBalloonOptions);

      // Create a manager for Placemarks.
      state.globalObjMngPlacemark = new window.djeymYMaps.ObjectManager(
        objMngPlacemarkOptions,
      );

      // Create a manager for Polylines.
      state.globalObjMngPolyline = new window.djeymYMaps.ObjectManager(
        geoObjectBalloonOptions,
      );

      // Create a manager for Polygons.
      state.globalObjMngPolygon = new window.djeymYMaps.ObjectManager(
        geoObjectBalloonOptions,
      );

      // Clear content of geo-object.
      const clearContentGeoObject = (geoObject) => {
        geoObject.properties.balloonContentHeader = "";
        geoObject.properties.balloonContentBody = "";
        geoObject.properties.balloonContentFooter = "";
        return geoObject;
      };

      // Ajax, uploading content for Cluster (balloonContent) - Header, Body and Footer.
      state.globalObjMngPlacemark.clusters.events.add("click", (event) => {
        Map.balloon.close(true);

        const objectId = event.get("objectId");
        const cluster = state.globalObjMngPlacemark.clusters.getById(objectId);
        const geoObjects = cluster.properties.geoObjects;
        const countObjs = geoObjects.length;
        const ids = [];

        for (let idx = 0; idx < countObjs; idx++) {
          ids.push(geoObjects[idx].properties.id);
        }

        for (let idx = 0; idx < countObjs; idx++) {
          state.globalObjMngPlacemark.clusters.balloon.setData(
            clearContentGeoObject(geoObjects[idx]),
          );
        }

        setTimeout(() => {
          state.globalObjMngPlacemark.clusters.balloon.open(objectId);
        }, 100);

        window.$.get("/djeym/ajax-balloon-content/", {
          ids: JSON.stringify(ids),
          objType: "Point",
          isPresets: "True",
        })
          .done((data) => {
            for (let idx = 0, marker, content; idx < countObjs; idx++) {
              marker = geoObjects[idx];
              content = data[marker.properties.id];
              marker.properties.balloonContentHeader = content.header;
              marker.properties.balloonContentBody = content.body;
              marker.properties.balloonContentFooter = content.footer;
            }
            window
              .$("ymaps:regex(class, .*-cluster-tabs__menu-item.*)")
              .eq(0)
              .trigger("click");
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Uploading content for Cluster.",
              },
              { root: true },
            );
          });
      });

      // Ajax - Saving, Reloading and Deleting Geo Objects.
      const runAjaxContextMenu = (geoType, actionType) => {
        commit(
          "setDataAction",
          {
            geoType: geoType,
            actionType: actionType,
          },
          { root: true },
        );
        dispatch("ajaxContextMenu", null, { root: true });
      };

      // Messages error.
      const messageErrorAddCategory = () => {
        return (
          '<div class="djeym-fake-buttons" style="background:' +
          rootState.generalSettings.colorControlsTheme +
          ';">' +
          '<span class="mdi mdi-check-circle mdi-24px" style="color:' +
          rootState.generalSettings.colorButtonsTextTheme +
          ';"></span></div><br>' +
          i18n.t("message.105")
        );
      };
      const messageErrorAddHeader = () => {
        return (
          '<div class="djeym-fake-buttons" style="background:' +
          rootState.generalSettings.colorControlsTheme +
          ';">' +
          '<span class="mdi mdi-page-layout-header mdi-24px" style="color:' +
          rootState.generalSettings.colorButtonsTextTheme +
          ';"></span></div><br>' +
          i18n.t("message.106")
        );
      };

      // Transfering the data for geo objects from the manager to the context menu for editable.
      function transferToContextMenu(geoObject) {
        Map.balloon.close();
        /* Cancel the action if the map has an editable geo object.
          (Отменяем действие, если на карте редактируемый геообъект.) */
        if (state.editableGeoObject !== null) {
          commit(
            "modals/messageDialogShow",
            {
              status: "accent",
              title: i18n.t("message.85"),
              text: i18n.t("message.41"),
              cancelBtn: true,
              okBtn: false,
              actionBtnCancel: () => {
                commit("modals/messageDialogClose", null, { root: true });
              },
              actionBtnOk: null,
            },
            { root: true },
          );
          return;
        }

        const pk = geoObject.properties.id;
        const geoObjectType = geoObject.geometry.type;

        window.$.get("/djeym/ajax-balloon-content/", {
          objID: pk,
          objType: geoObjectType,
          isPresets: "False",
        })
          .done((data) => {
            geoObject.properties.balloonContentHeader = data.header;
            geoObject.properties.balloonContentBody = data.body;
            geoObject.properties.balloonContentFooter = data.footer;

            let properties = {
              balloonContentHeader: geoObject.properties.balloonContentHeader,
              balloonContentBody: geoObject.properties.balloonContentBody,
              balloonContentFooter: geoObject.properties.balloonContentFooter,
              id: geoObject.properties.id,
              categoryID: geoObject.properties.categoryID,
              subCategoryIDs: geoObject.properties.subCategoryIDs,
            };

            let options = { draggable: true };

            if (geoObjectType === "Point") {
              options["iconLayout"] = "default#image";
              options["iconImageHref"] = geoObject.options.iconImageHref;
              options["iconImageSize"] = geoObject.options.iconImageSize;
              options["iconImageOffset"] = geoObject.options.iconImageOffset;
              properties["iconSlug"] = geoObject.properties.iconSlug;
            } else if (
              geoObjectType === "LineString" ||
              geoObjectType === "Polygon"
            ) {
              options["strokeWidth"] = geoObject.options.strokeWidth;
              options["strokeColor"] = geoObject.options.strokeColor;
              options["strokeStyle"] = geoObject.options.strokeStyle;
              options["strokeOpacity"] = geoObject.options.strokeOpacity;
              if (geoObjectType === "Polygon") {
                options["fillColor"] = geoObject.options.fillColor;
                options["fillOpacity"] = geoObject.options.fillOpacity;
              }
            }

            const tmpObj = new window.djeymYMaps.GeoObject(
              {
                geometry: {
                  type: geoObjectType,
                  coordinates: geoObject.geometry.coordinates,
                },
                properties: properties,
              },
              options,
            );

            const globalObjMngName = {
              Point: "globalObjMngPlacemark",
              LineString: "globalObjMngPolyline",
              Polygon: "globalObjMngPolygon",
            }[geoObjectType];

            state[globalObjMngName].remove(geoObject);
            commit("setEditableGeoObject", tmpObj);
            Map.geoObjects.add(tmpObj);
            commit("setShowBtnFindEditableGeoObject", true, { root: true });

            let contextMenu = (payload) => {
              commit("setMapSettingsDrawer", false, { root: true });
              commit(
                "modals/geoObjectDialogShow",
                {
                  title: i18n.t(
                    `message.${
                      { Point: 100, LineString: 109, Polygon: 111 }[
                        payload.geoType
                      ]
                    }`,
                  ),
                  editBtn: true,
                  saveBtn: true,
                  cancelBtn: true,
                  deleteBtn: true,
                  actionBtnEdit: () =>
                    commit("modals/geoObjectDialogClose", null, { root: true }),
                  actionBtnSave: () => {
                    let errorCategory = false;
                    let errorHeader = false;
                    if (payload.geoType === "Point") {
                      errorCategory = !rootState.contextmenuPlacemark.category;
                      errorHeader =
                        rootState.contextmenuPlacemark.header.length === 0;
                    } else if (payload.geoType === "LineString") {
                      errorCategory = !rootState.contextmenuRoute.category;
                      errorHeader =
                        rootState.contextmenuRoute.header.length === 0;
                    } else if (payload.geoType === "Polygon") {
                      errorCategory = !rootState.contextmenuTerritory.category;
                      errorHeader =
                        rootState.contextmenuTerritory.header.length === 0;
                    }
                    if (errorCategory) {
                      commit(
                        "modals/alertSnackbarShow",
                        payload.messageErrorAddCategory(),
                        { root: true },
                      );
                      return;
                    }
                    if (errorHeader) {
                      commit(
                        "modals/alertSnackbarShow",
                        payload.messageErrorAddHeader(),
                        { root: true },
                      );
                      return;
                    }
                    runAjaxContextMenu(
                      {
                        Point: "placemark",
                        LineString: "polyline",
                        Polygon: "polygon",
                      }[payload.geoType],
                      "save",
                    );
                  },
                  actionBtnCancel: () => {
                    commit("modals/alertSnackbarClose", null, { root: true });
                    runAjaxContextMenu(
                      {
                        Point: "placemark",
                        LineString: "polyline",
                        Polygon: "polygon",
                      }[payload.geoType],
                      "reload",
                    );
                  },
                  actionBtnDelete: () => {
                    runAjaxContextMenu(
                      {
                        Point: "placemark",
                        LineString: "polyline",
                        Polygon: "polygon",
                      }[payload.geoType],
                      "delete",
                    );
                  },
                  componentHeatPoint: false,
                  componentPlacemark: payload.geoType === "Point",
                  componentPolyline: payload.geoType === "LineString",
                  componentPolygon: payload.geoType === "Polygon",
                },
                { root: true },
              );
            };
            tmpObj.events.add("contextmenu", () => {
              Map.balloon.close();
              contextMenu({
                geoType: geoObjectType,
                messageErrorAddCategory: messageErrorAddCategory,
                messageErrorAddHeader: messageErrorAddHeader,
              });
            });
            contextMenu({
              geoType: geoObjectType,
              messageErrorAddCategory: messageErrorAddCategory,
              messageErrorAddHeader: messageErrorAddHeader,
            });
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Transfering the data for geo objects from the manager.",
              },
              { root: true },
            );
          });
      }

      /* Ajax, uploading content for geo objects (balloonsContent) -
         Header, Body and Footer. */
      const ajaxGetBalloonContent = (geoObject) => {
        Map.balloon.close(true);
        const geoObjectType = geoObject.geometry.type;

        setTimeout(() => {
          if (geoObjectType === "Point") {
            state.globalObjMngPlacemark.objects.balloon.open(geoObject.id);
          } else if (geoObjectType === "LineString") {
            state.globalObjMngPolyline.objects.balloon.open(geoObject.id);
          } else if (geoObjectType === "Polygon") {
            state.globalObjMngPolygon.objects.balloon.open(geoObject.id);
          }
        }, 100);

        window.$.get("/djeym/ajax-balloon-content/", {
          objID: geoObject.properties.id,
          objType: geoObjectType,
          isPresets: "True",
        })
          .done((data) => {
            geoObject.properties.balloonContentHeader = data.header;
            geoObject.properties.balloonContentBody = data.body;
            geoObject.properties.balloonContentFooter = data.footer;

            if (geoObjectType === "Point") {
              state.globalObjMngPlacemark.objects.balloon.setData(geoObject);
            } else if (geoObjectType === "LineString") {
              state.globalObjMngPolyline.objects.balloon.setData(geoObject);
            } else if (geoObjectType === "Polygon") {
              state.globalObjMngPolygon.objects.balloon.setData(geoObject);
            }
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Uploading content for geo objects (balloonsContent).",
              },
              { root: true },
            );
          });
      };

      // Transferring geo object from manager to map for editing.
      state.globalObjMngPlacemark.objects.events.add("contextmenu", (event) => {
        commit("setMapSettingsDrawer", false, { root: true });
        const objectId = event.get("objectId");
        const geoObject = state.globalObjMngPlacemark.objects.getById(objectId);
        transferToContextMenu(geoObject);
      });
      state.globalObjMngPolyline.objects.events.add("contextmenu", (event) => {
        commit("setMapSettingsDrawer", false, { root: true });
        const objectId = event.get("objectId");
        const geoObject = state.globalObjMngPolyline.objects.getById(objectId);
        transferToContextMenu(geoObject);
      });
      state.globalObjMngPolygon.objects.events.add("contextmenu", (event) => {
        commit("setMapSettingsDrawer", false, { root: true });
        const objectId = event.get("objectId");
        const geoObject = state.globalObjMngPolygon.objects.getById(objectId);
        transferToContextMenu(geoObject);
      });

      // Ajax, uploading content for "balloonContent" - Header, Body and Footer.
      state.globalObjMngPlacemark.objects.events.add("click", (event) => {
        const objectId = event.get("objectId");
        let geoObject = state.globalObjMngPlacemark.objects.getById(objectId);
        geoObject = clearContentGeoObject(geoObject);
        ajaxGetBalloonContent(geoObject);
      });
      state.globalObjMngPolyline.objects.events.add("click", (event) => {
        const objectId = event.get("objectId");
        let geoObject = state.globalObjMngPolyline.objects.getById(objectId);
        geoObject = clearContentGeoObject(geoObject);
        ajaxGetBalloonContent(geoObject);
      });
      state.globalObjMngPolygon.objects.events.add("click", (event) => {
        const objectId = event.get("objectId");
        let geoObject = state.globalObjMngPolygon.objects.getById(objectId);
        geoObject = clearContentGeoObject(geoObject);
        ajaxGetBalloonContent(geoObject);
      });

      // Add object manager to map.
      Map.geoObjects.add(state.globalObjMngPlacemark);
      Map.geoObjects.add(state.globalObjMngPolyline);
      Map.geoObjects.add(state.globalObjMngPolygon);

      // Run filtering by categories.
      dispatch("categoryFilters/refreshVisibilityGeoObjects", null, {
        root: true,
      });

      // AJAX - LOADING GEO OBJECTS TO MAP ---------------------------------------------------------
      // Upload Placemarks.
      const loadPlacemarkGeoObjects = (offset) => {
        window.$.getJSON("/djeym/ajax-upload-placemarks/", {
          mapID: window.djeymMapID,
          offset: offset,
        })
          .done((data) => {
            setTimeout(() => {
              if (data.length > 0) {
                dispatch("addPlacemarkTypeObjects", data);
                offset += 1000;
                loadPlacemarkGeoObjects(offset);
              } else {
                setTimeout(() => loadHeatPoints(0), 0);
              }
            }, 0);
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Load Placemarks.",
              },
              { root: true },
            );
          });
      };
      loadPlacemarkGeoObjects(0);

      // Upload Heat Points.
      const loadHeatPoints = (offset) => {
        window.$.getJSON("/djeym/ajax-upload-heat-points/", {
          mapID: window.djeymMapID,
          offset: offset,
        })
          .done((data) => {
            setTimeout(() => {
              if (data.length > 0) {
                dispatch("addHeatPoints", data);
                offset += 1000;
                loadHeatPoints(offset);
              } else {
                setTimeout(() => loadPolylineGeoObjects(0), 0);
              }
            }, 0);
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Loading Thermal points.",
              },
              { root: true },
            );
          });
      };

      // Upload Polylines.
      const loadPolylineGeoObjects = (offset) => {
        window.$.getJSON("/djeym/ajax-upload-polylines/", {
          mapID: window.djeymMapID,
          offset: offset,
        })
          .done((data) => {
            setTimeout(() => {
              if (data.length > 0) {
                dispatch("addPolylineTypeObjects", data);
                offset += 500;
                loadPolylineGeoObjects(offset);
              } else {
                setTimeout(() => loadPolygonGeoObjects(0), 0);
              }
            }, 0);
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Load Polylines.",
              },
              { root: true },
            );
          });
      };

      // Upload Polygons.
      const loadPolygonGeoObjects = (offset) => {
        window.$.getJSON("/djeym/ajax-upload-polygons/", {
          mapID: window.djeymMapID,
          offset: offset,
        })
          .done((data) => {
            setTimeout(() => {
              if (data.length > 0) {
                dispatch("addPolygonTypeObjects", data);
                offset += 500;
                loadPolygonGeoObjects(offset);
              } else {
                setTimeout(() => {
                  commit("enableShowAllSettings", null, { root: true });
                  // commit('setMapSettingsDrawer', true, { root: true })
                }, 0);
              }
            }, 0);
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Load Polygons.",
              },
              { root: true },
            );
          });
      };
    },
  },
};
