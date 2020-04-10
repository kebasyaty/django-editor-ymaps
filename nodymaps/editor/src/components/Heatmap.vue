<!--
---------------------------------
Component for setting of Heat map.
---------------------------------
-->
<template>
  <v-container fluid>
    <v-card
      v-for="panelNum in 2"
      :key="`panel-${panelNum}`"
      :class="`mt-${panelNum === 2 ? 8 : 0 }`"
      :elevation="minElevation"
    >
      <template v-if="panelNum === 1">
        <v-card-text class="py-0">
          <v-container fluid class="pa-0">
            <v-row>
              <v-col cols="12">
                <v-switch
                  v-model="controls.panel1.isActive"
                  inset
                  hide-details
                  :label="$t('message.46')"
                  class="mt-0 pt-0"
                  :color="colorControlsTheme"
                  @change="saveUpdate()"
                ></v-switch>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-btn small block depressed color="orange darken-3" @click="resetByDefault()">
                  <v-icon color="grey darken-4" class="mr-2">mdi-restart</v-icon>
                  <span class="grey--text text--darken-4">{{ $t('message.47') }}</span>
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </template>
      <template v-else>
        <v-simple-table>
          <template v-slot:default>
            <tbody>
              <tr v-for="(val, key, index) in controls.panel2" :key="`control-${key}`">
                <td :class="key !== 'dissipating' ? 'pb-1' : 'pb-0'">
                  <v-card-title
                    v-if="key !== 'dissipating'"
                    class="subtitle-1 pb-0"
                  >{{ $t(`message.${transSettings[index]}`) }}</v-card-title>
                  <v-card-actions class="mb-0">
                    <template v-if="key === 'gradient'">
                      <v-container fluid class="pa-0">
                        <v-row>
                          <v-col
                            cols="3"
                            v-for="(color, title, index2) in val"
                            :key="title"
                            class="pa-0 text-center"
                          >
                            <v-btn
                              fab
                              small
                              depressed
                              :color="[updateGradientColor1, updateGradientColor2, updateGradientColor3, updateGradientColor4][index2]"
                              @click="recolor(title)"
                            ></v-btn>
                          </v-col>
                        </v-row>
                      </v-container>
                    </template>
                    <template v-else-if="key === 'radius'">
                      <v-text-field
                        outlined
                        dense
                        type="number"
                        v-model="controls.panel2.radius"
                        min="1"
                        :rules="rulesRadius()"
                        class="py-0 my-0"
                        :color="colorControlsTheme"
                        @input="actionRefreshRadius()"
                      ></v-text-field>
                    </template>
                    <template v-else-if="key === 'dissipating'">
                      <v-switch
                        v-model="controls.panel2.dissipating"
                        inset
                        hide-details
                        :label="$t('message.50')"
                        class="mt-0 pt-0"
                        :color="colorControlsTheme"
                        @change="actionRefreshDissipating()"
                      ></v-switch>
                    </template>
                    <template v-else-if="key === 'opacity' || key === 'intensity'">
                      <span class="subtitle-2 pr-1">{{ controls.panel2[key] }}</span>
                      <v-slider
                        v-model="controls.panel2[key]"
                        :track-color="$vuetify.theme.dark ? 'grey darken-1' : 'grey lighten-2'"
                        min="0.1"
                        max="1"
                        step="0.1"
                        thumb-label
                        hide-details
                        :color="colorControlsTheme"
                        @input="key === 'opacity' ? actionRefreshOpacity() : actionRefreshIntensity()"
                      ></v-slider>
                    </template>
                  </v-card-actions>
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
        <v-card-actions class="pt-0 pb-5">
          <v-spacer></v-spacer>
          <v-btn small fab depressed :color="colorControlsTheme" @click="saveUpdate()">
            <v-icon :color="colorButtonsTextTheme">mdi-content-save</v-icon>
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </template>
    </v-card>
  </v-container>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

export default {
  name: 'Heatmap',
  data: () => ({
    // Translations of Titles
    transSettings: [48, 49, 50, 51, 52]
  }),
  computed: {
    ...mapState('heatmap', [
      'controls'
    ]),
    ...mapState('generalSettings', [
      'colorControlsTheme',
      'colorButtonsTextTheme',
      'minElevation'
    ]),
    // Refresh colors of Gradient
    updateGradientColor1: {
      get () {
        return this.controls.panel2.gradient.color1
      },
      set (newColor) {
        this.refreshGradientColor1(newColor)
      }
    },
    updateGradientColor2: {
      get () {
        return this.controls.panel2.gradient.color2
      },
      set (newColor) {
        this.refreshGradientColor2(newColor)
      }
    },
    updateGradientColor3: {
      get () {
        return this.controls.panel2.gradient.color3
      },
      set (newColor) {
        this.refreshGradientColor3(newColor)
      }
    },
    updateGradientColor4: {
      get () {
        return this.controls.panel2.gradient.color4
      },
      set (newColor) {
        this.refreshGradientColor4(newColor)
      }
    }
  },
  methods: {
    ...mapMutations([
      'setMapSettingsDrawer'
    ]),
    ...mapMutations('heatmap', [
      // Refresh Gradient Color
      'refreshGradientColor1',
      'refreshGradientColor2',
      'refreshGradientColor3',
      'refreshGradientColor4',
      'setDataActionPalette'
    ]),
    ...mapMutations('modals', [
      // Controls
      'controlsDialogShow', // Open
      'controlsDialogClose', // Close
      // Message
      'messageDialogShow', // Open
      'messageDialogClose' // Close
    ]),
    ...mapActions('heatmap', [
      'actionPalette',
      'actionReset',
      'actionAjaxUpdate',
      'actionRefreshRadius',
      'actionRefreshDissipating',
      'actionRefreshOpacity',
      'actionRefreshIntensity'
    ]),
    // Recolor colors of gradient
    recolor (target) { // target - from color1 to color4
      this.setMapSettingsDrawer(false)
      const numColor = target.slice(-1)
      this.setDataActionPalette({ numColor: numColor })
      this.controlsDialogShow({
        title: `${this.$t('message.48')} - ${target[0].toUpperCase() + target.slice(1, 5) + ' ' + numColor}`,
        text: '',
        cancelBtn: true,
        saveBtn: true,
        componentPalette: true,
        palette: { currentColor: this[`updateGradientColor${numColor}`] },
        actionBtnSave: this.actionPalette,
        actionBtnCancel: () => {
          this.controlsDialogClose()
          this.setMapSettingsDrawer(true)
        }
      })
    },
    // Rules
    rulesRadius () {
      return [
        num => !!num || this.$t('message.53'),
        num => (+num > 0) || `${this.$t('message.54')} = 1`
      ]
    },
    // Reset by default
    resetByDefault () {
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
        actionBtnOk: this.actionReset
      })
    },
    saveUpdate () {
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
        actionBtnOk: this.actionAjaxUpdate
      })
    }
  }
}
</script>
