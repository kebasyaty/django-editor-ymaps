<!--
------------------------------------------------
Component for creating and editable Territories.
------------------------------------------------
-->
<template>
  <v-conteiner fluid>
    <!-- Buttons - Header, Body, Footer, Categories and Subcategories. -->
    <v-row align="center" justify="center" class="pb-8">
      <v-btn v-for="(icon, index) in icons" :key="`action-btn-${index}`" small fab depressed :color="colorControlsTheme"
        class="mx-1" @click="openDialog(index)">
        <v-icon :color="colorButtonsTextTheme">{{ icons[index] }}</v-icon>
      </v-btn>
    </v-row>
    <!-- Calculate Area -->
    <v-row v-if="editableGeoObject !== null && coordinates.length > 0">
      <v-col cols="12" class="pt-0 text-center">
        <span class="grey--text text--darken-2 subtitle-2 font-weight-bold" v-text="calculateArea()"></span>
      </v-col>
    </v-row>
    <!-- Stroke -->
    <v-row align="center" justify="center">
      <v-col cols="12" class="pt-0">
        <v-card-subtitle class="font-italic py-0">{{
          $t("message.127")
        }}</v-card-subtitle>
        <v-divider></v-divider>
      </v-col>
      <!-- Color -->
      <v-col cols="12" class="text-center py-0">
        <v-btn block x-small depressed :color="updateStrokeColor" @click="recolor('stroke')"></v-btn>
      </v-col>
      <!-- Style -->
      <v-col cols="12">
        <v-select v-model="updateStrokeStyle" :items="strokeStyleList" :label="$t('message.114')" item-text="title"
          item-value="value" dense full-width hide-details :color="colorControlsTheme" :item-color="colorControlsTheme"
          @change="actionRefreshStrokeStyle()"></v-select>
      </v-col>
      <!-- Width -->
      <v-col cols="12" class="pt-0 pl-3 pr-2">
        <v-slider v-model="updateStrokeWidth" :track-color="$vuetify.theme.dark ? 'grey darken-1' : 'grey lighten-2'
          " min="1" max="25" thumb-label hide-details prepend-icon="mdi-arrow-split-vertical"
          :color="colorControlsTheme" @input="actionRefreshStrokeWidth()"></v-slider>
      </v-col>
      <!-- Opacity -->
      <v-col cols="12" class="pl-3 pr-2 py-0">
        <v-slider v-model="updateStrokeOpacity" :track-color="$vuetify.theme.dark ? 'grey darken-1' : 'grey lighten-2'
          " min="0.1" max="1" step="0.1" thumb-label hide-details prepend-icon="mdi-opacity"
          :color="colorControlsTheme" @input="actionRefreshStrokeOpacity()"></v-slider>
      </v-col>
    </v-row>
    <!-- Fill -->
    <v-row align="center" justify="center">
      <v-col cols="12" class="pt-0">
        <v-card-subtitle class="font-italic pt-2 pb-0">{{
          $t("message.128")
        }}</v-card-subtitle>
        <v-divider></v-divider>
      </v-col>
      <!-- Color -->
      <v-col cols="12" class="text-center py-0">
        <v-btn block x-small depressed :color="updateFillColor" @click="recolor('fill')"></v-btn>
      </v-col>
      <!-- Opacity -->
      <v-col cols="12" class="pl-3 pr-2 pt-2 pb-0">
        <v-slider v-model="updateFillOpacity" :track-color="$vuetify.theme.dark ? 'grey darken-1' : 'grey lighten-2'
          " min="0.1" max="1" step="0.1" thumb-label hide-details prepend-icon="mdi-opacity"
          :color="colorControlsTheme" @input="actionRefreshFillOpacity()"></v-slider>
      </v-col>
    </v-row>
  </v-conteiner>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
  name: "ContextmenuTerritory",
  components: {},
  data: () => ({
    icons: [
      "mdi-page-layout-header",
      "mdi-page-layout-body",
      "mdi-page-layout-footer",
      "mdi-check-circle",
    ],
  }),
  computed: {
    ...mapState("generalSettings", [
      "colorControlsTheme",
      "colorButtonsTextTheme",
    ]),
    ...mapState("ymap", ["editableGeoObject"]),
    ...mapState("contextmenuTerritory", [
      "category",
      "subcategories",
      "strokeColor",
      "strokeStyle",
      "strokeWidth",
      "strokeOpacity",
      "fillColor",
      "fillOpacity",
      "coordinates",
    ]),
    ...mapState("selectingCategories", {
      selectedControls: "controls",
    }),
    updateStrokeColor: {
      get() {
        return this.strokeColor;
      },
      set(color) {
        this.setStrokeColor(color);
      },
    },
    updateStrokeStyle: {
      get() {
        return this.strokeStyle;
      },
      set(style) {
        this.setStrokeStyle(style);
      },
    },
    updateStrokeWidth: {
      get() {
        return this.strokeWidth;
      },
      set(num) {
        this.setStrokeWidth(num);
      },
    },
    updateStrokeOpacity: {
      get() {
        return this.strokeOpacity;
      },
      set(num) {
        this.setStrokeOpacity(num);
      },
    },
    updateFillColor: {
      get() {
        return this.fillColor;
      },
      set(color) {
        this.setFillColor(color);
      },
    },
    updateFillOpacity: {
      get() {
        return this.fillOpacity;
      },
      set(num) {
        this.setFillOpacity(num);
      },
    },
    strokeStyleList: function () {
      return [
        { value: "solid", title: this.$t("message.115") },
        { value: "dash", title: this.$t("message.116") },
        { value: "dashdot", title: this.$t("message.117") },
        { value: "dot", title: this.$t("message.118") },
        { value: "longdash", title: this.$t("message.119") },
        { value: "longdashdot", title: this.$t("message.120") },
        { value: "longdashdotdot", title: this.$t("message.121") },
        { value: "shortdash", title: this.$t("message.122") },
        { value: "shortdashdot", title: this.$t("message.123") },
        { value: "shortdashdotdot", title: this.$t("message.124") },
        { value: "shortdot", title: this.$t("message.125") },
      ];
    },
  },
  methods: {
    ...mapMutations("contextmenuTerritory", [
      "setPK",
      "setCategory",
      "setSubcategories",
      "setHeader",
      "setBody",
      "setFooter",
      "setStrokeColor",
      "setStrokeStyle",
      "setStrokeWidth",
      "setStrokeOpacity",
      "setFillColor",
      "setFillOpacity",
      "setCoordinates",
      "setDataActionPalette",
    ]),
    ...mapMutations("modals", [
      // Controls
      "controlsDialogShow", // Open
      "controlsDialogClose", // Close
      // Simple messages
      "alertSnackbarClose", // Close
    ]),
    ...mapMutations(["setDataAction"]),
    ...mapActions("contextmenuTerritory", [
      "restoreDefaults",
      "actionPalette",
      "actionRefreshStrokeStyle",
      "actionRefreshStrokeWidth",
      "actionRefreshStrokeOpacity",
      "actionRefreshFillOpacity",
    ]),
    // Calculate Area.
    calculateArea() {
      let area = window.djeymYMaps.util.calculateArea(this.editableGeoObject);
      // If the area exceeds 1,000,000 m², then we bring it to km².
      // (Если площадь превышает 1 000 000 м², то приводим ее к км².)
      if (area <= 1e6) {
        area += " м²";
      } else {
        area = (area / 1e6).toFixed(3) + " км²";
      }
      return area;
    },
    // Open CKEditor or Category list and Subcategory list.
    openDialog(index) {
      this.alertSnackbarClose();
      switch (index) {
        case 0:
        case 1:
        case 2:
          // Open CKEditor.
          this.setDataAction({
            geoType: "polygon",
            position: ["headerTerritory", "bodyTerritory", "footerTerritory"][
              index
            ],
          });
          this.controlsDialogShow({
            title: this.$t(`message.${[101, 102, 103][index]}`),
            text: "",
            cancelBtn: true,
            saveBtn: true,
            componentCKEditor: true,
            actionBtnSave: () => {
              const mutation = ["setHeader", "setBody", "setFooter"][index];
              const textHtml = window.djeymCKEditor.val();
              this[mutation](textHtml);
              if (this.editableGeoObject !== null) {
                switch (mutation) {
                  case "setHeader":
                    this.editableGeoObject.properties.set(
                      "balloonContentHeader",
                      textHtml,
                    );
                    break;
                  case "setBody":
                    this.editableGeoObject.properties.set(
                      "balloonContentBody",
                      textHtml,
                    );
                    break;
                  case "setFooter":
                    this.editableGeoObject.properties.set(
                      "balloonContentFooter",
                      textHtml,
                    );
                    break;
                }
              }
              this.controlsDialogClose();
            },
            actionBtnCancel: this.controlsDialogClose,
          });
          break;
        case 3:
          // Open Category list and Subcategory list.
          this.setDataAction({
            geoType: "polygon",
            category: this.category,
            subcategories: this.subcategories,
          });
          this.controlsDialogShow({
            title: this.$t("message.105"),
            text: "",
            cancelBtn: true,
            saveBtn: true,
            componentCategories: true,
            actionBtnSave: () => {
              this.setCategory(this.selectedControls.category);
              this.setSubcategories(this.selectedControls.subcategories);
              if (this.editableGeoObject !== null) {
                this.editableGeoObject.properties.set(
                  "categoryID",
                  this.category,
                );
                this.editableGeoObject.properties.set(
                  "subCategoryIDs",
                  this.subcategories,
                );
              }
              this.controlsDialogClose();
            },
            actionBtnCancel: this.controlsDialogClose,
          });
          break;
      }
    },
    // Change color for Stroke Color.
    recolor(target) {
      this.setDataActionPalette({
        target: { stroke: "strokeColor", fill: "fillColor" }[target],
      });
      this.controlsDialogShow({
        title: this.$t(`message.${{ stroke: 110, fill: 126 }[target]}`),
        text: "",
        cancelBtn: true,
        saveBtn: true,
        componentPalette: true,
        palette: {
          currentColor: {
            stroke: this.updateStrokeColor,
            fill: this.updateFillColor,
          }[target],
        },
        actionBtnSave: this.actionPalette,
        actionBtnCancel: this.controlsDialogClose,
      });
    },
  },
  created() {
    // Updating data
    if (this.editableGeoObject === null) {
      this.restoreDefaults(); // Restore Defaults
    } else {
      this.setPK(this.editableGeoObject.properties.get("id"));
      this.setCategory(this.editableGeoObject.properties.get("categoryID"));
      this.setSubcategories(
        this.editableGeoObject.properties.get("subCategoryIDs"),
      );
      this.setHeader(
        this.editableGeoObject.properties.get("balloonContentHeader"),
      );
      this.setBody(this.editableGeoObject.properties.get("balloonContentBody"));
      this.setFooter(
        this.editableGeoObject.properties.get("balloonContentFooter"),
      );
      this.setStrokeColor(this.editableGeoObject.options.get("strokeColor"));
      const valStyle = this.editableGeoObject.options.get("strokeStyle");
      this.setStrokeStyle(
        this.strokeStyleList.filter((style) => style.value === valStyle)[0],
      );
      this.setStrokeWidth(this.editableGeoObject.options.get("strokeWidth"));
      this.setStrokeOpacity(
        this.editableGeoObject.options.get("strokeOpacity"),
      );
      this.setFillColor(this.editableGeoObject.options.get("fillColor"));
      this.setFillOpacity(this.editableGeoObject.options.get("fillOpacity"));
      this.setCoordinates(this.editableGeoObject.geometry.getCoordinates());
      this.editableGeoObject.editor.startEditing();
      this.editableGeoObject.editor.startDrawing();
    }
  },
};
</script>
