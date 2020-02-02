/*
* Module for the MenuCreateGeoObject.vue component.
*/

import helpers from '@/helpers.js'

export default {
  namespaced: true,
  state: {
    coords: [0, 0]
  },
  getters: {},
  mutations: {
    setLatitude (state, coord) {
      state.coords[0] = helpers.roundCoord(coord)
    },
    setLongitude (state, coord) {
      state.coords[1] = helpers.roundCoord(coord)
    }
  },
  actions: {
    // Open geoObjectDialogShow for Route or Territory.
    actionCreateNewGeoObjecte ({ state, commit, dispatch, rootState }, payload) {
      commit('modals/geoObjectDialogShow', {
        title: payload.title,
        editBtn: true,
        saveBtn: payload.showSaveBtn,
        cancelBtn: true,
        deleteBtn: false,
        actionBtnEdit: () => {
          if (!rootState[payload.storeModuleName].category) {
            commit('modals/alertSnackbarShow',
              payload.messageErrorAddCategory(), { root: true })
            return
          }
          if (rootState[payload.storeModuleName].header.length === 0) {
            commit('modals/alertSnackbarShow',
              payload.messageErrorAddHeader(), { root: true })
            return
          }
          commit('modals/alertSnackbarClose', null, { root: true })
          commit('modals/geoObjectDialogClose', null, { root: true })
        },
        actionBtnSave: () => {
          if (!rootState[payload.storeModuleName].category) {
            commit('modals/alertSnackbarShow',
              payload.messageErrorAddCategory(), { root: true })
            return
          }
          if (rootState[payload.storeModuleName].header.length === 0) {
            commit('modals/alertSnackbarShow',
              payload.messageErrorAddHeader(), { root: true })
            return
          }
          commit('setDataAction', { geoType: payload.geoType, actionType: 'save' }, { root: true })
          dispatch('ajaxContextMenu', null, { root: true })
        },
        actionBtnCancel: () => {
          if (rootState.ymap.editableGeoObject !== null) {
            rootState.ymap.Map.geoObjects.remove(rootState.ymap.editableGeoObject)
          }
          commit('ymap/setEditableGeoObject', null, { root: true })
          dispatch(`${payload.storeModuleName}/restoreDefaults`, null, { root: true })
          commit('modals/alertSnackbarClose', null, { root: true })
          commit('modals/geoObjectDialogClose', null, { root: true })
        },
        actionBtnDelete: null,
        componentHeatPoint: false,
        componentPlacemark: false,
        componentPolyline: payload.geoType === 'polyline',
        componentPolygon: payload.geoType === 'polygon'
        // componentPolygon: payload.geoType === 'polygon'
      }, { root: true })
    }
  }
}
