/*
 * Module for the MapControls.vue component.
 */

export default {
  namespaced: true,
  state: {
    controls: [],
    activeControls: [],
  },
  getters: {},
  mutations: {},
  actions: {
    actionSetFromAjax({ state }, obj) {
      state.controls = obj.controls;
      state.activeControls = obj.activeControls;
    },
    // Ajax - Save change
    actionAjaxUpdate({ state, commit, dispatch, rootState }) {
      if (rootState.enableAjax) {
        commit("modals/globalProgressBarShow", true, { root: true });
        commit("modals/messageDialogClose", null, { root: true });
        window.$.post("/djeym/ajax-update-map-controls/", {
          csrfmiddlewaretoken: window.djeymCSRFToken,
          ymap: window.djeymMapID,
          geolocation: state.controls[0].isActive ? "True" : "False",
          search: state.controls[1].isActive ? "True" : "False",
          provider: state.controls[2].isActive ? "True" : "False",
          route: state.controls[3].isActive ? "True" : "False",
          traffic: state.controls[4].isActive ? "True" : "False",
          typeselector: state.controls[5].isActive ? "True" : "False",
          fullscreen: state.controls[6].isActive ? "True" : "False",
          zoom: state.controls[7].isActive ? "True" : "False",
          ruler: state.controls[8].isActive ? "True" : "False",
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
                hint: "Ajax - Saving - Update Map controls.",
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
