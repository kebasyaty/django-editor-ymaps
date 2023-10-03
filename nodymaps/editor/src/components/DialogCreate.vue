<!--
-----------------------------------------------------
Component for setting of dialog a create geo objects.
-----------------------------------------------------
-->
<template>
  <v-conteiner fluid>
    <v-row align="center" justify="center" style="width: 252px" class="pb-8">
      <v-btn
        v-for="(icon, index) in icons"
        :key="`action-btn-${index}`"
        small
        fab
        depressed
        class="mx-1"
        :disabled="index === 3 ? !controlsHeatmap.panel1.isActive : false"
        :color="colorControlsTheme"
        @click="createGeoObject(index)"
      >
        <v-icon :color="colorButtonsTextTheme">{{ icons[index] }}</v-icon>
      </v-btn>
    </v-row>
    <v-row class="pt-5" style="width: 252px">
      <v-col cols="12" class="py-0">
        <v-text-field
          id="id-djeym-latitude"
          v-model="updateLatitude"
          :label="$t('message.90')"
          :placeholder="$t('message.90')"
          hint="-90.0 ... 90.0"
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
import { mapState, mapMutations, mapActions } from "vuex";
import helpers from "@/helpers";
import i18n from "@/locales/i18n";

export default {
  name: "DialogCreate",
  data: () => ({
    icons: ["mdi-map-marker", "mdi-routes", "mdi-beach", "mdi-fire"],
  }),
  computed: {
    ...mapState("dialogCreate", {
      coordsCreate: "coords",
    }),
    ...mapState("generalSettings", [
      "colorControlsTheme",
      "colorButtonsTextTheme",
    ]),
    ...mapState("heatmap", {
      controlsHeatmap: "controls",
    }),
    ...mapState("contextmenuPlacemark", {
      categoryPlacemark: "category",
      headerPlacemark: "header",
    }),
    ...mapState("ymap", ["Map"]),
    ...mapState("contextmenuRoute", {
      strokeColorRoute: "strokeColor",
      strokeStyleRoute: "strokeStyle",
      strokeWidthRoute: "strokeWidth",
      strokeOpacityRoute: "strokeOpacity",
    }),
    ...mapState("contextmenuTerritory", {
      strokeColorTerritory: "strokeColor",
      strokeStyleTerritory: "strokeStyle",
      strokeWidthTerritory: "strokeWidth",
      strokeOpacityTerritory: "strokeOpacity",
      fillColorTerritory: "fillColor",
      fillOpacityTerritory: "fillOpacity",
    }),
    updateLatitude: {
      get() {
        return this.coordsCreate[0];
      },
      set(coord) {
        this.setLatitude(coord);
      },
    },
    updateLongitude: {
      get() {
        return this.coordsCreate[1];
      },
      set(coord) {
        this.setLongitude(coord);
      },
    },
  },
  methods: {
    ...mapMutations("dialogCreate", ["setLatitude", "setLongitude"]),
    ...mapMutations("modals", [
      // GeoObject
      "geoObjectDialogShow",
      "geoObjectDialogClose",
      // Controls
      "controlsDialogClose",
      // Message
      "messageDialogShow",
      "messageDialogClose",
      // Simple messages
      "alertSnackbarShow",
      "alertSnackbarClose",
    ]),
    ...mapMutations(["setDataAction"]),
    ...mapMutations("ymap", ["setEditableGeoObject"]),
    ...mapActions(["ajaxContextMenu"]),
    ...mapActions("dialogCreate", ["actionCreateNewGeoObjecte"]),
    // Rules
    rulesLatitude() {
      return [(coord) => helpers.checkLatitude(coord) || this.$t("message.92")];
    },
    rulesLongitude() {
      return [
        (coord) => helpers.checkLongitude(coord) || this.$t("message.92"),
      ];
    },
    // Messages error.
    messageError(title, text) {
      this.messageDialogShow({
        status: "error",
        title: title,
        text: text,
        cancelBtn: true,
        okBtn: false,
        actionBtnCancel: this.messageDialogClose,
        actionBtnOk: null,
      });
    },
    messageErrorAddCategory() {
      return (
        '<div class="djeym-fake-buttons" style="background:' +
        this.colorControlsTheme +
        ';">' +
        '<span class="mdi mdi-check-circle mdi-24px" style="color:' +
        this.colorButtonsTextTheme +
        ';"></span></div><br>' +
        i18n.t("message.105")
      );
    },
    messageErrorAddHeader() {
      return (
        '<div class="djeym-fake-buttons" style="background:' +
        this.colorControlsTheme +
        ';">' +
        '<span class="mdi mdi-page-layout-header mdi-24px" style="color:' +
        this.colorButtonsTextTheme +
        ';"></span></div><br>' +
        i18n.t("message.106")
      );
    },
    // Create Geo-object
    createGeoObject(index) {
      if (index === 0 || index === 3) {
        let latitude = window.$("#id-djeym-latitude").val();
        let longitude = window.$("#id-djeym-longitude").val();
        if (
          !helpers.checkLatitude(latitude) ||
          !helpers.checkLongitude(longitude)
        ) {
          this.messageError(this.$t("message.86"), this.$t("message.92"));
          return;
        }
      }

      const errorTitle = this.$t("message.86");
      const errorText = this.$t("message.92");
      this.controlsDialogClose();

      switch (index) {
        case 0: // Create Placemark.
          this.geoObjectDialogShow({
            title: this.$t("message.100"),
            editBtn: false,
            saveBtn: true,
            cancelBtn: true,
            deleteBtn: false,
            actionBtnEdit: null,
            actionBtnSave: () => {
              let isLatitude = helpers.checkLatitude(
                window.$("#id-djeym-latitude").val(),
              );
              let isLongitude = helpers.checkLongitude(
                window.$("#id-djeym-longitude").val(),
              );
              if (!isLatitude || !isLongitude) {
                this.messageError(errorTitle, errorText);
                return;
              }
              if (!this.categoryPlacemark) {
                this.alertSnackbarShow(this.messageErrorAddCategory());
                return;
              }
              if (this.headerPlacemark.length === 0) {
                this.alertSnackbarShow(this.messageErrorAddHeader());
                return;
              }
              this.setDataAction({ geoType: "placemark", actionType: "save" });
              this.ajaxContextMenu();
            },
            actionBtnCancel: () => {
              this.alertSnackbarClose();
              this.geoObjectDialogClose();
            },
            actionBtnDelete: null,
            componentPlacemark: true,
          });
          break;
        case 1: // Create Route.
        case 2: // Create Territory.
          // eslint-disable-next-line no-case-declarations
          let properties = {
            balloonContentHeader: "",
            balloonContentBody: "",
            balloonContentFooter: "",
            id: 0,
            categoryID: 0,
            subCategoryIDs: [],
          };
          // eslint-disable-next-line no-case-declarations
          let options = { draggable: true };
          if (index === 1) {
            // For Route.
            options["strokeWidth"] = this.strokeWidthRoute;
            options["strokeColor"] = this.strokeColorRoute;
            options["strokeStyle"] = this.strokeStyleRoute.value;
            options["strokeOpacity"] = this.strokeOpacityRoute;
          } else if (index === 2) {
            // For Territory.
            options["strokeWidth"] = this.strokeWidthTerritory;
            options["strokeColor"] = this.strokeColorTerritory;
            options["strokeStyle"] = this.strokeStyleTerritory.value;
            options["strokeOpacity"] = this.strokeOpacityTerritory;
            options["fillColor"] = this.fillColorTerritory;
            options["fillOpacity"] = this.fillOpacityTerritory;
          }
          // eslint-disable-next-line no-case-declarations
          const newGeoObjecte = new window.djeymYMaps.GeoObject(
            {
              geometry: {
                type: { 1: "LineString", 2: "Polygon" }[index],
                coordinates: [],
              },
              properties: properties,
            },
            options,
          );
          newGeoObjecte.events.add("contextmenu", () => {
            this.actionCreateNewGeoObjecte({
              title: i18n.t(`message.${{ 1: 109, 2: 111 }[index]}`),
              showSaveBtn: true,
              storeModuleName: {
                1: "contextmenuRoute",
                2: "contextmenuTerritory",
              }[index],
              messageErrorAddCategory: this.messageErrorAddCategory,
              messageErrorAddHeader: this.messageErrorAddHeader,
              geoType: { 1: "polyline", 2: "polygon" }[index],
            });
          });
          this.setEditableGeoObject(newGeoObjecte);
          this.Map.geoObjects.add(newGeoObjecte);
          this.actionCreateNewGeoObjecte({
            title: i18n.t(`message.${{ 1: 109, 2: 111 }[index]}`),
            showSaveBtn: false,
            storeModuleName: {
              1: "contextmenuRoute",
              2: "contextmenuTerritory",
            }[index],
            messageErrorAddCategory: this.messageErrorAddCategory,
            messageErrorAddHeader: this.messageErrorAddHeader,
            geoType: { 1: "polyline", 2: "polygon" }[index],
          });
          break;
        case 3: // Create Heat Point.
          this.geoObjectDialogShow({
            title: this.$t("message.97"),
            editBtn: false,
            saveBtn: true,
            cancelBtn: true,
            deleteBtn: false,
            actionBtnEdit: null,
            actionBtnSave: () => {
              const weight = parseInt(window.$("#id-djeym-weight").val());
              if (!/^\d+$/.test(weight)) {
                this.messageError(errorTitle, errorText);
                return;
              }
              this.setDataAction({ geoType: "heatpoint", actionType: "save" });
              this.ajaxContextMenu();
            },
            actionBtnCancel: this.geoObjectDialogClose,
            actionBtnDelete: null,
            componentHeatPoint: true,
          });
          break;
      }
    },
  },
};
</script>
