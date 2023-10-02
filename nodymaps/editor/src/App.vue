<template>
  <v-app id="djeym-app">
    <!-- Panel for Map Settings -->
    <v-navigation-drawer v-model="updateMapSettingsDrawer" app hide-overlay temporary :width="widthPanelSettings">
      <v-card-actions class="pb-0">
        <v-spacer></v-spacer>
        <!-- Button - Сlose panel -->
        <v-btn icon @click.stop="updateMapSettingsDrawer = false">
          <v-icon :color="colorControlsTheme">mdi-close</v-icon>
        </v-btn>
      </v-card-actions>
      <v-tabs v-model="mapSettingsTab" height="42" show-arrows center-active :color="colorControlsTheme">
        <v-tabs-slider></v-tabs-slider>
        <v-tab
v-for="(icon, index) in mapSettingsTabIcons" :key="`map-settings-button-${index}`"
          :href="`#mapSettingsTab-${index}`">
          <v-icon>mdi-{{ icon }}</v-icon>
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="mapSettingsTab" v-if="showAllSettings">
        <v-tab-item
v-for="(component, index) in componentList" :key="`map-settings-item-${index}`"
          :value="`mapSettingsTab-${index}`">
          <v-card flat>
            <v-card-title class="title justify-center">{{
              $t(`message.${transMapSettings[index]}`)
            }}</v-card-title>
          </v-card>
          <v-divider></v-divider>
          <component :is="component"></component>
        </v-tab-item>
      </v-tabs-items>
    </v-navigation-drawer>

    <!-- Panel of App -->
    <v-app-bar app dense clipped-left :color="colorControlsTheme">
      <v-spacer></v-spacer>
      <!-- Button - Back to admin panel -->
      <v-btn icon :href="`/admin/djeym/map/${mapID}/change/`" color="white" class="mr-3">
        <v-tooltip bottom>
          <template #activator="{ on }">
            <v-icon :color="colorButtonsTextTheme" v-on="on">mdi-arrow-left-top-bold</v-icon>
          </template>
          <span>{{ $t("message.83") }}</span>
        </v-tooltip>
      </v-btn>

      <!-- Button - Logo icon -->
      <v-btn
icon href="https://pypi.org/project/django-editor-ymaps/" target="_blank" rel="nofollow noreferrer noopener"
        color="white" depressed>
        <IconLogo height="42" :color="colorButtonsTextTheme" />
      </v-btn>

      <!-- Button - Open Map Settings -->
      <v-btn icon color="white" class="ml-2" @click.stop="updateMapSettingsDrawer = true">
        <v-tooltip bottom>
          <template #activator="{ on }">
            <v-icon large :color="colorButtonsTextTheme" v-on="on">mdi-cog</v-icon>
          </template>
          <span>{{ $t("message.6") }}</span>
        </v-tooltip>
      </v-btn>

      <!-- Button - Add geo object -->
      <v-btn icon color="white" @click="helpCreateGeoobject()">
        <v-tooltip bottom>
          <template #activator="{ on }">
            <v-icon large :color="colorButtonsTextTheme" v-on="on">mdi-help</v-icon>
          </template>
          <span>{{ $t("message.84") }}</span>
        </v-tooltip>
      </v-btn>

      <!-- Button - Find Editable Geo Object -->
      <v-btn
class="ml-2" color="white" depressed fab small v-show="showBtnFindEditableGeoObject"
        @click="findEditableGeoObject()">
        <v-tooltip bottom>
          <template #activator="{ on }">
            <v-icon large color="red darken-2" v-on="on">mdi-crosshairs-gps</v-icon>
          </template>
          <span>{{ $t("message.2") }}</span>
        </v-tooltip>
      </v-btn>
      <v-spacer></v-spacer>
    </v-app-bar>

    <!-- Content - Map -->
    <div fluid id="djeymYMapsID" class="djeym-ymap pa-0"></div>

    <!-- Modals -->
    <Modals />
  </v-app>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";
import IconLogo from "@/components/icons/ordinary/IconLogo.vue";
import CategoryFilters from "@/components/CategoryFilters.vue";
import TileSources from "@/components/TileSources.vue";
import GeneralSettings from "@/components/GeneralSettings.vue";
import MapControls from "@/components/MapControls.vue";
import Heatmap from "@/components/Heatmap.vue";
import LoadIndicators from "@/components/LoadIndicators.vue";
import Presets from "@/components/Presets.vue";
import Help from "@/components/Help.vue";
import Modals from "@/components/Modals.vue";

export default {
  name: "App",
  components: {
    IconLogo,
    CategoryFilters,
    TileSources,
    GeneralSettings,
    MapControls,
    Heatmap,
    LoadIndicators,
    Presets,
    Help,
    Modals,
  },
  data: () => ({
    // Panel for Icons.
    iconsDrawer: false, // Open/Close
    mapSettingsTabIcons: [
      "checkbox-marked-circle-outline",
      "map-check",
      "cogs",
      "tune",
      "fire",
      "shape-circle-plus",
      "needle",
      "help",
    ],
    componentList: [
      "CategoryFilters",
      "TileSources",
      "GeneralSettings",
      "MapControls",
      "Heatmap",
      "LoadIndicators",
      "Presets",
      "Help",
    ],
    transMapSettings: [8, 9, 10, 61, 11, 12, 13, 14],
    // Tab - Map Settings.
    mapSettingsTab: null, // Open/Close
  }),
  computed: {
    ...mapState([
      "enableAjax",
      "showAllSettings",
      "showBtnFindEditableGeoObject",
      // Panel for Map Settings.
      "mapSettingsDrawer", // Open/Close
      "widthPanelSettings",
    ]),
    ...mapState("generalSettings", [
      "colorControlsTheme",
      "colorButtonsTextTheme",
      "minElevation",
      "maxElevation",
    ]),
    ...mapState("ymap", ["mapID"]),
    updateMapSettingsDrawer: {
      get() {
        return this.mapSettingsDrawer;
      },
      set(flag) {
        this.setMapSettingsDrawer(flag);
      },
    },
  },
  methods: {
    ...mapMutations(["setMapSettingsDrawer"]),
    ...mapMutations("modals", [
      // Message.
      "messageDialogShow", // Open
      "messageDialogClose", // Close
      // Global progress bar.
      "globalProgressBarShow", // Open
    ]),
    ...mapActions(["ajaxUploadSettings"]),
    ...mapActions("ymap", ["findEditableGeoObject"]),
    helpCreateGeoobject() {
      this.messageDialogShow({
        status: "info",
        title: this.$t("message.87"),
        text: `1) ${this.$t("message.40")}<br /><br />2) ${this.$t("message.148")}`,
        cancelBtn: false,
        okBtn: true,
        actionBtnCancel: null,
        actionBtnOk: this.messageDialogClose,
      });
    },
  },
  mounted() {
    /* 1.Ajax - Upload all settings.
       2.Start Map initialization. */
    window.djeymYMaps
      .ready(["util.calculateArea"])
      .then(() => this.ajaxUploadSettings());
  },
};
</script>

<style scoped>
.djeym-ymap {
  min-height: 300px !important;
  position: absolute;
  top: 48px;
  right: 0;
  bottom: 0;
  left: 0;
}
</style>
