<!--
------------------------
Component for Help info.
------------------------
-->
<template>
  <v-container fluid>
    <v-card :elevation="minElevation">
      <v-card-text class="title px-0 pt-5 pb-0 font-weight-bold text-center">
        <IconLogo
          height="42"
          :color="$vuetify.theme.dark ? '#757575' : '#E0E0E0'"
        />
        <span class="pl-3 djeym-pos-relative valign-title"
          >django-editor-ymaps</span
        >
      </v-card-text>
      <v-card-text class="text-center pa-2">{{ $t("message.68") }}</v-card-text>
      <v-card-text class="pa-2">
        <div
          class="mt-0 text-center"
          v-for="(link, index) in techLinks"
          :key="`tech-link-${index}`"
        >
          <v-btn
            link
            text
            x-small
            color="primary"
            target="_blank"
            rel="nofollow noreferrer noopener"
            :href="link.url"
            >{{ link.title }}</v-btn
          >
          <div class="px-10">
            <v-divider v-if="index === 1"></v-divider>
          </div>
        </div>
      </v-card-text>
      <v-card-text class="px-1 pt-1 pb-4 text-center">
        <v-icon :color="$vuetify.theme.dark ? '#757575' : '#E0E0E0'" x-large
          >mdi-compass-outline</v-icon
        >
      </v-card-text>
      <v-card-text class="pa-0">
        <v-container fluid class="pa-0">
          <v-row no-gutters>
            <v-col cols="12" class="text-center">
              <span class="font-weight-bold">Version (DjEYM):&ensp;</span>
              <span>{{ controls.version }}</span>
            </v-col>
          </v-row>
          <v-row no-gutters class="mt-3">
            <v-col cols="12">
              <v-row no-gutters>
                <v-col cols="12" class="text-center">
                  <span class="font-weight-bold">Requirements:&emsp;</span>
                </v-col>
                <v-col cols="12" class="text-center">
                  <span>{{ `Python ${controls.requirements.python}` }}</span>
                  <span class="pl-3">{{
                    `Django ${controls.requirements.django}`
                  }}</span>
                </v-col>
                <v-col cols="12" class="text-center">
                  <span>{{ `Vue.js ${controls.requirements.vue}` }}</span>
                  <span class="pl-3">{{
                    `Vuetify.js ${controls.requirements.vuetify}`
                  }}</span>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-text class="px-1 py-3 text-center">
        <v-icon :color="$vuetify.theme.dark ? '#757575' : '#E0E0E0'" x-large
          >mdi-compass-outline</v-icon
        >
      </v-card-text>
      <v-card-actions class="pb-4">
        <v-spacer></v-spacer>
        <v-btn
          fab
          :outlined="!$vuetify.theme.dark"
          small
          depressed
          :color="$vuetify.theme.dark ? 'grey darken-1' : 'grey lighten-1'"
          v-for="(item, index) in controls.links"
          :key="`link-${index}`"
          :href="item.link"
          :target="item.title === 'Feedback' ? '' : '_blank'"
          rel="nofollow noreferrer noopener"
        >
          <v-tooltip bottom>
            <template #activator="{ on }">
              <v-icon color="grey lighten-1" v-on="on">{{
                `mdi-${item.icon}`
              }}</v-icon>
            </template>
            <span>{{ item.title }}</span>
          </v-tooltip>
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import IconLogo from "@/components/icons/ordinary/IconLogo.vue";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Help",
  components: {
    IconLogo,
  },
  data: () => ({
    techLinks: [
      {
        title: "(ru) Получить API-ключ",
        url: "https://tech.yandex.ru/maps/jsapi/doc/2.1/quick-start/index-docpage/#get-api-key",
      },
      {
        title: "(en) Get the API key",
        url: "https://tech.yandex.com/maps/jsapi/doc/2.1/quick-start/index-docpage/#get-api-key",
      },
      {
        title: "(ru) Условия использования Яндекс.Карт",
        url: "https://tech.yandex.ru/maps/jsapi/doc/2.1/terms/index-docpage/",
      },
      {
        title: "(en) Terms of use for the Yandex.Maps",
        url: "https://tech.yandex.com/maps/jsapi/doc/2.1/terms/index-docpage/",
      },
    ],
  }),
  computed: {
    ...mapState("help", ["controls"]),
    ...mapState("generalSettings", ["minElevation"]),
  },
  methods: {},
};
</script>

<style scoped>
.valign-title {
  top: -16px !important;
}
</style>
