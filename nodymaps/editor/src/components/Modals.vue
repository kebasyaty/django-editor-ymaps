<!--
---------------------------
Component for popup dialogs.
---------------------------
-->
<template>
  <div>
    <!-- GeoObject -->
    <v-overlay z-index="8" :value="geoObjectDialog">
      <v-card :light="!$vuetify.theme.dark" width="300px" max-width="300px">
        <v-card-title
          class="title justify-center"
          :style="`background-color:${colorControlsTheme};color:${colorButtonsTextTheme};`"
          v-html="titleGeoObjectDialog"
        ></v-card-title>
        <v-divider></v-divider>
        <v-card-text :class="componentGeoObjectPlacemark ? 'pt-5 pb-0' : 'pt-5'">
          <!-- Context Menu - Create and editable a Heat Point. -->
          <ContextmenuHeatPoint v-if="componentGeoObjectHeatPoint" />
          <!-- Context Menu - Create and editable a Placemark. -->
          <ContextmenuPlacemark v-if="componentGeoObjectPlacemark" />
          <!-- Context Menu - Create and editable a Route. -->
          <ContextmenuRoute v-if="componentGeoObjectPolyline" />
          <!-- Context Menu - Create and editable a Territory. -->
          <ContextmenuTerritory v-if="componentGeoObjectPolygon" />
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            icon
            color="grey lighten-1"
            class="px-0"
            @click="geoObjectCurrentActionBtnEdit()"
            v-show="geoObjectEditBtn"
          >
            <v-icon large v-text="getIconBtnEdit()"></v-icon>
          </v-btn>
          <v-btn
            icon
            color="grey lighten-1"
            class="px-0"
            @click="geoObjectCurrentActionBtnSave()"
            v-show="geoObjectSaveBtn"
          >
            <v-icon large>mdi-content-save-outline</v-icon>
          </v-btn>
          <v-btn
            icon
            color="grey lighten-1"
            class="px-0"
            @click="geoObjectCurrentActionBtnCancel()"
            v-show="geoObjectCancelBtn"
          >
            <v-icon large>mdi-cancel</v-icon>
          </v-btn>
          <v-btn
            icon
            color="grey lighten-1"
            class="px-0"
            @click="geoObjectCurrentActionBtnDelete()"
            v-show="geoObjectDeleteBtn"
          >
            <v-icon large>mdi-trash-can-outline</v-icon>
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-overlay>

    <!-- Controls -->
    <v-overlay z-index="9" :value="controlsDialog">
      <v-card :light="!$vuetify.theme.dark" max-height="80%">
        <v-card-title
          class="title justify-center"
          :style="controlsTitleColor(componentControlsMenu)"
          v-html="titleControlsDialog"
        ></v-card-title>
        <v-divider></v-divider>
        <v-card-text v-if="componentControlsText" v-html="textControlsDialog" class="pt-5"></v-card-text>
        <v-card-text v-if="componentControlsPalette" class="pt-5">
          <v-color-picker
            mode="hexa"
            v-model="updateCurrentColorPalette"
            hide-mode-switch
            show-swatches
          ></v-color-picker>
        </v-card-text>
        <!-- Menu - Select a type and create a geo object. -->
        <v-card-text v-if="componentControlsMenu" class="pt-5">
          <DialogCreate />
        </v-card-text>
        <!-- Icon list - Select the icon for the marker. -->
        <v-card-text v-show="componentControlsIconCollection" class="pt-5">
          <IconCollection />
        </v-card-text>
        <!-- CKEditor - Text editor. -->
        <v-card-text v-if="componentControlsCKEditor" class="px-3 py-0">
          <CKEditor />
        </v-card-text>
        <!-- Selecting a Categories. -->
        <v-card-text v-if="componentControlsCategories" class="px-3 py-0">
          <SelectingCategories />
        </v-card-text>
        <!-- Image cropping. -->
        <v-card-text v-if="componentControlsImageCrop" class="px-3 py-0" style="min-width: 324px;">
          <ImageCrop />
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            icon
            color="grey lighten-1"
            class="px-0"
            @click="controlsCurrentActionBtnSave()"
            v-show="controlsSaveBtn"
          >
            <v-icon large>mdi-content-save-outline</v-icon>
          </v-btn>
          <v-btn
            icon
            color="grey lighten-1"
            class="px-0"
            @click="controlsCurrentActionBtnCancel()"
            v-show="controlsCancelBtn"
          >
            <v-icon large>mdi-cancel</v-icon>
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-overlay>

    <!-- Message -->
    <v-dialog v-model="messageDialog" persistent max-width="500">
      <v-card :light="!$vuetify.theme.dark">
        <v-card-title class="title" :class="statusMessageDialog" v-text="titleMessageDialog"></v-card-title>
        <v-card-text class="pt-5 font-weight-bold">
          <table>
            <tr>
              <td width="56" style="position: relative; min-height: 42px;">
                <div style="position: absolute; top: 50%; margin-top: -21px;">
                  <IconStarCompass height="42" color="#BDBDBD" />
                </div>
              </td>
              <td v-html="textMessageDialog"></td>
            </tr>
          </table>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            icon
            color="grey lighten-1"
            class="px-0"
            @click="messageCurrentActionBtnCancel()"
            v-show="messageCancelBtn"
          >
            <v-icon large>mdi-cancel</v-icon>
          </v-btn>
          <v-btn
            icon
            color="grey lighten-1"
            class="px-0"
            @click="messageCurrentActionBtnOk()"
            v-show="messageOkBtn"
          >
            <v-icon large>mdi-thumb-up-outline</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Simple messages -->
    <v-snackbar v-model="alertSnackbar" top multi-line vertical :timeout="0">
      <span class="font-weight-bold" v-html="textSnackbar"></span>
      <v-btn text color="pink" @click="alertSnackbarClose()">close</v-btn>
    </v-snackbar>

    <!-- Global progress bar -->
    <v-overlay z-index="10000" :value="globalProgressBar">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import DialogCreate from '@/components/DialogCreate.vue'
import IconStarCompass from '@/components/icons/ordinary/IconStarCompass.vue'
import IconCollection from '@/components/IconCollection.vue'
import CKEditor from '@/components/CKEditor.vue'
import SelectingCategories from '@/components/SelectingCategories.vue'
import ImageCrop from '@/components/ImageCrop.vue'
import ContextmenuHeatPoint from '@/components/ContextmenuHeatPoint.vue'
import ContextmenuPlacemark from '@/components/ContextmenuPlacemark.vue'
import ContextmenuRoute from '@/components/ContextmenuRoute.vue'
import ContextmenuTerritory from '@/components/ContextmenuTerritory.vue'

export default {
  name: 'Modals',
  components: {
    DialogCreate,
    IconStarCompass,
    IconCollection,
    CKEditor,
    SelectingCategories,
    ImageCrop,
    ContextmenuHeatPoint,
    ContextmenuPlacemark,
    ContextmenuRoute,
    ContextmenuTerritory
  },
  computed: {
    ...mapState('modals', [
      // GeoObject ---------------------------------------------------------------------------------
      'geoObjectDialog', // Open/Close
      'titleGeoObjectDialog',
      'geoObjectEditBtn',
      'geoObjectSaveBtn',
      'geoObjectCancelBtn',
      'geoObjectDeleteBtn',
      'geoObjectCurrentActionBtnEdit',
      'geoObjectCurrentActionBtnSave',
      'geoObjectCurrentActionBtnCancel',
      'geoObjectCurrentActionBtnDelete',
      'componentGeoObjectHeatPoint', // Show/Hide
      'componentGeoObjectPlacemark', // Show/Hide
      'componentGeoObjectPolyline', // Show/Hide
      'componentGeoObjectPolygon', // Show/Hide
      // Controls ----------------------------------------------------------------------------------
      'controlsDialog', // Open/Close
      'titleControlsDialog',
      'textControlsDialog',
      'controlsCancelBtn',
      'controlsSaveBtn',
      'componentControlsText', // Show/Hide
      'componentControlsPalette', // Show/Hide
      'componentControlsMenu', // Show/Hide
      'componentControlsIconCollection', // Show/Hide
      'componentControlsCKEditor', // Show/Hide
      'componentControlsCategories', // Show/Hide
      'componentControlsImageCrop', // Show/Hide
      'currentColorPalette',
      'controlsCurrentActionBtnCancel',
      'controlsCurrentActionBtnSave',
      // Message -----------------------------------------------------------------------------------
      'messageDialog', // Open/Close
      'titleMessageDialog',
      'statusMessageDialog',
      'textMessageDialog',
      'messageCancelBtn',
      'messageOkBtn',
      'messageCurrentActionBtnCancel',
      'messageCurrentActionBtnOk',
      // Simple messages ---------------------------------------------------------------------------
      'alertSnackbar', // Open/Close
      'textSnackbar',
      // Global progress bar -----------------------------------------------------------------------
      'globalProgressBar'
    ]),
    ...mapState('generalSettings', [
      'colorControlsTheme',
      'colorButtonsTextTheme'
    ]),
    ...mapState('ymap', [
      'editableGeoObject'
    ]),
    // Refresh current palette color.
    updateCurrentColorPalette: {
      get () {
        return this.currentColorPalette
      },
      set (newColor) {
        this.refreshCurrentColorPalette(newColor)
      }
    }
  },
  methods: {
    ...mapMutations('modals', [
      // GeoObject
      'geoObjectDialogClose', // Close
      // Controls
      'controlsDialogClose', // Close
      'refreshCurrentColorPalette',
      // Message
      'messageDialogClose', // Close
      // Simple messages.
      'alertSnackbarClose' // Close
    ]),
    controlsTitleColor (flag) {
      return flag
        ? `background-color:${this.colorControlsTheme};color:${this.colorButtonsTextTheme};` : ''
    },
    // Get Icon for button "Edit" - Popup "geoObjectDialog".
    getIconBtnEdit () {
      let iconName
      if (this.componentGeoObjectPlacemark) {
        iconName = 'mdi-map-marker-distance'
      } else if (this.editableGeoObject !== null) {
        const coordinates = this.editableGeoObject.geometry.getCoordinates()
        try {
          if (coordinates.length > 1 || coordinates[0].length > 1) {
            iconName = 'mdi-square-edit-outline'
          } else {
            iconName = 'mdi-plus-thick'
          }
        } catch (err) {
          iconName = 'mdi-plus-thick'
        }
      }
      return iconName
    }
  }
}
</script>
