<!--
-----------------------------
Component for Icon Collection.
(Selecting icons for markers.)
-----------------------------
-->
<template>
  <v-container fluid class="px-1 py-0">
    <v-row dense style="width:320px;height:360px;overflow-y:scroll;">
      <v-col cols="3" v-for="icon in iconCollection" :key="`icon-slug-${icon.slug}`">
        <v-hover v-slot:default="{ hover }">
          <v-card
            :elevation="hover ? maxElevation : minElevation"
            class="djeym-curs-p"
            width="67px"
            height="97px"
          >
            <v-card-text class="px-1 pt-2 pb-1 text-center">
              <v-img
                contain
                :src="icon.url"
                :alt="icon.title"
                max-width="100%"
                max-height="60px"
                @click="assignNewIcon(icon.slug, icon.url, icon.size, icon.offset)"
              ></v-img>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-text class="pa-1 overline text-truncate text-center">{{ icon.title }}</v-card-text>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'IconCollection',
  computed: {
    ...mapState([
      'iconCollection'
    ]),
    ...mapState('generalSettings', [
      'colorControlsTheme',
      'minElevation',
      'maxElevation'
    ]),
    ...mapState('ymap', [
      'editableGeoObject'
    ])
  },
  methods: {
    ...mapMutations('contextmenuPlacemark', [
      'setIconSlug',
      'setIconUrl'
    ]),
    ...mapMutations('modals', [
      // Controls
      'controlsDialogClose' // Close
    ]),
    assignNewIcon (slug, url, size, offset) {
      this.setIconSlug(slug)
      this.setIconUrl(url)
      if (this.editableGeoObject !== null) {
        this.editableGeoObject.properties.set('iconSlug', slug)
        this.editableGeoObject.options.set('iconImageHref', url)
        this.editableGeoObject.options.set('iconImageSize', size)
        this.editableGeoObject.options.set('iconImageOffset', offset)
      }
      this.controlsDialogClose()
    }
  }
}
</script>
