/*
 * Module for the Heatmap.vue component.
 */

import i18n from "@/locales/i18n.js";

export default {
  namespaced: true,
  state: {
    controls: {},
    // Data for action "Palette".
    dataActionPalette: {},
  },
  getters: {},
  mutations: {
    // Refresh Gradient Color.
    refreshGradientColor1(state, color) {
      state.controls.panel2.gradient.color1 = color;
    },
    refreshGradientColor2(state, color) {
      state.controls.panel2.gradient.color2 = color;
    },
    refreshGradientColor3(state, color) {
      state.controls.panel2.gradient.color3 = color;
    },
    refreshGradientColor4(state, color) {
      state.controls.panel2.gradient.color4 = color;
    },
    // Set data for palette.
    setDataActionPalette(state, payload) {
      state.dataActionPalette = payload;
    },
  },
  actions: {
    actionSetFromAjax({ state }, obj) {
      state.controls = obj;
    },
    actionPalette({ state, commit, dispatch, rootState }) {
      let hexColor = rootState.modals.currentColorPalette.toUpperCase();
      if (hexColor.length > 7) {
        hexColor = hexColor.slice(0, 7);
      }
      state.controls.panel2.gradient[
        "color" + state.dataActionPalette.numColor
      ] = hexColor;
      commit("modals/controlsDialogClose", null, { root: true });
      commit("setMapSettingsDrawer", true, { root: true });
      dispatch("actionRefreshGradient");
    },
    // Reset by default.
    actionReset({ state, commit, dispatch }) {
      // state.controls.panel1.isActive = false.
      state.controls.panel2.gradient.color1 = "#66BB6A";
      state.controls.panel2.gradient.color2 = "#FDD835";
      state.controls.panel2.gradient.color3 = "#EF5350";
      state.controls.panel2.gradient.color4 = "#B71C1C";
      state.controls.panel2.radius = 10;
      state.controls.panel2.dissipating = false;
      state.controls.panel2.opacity = 0.8;
      state.controls.panel2.intensity = 0.2;
      dispatch("actionRefreshGradient");
      dispatch("actionRefreshRadius");
      dispatch("actionRefreshDissipating");
      dispatch("actionRefreshOpacity");
      dispatch("actionRefreshIntensity");
      commit("modals/messageDialogClose", null, { root: true });
      commit("setMapSettingsDrawer", true, { root: true });
    },
    // Ajax - Save change.
    actionAjaxUpdate({ state, commit, dispatch, rootState }) {
      if (rootState.enableAjax) {
        commit("modals/globalProgressBarShow", true, { root: true });
        commit("modals/messageDialogClose", null, { root: true });
        const radius = +state.controls.panel2.radius;
        if (!(Number.isInteger(radius) && radius > 0)) {
          commit("modals/globalProgressBarShow", false, { root: true });
          commit(
            "modals/messageDialogShow",
            {
              status: "error",
              title: i18n.t("message.86"),
              text: i18n.t("message.49"),
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
        window.$.post("/djeym/ajax-update-heatmap-settings/", {
          csrfmiddlewaretoken: window.djeymCSRFToken,
          ymap: window.djeymMapID,
          radius: radius,
          dissipating: state.controls.panel2.dissipating ? "True" : "False",
          opacity: state.controls.panel2.opacity,
          intensity: state.controls.panel2.intensity,
          gradient_color1: state.controls.panel2.gradient.color1,
          gradient_color2: state.controls.panel2.gradient.color2,
          gradient_color3: state.controls.panel2.gradient.color3,
          gradient_color4: state.controls.panel2.gradient.color4,
          active: state.controls.panel1.isActive ? "True" : "False",
        })
          .done(() => {
            window.location.reload(true);
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch(
              "modals/ajaxErrorProcessing",
              {
                jqxhr: jqxhr,
                textStatus: textStatus,
                error: error,
                hint: "Ajax - Saving - Update Heatmap settings.",
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
    // Refresh Gradient in 'globalHeatmap'.
    actionRefreshGradient({ state, rootState }) {
      const heatmapControls = state.controls;
      if (heatmapControls.panel1.isActive) {
        rootState.ymap.globalHeatmap.options.set("gradient", {
          0.1: heatmapControls.panel2.gradient.color1,
          0.2: heatmapControls.panel2.gradient.color2,
          0.7: heatmapControls.panel2.gradient.color3,
          1.0: heatmapControls.panel2.gradient.color4,
        });
      }
    },
    // Refresh Radius in 'globalHeatmap'.
    actionRefreshRadius({ state, rootState }) {
      const heatmapControls = state.controls;
      if (heatmapControls.panel1.isActive) {
        rootState.ymap.globalHeatmap.options.set(
          "radius",
          +heatmapControls.panel2.radius || 1,
        );
      }
    },
    // Refresh Dissipating in 'globalHeatmap'.
    actionRefreshDissipating({ state, rootState }) {
      const heatmapControls = state.controls;
      if (heatmapControls.panel1.isActive) {
        rootState.ymap.globalHeatmap.options.set(
          "dissipating",
          heatmapControls.panel2.dissipating,
        );
      }
    },
    // Refresh Opacity in 'globalHeatmap'.
    actionRefreshOpacity({ state, rootState }) {
      const heatmapControls = state.controls;
      if (heatmapControls.panel1.isActive) {
        rootState.ymap.globalHeatmap.options.set(
          "opacity",
          +heatmapControls.panel2.opacity,
        );
      }
    },
    // Refresh Intensity in 'globalHeatmap'.
    actionRefreshIntensity({ state, rootState }) {
      const heatmapControls = state.controls;
      if (heatmapControls.panel1.isActive) {
        rootState.ymap.globalHeatmap.options.set(
          "intensityOfMidpoint",
          +heatmapControls.panel2.intensity,
        );
      }
    },
  },
};
