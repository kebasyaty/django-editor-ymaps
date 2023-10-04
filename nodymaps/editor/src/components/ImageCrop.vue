<!--
------------------------------
Component for cropping images.
------------------------------
-->
<template>
  <v-conteiner fluid>
    <v-row class="pa-3">
      <v-file-input
        :label="$t('message.135')"
        outlined
        dense
        prepend-icon="mdi-camera"
        accept="image/jpeg"
        hide-details
        full-width
        :color="colorControlsTheme"
        @change="newImg"
      ></v-file-input>
    </v-row>
    <v-row align="center" justify="center">
      <vue-croppie
        ref="croppieRef"
        :enable-orientation="true"
        :enforce-boundary="true"
        :mouse-wheel-zoom="false"
        :enable-resize="false"
        :show-zoomer="false"
        :enable-zoom="true"
        :boundary="{ width: 300, height: 300, type: 'square' }"
        :viewport="{ width: 100, height: 250, type: 'square' }"
      ></vue-croppie>
    </v-row>
    <v-row align="center" justify="center" class="pa-3">
      <!-- Button - Rotate angle is Number -->
      <!--
      <v-btn
        fab
        small
        depressed
        :color="colorControlsTheme"
        @click="btnRotate(-90)"
        class="mx-1"
      >
        <v-icon :color="colorButtonsTextTheme">mdi-rotate-left</v-icon>
      </v-btn>
      <v-btn
        fab
        small
        depressed
        :color="colorControlsTheme"
        @click="btnRotate(90)"
        class="mx-1"
      >
        <v-icon :color="colorButtonsTextTheme">mdi-rotate-right</v-icon>
      </v-btn>
      -->
      <!-- Button - Cropping  -->
      <v-btn
        fab
        small
        depressed
        :color="colorControlsTheme"
        @click="btnCrop()"
        class="mx-1"
      >
        <v-icon :color="colorButtonsTextTheme">mdi-crop</v-icon>
      </v-btn>
      <!-- Button - Cancel  -->
      <v-btn
        fab
        small
        depressed
        :color="colorControlsTheme"
        @click="btnCancel()"
        class="mx-1"
      >
        <v-icon :color="colorButtonsTextTheme">mdi-close-thick</v-icon>
      </v-btn>
    </v-row>
  </v-conteiner>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
  name: "ImageCrop",

  data: () => ({
    currImg: null,
  }),
  computed: {
    ...mapState(["dataAction"]),
    ...mapState("generalSettings", [
      // Colors for Theme.
      "colorControlsTheme",
      "colorButtonsTextTheme",
    ]),
  },
  methods: {
    ...mapMutations(["setCurrentImageCrop", "setMapSettingsDrawer"]),
    ...mapMutations("modals", [
      // Simple messages
      "alertSnackbarShow", // Open
      "alertSnackbarClose", // Close
      // Controls
      "controlsDialogClose", // Close
      "destroyComponentControlsImageCrop", // Show/Hide
    ]),
    ...mapActions("generalSettings", ["actionRefreshImgBgPanelFront"]),
    // Rotates the image.
    /*
    btnRotate(rotationAngle) {
      this.$refs.croppieRef.rotate(rotationAngle);
    },
    */
    btnCrop() {
      if (this.currImg !== null) {
        this.$refs.croppieRef.result(this.dataAction.options, (output) => {
          this.setCurrentImageCrop(output);
          this.alertSnackbarClose();
          this.destroyComponentControlsImageCrop();
          this.actionRefreshImgBgPanelFront();
          this.controlsDialogClose();
          this.setMapSettingsDrawer(true);
        });
      } else {
        this.alertSnackbarShow(`${this.$t("message.135")} !`);
      }
    },
    btnCancel() {
      this.alertSnackbarClose();
      this.destroyComponentControlsImageCrop();
      this.controlsDialogClose();
      this.setMapSettingsDrawer(true);
    },
    newImg(file) {
      this.currImg = file;
      this.alertSnackbarClose();
      // Check for the various File API support.
      if (window.File && window.FileReader && window.FileList && window.Blob) {
        if (file !== null) {
          const fr = new FileReader();
          fr.onload = () => {
            // Transfer the image for cropping.
            this.$refs.croppieRef.bind({
              url: fr.result,
            });
          };
          fr.readAsDataURL(file);
        }
      } else {
        this.alertSnackbarShow(this.$t("message.137"));
      }
    },
    mounted() {
      this.$refs.croppieRef.refresh();
      // Transfer the image for cropping.
      this.$refs.croppieRef.bind({
        url: window.djeymDefaultImageCrop,
        orientation: 1,
      });
    },
    beforeDestroy() {
      this.currImg = null;
      this.$refs.croppieRef.destroy();
    },
  },
};
</script>
