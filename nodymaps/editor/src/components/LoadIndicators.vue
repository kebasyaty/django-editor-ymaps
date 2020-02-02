<!--
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Component for setting Upload indicator.
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
-->
<template>
  <v-container fluid>
    <v-card :elevation="minElevation">
      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <template v-for="(val, key, index) in controls">
              <tr v-if="key !== 'currentIndicator'" :key="`control-${key}`">
                <td class="pb-2">
                  <v-card-title
                    v-if="key !== 'disableAnimation'"
                    :class="`subtitle-1${key === 'size' ? ' pb-0' : ''}`"
                  >
                    <v-container fluid class="pa-0">
                      <v-row>
                        <v-col cols="12" class="pa-0">{{ $t(`message.${transTitles[index]}`) }}</v-col>
                        <v-col
                          cols="12"
                          v-if="key === 'speed'"
                          class="body-2 font-italic pl-1 pr-0 py-0"
                          v-html="`( ${$t('message.59')} <span class='font-weight-bold'>${controls.speed}</span> ${$t('message.60')} )`"
                        ></v-col>
                      </v-row>
                    </v-container>
                  </v-card-title>
                  <v-card-actions :class="key === 'disableAnimation' ? 'pt-3' : 'pt-0'">
                    <template v-if="key === 'indicators'">
                      <v-container fluid class="pa-0">
                        <v-row v-for="item in val" :key="`indicator-${item.slug}`">
                          <v-col cols="2">
                            <v-img :src="item.img"></v-img>
                          </v-col>
                          <v-col cols="10">
                            <v-switch
                              v-model="updateCurrentIndicator"
                              inset
                              :value="item.slug"
                              hide-details
                              :label="item.title"
                              class="mt-0"
                              :color="colorControlsTheme"
                            ></v-switch>
                          </v-col>
                        </v-row>
                      </v-container>
                    </template>
                    <template v-else-if="key === 'size'">
                      <v-radio-group v-model="updateSize" row mandatory hide-details>
                        <v-radio
                          v-for="size in [64, 96, 128]"
                          :key="`size-${size}`"
                          :label="size.toString()"
                          :value="size"
                          :color="colorControlsTheme"
                        ></v-radio>
                      </v-radio-group>
                    </template>
                    <template v-else-if="key === 'speed'">
                      <v-slider
                        v-model="updateSpeed"
                        :track-color="$vuetify.theme.dark ? 'grey darken-1' : 'grey lighten-2'"
                        min="0.1"
                        max="1"
                        step="0.1"
                        thumb-label
                        hide-details
                        :color="colorControlsTheme"
                      ></v-slider>
                    </template>
                    <template v-else-if="key === 'disableAnimation'">
                      <v-icon color="red" class="mr-3 pt-1">mdi-cancel</v-icon>
                      <v-switch
                        v-model="controls.disableAnimation"
                        inset
                        hide-details
                        :label="$t('message.58')"
                        class="mt-0"
                        :color="colorControlsTheme"
                      ></v-switch>
                    </template>
                  </v-card-actions>
                </td>
              </tr>
            </template>
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
    </v-card>
  </v-container>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

export default {
  name: 'LoadIndicators',
  data: () => ({
    transTitles: [55, 56, 57]
  }),
  computed: {
    ...mapState('loadIndicators', [
      'controls'
    ]),
    ...mapState('generalSettings', [
      'colorControlsTheme',
      'colorButtonsTextTheme',
      'minElevation'
    ]),
    updateSize: {
      get () {
        return this.controls.size
      },
      set (value) {
        this.setSize(value)
      }
    },
    updateSpeed: {
      get () {
        return this.controls.speed
      },
      set (value) {
        this.setSpeed(value)
      }
    },
    updateCurrentIndicator: {
      get () {
        return this.controls.currentIndicator
      },
      set (value) {
        this.setCurrentIndicator(value)
      }
    }
  },
  methods: {
    ...mapMutations([
      'setMapSettingsDrawer'
    ]),
    ...mapMutations('loadIndicators', [
      'setSize',
      'setSpeed',
      'setCurrentIndicator'
    ]),
    ...mapMutations('modals', [
      // Message
      'messageDialogShow', // Open
      'messageDialogClose' // Close
    ]),
    ...mapActions('loadIndicators', [
      'actionAjaxUpdate'
    ]),
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
