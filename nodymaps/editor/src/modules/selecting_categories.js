/*
 * Module for the SelectingCategories.vue component.
 */

export default {
  namespaced: true,
  state: {
    controls: {
      category: null,
      subcategories: [],
    },
  },
  getters: {},
  mutations: {
    setCategory(state, txtNum) {
      state.controls.category = txtNum;
    },
    setSubcategories(state, arrTxtNum) {
      state.controls.subcategories = arrTxtNum;
    },
  },
  actions: {},
};
