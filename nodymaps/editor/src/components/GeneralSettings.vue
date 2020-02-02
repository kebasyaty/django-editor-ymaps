<!--
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Component for General Settings Map and Editor.
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
-->
<template>
  <v-container fluid>
    <v-card
      :elevation="minElevation"
      v-for="(panel, title, index) in controls"
      :key="title"
      :class="title !== 'panel1_69' ? 'mt-5': ''"
    >
      <v-card-title class="subtitle-1">{{ $t(`message.${title.slice(-2)}`) }}</v-card-title>
      <v-divider></v-divider>
      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <tr v-for="(control, index2) in panel" :key="`control-${index2}`">
              <td
                width="56"
                :class="control.imgBgPanelFront !== undefined ? 'pl-2 pr-0 py-2' : control.hideGroupNamePanelFront !== undefined ? 'pt-1' : ''"
              >
                <v-icon v-if="control.icon !== undefined">{{ control.icon }}</v-icon>
                <v-img
                  v-else-if="control.imgBgPanelFront !== undefined"
                  :src="control.imgBgPanelFront || undefined"
                  width="48px"
                  max-height="100%"
                ></v-img>
              </td>
              <td
                v-if="control.layout === undefined && control.theme === undefined &&
                control.widthPanelEditor === undefined && control.widthPanelFront === undefined &&
                control.imgBgPanelFront === undefined && control.widthMapFront === undefined &&
                control.heightMapFront === undefined"
                :class="control.count === undefined ? index === 0 && index2 === 1 ? 'pt-2 pb-1' : 'auto' : 'pt-4'"
              >
                <v-switch
                  v-model="control.isActive"
                  inset
                  hide-details
                  :label="$t(`message.${transTitleControls[index][index2]}`)"
                  class="mt-0 pt-0"
                  :color="colorControlsTheme"
                ></v-switch>
                <div
                  v-if="index === 0 && index2 === 1"
                  class="caption warning--text pt-1"
                >{{ `(${$t('message.142')})` }}</div>
                <div v-if="control.count !== undefined" class="mt-5 mb-6">
                  <v-container fluid class="pa-0">
                    <v-row>
                      <v-col cols="3" class="pr-0 py-0">
                        <div class="sample-color">
                          <div
                            class="sample-color__selected-tone"
                            :style="`background-color: ${updateColorBackgroundCountObjects};`"
                          ></div>
                        </div>
                      </v-col>
                      <v-col cols="9" class="py-0">
                        <v-btn
                          small
                          block
                          depressed
                          @click="recolorCountObjects('background')"
                          :color="colorControlsTheme"
                        >
                          <span :style="`color: ${colorButtonsTextTheme};`">{{ $t('message.76') }}</span>
                        </v-btn>
                      </v-col>
                    </v-row>
                    <v-row class="mt-1">
                      <v-col cols="3" class="pr-0 py-0 mt-2">
                        <div class="sample-color">
                          <div
                            class="sample-color__selected-tone"
                            :style="`background-color: ${updateTextColorCountObjects};`"
                          ></div>
                        </div>
                      </v-col>
                      <v-col cols="9" class="py-0">
                        <v-btn
                          small
                          block
                          depressed
                          @click="recolorCountObjects('text')"
                          class="mt-2"
                          :color="colorControlsTheme"
                        >
                          <span :style="`color: ${colorButtonsTextTheme};`">{{ $t('message.25') }}</span>
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-container>
                </div>
              </td>
              <td v-else-if="control.layout !== undefined" class="pt-3">
                <v-card-title
                  class="subtitle-1 pa-0"
                >{{ $t(`message.${transTitleControls[index][index2]}`) }}</v-card-title>
                <v-radio-group v-model="control.layout">
                  <v-radio
                    :label="$t('message.22')"
                    value="cluster#balloonTwoColumns"
                    :color="colorControlsTheme"
                  ></v-radio>
                  <v-radio
                    :label="$t('message.23')"
                    value="cluster#balloonCarousel"
                    :color="colorControlsTheme"
                  ></v-radio>
                </v-radio-group>
              </td>
              <td v-else-if="control.theme !== undefined" class="pt-3">
                <v-card-title
                  class="subtitle-1 pa-0"
                >{{ $t(`message.${transTitleControls[index][index2]}`) }}</v-card-title>
                <v-container fluid class="px-0 pt-2 pb-5">
                  <v-row>
                    <v-col cols="12">
                      <v-select
                        v-model="updateThemeType"
                        dense
                        outlined
                        hide-details
                        :label="$t('message.75')"
                        :items="getItemsTheme()"
                        :color="colorControlsTheme"
                        :item-color="colorControlsTheme"
                      ></v-select>
                    </v-col>
                  </v-row>
                  <v-row class="mt-2">
                    <v-col cols="3" class="pr-0 py-0">
                      <div class="sample-color mt-2">
                        <div
                          class="sample-color__selected-tone"
                          :style="`background-color: ${updateColorControlsTheme};`"
                        ></div>
                      </div>
                    </v-col>
                    <v-col cols="9" class="py-0">
                      <v-btn
                        small
                        block
                        depressed
                        @click="recolorTheme('controls')"
                        class="mt-2"
                        :color="colorControlsTheme"
                      >
                        <span :style="`color: ${colorButtonsTextTheme};`">{{ $t('message.72') }}</span>
                      </v-btn>
                    </v-col>
                  </v-row>
                  <v-row class="mt-3">
                    <v-col cols="3" class="pr-0 py-0">
                      <div class="sample-color">
                        <div
                          class="sample-color__selected-tone"
                          :style="`background-color: ${updateColorButtonsTextTheme};`"
                        ></div>
                      </div>
                    </v-col>
                    <v-col cols="9" class="py-0">
                      <v-btn
                        small
                        block
                        depressed
                        @click="recolorTheme('buttons')"
                        :color="colorControlsTheme"
                      >
                        <span :style="`color: ${colorButtonsTextTheme};`">{{ $t('message.24') }}</span>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </td>
              <td v-else-if="control.widthPanelEditor !== undefined" class="pt-6">
                <v-text-field
                  v-model="panel[index2].widthPanelEditor"
                  :label="$t('message.81')"
                  outlined
                  dense
                  full-width
                  type="number"
                  min="300"
                  :color="colorControlsTheme"
                  :rules="rulesWidthPanel(300)"
                  @input="actionRefreshWidthPanelEditor()"
                ></v-text-field>
              </td>
              <td v-else-if="control.widthPanelFront !== undefined" class="pt-6">
                <v-text-field
                  v-model="panel[index2].widthPanelFront"
                  :label="$t('message.81')"
                  outlined
                  dense
                  full-width
                  type="number"
                  min="260"
                  :color="colorControlsTheme"
                  :rules="rulesWidthPanel(260)"
                ></v-text-field>
              </td>
              <td v-else-if="control.imgBgPanelFront !== undefined" class="py-2">
                <v-container fluid class="pa-0">
                  <v-row>
                    <v-col cols="12" class="pt-0 pb-1">
                      <v-card-title class="subtitle-1 pa-0">{{ $t('message.131') }}</v-card-title>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="8" class="py-0">
                      <v-btn
                        small
                        block
                        depressed
                        @click="addImgBgPanelFront()"
                        :color="colorControlsTheme"
                      >
                        <v-icon :color="colorButtonsTextTheme">mdi-plus-thick</v-icon>
                      </v-btn>
                    </v-col>
                    <v-col cols="4" class="py-0">
                      <v-btn
                        small
                        block
                        depressed
                        @click="delImgBgPanelFront()"
                        color="red darken-3"
                        :disabled="disabledBtnDelImgBgPanelFront"
                      >
                        <v-icon color="grey lighten-5">mdi-trash-can-outline</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="3" class="pr-0">
                      <div class="sample-color">
                        <div
                          class="sample-color__selected-tone"
                          :style="`background-color: ${updateTintingPanelFront};`"
                        ></div>
                      </div>
                    </v-col>
                    <v-col cols="9">
                      <v-btn
                        small
                        block
                        depressed
                        @click="recolorTintingPanelFront()"
                        :color="colorControlsTheme"
                      >
                        <span :style="`color: ${colorButtonsTextTheme};`">{{ $t('message.133') }}</span>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </td>
              <td v-else-if="control.widthMapFront !== undefined" class="pt-1 pb-2">
                <v-card-title class="subtitle-1 py-0 px-0">{{ $t('message.132') }}</v-card-title>
                <v-text-field
                  v-model="panel[index2].widthMapFront"
                  outlined
                  dense
                  full-width
                  hide-details
                  :color="colorControlsTheme"
                ></v-text-field>
              </td>
              <td v-else-if="control.heightMapFront !== undefined" class="pt-1 pb-2">
                <v-card-title class="subtitle-1 py-0 px-0">{{ $t('message.138') }}</v-card-title>
                <v-text-field
                  v-model="panel[index2].heightMapFront"
                  outlined
                  dense
                  full-width
                  hide-details
                  :color="colorControlsTheme"
                ></v-text-field>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-card-actions :class="addStyleBtnSave(index)">
        <v-spacer></v-spacer>
        <v-btn fab small depressed :color="colorControlsTheme" @click="saveUpdate(index)">
          <v-icon :color="colorButtonsTextTheme">mdi-content-save</v-icon>
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

export default {
  name: 'GeneralSettings',
  data: () => ({
    // Translations - Titles for controls.
    transTitleControls: [
      { 0: 26, 1: 104, 2: 29, 3: 30, 4: 28 },
      { 0: 27 },
      { 0: 27, 2: 130 }
    ]
  }),
  computed: {
    ...mapState('generalSettings', [
      'controls',
      // Colors for Theme.
      'themeType',
      'colorControlsTheme',
      'colorButtonsTextTheme',
      'minElevation',
      // Colors - Display the number of objects in the cluster icon.
      'colorBackgroundCountObjects',
      'textColorCountObjects',
      // Panel tinting on front page.
      'tintingPanelFront',
      // Disabling of button - Delete image background for Panel on front page.
      'disabledBtnDelImgBgPanelFront'
    ]),
    // Refresh current color background - Count of objects in the cluster.
    updateColorBackgroundCountObjects: {
      get () {
        return this.colorBackgroundCountObjects
      },
      set (newColor) {
        this.refreshColorBackgroundCountObjects(newColor)
      }
    },
    // Refresh current text color - Count of objects in the cluster.
    updateTextColorCountObjects: {
      get () {
        return this.textColorCountObjects
      },
      set (newColor) {
        this.refreshTextColorCountObjects(newColor)
      }
    },
    // Update type theme (dark or light).
    updateThemeType: {
      get () {
        return this.themeType
      },
      set (newType) {
        this.actionThemeType(newType)
      }
    },
    // Refresh current color of controls.
    updateColorControlsTheme: {
      get () {
        return this.colorControlsTheme
      },
      set (newColor) {
        this.refreshColorControlsTheme(newColor)
      }
    },
    // Refresh current color of text on buttons.
    updateColorButtonsTextTheme: {
      get () {
        return this.colorButtonsTextTheme
      },
      set (newColor) {
        this.refreshColorButtonsTextTheme(newColor)
      }
    },
    // Panel tinting on front page.
    updateTintingPanelFront: {
      get () {
        return this.tintingPanelFront
      },
      set (newColor) {
        this.refreshTintingPanelFront(newColor)
      }
    }
  },
  methods: {
    ...mapMutations([
      'setMapSettingsDrawer',
      'setDataAction'
    ]),
    ...mapMutations('modals', [
      // Controls
      'controlsDialogShow', // Open
      'controlsDialogClose', // Close
      'destroyComponentControlsImageCrop', // Show/Hide
      // Message
      'messageDialogShow', // Open
      'messageDialogClose', // Close
      // Simple messages
      'alertSnackbarClose' // Close
    ]),
    ...mapMutations('generalSettings', [
      'refreshColorControlsTheme',
      'refreshColorButtonsTextTheme',
      'refreshColorBackgroundCountObjects',
      'refreshTextColorCountObjects',
      'refreshTintingPanelFront',
      'setDataActionPalette',
      'setDataActionSaveUpdate'
    ]),
    ...mapActions('generalSettings', [
      'actionThemeType',
      'actionPalette',
      'actionAjaxUpdate',
      'actionRefreshWidthPanelEditor',
      'actionRefreshImgBgPanelFront',
      'actionDeleteImgBgPanelFront'
    ]),
    // Get Items for Map Type.
    getItemsTheme () {
      return [
        { text: this.$t('message.74'), value: 'light' },
        { text: this.$t('message.73'), value: 'dark' }
      ]
    },
    // Styles for Button "Save".
    addStyleBtnSave (index) {
      let result = ''
      switch (index) {
        case 0:
          result = 'pt-2 pb-5'
          break
        case 1:
          result = 'pt-0 pb-5'
          break
        case 2:
          result = 'py-5'
          break
      }
      return result
    },
    // Count of objects in the cluster - Change color.
    recolorCountObjects (target) { // target - background or text.
      this.setMapSettingsDrawer(false)
      this.setDataActionPalette({
        target: {
          background: 'colorBackgroundCountObjects',
          text: 'textColorCountObjects'
        }[target]
      })
      this.controlsDialogShow({
        title: { background: this.$t('message.76'), text: this.$t('message.25') }[target],
        text: '',
        cancelBtn: true,
        saveBtn: true,
        componentPalette: true,
        palette: {
          currentColor: {
            background: this.colorBackgroundCountObjects,
            text: this.textColorCountObjects
          }[target]
        },
        actionBtnCancel: () => {
          this.controlsDialogClose()
          this.setMapSettingsDrawer(true)
        },
        actionBtnSave: this.actionPalette
      })
    },
    // Recolor for theme of Editor maps.
    recolorTheme (target) { // target - background or controls.
      this.setMapSettingsDrawer(false)
      this.setDataActionPalette({
        target: {
          controls: 'colorControlsTheme',
          buttons: 'colorButtonsTextTheme'
        }[target]
      })
      this.controlsDialogShow({
        title: { buttons: this.$t('message.24'), controls: this.$t('message.72') }[target],
        text: '',
        cancelBtn: true,
        saveBtn: true,
        componentPalette: true,
        palette: {
          currentColor: {
            controls: this.colorControlsTheme,
            buttons: this.colorButtonsTextTheme
          }[target]
        },
        actionBtnCancel: () => {
          this.controlsDialogClose()
          this.setMapSettingsDrawer(true)
        },
        actionBtnSave: this.actionPalette
      })
    },
    // Panel tinting on front page.
    recolorTintingPanelFront () {
      this.setMapSettingsDrawer(false)
      this.setDataActionPalette({ target: 'tintingPanelFront' })
      this.controlsDialogShow({
        title: this.$t('message.133'),
        text: '',
        cancelBtn: true,
        saveBtn: true,
        componentPalette: true,
        palette: { currentColor: this.tintingPanelFront },
        actionBtnCancel: () => {
          this.controlsDialogClose()
          this.setMapSettingsDrawer(true)
        },
        actionBtnSave: this.actionPalette
      })
    },
    // Save changed of settings.
    saveUpdate (index) {
      this.setMapSettingsDrawer(false)
      this.setDataActionSaveUpdate({ reloadPage: index < 2 })
      this.messageDialogShow({
        status: 'accent',
        title: this.$t('message.85'),
        text: this.$t('message.44'),
        cancelBtn: true,
        okBtn: true,
        actionBtnCancel: () => {
          this.messageDialogClose()
          this.setMapSettingsDrawer(true)
        },
        actionBtnOk: this.actionAjaxUpdate
      })
    },
    // Rules
    rulesWidthPanel (minNum) {
      return [
        num => !!num || this.$t('message.53'),
        num => +num >= 300 || `${this.$t('message.54')} = ${minNum}`
      ]
    },
    // Add image for panel background.
    addImgBgPanelFront () {
      this.setDataAction({
        options: {
          type: 'base64',
          format: 'jpeg',
          quality: '0.4',
          size: {
            width: 800
          },
          circle: false
        }
      })
      this.setMapSettingsDrawer(false)
      this.controlsDialogShow({
        title: this.$t('message.136'),
        text: '',
        cancelBtn: true,
        saveBtn: true,
        componentImageCrop: true,
        actionBtnCancel: () => {
          this.alertSnackbarClose()
          this.destroyComponentControlsImageCrop()
          this.controlsDialogClose()
          this.setMapSettingsDrawer(true)
        },
        actionBtnSave: () => {
          this.alertSnackbarClose()
          this.destroyComponentControlsImageCrop()
          this.actionRefreshImgBgPanelFront()
          this.controlsDialogClose()
          this.setMapSettingsDrawer(true)
        }
      })
    },
    // Delete the background image for the panel.
    delImgBgPanelFront () {
      this.setMapSettingsDrawer(false)
      this.messageDialogShow({
        status: 'accent',
        title: this.$t('message.85'),
        text: this.$t('message.44'),
        cancelBtn: true,
        okBtn: true,
        actionBtnCancel: () => {
          this.messageDialogClose()
          this.setMapSettingsDrawer(true)
        },
        actionBtnOk: this.actionDeleteImgBgPanelFront
      })
    }
  }
}
</script>

<style scoped>
/* To display the current color -
   Display the number of objects on the cluster icon */
.sample-color {
  width: 100%;
  height: 28px;
  position: relative;
  border: 1px solid #bdbdbd;
  background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAGElEQVQYlWNgYGCQwoKxgqGgcJA5h3yFAAs8BRWVSwooAAAAAElFTkSuQmCC')
    repeat;
}
.sample-color__selected-tone {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}
</style>
