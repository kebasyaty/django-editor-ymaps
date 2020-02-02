/*
* Module for the ContextmenuTerritory.vue component.
*/

import i18n from '@/i18n.js'

export default {
  namespaced: true,
  state: {
    pk: 0,
    category: null,
    subcategories: [],
    header: '',
    body: '',
    footer: '',
    strokeColor: '#4caf50',
    strokeStyle: { value: 'solid', title: i18n.t('message.115') },
    strokeWidth: 5,
    strokeOpacity: 0.9,
    fillColor: '#00C853',
    fillOpacity: 0.9,
    coordinates: [],
    // Data for action "Palette".
    dataActionPalette: {}
  },
  getters: {},
  mutations: {
    setPK (state, num) {
      state.pk = +num
    },
    setCategory (state, num) {
      state.category = +num
    },
    setSubcategories (state, arr) {
      state.subcategories = arr.map(item => +item)
    },
    setHeader (state, text) {
      state.header = text
    },
    setBody (state, text) {
      state.body = text
    },
    setFooter (state, text) {
      state.footer = text
    },
    setStrokeColor (state, color) {
      state.strokeColor = color
    },
    setStrokeStyle (state, style) {
      state.strokeStyle = style
    },
    setStrokeWidth (state, num) {
      state.strokeWidth = +num
    },
    setStrokeOpacity (state, num) {
      state.strokeOpacity = +num
    },
    setFillColor (state, color) {
      state.fillColor = color
    },
    setFillOpacity (state, num) {
      state.fillOpacity = +num
    },
    setCoordinates (state, arrCoords) {
      state.coordinates = arrCoords
    },
    // Set data for palette.
    setDataActionPalette (state, payload) {
      state.dataActionPalette = payload
    }
  },
  actions: {
    restoreDefaults ({ state }) {
      state.pk = 0
      state.category = null
      state.subcategories = []
      state.header = ''
      state.body = ''
      state.footer = ''
      state.strokeColor = '#4caf50'
      state.strokeStyle = { value: 'solid', title: i18n.t('message.115') }
      state.strokeWidth = 5
      state.strokeOpacity = 0.9
      state.fillColor = '#00C853'
      state.fillOpacity = 0.9
      state.coordinates = []
    },
    actionPalette ({ state, commit, rootState }) {
      const target = state.dataActionPalette.target
      let hexColor = rootState.modals.currentColorPalette.toUpperCase()
      if (hexColor.length > 7) { hexColor = hexColor.slice(0, 7) }
      state[target] = hexColor
      rootState.ymap.editableGeoObject.options.set(target, hexColor)
      commit('modals/controlsDialogClose', null, { root: true })
    },
    actionRefreshStrokeStyle ({ state, rootState }) {
      rootState.ymap.editableGeoObject.options.set('strokeStyle', state.strokeStyle)
    },
    actionRefreshStrokeWidth ({ state, rootState }) {
      rootState.ymap.editableGeoObject.options.set('strokeWidth', +state.strokeWidth)
    },
    actionRefreshStrokeOpacity ({ state, rootState }) {
      rootState.ymap.editableGeoObject.options.set('strokeOpacity', +state.strokeOpacity)
    },
    actionRefreshFillOpacity ({ state, rootState }) {
      rootState.ymap.editableGeoObject.options.set('fillOpacity', state.fillOpacity)
    }
  }
}
