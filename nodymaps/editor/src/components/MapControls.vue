<!--
-----------------------------------
Component for setting Map Controls.
-----------------------------------
-->
<template>
  <v-container fluid>
    <v-card :elevation="minElevation">
      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <tr v-for="(control, index) in controls" :key="`control-${index}`">
              <td>
                <v-img :width="+(control.width / 3).toFixed(2)" :src="control.img"
                  :alt="$t(`message.${transMapControls[index]}`)"></v-img>
              </td>
              <td>
                <v-switch v-model="control.isActive" inset hide-details :label="$t(`message.${transMapControls[index]}`)"
                  class="mt-0 pt-0" :color="colorControlsTheme"></v-switch>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
      <v-card-actions class="py-5">
        <v-spacer></v-spacer>
        <v-btn fab small depressed :color="colorControlsTheme" @click="saveUpdate()">
          <v-icon :color="colorButtonsTextTheme">mdi-content-save</v-icon>
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
  name: "MapControls",
  data: () => ({
    // Translations of Titles
    transMapControls: [31, 32, 33, 34, 35, 36, 37, 38, 39],
  }),
  computed: {
    ...mapState("mapControls", ["controls"]),
    ...mapState("generalSettings", [
      "colorControlsTheme",
      "colorButtonsTextTheme",
      "minElevation",
    ]),
  },
  methods: {
    ...mapMutations(["setMapSettingsDrawer"]),
    ...mapMutations("modals", [
      // Message
      "messageDialogShow", // Open
      "messageDialogClose", // Close
    ]),
    ...mapActions("mapControls", ["actionAjaxUpdate"]),
    saveUpdate() {
      this.setMapSettingsDrawer(false);
      this.messageDialogShow({
        status: "accent",
        title: this.$t("message.85"),
        text: this.$t("message.44"),
        cancelBtn: true,
        okBtn: true,
        actionBtnCancel: () => {
          this.messageDialogClose();
          this.setMapSettingsDrawer(true);
        },
        actionBtnOk: this.actionAjaxUpdate,
      });
    },
  },
};
</script>
