/*
 * Module for the GeneralSettings.vue component.
 */

import Vuetify from "@/plugins/vuetify.js";
import i18n from "@/locales/i18n.js";

export default {
  namespaced: true,
  state: {
    // Theme.
    themeType: "dark", // dark or light.
    colorControlsTheme: "#FFFFFF", // white
    colorButtonsTextTheme: "#FFFFFF", // white
    // Vuetify - For the "elevation" Attribute - Cards, Buttons and etc...
    minElevation: 2,
    maxElevation: 4,
    // Settings of controls.
    controls: {},
    // Colors - Display the number of objects in the cluster icon.
    colorBackgroundCountObjects: "#FAFAFA",
    textColorCountObjects: "#212121",
    // Panel tinting on front page.
    tintingPanelFront: "#00000000",
    // The background color under the controls on the front page.
    colorBgControlsPanelFront: "#00000000",
    // Disabling of button - Delete image background for Panel on front page.
    disabledBtnDelImgBgPanelFront: true,
    // Data for action "Palette".
    dataActionPalette: {},
    // Data for action "actionAjaxUpdate".
    dataActionSaveUpdate: {},
  },
  getters: {},
  mutations: {
    // Refresh current color of controls.
    refreshColorControlsTheme(state, color) {
      state.colorControlsTheme = color;
    },
    // Refresh current color of text on buttons.
    refreshColorButtonsTextTheme(state, color) {
      state.colorButtonsTextTheme = color;
    },
    // Refresh current color background - Count of objects in the cluster.
    refreshColorBackgroundCountObjects(state, color) {
      state.colorBackgroundCountObjects = color;
    },
    // Refresh current text color - Count of objects in the cluster.
    refreshTextColorCountObjects(state, color) {
      state.textColorCountObjects = color;
    },
    // Panel tinting on front page.
    refreshTintingPanelFront(state, color) {
      state.tintingPanelFront = color;
    },
    // Set data for palette.
    setDataActionPalette(state, payload) {
      state.dataActionPalette = payload;
    },
    // Set data for save settings.
    setDataActionSaveUpdate(state, payload) {
      state.dataActionSaveUpdate = payload;
    },
    // Disabling of button - Delete image background for Panel on front page.
    setDisabledBtnDelImgBgPanelFront(state, flag) {
      state.disabledBtnDelImgBgPanelFront = flag;
    },
  },
  actions: {
    // Set general settings from Ajax.
    actionSetFromAjax({ state, dispatch }, obj) {
      state.themeType = obj.themeType;
      state.colorControlsTheme = obj.colorControlsTheme;
      state.colorButtonsTextTheme = obj.colorButtonsTextTheme;
      state.colorBackgroundCountObjects = obj.colorBackgroundCountObjects;
      state.textColorCountObjects = obj.textColorCountObjects;
      state.tintingPanelFront = obj.tintingPanelFront;
      state.controls = obj.controls;
      dispatch("actionThemeType", obj.themeType);
      state.disabledBtnDelImgBgPanelFront =
        !state.controls.panel3_71[3].imgBgPanelFront;
    },
    // Update type theme.
    actionThemeType({ state }, type) {
      state.themeType = type;
      Vuetify.framework.theme.dark = { dark: true, light: false }[type];
      state.minElevation = { dark: 4, light: 2 }[type];
      state.maxElevation = state.minElevation * 2;
    },
    // To job with the paint palette.
    actionPalette({ state, commit, rootState }) {
      let hexColor = rootState.modals.currentColorPalette.toUpperCase();
      const target = state.dataActionPalette.target;
      switch (target) {
        case "colorPanelFront":
        case "tintingPanelFront":
          if (hexColor.length === 7) {
            hexColor += "FF";
          }
          break;
        default:
          if (hexColor.length > 7) {
            hexColor = hexColor.slice(0, 7);
          }
          break;
      }
      state[target] = hexColor;
      rootState.modals.controlsCurrentActionBtnCancel = null;
      rootState.modals.controlsCurrentActionBtnSave = null;
      commit("modals/controlsDialogClose", null, {
        root: true,
      });
      commit("setMapSettingsDrawer", true, { root: true });
    },
    // Refresh width Panel Editor.
    actionRefreshWidthPanelEditor({ state, commit }) {
      const width = state.controls.panel2_70[1].widthPanelEditor;
      if (width >= 300) {
        commit("setWidthPanelSettings", width, { root: true });
      }
    },
    // Refresh the current cropped image for the panel background.
    actionRefreshImgBgPanelFront({ state, commit, rootState }) {
      const currentImageCrop = rootState.currentImageCrop;
      if (currentImageCrop !== null) {
        state.controls.panel3_71[3].imgBgPanelFront = currentImageCrop;
        commit("setCurrentImageCrop", null, { root: true });
      }
      commit("setDataAction", {}, { root: true });
    },
    // Delete the background image for the panel.
    actionDeleteImgBgPanelFront({ state, commit, dispatch, rootState }) {
      if (rootState.enableAjax) {
        commit("modals/messageDialogClose", null, { root: true });
        commit("modals/globalProgressBarShow", true, { root: true });
        window.$.post("/djeym/ajax-del-img-bg-panel-front/", {
          csrfmiddlewaretoken: window.djeymCSRFToken,
          mapID: window.djeymMapID,
        })
          .done(() => {
            state.controls.panel3_71[3].imgBgPanelFront = "";
            commit("setDisabledBtnDelImgBgPanelFront", true);
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Delete the background image for the panel.",
              },
              { root: true },
            );
          })
          .always(function () {
            setTimeout(() => {
              commit("modals/globalProgressBarShow", false, { root: true });
              commit("setMapSettingsDrawer", true, { root: true });
            }, 1000);
          });
      }
    },
    // Ajax - Save change.
    actionAjaxUpdate({ state, commit, dispatch, rootState }) {
      if (rootState.enableAjax) {
        commit("modals/messageDialogClose", null, { root: true });
        commit("modals/globalProgressBarShow", true, { root: true });

        const widthPanelEditor = state.controls.panel2_70[1].widthPanelEditor;
        const widthPanelFront = state.controls.panel3_71[1].widthPanelFront;

        if (
          !isFinite(widthPanelEditor) ||
          widthPanelEditor < 300 ||
          !isFinite(widthPanelFront) ||
          widthPanelFront < 260
        ) {
          commit("modals/globalProgressBarShow", false, { root: true });
          commit(
            "modals/messageDialogShow",
            {
              status: "error",
              title: i18n.t("message.86"),
              text: i18n.t("message.81"),
              cancelBtn: true,
              okBtn: false,
              actionBtnCancel: () => {
                commit("modals/messageDialogClose", null, { root: true });
                commit("setMapSettingsDrawer", true, { root: true });
              },
              actionBtnOk: null,
            },
            { root: true },
          );
          return;
        }

        const fd = new FormData();
        fd.append("ymap", window.djeymMapID);
        fd.append("csrfmiddlewaretoken", window.djeymCSRFToken);
        fd.append("clustering_edit", state.controls.panel2_70[0].isActive);
        fd.append("clustering_site", state.controls.panel3_71[0].isActive);
        fd.append("cluster_layout", state.controls.panel1_69[2].layout);
        fd.append("cluster_icon_content", state.controls.panel1_69[3].isActive);
        fd.append(
          "cluster_icon_content_bg_color",
          state.colorBackgroundCountObjects,
        );
        fd.append(
          "cluster_icon_content_txt_color",
          state.textColorCountObjects,
        );
        fd.append("controls_color", state.colorControlsTheme);
        fd.append("buttons_text_color", state.colorButtonsTextTheme);
        fd.append("theme_type", state.themeType);
        fd.append("roundtheme", state.controls.panel1_69[0].isActive);
        fd.append("panorama", state.controls.panel1_69[1].isActive);
        fd.append("width_panel_editor", widthPanelEditor);
        fd.append("width_panel_front", widthPanelFront);
        fd.append("open_panel_front", state.controls.panel3_71[2].isActive);
        const imgBgPanelFront = state.controls.panel3_71[3].imgBgPanelFront;
        fd.append(
          "img_bg_panel_front_b64",
          /base64/.test(imgBgPanelFront) ? imgBgPanelFront : "",
        );
        fd.append("tinting_panel_front", state.tintingPanelFront);
        fd.append("width_map_front", state.controls.panel3_71[4].widthMapFront);
        fd.append(
          "height_map_front",
          state.controls.panel3_71[5].heightMapFront,
        );

        window.$.ajax({
          type: "POST",
          url: "/djeym/ajax-update-general-settings/",
          data: fd,
          cache: false,
          processData: false,
          contentType: false,
          dataType: "json",
        })
          .done(() => {
            if (state.dataActionSaveUpdate.reloadPage) {
              window.location.reload(true);
            } else {
              commit(
                "setDisabledBtnDelImgBgPanelFront",
                !state.controls.panel3_71[3].imgBgPanelFront,
              );
              commit("modals/globalProgressBarShow", false, { root: true });
              commit("setMapSettingsDrawer", true, { root: true });
            }
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Saving - Update General settings.",
              },
              { root: true },
            );
          })
          .always(() => {
            setTimeout(
              () =>
                commit("modals/globalProgressBarShow", false, { root: true }),
              1000,
            );
          });
      }
    },
  },
};
