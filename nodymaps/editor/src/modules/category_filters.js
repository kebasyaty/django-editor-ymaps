/*
* Module for the CategoryFilters.vue component.
*/

import i18n from '@/i18n.js'

export default {
  namespaced: true,
  state: {
    panel: [],
    multiple: true, // Multiple or solo choice.
    tabIcons: { // Category Icons
      'marker': 'mdi-map-marker',
      'route': 'mdi-routes',
      'territory': 'mdi-beach'
    },
    centerGeoTypes: false,
    hideGeoTypes: false,
    geoTypeNameMarker: '',
    geoTypeNameRoute: '',
    geoTypeNameTerritory: '',
    hideGroupNames: false,
    groupNameCategories: '',
    groupNameSubcategories: '',
    controlsShape: 'shaped',
    effectRipple: true,
    filters: {
      a: [], // Categories of placemarks
      b: [], // Subcategories of placemarks
      c: [], // Categories of Routes
      d: [], // Subcategories of Routes
      e: [], // Categories of Territories
      f: [] // Subcategories of Territories
    },
    models: {
      a: [], // Categories of placemarks
      b: [], // Subcategories of placemarks
      c: [], // Categories of Routes
      d: [], // Subcategories of Routes
      e: [], // Categories of Territories
      f: [] // Subcategories of Territories
    }
  },
  getters: {},
  mutations: {
    setMultiple (state, flag) {
      state.multiple = flag
    },
    setCenterGeoTypes (state, flag) {
      state.centerGeoTypes = flag
    },
    setHideGeoTypes (state, flag) {
      state.hideGeoTypes = flag
    },
    setGeoTypeNameMarker (state, text) {
      state.geoTypeNameMarker = text
    },
    setGeoTypeNameRoute (state, text) {
      state.geoTypeNameRoute = text
    },
    setGeoTypeNameTerritory (state, text) {
      state.geoTypeNameTerritory = text
    },
    setHideGroupNames (state, flag) {
      state.hideGroupNames = flag
    },
    setGroupNameCategories (state, text) {
      state.groupNameCategories = text
    },
    setGroupNameSubcategories (state, text) {
      state.groupNameSubcategories = text
    },
    setControlsShape (state, shape) {
      state.controlsShape = shape
    },
    setEffectRipple (state, flag) {
      state.effectRipple = flag
    }
  },
  actions: {
    actionSetFromAjax ({ state }, payload) {
      const multiple = payload.multiple
      const filters = payload.filters
      let models = state.models

      state.multiple = multiple
      state.tabIcons = payload.tabIcons
      state.centerGeoTypes = payload.centerGeoTypes
      state.hideGeoTypes = payload.hideGeoTypes
      state.geoTypeNameMarker = payload.geoTypeNameMarker
      state.geoTypeNameRoute = payload.geoTypeNameRoute
      state.geoTypeNameTerritory = payload.geoTypeNameTerritory
      state.hideGroupNames = payload.hideGroupNames
      state.groupNameCategories = payload.groupNameCategories
      state.groupNameSubcategories = payload.groupNameSubcategories
      state.controlsShape = payload.controlsShape
      state.effectRipple = payload.effectRipple
      state.filters = filters

      // Fill models state
      let flag = true
      for (let key in filters) {
        if (flag) {
          if (multiple) {
            models[key] = Array.from(Array(filters[key].length).keys())
          } else {
            models[key] = 0
          }
        }
        flag = !flag
      }
    },
    actionCheckNameIcon ({ state }, tabName) {
      const iconName = state.tabIcons[tabName]
      if (iconName) {
        state.tabIcons[tabName] = state.tabIcons[tabName].toLowerCase()
        if (!/^mdi-/.test(iconName)) {
          state.tabIcons[tabName] = 'mdi-' + iconName
        }
      }
    },
    generalFilter ({ state, rootState }, payload) {
      const categoriesIDs = []
      const subcategoriesIDs = []
      let countSubcategories = 0

      state.filters[payload.filterName1].forEach(item => {
        if (item.isActive) { categoriesIDs.push(item.id) }
      })

      state.filters[payload.filterName2].forEach(item => {
        if (item.isActive) { subcategoriesIDs.push(item.id) }
      })

      countSubcategories = subcategoriesIDs.length

      if (countSubcategories > 0) {
        rootState.ymap[payload.globalObjMngName].setFilter(object => {
          let tmpIDs = object.properties.subCategoryIDs
          return categoriesIDs.includes(object.properties.categoryID) &&
            tmpIDs.filter(num => subcategoriesIDs.includes(num)).length ===
            countSubcategories
        })
      } else {
        rootState.ymap[payload.globalObjMngName].setFilter(object => {
          return categoriesIDs.includes(object.properties.categoryID)
        })
      }
    },
    actionFiltering ({ state, dispatch }, payload) {
      const categoryID = payload.id
      const modelKey = payload.modelKey
      // If multiple = false - Disable previous selection.
      if (!state.multiple && ['a', 'c', 'e', 'g', 'i'].includes(modelKey)) {
        let filter = state.filters[modelKey]
        for (let idx = 0, len = filter.length; idx < len; idx++) {
          let control = filter[idx]
          if (control.isActive && control.id !== categoryID) {
            control.isActive = false
            break
          }
        }
      }
      // Filtration of geo objects
      switch (modelKey) {
        /* Categories of placemarks and
           Subcategories of placemarks */
        case 'a':
        case 'b':
          dispatch('generalFilter', {
            filterName1: 'a',
            filterName2: 'b',
            globalObjMngName: 'globalObjMngPlacemark'
          })
          break
        /* Categories of Routes and
           Subcategories of Routes */
        case 'c':
        case 'd':
          dispatch('generalFilter', {
            filterName1: 'c',
            filterName2: 'd',
            globalObjMngName: 'globalObjMngPolyline'
          })
          break
        /* Categories of Territories and
           Subcategories of Territories */
        case 'e':
        case 'f':
          dispatch('generalFilter', {
            filterName1: 'e',
            filterName2: 'f',
            globalObjMngName: 'globalObjMngPolygon'
          })
          break
      }
    },
    // Refresh visibility of geo objects.
    refreshVisibilityGeoObjects ({ state, dispatch }) {
      const filters = [
        { filterName1: 'a', filterName2: 'b', globalObjMngName: 'globalObjMngPlacemark' },
        { filterName1: 'c', filterName2: 'd', globalObjMngName: 'globalObjMngPolyline' },
        { filterName1: 'e', filterName2: 'f', globalObjMngName: 'globalObjMngPolygon' }
      ]
      filters.forEach(item => {
        dispatch('generalFilter', {
          filterName1: item.filterName1,
          filterName2: item.filterName2,
          globalObjMngName: item.globalObjMngName
        })
      })
    },
    actionRefreshStateControls ({ state, dispatch }) {
      const multiple = state.multiple
      let counter = 1
      // Refresh filters state
      let flag
      for (let key in state.filters) {
        flag = true
        let filter = state.filters[key]
        for (let idx = 0, len = filter.length; idx < len; idx++) {
          filter[idx].isActive = flag && counter % 2 !== 0
          flag = multiple
        }
        ++counter
      }
      // Refresh models state
      flag = true
      for (let key in state.filters) {
        if (flag) {
          if (multiple) {
            state.models[key] = Array.from(Array(state.filters[key].length).keys())
          } else {
            state.models[key] = 0
          }
        } else {
          state.models[key] = []
        }
        flag = !flag
      }
      // Refresh visibility of geo objects.
      dispatch('refreshVisibilityGeoObjects', null)
    },
    actionReset ({ state, commit, dispatch }) {
      state.multiple = true
      state.centerGeoTypes = false
      state.hideGeoTypes = false
      state.geoTypeNameMarker = ''
      state.geoTypeNameRoute = ''
      state.geoTypeNameTerritory = ''
      state.hideGroupNames = false
      state.groupNameCategories = ''
      state.groupNameSubcategories = ''
      state.controlsShape = 'shaped'
      state.effectRipple = true

      const defaultTabIcons = {
        'marker': 'mdi-map-marker',
        'route': 'mdi-routes',
        'territory': 'mdi-beach'
      }
      let tabIcons = state.tabIcons
      for (let key in tabIcons) {
        tabIcons[key] = defaultTabIcons[key]
      }

      let flag = true
      // Reset filters state
      for (let key in state.filters) {
        let filter = state.filters[key]
        for (let idx = 0, len = filter.length; idx < len; idx++) {
          filter[idx].isActive = flag
        }
        flag = !flag
      }
      // Reset models state
      flag = true
      for (let key in state.filters) {
        if (flag) {
          state.models[key] = Array.from(Array(state.filters[key].length).keys())
        } else {
          state.models[key] = []
        }
        flag = !flag
      }
      dispatch('refreshVisibilityGeoObjects', null)
      commit('modals/messageDialogClose', null, { root: true })
      commit('setMapSettingsDrawer', true, { root: true })
    },
    // Ajax - Save change
    actionSave ({ state, commit, dispatch, rootState }) {
      commit('modals/globalProgressBarShow', true, { root: true })
      commit('modals/messageDialogClose', null, { root: true })
      state.panel = []

      const mapID = window.djeymMapID

      // Deep copy of filters state
      let filterSettings = JSON.stringify({
        multiple: state.multiple,
        tabIcons: state.tabIcons,
        centerGeoTypes: state.centerGeoTypes,
        hideGeoTypes: state.hideGeoTypes,
        geoTypeNameMarker: state.geoTypeNameMarker,
        geoTypeNameRoute: state.geoTypeNameRoute,
        geoTypeNameTerritory: state.geoTypeNameTerritory,
        hideGroupNames: state.hideGroupNames,
        groupNameCategories: state.groupNameCategories,
        groupNameSubcategories: state.groupNameSubcategories,
        controlsShape: state.controlsShape,
        effectRipple: state.effectRipple,
        filters: state.filters
      })
      filterSettings = JSON.parse(filterSettings)

      // Check icon fields
      const transTabIcons = {
        'marker': 15,
        'route': 16,
        'territory': 17
      }
      for (let key in filterSettings.tabIcons) {
        if (!filterSettings.tabIcons[key]) {
          commit('modals/globalProgressBarShow', false, { root: true })
          commit('modals/messageDialogShow', {
            status: 'error',
            title: i18n.t('message.86'),
            text: `${i18n.t('message.' + transTabIcons[key])}:<br>${i18n.t('message.79')} !`,
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
      }

      // Normalize filters state
      const multiple = filterSettings.multiple
      let counter = 1
      let flag
      for (let key in filterSettings.filters) {
        flag = true
        let filter = filterSettings.filters[key]
        for (let idx = 0, len = filter.length; idx < len; idx++) {
          filter[idx].isActive = flag && counter % 2 !== 0
          flag = multiple
        }
        ++counter
      }

      // Save change
      if (rootState.enableAjax) {
        window.$.post('/djeym/ajax-update-filters-categories/', {
          csrfmiddlewaretoken: window.djeymCSRFToken,
          mapID: mapID,
          jsonCategories: JSON.stringify(filterSettings)
        })
          .fail((jqxhr, textStatus, error) => {
            dispatch('modals/ajaxErrorProcessing', {
              jqxhr: jqxhr,
              textStatus: textStatus,
              error: error,
              hint: 'Ajax - Saving - Update filters for categories.'
            }, { root: true })
          })
          .always(() => {
            setTimeout(() => {
              commit('modals/globalProgressBarShow', false, { root: true })
              commit('setMapSettingsDrawer', true, { root: true })
            }, 1000)
          })
      }
    }
  }
}
