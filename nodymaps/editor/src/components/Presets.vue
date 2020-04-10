<!--
--------------------------------
Component for setting of Presets.
--------------------------------
-->
<template>
  <v-container fluid>
    <v-expansion-panels v-model="panel" accordion focusable>
      <v-expansion-panel v-for="(control, index) in controls" :key="`panel-${index}`">
        <v-expansion-panel-header>
          <span>
            <v-icon class="pb-1 pr-2">{{ control.icon }}</v-icon>
            {{ control.title }}
          </span>
          <template v-slot:actions>
            <v-icon :color="colorControlsTheme">$expand</v-icon>
          </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-simple-table>
            <template v-slot:default>
              <tbody>
                <tr>
                  <td colspan="2" class="pt-2">
                    <v-card-title class="subtitle-1 pa-0">{{ $t('message.62') }}</v-card-title>
                    <v-text-field
                      dense
                      outlined
                      type="number"
                      v-model="controls[index].position"
                      min="0"
                      :rules="rulesPosition()"
                      :color="colorControlsTheme"
                    ></v-text-field>
                  </td>
                </tr>
                <tr
                  v-for="(item, index2) in injections()"
                  :key="`injection-${control.id}-${index2}`"
                >
                  <td width="56">
                    <v-icon>{{ item.icon }}</v-icon>
                  </td>
                  <td class="py-2">
                    <v-switch
                      v-model="controls[index][item.title]"
                      inset
                      hide-details
                      :label="$t(`message.${item.trans}`)"
                      :color="colorControlsTheme"
                      class="mt-0 pt-0"
                    ></v-switch>
                  </td>
                </tr>
                <tr>
                  <td colspan="2" class="pt-3 pb-1">
                    <v-card-title class="subtitle-1 px-0 pt-0 pb-2">{{ $t('message.66') }}</v-card-title>
                    <v-row no-gutters>
                      <template v-for="(item, index3) in targets()">
                        <v-col cols="1" :key="`target-icon-${control.id}-${index3}`" class="mb-3">
                          <v-icon>{{ item.icon }}</v-icon>
                        </v-col>
                        <v-col
                          cols="3"
                          :key="`switch-target-${control.id}-${index3}`"
                          class="pl-2 pr-3 mb-3"
                        >
                          <v-switch
                            v-model="controls[index][item.title]"
                            inset
                            hide-details
                            class="mt-0 pt-0"
                            :color="colorControlsTheme"
                          ></v-switch>
                        </v-col>
                      </template>
                    </v-row>
                  </td>
                </tr>
                <tr>
                  <td colspan="2" class="pt-3">
                    <v-card-title class="subtitle-1 pa-0">{{ $t('message.67') }}</v-card-title>
                    <v-card-text v-html="control.description"></v-card-text>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
          <v-card-actions class="pt-0 pb-1">
            <v-spacer></v-spacer>
            <v-btn small fab depressed :color="colorControlsTheme" @click="saveUpdate(control.id)">
              <v-icon :color="colorButtonsTextTheme">mdi-content-save</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

export default {
  name: 'Presets',
  data: () => ({}),
  computed: {
    ...mapState('presets', [
      'panel',
      'controls'
    ]),
    ...mapState('generalSettings', [
      'colorControlsTheme',
      'colorButtonsTextTheme'
    ])
  },
  methods: {
    ...mapMutations([
      'setMapSettingsDrawer'
    ]),
    ...mapMutations('modals', [
      // Message
      'messageDialogShow', // Open
      'messageDialogClose' // Close
    ]),
    ...mapActions('presets', [
      'setDataActionAjaxUpdate',
      'actionAjaxUpdate'
    ]),
    // Rules
    rulesPosition () {
      return [
        num => (!!num || num === 0) || this.$t('message.53'),
        num => +num >= 0 || `${this.$t('message.54')} = 0`
      ]
    },
    /* Optimization of HTML code repetitions for injection positioning.
       (Оптимизация повторов HTML-кода для позиционирования инъекций.) */
    injections () {
      return [
        { icon: 'mdi-page-layout-header', title: 'autoheader', trans: 63 },
        { icon: 'mdi-page-layout-body', title: 'autobody', trans: 64 },
        { icon: 'mdi-page-layout-footer', title: 'autofooter', trans: 65 }
      ]
    },
    /* Optimization of HTML code repetitions for the type of geo objects.
       (Оптимизация повторов HTML-кода для типа геообъектов.) */
    targets () {
      return [
        { icon: 'mdi-map-marker', title: 'placemark' },
        { icon: 'mdi-routes', title: 'polyline' },
        { icon: 'mdi-beach', title: 'polygon' },
        { icon: 'mdi-circle', title: 'circle' },
        { icon: 'mdi-rectangle', title: 'rectangle' }
      ].slice(0, 3)
    },
    saveUpdate (id) {
      this.setMapSettingsDrawer(false)
      this.setDataActionAjaxUpdate({ id: id })
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
