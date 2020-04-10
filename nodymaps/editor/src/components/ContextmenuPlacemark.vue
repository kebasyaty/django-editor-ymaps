<!--
----------------------------------------------
Component for creating and editable Placemarks.
----------------------------------------------
-->
<template>
  <v-conteiner fluid>
    <!-- Buttons - Header, Body, Footer, Categories and Subcategories. -->
    <v-row align="center" justify="center">
      <v-btn
        v-for="(icon, index) in icons"
        :key="`action-btn-${index}`"
        small
        fab
        depressed
        :color="colorControlsTheme"
        class="mx-1"
        @click="openDialog(index)"
      >
        <v-icon :color="colorButtonsTextTheme">{{ icons[index] }}</v-icon>
      </v-btn>
    </v-row>
    <!-- Marker Icon -->
    <v-row align="center" justify="center">
      <v-col cols="12" class="px-0 pt-7 pb-0">
        <v-img
          :src="updateIconUrl"
          contain
          max-width="100%"
          max-height="60px"
          class="icon-marker"
          @click="openIconCollection()"
        ></v-img>
      </v-col>
    </v-row>
    <!-- Coordinates - Latitude and Longitude. -->
    <v-row class="pt-5">
      <v-col cols="12" class="py-0">
        <v-text-field
          id="id-djeym-latitude"
          v-model="updateLatitude"
          :label="$t('message.90')"
          :placeholder="$t('message.90')"
          hint="-90.0 ... 90.0"
          outlined
          clearable
          dense
          full-width
          maxlength="19"
          :rules="rulesLatitude()"
          :color="colorControlsTheme"
        ></v-text-field>
      </v-col>
      <v-col cols="12" class="py-0">
        <v-text-field
          id="id-djeym-longitude"
          v-model="updateLongitude"
          :label="$t('message.91')"
          :placeholder="$t('message.91')"
          hint="-180.0 ... 180.0"
          outlined
          clearable
          dense
          full-width
          maxlength="20"
          :rules="rulesLongitude()"
          :color="colorControlsTheme"
        ></v-text-field>
      </v-col>
    </v-row>
  </v-conteiner>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import helpers from '@/helpers.js'

export default {
  name: 'ContextmenuPlacemark',
  data: () => ({
    icons: [
      'mdi-page-layout-header',
      'mdi-page-layout-body',
      'mdi-page-layout-footer',
      'mdi-check-circle'
    ],
    transTitle: [101, 102, 103]
  }),
  computed: {
    ...mapState('generalSettings', [
      'colorControlsTheme',
      'colorButtonsTextTheme'
    ]),
    ...mapState('ymap', [
      'editableGeoObject'
    ]),
    ...mapState([
      'iconCollection'
    ]),
    ...mapState('contextmenuPlacemark', [
      'iconUrl',
      'category',
      'subcategories',
      'coordinates'
    ]),
    ...mapState('selectingCategories', {
      selectedControls: 'controls'
    }),
    updateIconUrl: {
      get () {
        return this.iconUrl
      },
      set (url) {
        this.setIconUrl(url)
      }
    },
    updateLatitude: {
      get () {
        return this.coordinates[0]
      },
      set (coord) {
        this.setLatitude(coord)
      }
    },
    updateLongitude: {
      get () {
        return this.coordinates[1]
      },
      set (coord) {
        this.setLongitude(coord)
      }
    }
  },
  methods: {
    ...mapMutations('contextmenuPlacemark', [
      'setPK',
      'setCategory',
      'setSubcategories',
      'setHeader',
      'setBody',
      'setFooter',
      'setIconSlug',
      'setLatitude',
      'setLongitude',
      'setIconUrl'
    ]),
    ...mapMutations('modals', [
      // Controls
      'controlsDialogShow', // Open
      'controlsDialogClose', // Close
      // Simple messages
      'alertSnackbarClose' // Close
    ]),
    ...mapMutations([
      'setDataAction'
    ]),
    ...mapActions('contextmenuPlacemark', [
      'restoreDefaults'
    ]),
    // Rules
    rulesLatitude () {
      return [
        coord => helpers.checkLatitude(coord) || this.$t('message.92')
      ]
    },
    rulesLongitude () {
      return [
        coord => helpers.checkLongitude(coord) || this.$t('message.92')
      ]
    },
    // Open Icon list.
    openIconCollection () {
      this.alertSnackbarClose()
      this.controlsDialogShow({
        title: this.$t('message.7'),
        text: '',
        cancelBtn: true,
        saveBtn: false,
        componentIcons: true,
        actionBtnSave: null,
        actionBtnCancel: this.controlsDialogClose
      })
    },
    // Open CKEditor or Category list and Subcategory list.
    openDialog (index) {
      this.alertSnackbarClose()
      switch (index) {
        case 0:
        case 1:
        case 2:
          // Open CKEditor.
          this.setDataAction({
            geoType: 'placemark',
            position: ['headerPlacemark', 'bodyPlacemark', 'footerPlacemark'][index]
          })
          this.controlsDialogShow({
            title: this.$t(`message.${this.transTitle[index]}`),
            text: '',
            cancelBtn: true,
            saveBtn: true,
            componentCKEditor: true,
            actionBtnSave: () => {
              const mutation = ['setHeader', 'setBody', 'setFooter'][index]
              const textHtml = window.djeymCKEditor.val()
              this[mutation](textHtml)
              if (this.editableGeoObject !== null) {
                switch (mutation) {
                  case 'setHeader':
                    this.editableGeoObject.properties.set('balloonContentHeader', textHtml)
                    break
                  case 'setBody':
                    this.editableGeoObject.properties.set('balloonContentBody', textHtml)
                    break
                  case 'setFooter':
                    this.editableGeoObject.properties.set('balloonContentFooter', textHtml)
                    break
                }
              }
              this.controlsDialogClose()
            },
            actionBtnCancel: this.controlsDialogClose
          })
          break
        case 3:
          // Open Category list and Subcategory list.
          this.setDataAction({
            geoType: 'placemark',
            category: this.category,
            subcategories: this.subcategories
          })
          this.controlsDialogShow({
            title: this.$t('message.105'),
            text: '',
            cancelBtn: true,
            saveBtn: true,
            componentCategories: true,
            actionBtnSave: () => {
              this.setCategory(this.selectedControls.category)
              this.setSubcategories(this.selectedControls.subcategories)
              if (this.editableGeoObject !== null) {
                this.editableGeoObject.properties.set('categoryID', this.category)
                this.editableGeoObject.properties.set('subCategoryIDs', this.subcategories)
              }
              this.controlsDialogClose()
            },
            actionBtnCancel: this.controlsDialogClose
          })
          break
      }
    }
  },
  created () {
    // Updating data
    if (this.editableGeoObject === null) {
      this.restoreDefaults() // Restore Defaults
    } else {
      this.setPK(this.editableGeoObject.properties.get('id'))
      this.setCategory(this.editableGeoObject.properties.get('categoryID'))
      this.setSubcategories(this.editableGeoObject.properties.get('subCategoryIDs'))
      this.setHeader(this.editableGeoObject.properties.get('balloonContentHeader'))
      this.setBody(this.editableGeoObject.properties.get('balloonContentBody'))
      this.setFooter(this.editableGeoObject.properties.get('balloonContentFooter'))
      const iconSlug = this.editableGeoObject.properties.get('iconSlug')
      this.setIconSlug(iconSlug)
      if (iconSlug !== 'djeym-marker-default') {
        this.setIconUrl(this.iconCollection.filter(item => item.slug === iconSlug)[0].url)
      } else {
        this.setIconUrl('/static/djeym/img/center.svg')
      }
      const coords = this.editableGeoObject.geometry.getCoordinates()
      this.setLatitude(coords[0])
      this.setLongitude(coords[1])
    }
  }
}
</script>

<style scoped>
.icon-marker {
  z-index: 2;
  cursor: pointer;
}
</style>
