/*
* Module for the LoadingIndicators.vue component.
*/

export default {
  namespaced: true,
  state: {
    controls: {}
  },
  getters: {},
  mutations: {
    setSize (state, value) {
      state.controls.size = value
    },
    setSpeed (state, value) {
      state.controls.speed = value
    },
    setCurrentIndicator (state, value) {
      state.controls.currentIndicator = value
    }
  },
  actions: {
    actionSetFromAjax ({ state }, obj) {
      state.controls = obj
    },
    // Ajax - Save change
    actionAjaxUpdate ({ state, commit, dispatch, rootState }) {
      if (rootState.enableAjax) {
        commit('modals/globalProgressBarShow', true, { root: true })
        commit('modals/messageDialogClose', null, { root: true })
        window.$.post('/djeym/ajax-update-load-indicator/', {
          csrfmiddlewaretoken: window.djeymCSRFToken,
          mapID: window.djeymMapID,
          slug: state.controls.currentIndicator,
          size: state.controls.size,
          speed: state.controls.speed,
          animation: state.controls.disableAnimation ? 'True' : 'False'
        })
          .done(() => {
            window.location.reload(true)
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch('modals/ajaxErrorProcessing', {
              jqxhr: jqxhr,
              textStatus: textStatus,
              error: error,
              hint: 'Ajax - Saving - Update Load indicator.'
            }, { root: true })
          })
          .always(() => {
            setTimeout(() => commit('modals/globalProgressBarShow', false, { root: true }), 1000)
          })
      }
    }
  }
}
