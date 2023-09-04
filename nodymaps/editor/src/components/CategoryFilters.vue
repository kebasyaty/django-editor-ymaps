<!--
--------------------------------------------------
Component for filtering geo objects by categories.
--------------------------------------------------
-->
<template>
  <div>
    <v-tabs v-model="filtersTab" height="42" centered show-arrows center-active :color="colorControlsTheme">
      <v-tabs-slider></v-tabs-slider>
      <v-tab v-for="(name, index) in tabNameList" :key="`filter-button-${index}`" :href="`#filterTab-${index}`"
        :ripple="effectRipple">
        <v-icon>{{ tabIcons[name] }}</v-icon>
      </v-tab>
    </v-tabs>

    <!-- Start Appearance Settings -->
    <v-card flat>
      <v-card-text class="mt-2 pb-2">
        <v-expansion-panels v-model="panel" flat hover>
          <v-expansion-panel>
            <v-expansion-panel-header class="py-1" :color="colorControlsTheme">
              <span>
                <v-icon class="pr-2" :color="colorButtonsTextTheme">mdi-cog</v-icon>
                <span :style="`color: ${colorButtonsTextTheme};`">{{
                  $t("message.6")
                }}</span>
              </span>
              <template v-slot:actions>
                <v-icon :color="colorButtonsTextTheme">$expand</v-icon>
              </template>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <!-- Button - Reset by default -->
              <v-btn class="my-5" small block depressed color="orange darken-3" @click="resetByDefault()">
                <v-icon color="grey darken-4" class="mr-2">mdi-restart</v-icon>
                <span class="grey--text text--darken-4">{{
                  $t("message.47")
                }}</span>
              </v-btn>
              <v-divider></v-divider>
              <!-- Multiple choice ? -->
              <v-switch v-model="updateMultiple" inset hide-details :label="$t('message.78')" class="mt-5 pt-0"
                :color="colorControlsTheme" @change="actionRefreshStateControls()"></v-switch>
              <!-- Links - Material design icons -->
              <div class="subtitle-1 mt-5 text-center">
                {{ $t("message.80") }}
              </div>
              <v-divider></v-divider>
              <div class="mt-0 text-center" v-for="(link, index) in iconsLinkList" :key="`icon-link-${index}`"
                :class="iconsLinkList.length === index + 1 ? 'mb-3' : ''">
                <v-btn link text x-small depressed color="primary" target="_blank" rel="nofollow noreferrer noopener"
                  :href="link">{{ link }}</v-btn>
              </div>
              <!-- Replacing category icons for tabs. -->
              <v-text-field v-for="(tabName, index) in tabNameList" :key="`icon-${tabName}`" v-model="tabIcons[tabName]"
                :placeholder="$t(`message.${transCategoryNames[index]}`)" :color="colorControlsTheme"
                :prepend-icon="tabIcons[tabName]" @change="actionCheckNameIcon(tabName)" single-line outlined rounded
                dense clearable :rules="rulesReplacingCategoryIcons()"></v-text-field>
              <!-- Geo-types - Places, Routes, Territories -->
              <div class="subtitle-1 text-center">{{ $t("message.140") }}</div>
              <v-divider></v-divider>
              <div class="caption text-center">
                {{ `(${$t("message.144")})` }}
              </div>
              <!-- Changing category names -->
              <v-text-field v-model="updateGeoTypeNameMarker" :placeholder="$t('message.15')" :color="colorControlsTheme"
                single-line outlined dense hide-details full-width clearable class="my-3"></v-text-field>
              <v-text-field v-model="updateGeoTypeNameRoute" :placeholder="$t('message.16')" :color="colorControlsTheme"
                single-line outlined dense hide-details full-width clearable class="mb-3"></v-text-field>
              <v-text-field v-model="updateGeoTypeNameTerritory" :placeholder="$t('message.17')"
                :color="colorControlsTheme" single-line outlined dense hide-details full-width clearable
                class="mb-5"></v-text-field>
              <!-- Geo-type names by center -->
              <v-switch v-model="updateCenterGeoTypes" inset hide-details :label="$t('message.143')" class="mt-0 pt-0"
                :color="colorControlsTheme"></v-switch>
              <!-- Hide Geo-Types -->
              <v-switch v-model="updateHideGeoTypes" inset hide-details :label="$t('message.141')" class="pt-0"
                :color="colorControlsTheme"></v-switch>
              <!-- Groups - Categories, Subcategories -->
              <div class="subtitle-1 mt-5 text-center">
                {{ $t("message.139") }}
              </div>
              <v-divider></v-divider>
              <div class="caption text-center">
                {{ `(${$t("message.20")}, ${$t("message.21")})` }}
              </div>
              <!-- Changing group names -->
              <v-text-field v-model="updateGroupNameCategories" :placeholder="$t('message.20')"
                :color="colorControlsTheme" single-line outlined dense hide-details clearable full-width
                class="my-3"></v-text-field>
              <v-text-field v-model="updateGroupNameSubcategories" :placeholder="$t('message.21')"
                :color="colorControlsTheme" single-line outlined dense hide-details clearable full-width
                class="mb-5"></v-text-field>
              <!-- Hide group names (Categories, Subcategories) -->
              <v-switch v-model="updateHideGroupNames" inset hide-details :label="$t('message.134')" class="mt-2 pt-0"
                :color="colorControlsTheme"></v-switch>
              <!-- Change appearance of active controls -->
              <div class="subtitle-1 mt-5 text-center">
                {{ $t("message.145") }}
              </div>
              <v-divider></v-divider>
              <!-- Select shape of highlighting for of active controls -->
              <v-select v-model="updateControlsShape" dense outlined hide-details :label="$t('message.146')"
                :items="getItemsControlsShape()" :color="colorControlsTheme" :item-color="colorControlsTheme"
                class="mt-4"></v-select>
              <!-- Effect Ripple -->
              <v-switch v-model="updateEffectRipple" inset hide-details :label="$t('message.147')" class="mt-5 pt-0"
                :color="colorControlsTheme"></v-switch>
              <!-- Button - Save Update Settings -->
              <v-card-actions class="pt-6 pb-1">
                <v-spacer></v-spacer>
                <v-btn small fab depressed :color="colorControlsTheme" @click="actionSaveUpdate()">
                  <v-icon :color="colorButtonsTextTheme">mdi-content-save</v-icon>
                </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-text>
    </v-card>
    <!-- End Appearance Settings -->

    <!-- Start - Filter list - Controls -->
    <v-tabs-items v-model="filtersTab">
      <v-tab-item v-for="(step, index) in 3" :key="`filter-item-${step}`" :value="`filterTab-${index}`">
        <template v-if="index === 0">
          <v-card-title v-if="!hideGeoTypes" class="title pt-1 pb-0" :class="centerGeoTypes ? 'justify-center' : ''">{{
            geoTypeNameMarker ? geoTypeNameMarker : $t("message.15")
          }}</v-card-title>
        </template>
        <template v-if="index === 1">
          <v-card-title v-if="!hideGeoTypes" class="title pt-1 pb-0" :class="centerGeoTypes ? 'justify-center' : ''">{{
            geoTypeNameRoute ? geoTypeNameRoute : $t("message.16")
          }}</v-card-title>
        </template>
        <template v-if="index === 2">
          <v-card-title v-if="!hideGeoTypes" class="title pt-1 pb-0" :class="centerGeoTypes ? 'justify-center' : ''">{{
            geoTypeNameTerritory ? geoTypeNameTerritory : $t("message.17")
          }}</v-card-title>
        </template>

        <v-container fluid class="pt-1">
          <v-divider v-if="!hideGeoTypes"></v-divider>
          <v-list :shaped="controlsShape === 'shaped'" :rounded="controlsShape === 'rounded'"
            :flat="controlsShape === 'flat'" dense v-for="(filter, modelKey, index2) in nextTwoFilters(index)"
            :key="`filters-${modelKey}`" :class="index2 ? 'pa-0' : 'px-0 pt-2 pb-0'">
            <template v-if="index2 === 0">
              <v-card-subtitle class="font-italic px-0 pb-1" :class="index2 ? 'pt-1' : 'pt-0'">{{
                filter.length && !hideGroupNames
                ? groupNameCategories
                  ? groupNameCategories
                  : $t("message.20")
                : ""
              }}</v-card-subtitle>
            </template>
            <template v-if="index2 === 1">
              <v-card-subtitle class="font-italic px-0 pb-1" :class="index2 ? 'pt-1' : 'pt-0'">{{
                filter.length && !hideGroupNames
                ? groupNameSubcategories
                  ? groupNameSubcategories
                  : $t("message.21")
                : ""
              }}</v-card-subtitle>
            </template>

            <v-list-item-group v-model="models[modelKey]" :multiple="(index2 + 1) % 2 == 0 ? true : multiple">
              <v-list-item v-for="control in filter" :key="`control-${control.id}`" :color="control.color"
                :ripple="effectRipple" class="mb-1" @click="
                  [
                    (control.isActive = !control.isActive),
                    actionFiltering({ id: control.id, modelKey: modelKey }),
                  ]
                  ">
                <v-list-item-icon class="my-auto mr-3">
                  <v-icon :color="control.color">{{ control.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title class="subtitle-2 djeym-white-space-normal">{{ control.title }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-container>
      </v-tab-item>
    </v-tabs-items>
    <!-- End - Filter list - Controls -->
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
  name: "CategoryFilters",
  data: () => ({
    filtersTab: null, // Open/Close
    transCategoryNames: [15, 16, 17],
    tabNameList: ["marker", "route", "territory"],
    iconsLinkList: ["http://materialdesignicons.com/"],
  }),
  computed: {
    ...mapState("categoryFilters", [
      "panel",
      "multiple", // Multiple or solo choice.
      "tabIcons", // Category Icons
      "centerGeoTypes",
      "hideGeoTypes",
      "geoTypeNameMarker",
      "geoTypeNameRoute",
      "geoTypeNameTerritory",
      "hideGroupNames",
      "groupNameCategories",
      "groupNameSubcategories",
      "controlsShape",
      "effectRipple",
      "filters",
      "models",
    ]),
    ...mapState("generalSettings", [
      "colorControlsTheme",
      "colorButtonsTextTheme",
    ]),
    updateMultiple: {
      get() {
        return this.multiple;
      },
      set(flag) {
        this.setMultiple(flag);
      },
    },
    updateCenterGeoTypes: {
      get() {
        return this.centerGeoTypes;
      },
      set(flag) {
        this.setCenterGeoTypes(flag);
      },
    },
    updateHideGeoTypes: {
      get() {
        return this.hideGeoTypes;
      },
      set(flag) {
        this.setHideGeoTypes(flag);
      },
    },
    updateGeoTypeNameMarker: {
      get() {
        return this.geoTypeNameMarker;
      },
      set(text) {
        this.setGeoTypeNameMarker(text);
      },
    },
    updateGeoTypeNameRoute: {
      get() {
        return this.geoTypeNameRoute;
      },
      set(text) {
        this.setGeoTypeNameRoute(text);
      },
    },
    updateGeoTypeNameTerritory: {
      get() {
        return this.geoTypeNameTerritory;
      },
      set(text) {
        this.setGeoTypeNameTerritory(text);
      },
    },
    updateHideGroupNames: {
      get() {
        return this.hideGroupNames;
      },
      set(flag) {
        this.setHideGroupNames(flag);
      },
    },
    updateGroupNameCategories: {
      get() {
        return this.groupNameCategories;
      },
      set(text) {
        this.setGroupNameCategories(text);
      },
    },
    updateGroupNameSubcategories: {
      get() {
        return this.groupNameSubcategories;
      },
      set(text) {
        this.setGroupNameSubcategories(text);
      },
    },
    updateControlsShape: {
      get() {
        return this.controlsShape;
      },
      set(shape) {
        this.setControlsShape(shape);
      },
    },
    updateEffectRipple: {
      get() {
        return this.effectRipple;
      },
      set(flag) {
        this.setEffectRipple(flag);
      },
    },
  },
  methods: {
    ...mapMutations(["setMapSettingsDrawer"]),
    ...mapMutations("categoryFilters", [
      "setMultiple",
      "setCenterGeoTypes",
      "setHideGeoTypes",
      "setGeoTypeNameMarker",
      "setGeoTypeNameRoute",
      "setGeoTypeNameTerritory",
      "setHideGroupNames",
      "setGroupNameCategories",
      "setGroupNameSubcategories",
      "setControlsShape",
      "setEffectRipple",
    ]),
    ...mapMutations("modals", [
      // Message
      "messageDialogShow", // Open
      "messageDialogClose", // Close
    ]),
    ...mapActions("categoryFilters", [
      "actionCheckNameIcon",
      "actionFiltering",
      "actionRefreshStateControls",
      "actionReset",
      "actionSave",
    ]),
    // Get a pair (categories + subcategories) for one a geo object type.
    nextTwoFilters(index) {
      const filters = this.filters;
      let result = {};
      Object.keys(filters)
        .slice((index *= 2), index + 2)
        .map((key) => ({ [key]: filters[key] }))
        .forEach((item) => {
          result[Object.keys(item)[0]] = Object.values(item)[0];
        });
      return result;
    },
    resetByDefault() {
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
        actionBtnOk: this.actionReset,
      });
    },
    // Rules
    rulesReplacingCategoryIcons() {
      return [(iconName) => !!iconName || this.$t("message.53")];
    },
    // Shapes of highlighting for of active controls
    getItemsControlsShape() {
      return [
        { text: "Shape", value: "shaped" },
        { text: "Round", value: "rounded" },
        { text: "Flat", value: "flat" },
        { text: "Default", value: "" },
      ];
    },
    // Save change
    actionSaveUpdate() {
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
        actionBtnOk: this.actionSave,
      });
    },
  },
};
</script>
