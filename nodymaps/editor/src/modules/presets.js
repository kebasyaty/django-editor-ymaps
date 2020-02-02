/*
* Module for the Presets.vue component.
*/

import i18n from '@/i18n.js'

export default {
  namespaced: true,
  state: {
    panel: [],
    controls: [],
    dataActionAjaxUpdate: {}
  },
  getters: {},
  mutations: {},
  actions: {
    setDataActionAjaxUpdate ({ state }, payload) {
      state.dataActionAjaxUpdate = payload
    },
    actionSetFromAjax ({ state }, arr) {
      state.controls = arr
    },
    // Ajax - Save change
    actionAjaxUpdate ({ state, commit, dispatch, rootState }) {
      if (rootState.enableAjax) {
        commit('modals/globalProgressBarShow', true, { root: true })
        commit('modals/messageDialogClose', null, { root: true })

        const presetID = state.dataActionAjaxUpdate.id
        const preset = state.controls.filter(item => item.id === presetID)[0]
        const position = +preset.position

        if (!(typeof position === 'number') || position < 0) {
          commit('modals/globalProgressBarShow', false, { root: true })
          commit('modals/messageDialogShow', {
            status: 'error',
            title: i18n.t('message.86'),
            text: i18n.t('message.62'),
            cancelBtn: true,
            okBtn: false,
            actionBtnCancel: () => {
              commit('modals/messageDialogClose', null, { root: true })
              commit('setMapSettingsDrawer', true, { root: true })
            },
            actionBtnOk: null
          }, { root: true })
          return
        }

        window.$.post('/djeym/ajax-update-preset-settings/', {
          csrfmiddlewaretoken: window.djeymCSRFToken,
          ymap: window.djeymMapID,
          presetID: presetID,
          autoheader: preset.autoheader,
          autobody: preset.autobody,
          autofooter: preset.autofooter,
          placemark: preset.placemark,
          polyline: preset.polyline,
          polygon: preset.polygon,
          circle: preset.circle,
          rectangle: preset.rectangle,
          position: position
        })
          .done(data => {
            state.panel = []
            state.controls = data.presets
          })
          .fail((jqxhr, textStatus, error) => {
            dispatch('modals/ajaxErrorProcessing', {
              jqxhr: jqxhr,
              textStatus: textStatus,
              error: error,
              hint: 'Ajax - Saving - Update settings of Preset.'
            }, { root: true })
          })
          .always(function () {
            setTimeout(() => {
              commit('modals/globalProgressBarShow', false, { root: true })
              commit('setMapSettingsDrawer', true, { root: true })
            }, 1000)
          })
      }
    }
  }
}
