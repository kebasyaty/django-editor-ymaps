/*
* Module for the ContextmenuHeatPoint.vue component.
*/

export default {
  namespaced: true,
  state: {
    pk: 0,
    action: 'save', // save, reload, delete
    title: '',
    weight: 0
  },
  getters: {},
  mutations: {
    setPK (state, num) {
      state.pk = num
    },
    setAction (state, action) {
      state.action = action // save, reload, delete
    },
    setTitle (state, text) {
      state.title = text
    },
    setWeight (state, num) {
      state.weight = num
    }
  },
  actions: {
    restoreDefaults ({ state }) {
      state.pk = 0
      state.action = 'save'
      state.title = ''
      state.weight = 0
    }
  }
}
