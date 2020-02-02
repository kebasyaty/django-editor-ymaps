/*
* Module for the Modals.vue component.
*/

import i18n from '@/i18n.js'

export default {
  namespaced: true,
  state: {
    // GeoObject -----------------------------------------------------------------------------------
    geoObjectDialog: false, // Open/Close
    titleGeoObjectDialog: 'Title',
    geoObjectEditBtn: true,
    geoObjectSaveBtn: true,
    geoObjectCancelBtn: true,
    geoObjectDeleteBtn: true,
    geoObjectCurrentActionBtnEdit: null,
    geoObjectCurrentActionBtnSave: null,
    geoObjectCurrentActionBtnCancel: null,
    geoObjectCurrentActionBtnDelete: null,
    componentGeoObjectHeatPoint: false, // Show/Hide
    componentGeoObjectPlacemark: false, // Show/Hide
    componentGeoObjectPolyline: false, // Show/Hide
    componentGeoObjectPolygon: false, // Show/Hide
    // Controls ------------------------------------------------------------------------------------
    controlsDialog: false, // Open/Close
    titleControlsDialog: 'Title',
    textControlsDialog: 'Text | Html',
    controlsCancelBtn: true,
    controlsSaveBtn: true,
    componentControlsText: false, // Show/Hide
    componentControlsPalette: false, // Show/Hide
    componentControlsMenu: false, // Show/Hide
    componentControlsIconCollection: false, // Show/Hide
    componentControlsCKEditor: false, // Show/Hide
    componentControlsCategories: false, // Show/Hide
    componentControlsImageCrop: false, // Show/Hide
    currentColorPalette: '#F44336FF',
    controlsCurrentActionBtnCancel: null,
    controlsCurrentActionBtnSave: null,
    // Message -------------------------------------------------------------------------------------
    messageDialog: false, // Open/Close
    statusMessageDialog: 'success', // accent ; error ; info ; success ; warning
    titleMessageDialog: 'Text | Html',
    textMessageDialog: 'Text | Html',
    messageCancelBtn: true,
    messageOkBtn: true,
    messageCurrentActionBtnCancel: null,
    messageCurrentActionBtnOk: null,
    // Simple messages -----------------------------------------------------------------------------
    alertSnackbar: false, // Open/Close
    textSnackbar: 'Text | Html',
    // Global progress bar--------------------------------------------------------------------------
    globalProgressBar: false // Open/Close
  },
  getters: {},
  mutations: {
    // GeoObject -----------------------------------------------------------------------------------
    geoObjectDialogShow (state, payload) { // Open
      state.titleGeoObjectDialog = payload.title
      state.geoObjectEditBtn = payload.editBtn // Show/Hide
      state.geoObjectSaveBtn = payload.saveBtn // Show/Hide
      state.geoObjectCancelBtn = payload.cancelBtn // Show/Hide
      state.geoObjectDeleteBtn = payload.deleteBtn // Show/Hide
      state.geoObjectCurrentActionBtnEdit = payload.actionBtnEdit
      state.geoObjectCurrentActionBtnSave = payload.actionBtnSave
      state.geoObjectCurrentActionBtnCancel = payload.actionBtnCancel
      state.geoObjectCurrentActionBtnDelete = payload.actionBtnDelete
      state.geoObjectDialog = true
      state.componentGeoObjectHeatPoint = !!payload.componentHeatPoint // Show/Hide
      state.componentGeoObjectPlacemark = !!payload.componentPlacemark // Show/Hide
      state.componentGeoObjectPolyline = !!payload.componentPolyline // Show/Hide
      state.componentGeoObjectPolygon = !!payload.componentPolygon // Show/Hide
    },
    geoObjectDialogClose (state) { // Close
      state.geoObjectDialog = false
    },
    // Controls ------------------------------------------------------------------------------------
    controlsDialogShow (state, payload) { // Open
      state.titleControlsDialog = payload.title
      state.textControlsDialog = payload.text
      state.controlsCancelBtn = payload.cancelBtn // Show/Hide
      state.controlsSaveBtn = payload.saveBtn // Show/Hide
      state.componentControlsText = !!payload.componentText
      state.componentControlsPalette = !!payload.componentPalette
      state.componentControlsMenu = !!payload.componentMenu
      state.componentControlsIconCollection = !!payload.componentIcons
      state.componentControlsCKEditor = !!payload.componentCKEditor
      state.componentControlsCategories = !!payload.componentCategories
      state.componentControlsImageCrop = !!payload.componentImageCrop
      if (payload.componentPalette) {
        state.currentColorPalette = payload.palette.currentColor
      }
      state.controlsCurrentActionBtnSave = payload.actionBtnSave
      state.controlsCurrentActionBtnCancel = payload.actionBtnCancel
      state.controlsDialog = true
    },
    controlsDialogClose (state) { // Close
      state.controlsDialog = false
    },
    refreshCurrentColorPalette (state, color) {
      state.currentColorPalette = color
    },
    destroyComponentControlsImageCrop (state) {
      state.componentControlsImageCrop = false
    },
    // Message -------------------------------------------------------------------------------------
    messageDialogShow (state, payload) { // Open
      state.statusMessageDialog = payload.status
      state.titleMessageDialog = payload.title
      state.textMessageDialog = payload.text
      state.messageCancelBtn = payload.cancelBtn // Show/Hide
      state.messageOkBtn = payload.okBtn // Show/Hide
      state.messageCurrentActionBtnCancel = payload.actionBtnCancel
      state.messageCurrentActionBtnOk = payload.actionBtnOk
      state.messageDialog = true
    },
    messageDialogClose (state) { // Close
      state.messageDialog = false
    },
    // Simple messages -----------------------------------------------------------------------------
    alertSnackbarShow (state, text) { // Open
      state.textSnackbar = text
      state.alertSnackbar = true
    },
    alertSnackbarClose (state) { // Close
      state.alertSnackbar = false
    },
    // Global progress bar -------------------------------------------------------------------------
    globalProgressBarShow (state, flag) { // Open/Close
      state.globalProgressBar = flag
    }
  },
  actions: {
    // Ajax - Error processing.
    ajaxErrorProcessing ({ commit }, payload) {
      const jqxhr = payload.jqxhr
      const textStatus = payload.textStatus
      const error = payload.error
      const err = `${textStatus} , ${error}`
      const hint = payload.hint
      let errDetail = ''

      if (jqxhr.responseJSON !== undefined &&
        jqxhr.responseJSON.detail !== undefined) {
        errDetail = jqxhr.responseJSON.detail
        window.console.log(`Request Failed: ${err} - ${errDetail}`)
        commit('messageDialogShow', {
          status: 'error',
          title: i18n.t('message.86'),
          text: `${errDetail} <br>Hint: ${hint}`,
          cancelBtn: true,
          okBtn: false,
          actionBtnCancel: () => commit('messageDialogClose'),
          actionBtnOk: null
        })
      } else {
        const msg = `ERROR<br>Request Failed -> ${err}`
        window.console.log(msg)
        commit('alertSnackbarShow', `${msg} <br>Hint -> ${hint}`)
      }
    }
  }
}
