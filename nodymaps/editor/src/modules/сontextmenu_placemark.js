/*
* Module for the ContextmenuPlacemark.vue component.
*/

import helpers from '@/helpers.js'

export default {
  namespaced: true,
  state: {
    pk: 0,
    category: null,
    subcategories: [],
    header: '',
    body: '',
    footer: '',
    iconSlug: '',
    coordinates: [0, 0],
    iconUrl: ''
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
    setIconSlug (state, slug) {
      state.iconSlug = slug
    },
    setLatitude (state, coord) {
      state.coordinates[0] = helpers.roundCoord(coord)
    },
    setLongitude (state, coord) {
      state.coordinates[1] = helpers.roundCoord(coord)
    },
    setIconUrl (state, url) {
      state.iconUrl = url
    }
  },
  actions: {
    restoreDefaults ({ state, rootState }) {
      const firstIcon = rootState.iconCollection[0]
      state.pk = 0
      state.category = null
      state.subcategories = []
      state.header = ''
      state.body = ''
      state.footer = ''
      state.iconSlug = firstIcon.slug
      state.coordinates = rootState.dialogCreate.coords
      state.iconUrl = firstIcon.url
    }
  }
}
