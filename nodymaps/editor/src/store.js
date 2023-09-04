import Vue from "vue";
import Vuex from "vuex";
import Modals from "@/modules/modals.js";
import CategoryFilters from "@/modules/category_filters.js";
import GeneralSettings from "@/modules/general_settings.js";
import TileSources from "@/modules/tile_sources.js";
import MapControls from "@/modules/map_controls.js";
import Heatmap from "@/modules/heatmap.js";
import LoadIndicators from "@/modules/load_indicators.js";
import Presets from "@/modules/presets.js";
import Help from "@/modules/help.js";
import YMap from "@/modules/ymap.js";
import DialogCreate from "@/modules/dialog_create.js";
import SelectingCategories from "@/modules/selecting_categories.js";
import ContextmenuHeatPoint from "@/modules/сontextmenu_heat_point.js";
import ContextmenuPlacemark from "@/modules/сontextmenu_placemark.js";
import ContextmenuRoute from "@/modules/сontextmenu_route.js";
import ContextmenuTerritory from "@/modules/contextmenu_territory.js";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    modals: Modals,
    categoryFilters: CategoryFilters,
    generalSettings: GeneralSettings,
    tileSources: TileSources,
    mapControls: MapControls,
    heatmap: Heatmap,
    loadIndicators: LoadIndicators,
    presets: Presets,
    help: Help,
    ymap: YMap,
    dialogCreate: DialogCreate,
    selectingCategories: SelectingCategories,
    contextmenuHeatPoint: ContextmenuHeatPoint,
    contextmenuPlacemark: ContextmenuPlacemark,
    contextmenuRoute: ContextmenuRoute,
    contextmenuTerritory: ContextmenuTerritory,
  },
  state: {
    enableAjax: true,
    showAllSettings: false,
    showBtnFindEditableGeoObject: false,
    // Icon Collection
    iconCollection: [],
    // Panel for Map Settings
    mapSettingsDrawer: false, // Open/Close
    widthPanelSettings: 380,
    // Current cropped image.
    currentImageCrop: null,
    // Data for actions
    dataAction: {},
  },
  getters: {},
  mutations: {
    enableShowAllSettings(state) {
      state.showAllSettings = true;
    },
    setShowBtnFindEditableGeoObject(state, flag) {
      state.showBtnFindEditableGeoObject = flag;
    },
    setIconCollection(state, arr) {
      state.iconCollection = arr;
    },
    setMapSettingsDrawer(state, flag) {
      state.mapSettingsDrawer = flag;
    },
    setWidthPanelSettings(state, value) {
      state.widthPanelSettings = value;
    },
    setCurrentImageCrop(state, img) {
      state.currentImageCrop = img;
    },
    setDataAction(state, payload) {
      state.dataAction = payload;
    },
  },
  actions: {
    // Ajax - Upload of Settings.
    ajaxUploadSettings({ state, commit, dispatch }) {
      if (state.enableAjax) {
        window.$.getJSON("/djeym/ajax-upload-settings-editor/", {
          mapID: window.djeymMapID,
        })
          .done((data) => {
            state.widthPanelSettings =
              data.generalSettings.controls.panel2_70[1].widthPanelEditor;
            dispatch("categoryFilters/actionSetFromAjax", data.categories, {
              root: true,
            });
            commit("tileSources/setFromAjax", data.tileSources, { root: true });
            dispatch(
              "generalSettings/actionSetFromAjax",
              data.generalSettings,
              { root: true },
            );
            dispatch("mapControls/actionSetFromAjax", data.mapControls, {
              root: true,
            });
            dispatch("heatmap/actionSetFromAjax", data.heatmapSettings, {
              root: true,
            });
            dispatch("loadIndicators/actionSetFromAjax", data.loadIndicators, {
              root: true,
            });
            dispatch("presets/actionSetFromAjax", data.presets, { root: true });
            commit("setIconCollection", data.iconCollection);
            dispatch("ymap/actionSetFromAjax", data.ymap, { root: true });
            dispatch("ymap/createYMap", null, { root: true });
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Upload all settings.",
              },
              { root: true },
            );
          });
      }
    },
    // Ajax - To save and update and delete geo objects.
    ajaxContextMenu({ state, commit, dispatch, rootState }) {
      commit("modals/globalProgressBarShow", true, { root: true });

      const dataGeoObj = new FormData();
      const geoType = state.dataAction.geoType;
      const actionType = state.dataAction.actionType;
      const editableGeoObject = rootState.ymap.editableGeoObject;

      switch (geoType) {
        case "heatpoint":
          // eslint-disable-next-line no-case-declarations
          let heatPoint = rootState.contextmenuHeatPoint;
          dataGeoObj.append("pk", heatPoint.pk);
          dataGeoObj.append("geoType", geoType);
          dataGeoObj.append("action", actionType);
          dataGeoObj.append("title", heatPoint.title);
          dataGeoObj.append("weight", heatPoint.weight);
          dataGeoObj.append(
            "coordinates",
            JSON.stringify(rootState.dialogCreate.coords),
          );
          break;
        case "placemark":
          // eslint-disable-next-line no-case-declarations
          let placemark = rootState.contextmenuPlacemark;
          dataGeoObj.append("pk", placemark.pk);
          dataGeoObj.append("geoType", geoType);
          dataGeoObj.append("action", actionType);
          dataGeoObj.append("category", placemark.category);
          dataGeoObj.append("header", placemark.header);
          dataGeoObj.append("body", placemark.body);
          dataGeoObj.append("footer", placemark.footer);
          dataGeoObj.append("icon_slug", placemark.iconSlug);
          if (editableGeoObject === null) {
            dataGeoObj.append(
              "coordinates",
              JSON.stringify(rootState.dialogCreate.coords),
            );
          } else {
            dataGeoObj.append(
              "coordinates",
              JSON.stringify(placemark.coordinates),
            );
          }
          placemark.subcategories.forEach((element) => {
            dataGeoObj.append("subcategories", element);
          });
          break;
        case "polyline":
          // eslint-disable-next-line no-case-declarations
          let route = rootState.contextmenuRoute;
          dataGeoObj.append("pk", route.pk);
          dataGeoObj.append("geoType", geoType);
          dataGeoObj.append("action", actionType);
          dataGeoObj.append("category", route.category);
          dataGeoObj.append("header", route.header);
          dataGeoObj.append("body", route.body);
          dataGeoObj.append("footer", route.footer);
          dataGeoObj.append("stroke_width", route.strokeWidth);
          dataGeoObj.append("stroke_color", route.strokeColor);
          dataGeoObj.append(
            "stroke_style",
            typeof route.strokeStyle === "string"
              ? route.strokeStyle
              : route.strokeStyle.value,
          );
          dataGeoObj.append("stroke_opacity", route.strokeOpacity);
          dataGeoObj.append("coordinates", JSON.stringify(route.coordinates));
          route.subcategories.forEach((element) => {
            dataGeoObj.append("subcategories", element);
          });
          break;
        case "polygon":
          // eslint-disable-next-line no-case-declarations
          let territory = rootState.contextmenuTerritory;
          dataGeoObj.append("pk", territory.pk);
          dataGeoObj.append("geoType", geoType);
          dataGeoObj.append("action", actionType);
          dataGeoObj.append("category", territory.category);
          dataGeoObj.append("header", territory.header);
          dataGeoObj.append("body", territory.body);
          dataGeoObj.append("footer", territory.footer);
          dataGeoObj.append("stroke_width", territory.strokeWidth);
          dataGeoObj.append("stroke_color", territory.strokeColor);
          dataGeoObj.append(
            "stroke_style",
            typeof territory.strokeStyle === "string"
              ? territory.strokeStyle
              : territory.strokeStyle.value,
          );
          dataGeoObj.append("stroke_opacity", territory.strokeOpacity);
          dataGeoObj.append("fill_color", territory.fillColor);
          dataGeoObj.append("fill_opacity", territory.fillOpacity);
          dataGeoObj.append(
            "coordinates",
            JSON.stringify(territory.coordinates),
          );
          territory.subcategories.forEach((element) => {
            dataGeoObj.append("subcategories", element);
          });
          break;
      }

      dataGeoObj.append("ymap", window.djeymMapID);
      dataGeoObj.append("csrfmiddlewaretoken", window.djeymCSRFToken);

      if (state.enableAjax) {
        window.$.ajax({
          type: "POST",
          url: "/djeym/ajax-save-geo-object/",
          data: dataGeoObj,
          cache: false,
          processData: false,
          contentType: false,
          dataType: "json",
        })
          .done((data) => {
            if (geoType !== "heatpoint" && editableGeoObject !== null) {
              commit("ymap/setEditableGeoObject", null, { root: true });
              rootState.ymap.Map.geoObjects.remove(editableGeoObject);
            }
            switch (geoType) {
              case "heatpoint":
                dispatch("contextmenuHeatPoint/restoreDefaults", null, {
                  root: true,
                });
                dispatch("ymap/addHeatPoints", data, { root: true });
                break;
              case "placemark":
                dispatch("contextmenuPlacemark/restoreDefaults", null, {
                  root: true,
                });
                if (actionType !== "delete") {
                  dispatch("ymap/addPlacemarkTypeObjects", data, {
                    root: true,
                  });
                }
                break;
              case "polyline":
                dispatch("contextmenuRoute/restoreDefaults", null, {
                  root: true,
                });
                if (actionType !== "delete") {
                  dispatch("ymap/addPolylineTypeObjects", data, { root: true });
                }
                break;
              case "polygon":
                dispatch("contextmenuTerritory/restoreDefaults", null, {
                  root: true,
                });
                if (actionType !== "delete") {
                  dispatch("ymap/addPolygonTypeObjects", data, { root: true });
                }
                break;
            }
            commit("setShowBtnFindEditableGeoObject", false);
            commit("modals/geoObjectDialogClose", null, { root: true });
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Saving Geo Objects.",
              },
              { root: true },
            );
          })
          .always(() => {
            commit("modals/globalProgressBarShow", false, { root: true });
          });
      }
    },
  },
});
