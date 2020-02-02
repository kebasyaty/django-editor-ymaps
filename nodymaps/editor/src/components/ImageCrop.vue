<!--
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Component for for cropping images.
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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
        :enableOrientation="true"
        :enforceBoundary="true"
        :mouseWheelZoom="false"
        :enableResize="false"
        :showZoomer="false"
        :enableZoom="true"
        :boundary="{ width: 300, height: 300, type: 'square'}"
        :viewport="{ width: 100, height: 250, type: 'square'}"
      ></vue-croppie>
    </v-row>
    <v-row align="center" justify="center" class="pa-3">
      <!-- Rotate angle is Number -->
      <v-btn fab small depressed :color="colorControlsTheme" @click="rotate(-90)" class="mx-1">
        <v-icon :color="colorButtonsTextTheme">mdi-rotate-left</v-icon>
      </v-btn>
      <v-btn fab small depressed :color="colorControlsTheme" @click="rotate(90)" class="mx-1">
        <v-icon :color="colorButtonsTextTheme">mdi-rotate-right</v-icon>
      </v-btn>
      <v-btn fab small depressed :color="colorControlsTheme" @click="crop()" class="mx-1">
        <v-icon :color="colorButtonsTextTheme">mdi-crop</v-icon>
      </v-btn>
    </v-row>
  </v-conteiner>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'ImageCrop',

  data: () => ({
    currImg: null
  }),
  computed: {
    ...mapState([
      'dataAction'
    ]),
    ...mapState('generalSettings', [
      // Colors for Theme.
      'colorControlsTheme',
      'colorButtonsTextTheme'
    ])
  },
  methods: {
    ...mapMutations([
      'setCurrentImageCrop'
    ]),
    ...mapMutations('modals', [
      // Simple messages
      'alertSnackbarShow', // Open
      'alertSnackbarClose' // Close
    ]),
    // Rotates the image.
    rotate (rotationAngle) {
      this.$refs.croppieRef.rotate(rotationAngle)
    },
    crop () {
      if (this.currImg !== null) {
        this.$refs.croppieRef.result(this.dataAction.options, (output) => {
          this.setCurrentImageCrop(output)
        })
      } else {
        this.alertSnackbarShow(`${this.$t('message.135')} !`)
      }
    },
    newImg (file) {
      this.currImg = file
      this.alertSnackbarClose()
      // Check for the various File API support.
      if (window.File && window.FileReader && window.FileList && window.Blob) {
        if (file !== null) {
          const fr = new FileReader()
          fr.onload = () => {
            // Transfer the image for cropping.
            this.$refs.croppieRef.bind({
              url: fr.result
            })
          }
          fr.readAsDataURL(file)
        }
      } else {
        this.alertSnackbarShow(this.$t('message.137'))
      }
    },
    mounted () {
      this.$refs.croppieRef.refresh()
      // Transfer the image for cropping.
      this.$refs.croppieRef.bind({
        url: window.djeymDefaultImageCrop,
        orientation: 1
      })
    },
    beforeDestroy () {
      this.currImg = null
      this.$refs.croppieRef.destroy()
    }
  }
}
</script>
