/*
 * Module for the TileSources.vue component.
 */

export default {
  namespaced: true,
  state: {
    tiles: [],
    currentTile: null,
    dataActionAjaxReplacement: {},
  },
  getters: {},
  mutations: {
    setFromAjax(state, payload) {
      state.tiles = payload.tiles;
      state.currentTile = payload.currentTile;
    },
    setDataActionAjaxReplacement(state, payload) {
      state.dataActionAjaxReplacement = payload;
    },
  },
  actions: {
    // Ajax - Save change
    actionAjaxReplacement({ state, commit, dispatch, rootState }) {
      if (rootState.enableAjax) {
        commit("modals/globalProgressBarShow", true, { root: true });
        commit("modals/messageDialogClose", null, { root: true });
        window.$.post("/djeym/ajax-update-tile-source/", {
          csrfmiddlewaretoken: window.djeymCSRFToken,
          mapID: window.djeymMapID,
          tileID: state.dataActionAjaxReplacement.id,
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
                hint: "Ajax - Saving - Update Tile source.",
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
