<template>
  <v-app id="djeym-app" class="djeym" :style="`width:${widthMap};height:${heightMap};`">
    <v-sheet tile :width="widthMap" :height="heightMap" class="overflow-hidden" style="position: relative">
      <!-- Panel for filtering by categories -->
      <v-navigation-drawer v-if="createPanel" v-model="openPanel" app hide-overlay absolute temporary
        :permanent="isPermanentPanel" :width="widthPanel" :height="heightMap" :src="imgBgPanel">
        <v-container fluid class="pa-0" :style="`min-height: 100%; background-color: ${tinting};`">
          <v-card-actions class="pb-0">
            <v-spacer></v-spacer>
            <!-- Button - Сlose panel -->
            <v-btn icon @click.stop="[(isPermanentPanel = false), (openPanel = false)]" :ripple="effectRipple">
              <v-icon :color="colorControls">mdi-close</v-icon>
            </v-btn>
          </v-card-actions>
          <v-tabs v-model="tab" height="42" centered show-arrows center-active background-color="transparent"
            :color="colorControls" :style="isHideTabs ? 'position: relative; top: -45px; z-index: -10;' : ''
              ">
            <v-tabs-slider></v-tabs-slider>
            <template v-for="(icon, index) in сategoryIcons">
              <v-tab v-if="isShowTab(index)" :key="`button-tab-${index}`" :href="`#tab-${index}`" :ripple="effectRipple">
                <v-icon>{{ icon }}</v-icon>
              </v-tab>
            </template>
          </v-tabs>

          <!-- Controls for filtering geo-objects on Map -->
          <v-tabs-items v-model="tab" :style="`background-color: transparent;${isHideTabs ? 'top: -45px;' : ''
            }`">
            <v-tab-item v-for="(step, index) in 3" :key="`item-${step}`" :value="`tab-${index}`">
              <template v-if="index === 0">
                <v-card-title v-if="!hideGeoTypes" class="title pt-3 pb-0 px-3"
                  :class="centerGeoTypes ? 'justify-center' : ''">{{
                    geoTypeNameMarker ? geoTypeNameMarker : $t("message.1")
                  }}</v-card-title>
              </template>
              <template v-if="index === 1">
                <v-card-title v-if="!hideGeoTypes" class="title pt-3 pb-0 px-3"
                  :class="centerGeoTypes ? 'justify-center' : ''">{{
                    geoTypeNameRoute ? geoTypeNameRoute : $t("message.2")
                  }}</v-card-title>
              </template>
              <template v-if="index === 2">
                <v-card-title v-if="!hideGeoTypes" class="title pt-3 pb-0 px-3"
                  :class="centerGeoTypes ? 'justify-center' : ''">{{
                    geoTypeNameTerritory
                    ? geoTypeNameTerritory
                    : $t("message.3")
                  }}</v-card-title>
              </template>

              <v-divider v-if="!hideGeoTypes"></v-divider>
              <div v-if="hideGeoTypes" class="pt-4"></div>
              <v-container fluid class="pt-0">
                <v-list :shaped="controlsShape === 'shaped'" :rounded="controlsShape === 'rounded'"
                  :flat="controlsShape === 'flat'" dense v-for="(filter, modelKey, index2) in nextTwoFilters(index)"
                  :key="`filters-${modelKey}`" class="pa-0" style="background-color: transparent">
                  <template v-if="index2 === 0">
                    <v-card-subtitle class="font-italic px-0 pb-1" :class="index2 ? 'pt-1' : 'pt-0'">{{
                      filter.length && !hideGroupNames
                      ? groupNameCategories
                        ? groupNameCategories
                        : $t("message.4")
                      : ""
                    }}</v-card-subtitle>
                  </template>
                  <template v-if="index2 === 1">
                    <v-card-subtitle class="font-italic px-0 pb-1" :class="index2 ? 'pt-1' : 'pt-0'">{{
                      filter.length && !hideGroupNames
                      ? groupNameSubcategories
                        ? groupNameSubcategories
                        : $t("message.5")
                      : ""
                    }}</v-card-subtitle>
                  </template>

                  <v-list-item-group v-model="models[modelKey]" :multiple="(index2 + 1) % 2 == 0 ? true : multiple">
                    <v-list-item v-for="control in filter" :key="`control-${control.id}`" :color="control.color"
                      :ripple="effectRipple" class="mb-1" @click="
                        [
                          (control.isActive = !control.isActive),
                          filtering({ id: control.id, modelKey: modelKey }),
                        ]
                        ">
                      <v-list-item-icon class="my-auto mr-3">
                        <v-icon :color="control.color">{{
                          control.icon
                        }}</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title class="subtitle-2 djeym-white-space-normal">{{ control.title
                        }}</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-container>
            </v-tab-item>
          </v-tabs-items>
        </v-container>
      </v-navigation-drawer>

      <!-- A form for adding a custom marker to the map -->
      <v-navigation-drawer v-if="createForm" v-model="openForm" app right absolute temporary hide-overlay
        :permanent="isPermanentForm" :height="heightMap">
        <v-container fluid class="pt-0">
          <v-row>
            <v-col cols="12" class="pt-3 pb-5">
              <v-select v-model="updateCustomMarkerCategory" :items="customMarkerCategoryList" item-text="title"
                item-value="id" :label="$t('message.4')" dense prepend-icon="mdi-select-marker" :color="colorControls"
                :item-color="colorControls" hide-details></v-select>
            </v-col>
          </v-row>
          <v-row v-if="customMarkerSubcategoryList.length">
            <v-col cols="12" class="pt-3 pb-5">
              <v-select v-model="updateCustomMarkerSubcategories" :items="customMarkerSubcategoryList" item-text="title"
                item-value="id" :label="$t('message.5')" dense multiple prepend-icon="mdi-select-multiple-marker"
                :color="colorControls" :item-color="colorControls" hide-details></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="pt-0 pb-0">
              <v-file-input :label="$t('message.7')" prepend-icon="mdi-camera-outline" accept="image/jpeg"
                :hint="$t('message.15')" persistent-hint clearable :color="colorControls"
                @change="optimizeImage"></v-file-input>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="py-0">
              <v-text-field v-model="customMarkerTitle" :label="$t('message.6')" :color="colorControls" counter="60"
                prepend-icon="mdi-map-marker-circle" :rules="titleRules()" clearable></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="py-0">
              <v-textarea v-model="customMarkerDescription" counter="300" :label="$t('message.8')" rows="1"
                prepend-icon="mdi-tooltip-text-outline" :color="colorControls" :rules="descriptionRules()"
                clearable></v-textarea>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="py-0">
              <v-text-field v-model="customMarkerEmail" :label="$t('message.11')" :color="colorControls" maxlength="254"
                prepend-icon="mdi-email-outline" clearable :rules="emailRules()"></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="9">
              <v-btn tile depressed block color="green darken-1" :ripple="effectRipple" @click="saveCustomMarker()">
                <span class="white--text">{{ $t("message.10") }}</span>
              </v-btn>
            </v-col>
            <v-col cols="3" class="pl-0">
              <v-btn tile depressed block color="red darken-1" :ripple="effectRipple" @click="closeCustomMarker()">
                <v-icon color="white">mdi-close</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-navigation-drawer>

      <!-- YMap -->
      <v-container fluid class="pa-0 fill-height">
        <div fluid id="djeymYMapsID" class="djeym-ymap"></div>
      </v-container>

      <!-- Simple messages -->
      <v-snackbar v-model="showAlert" top multi-line vertical :timeout="0"
        :color="$vuetify.theme.dark ? '#323232' : 'white'">
        <v-btn class="mt-0 pb-0" icon color="white" :ripple="effectRipple" @click="showAlert = !showAlert">
          <v-icon color="pink">mdi-close</v-icon>
        </v-btn>
        <span v-html="`<table width='294' class='djeym-pos-relative djeym-pos-top--8'><tr><td>${textAlert}</td></tr></table>`
          " :class="$vuetify.theme.dark
    ? 'grey--text text--lighten-5'
    : 'grey--text text--darken-4'
    "></span>
      </v-snackbar>

      <!-- Progress bar -->
      <v-overlay z-index="10000" :value="progressBar">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>

      <!-- Canvas for image optimization -->
      <canvas id="djeym-canvas" class="djeym-hide"></canvas>
    </v-sheet>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    enableAjax: true, // For development.
    createPanel: false, // Create Filter by Categories.
    createForm: false, // Create Add Marker.
    themeType: "light", // 'dark' or 'light'
    colorControls: "#FFA000",
    colorButtonsText: "#212121",
    widthMap: "0",
    heightMap: "0",
    openPanel: false,
    tmpOpenPanel: false,
    isPermanentPanel: false,
    widthPanel: 380,
    imgBgPanel: undefined,
    tinting: "#00000000",
    tab: null,
    multiple: true, // Ability to select multiple categories together.
    isHideTabs: false,
    centerGeoTypes: false,
    hideGeoTypes: false,
    geoTypeNameMarker: "",
    geoTypeNameRoute: "",
    geoTypeNameTerritory: "",
    hideGroupNames: false,
    groupNameCategories: "",
    groupNameSubcategories: "",
    controlsShape: "shaped",
    effectRipple: true,
    openForm: false,
    isPermanentForm: false,
    customMarkerTitle: null,
    customMarkerDescription: null,
    customMarkerEmail: null,
    customMarkerCategory: null,
    customMarkerSubcategories: [],
    customMarkerCategoryList: [],
    customMarkerSubcategoryList: [],
    customMarkerCoordinates: [0, 0],
    customPlacemark: null,
    progressBar: false,
    optimizedImgBlob: null,
    currImg: null,
    сategoryIcons: ["mdi-map-marker", "mdi-routes", "mdi-beach"],
    transCategoryNames: [1, 2, 3],
    transGroupNames: [4, 5],
    filters: {
      a: [], // Categories of placemarks
      b: [], // Subcategories of placemarks
      c: [], // Categories of Routes
      d: [], // Subcategories of Routes
      e: [], // Categories of Territories
      f: [], // Subcategories of Territories
    },
    models: {
      a: [], // Categories of placemarks
      b: [], // Subcategories of placemarks
      c: [], // Categories of Routes
      d: [], // Subcategories of Routes
      e: [], // Categories of Territories
      f: [], // Subcategories of Territories
    },
    // Settings for the Map.
    Map: null,
    mapCursor: null,
    isActiveHeatmap: false,
    globalHeatmap: null,
    globalHeatPoints: null,
    globalObjMngPlacemark: null,
    globalObjMngPolyline: null,
    globalObjMngPolygon: null,
    // Simple messages
    showAlert: false,
    textAlert: "",
  }),
  computed: {
    updateCustomMarkerCategory: {
      get() {
        return this.customMarkerCategory;
      },
      set(id) {
        this.customMarkerCategory = id;
      },
    },
    updateCustomMarkerSubcategories: {
      get() {
        return this.customMarkerSubcategories;
      },
      set(arrID) {
        this.customMarkerSubcategories = arrID;
      },
    },
  },
  methods: {
    optimizeImage(file) {
      // Check for the various File API support.
      if (window.File && window.FileReader && window.FileList && window.Blob) {
        this.currImg = file;
        if (file !== null) {
          // Reduce the image size to the maximum allowed.
          const MAX_SIZE = 966;
          const MAX_WIDTH = MAX_SIZE;
          const MAX_HEIGHT = MAX_SIZE;
          const fr = new FileReader();
          const tempImg = new Image();
          let tempW;
          let tempH;
          fr.onload = () => {
            tempImg.onload = () => {
              tempW = tempImg.width;
              tempH = tempImg.height;
              // Check the image size.
              if (tempW > tempH) {
                if (tempW > MAX_WIDTH) {
                  tempH = Math.floor(tempH * (MAX_WIDTH / tempW));
                  tempW = MAX_WIDTH;
                }
              } else {
                if (tempH > MAX_HEIGHT) {
                  tempW = Math.floor((tempW * MAX_HEIGHT) / tempH);
                  tempH = MAX_HEIGHT;
                }
              }
              // Optimize image size.
              const canvas = window.document.getElementById("djeym-canvas");
              const ctx = canvas.getContext("2d");
              ctx.clearRect(0, 0, canvas.width, canvas.height);
              canvas.width = tempW;
              canvas.height = tempH;
              ctx.drawImage(tempImg, 0, 0, tempW, tempH);
              const dataURI = canvas.toDataURL(file.type);
              const getImageBlob = (dataURI) => {
                const binary = atob(dataURI.split(",")[1]);
                const ab = new ArrayBuffer(binary.length);
                const ia = new Uint8Array(ab);

                for (let idx = 0; idx < binary.length; idx++) {
                  ia[idx] = binary.charCodeAt(idx);
                }
                return new Blob([ab], { type: "image/jpeg" });
              };
              this.optimizedImgBlob = getImageBlob(dataURI);
            };
            // Add image for listening the event.
            tempImg.src = fr.result;
          };
          // Read in the image file as a data URL.
          fr.readAsDataURL(file);
        }
      } else {
        this.alertSnackbarShow(this.$t("message.18"));
      }
    },
    // Rules
    titleRules() {
      return [
        (val) => !!val || this.$t("message.12"),
        (val) => String(val).length <= 60 || this.$t("message.13"),
      ];
    },
    descriptionRules() {
      return [
        (val) => !!val || this.$t("message.12"),
        (val) => String(val).length <= 300 || this.$t("message.14"),
      ];
    },
    emailRules() {
      return [(val) => !!val || this.$t("message.12")];
    },
    // Show tabs if there are categories or subcategories.
    isShowTab(index) {
      const filters = this.filters;
      switch (index) {
        case 0:
          return filters.a.length > 0 || filters.b.length > 0;
        case 1:
          return filters.c.length > 0 || filters.d.length > 0;
        case 2:
          return filters.e.length > 0 || filters.f.length > 0;
      }
    },
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
    // Filtration of geo objects.
    generalFilter(data) {
      const categoriesIDs = [];
      const subcategoriesIDs = [];
      let countSubcategories = 0;

      this.filters[data.filterName1].forEach((item) => {
        if (item.isActive) {
          categoriesIDs.push(item.id);
        }
      });

      this.filters[data.filterName2].forEach((item) => {
        if (item.isActive) {
          subcategoriesIDs.push(item.id);
        }
      });

      countSubcategories = subcategoriesIDs.length;

      if (countSubcategories > 0) {
        this[data.globalObjMngName].setFilter((object) => {
          let tmpIDs = object.properties.subCategoryIDs;
          return (
            categoriesIDs.includes(object.properties.categoryID) &&
            tmpIDs.filter((num) => subcategoriesIDs.includes(num)).length ===
            countSubcategories
          );
        });
      } else {
        this[data.globalObjMngName].setFilter((object) => {
          return categoriesIDs.includes(object.properties.categoryID);
        });
      }
    },
    filtering(data) {
      const categoryID = data.id;
      const modelKey = data.modelKey;
      // If multiple = false - Disable previous selection.
      if (!this.multiple && ["a", "c", "e", "g", "i"].includes(modelKey)) {
        let filter = this.filters[modelKey];
        for (let idx = 0, len = filter.length; idx < len; idx++) {
          let control = filter[idx];
          if (control.isActive && control.id !== categoryID) {
            control.isActive = false;
            break;
          }
        }
      }
      // Filtration of geo objects
      switch (modelKey) {
        /* Categories of placemarks and
           Subcategories of placemarks */
        case "a":
        case "b":
          this.generalFilter({
            filterName1: "a",
            filterName2: "b",
            globalObjMngName: "globalObjMngPlacemark",
          });
          break;
        /* Categories of Routes and
           Subcategories of Routes */
        case "c":
        case "d":
          this.generalFilter({
            filterName1: "c",
            filterName2: "d",
            globalObjMngName: "globalObjMngPolyline",
          });
          break;
        /* Categories of Territories and
           Subcategories of Territories */
        case "e":
        case "f":
          this.generalFilter({
            filterName1: "e",
            filterName2: "f",
            globalObjMngName: "globalObjMngPolygon",
          });
          break;
      }
    },
    // Refresh visibility of geo objects.
    refreshVisibilityGeoObjects() {
      const filters = [
        {
          filterName1: "a",
          filterName2: "b",
          globalObjMngName: "globalObjMngPlacemark",
        },
        {
          filterName1: "c",
          filterName2: "d",
          globalObjMngName: "globalObjMngPolyline",
        },
        {
          filterName1: "e",
          filterName2: "f",
          globalObjMngName: "globalObjMngPolygon",
        },
      ];
      filters.forEach((item) => {
        this.generalFilter({
          filterName1: item.filterName1,
          filterName2: item.filterName2,
          globalObjMngName: item.globalObjMngName,
        });
      });
    },
    // Ajax - Error message.
    ajaxErrorMessage(jqxhr, textStatus, error, hint) {
      const err = `${textStatus} , ${error}`;
      const msg = `ERROR<br>Request Failed -> ${err}`;
      let errDetail = "";
      if (
        jqxhr.responseJSON !== undefined &&
        jqxhr.responseJSON.detail !== undefined
      ) {
        errDetail = jqxhr.responseJSON.detail;
      }
      window.console.log(msg);
      this.textAlert = `${msg}<br>Hint -> ${hint}<br>${errDetail}`;
      this.showAlert = true;
    },
    // Ajax - Upload all settings.
    uploadSettings() {
      if (this.enableAjax) {
        window.$.getJSON("/djeym/ajax-upload-settings-front/", {
          mapID: window.djeymMapID,
        })
          .done((data) => {
            // Settings for Panel and Filters.
            this.themeType = data.themeType;
            this.$vuetify.theme.dark = { light: false, dark: true }[
              this.themeType
            ];
            this.colorControls = data.colorControls;
            this.colorButtonsText = data.colorButtonsText;
            this.widthPanel = data.widthPanel;
            this.сategoryIcons = data.сategoryIcons;
            this.imgBgPanel = data.imgBgPanel || undefined;
            this.tinting = data.tinting;
            this.centerGeoTypes = data.centerGeoTypes;
            this.hideGeoTypes = data.hideGeoTypes;
            this.geoTypeNameMarker = data.geoTypeNameMarker;
            this.geoTypeNameRoute = data.geoTypeNameRoute;
            this.geoTypeNameTerritory = data.geoTypeNameTerritory;
            this.hideGroupNames = data.hideGroupNames;
            this.groupNameCategories = data.groupNameCategories;
            this.groupNameSubcategories = data.groupNameSubcategories;
            this.controlsShape = data.controlsShape;
            this.effectRipple = data.effectRipple;

            const multiple = data.multiple;
            const filters = data.filters;
            this.multiple = multiple;
            this.filters = filters;
            // Fill models.
            const models = this.models;
            let flag = true;
            for (let key in filters) {
              if (flag) {
                if (multiple) {
                  models[key] = Array.from(Array(filters[key].length).keys());
                } else {
                  models[key] = 0;
                }
              }
              flag = !flag;
            }
            // Add categories and subcategories for custom markers.
            this.customMarkerCategoryList = filters.a.map((item) => {
              return { id: item.id, title: item.title };
            });
            this.customMarkerSubcategoryList = filters.b.map((item) => {
              return { id: item.id, title: item.title };
            });
            // Do need to show the tabs ?
            const arr = [
              filters.a.length > 0 || filters.b.length > 0,
              filters.c.length > 0 || filters.d.length > 0,
              filters.e.length > 0 || filters.f.length > 0,
            ];
            this.isHideTabs = arr.filter((item) => item).length < 2;
            // Status of panel.
            if (data.openPanel) {
              this.tmpOpenPanel = true;
            } else {
              this.isPermanentPanel = false;
              this.tmpOpenPanel = false;
            }
            // Settings for a Map.
            this.isActiveHeatmap = data.heatmap.isActive;
            // Start create Map.
            window.djeymYMaps.ready().then(() => this.initMap(data));
          })
          .fail((jqxhr, textStatus, error) => {
            const hint = "Ajax - Upload all settings.";
            this.ajaxErrorMessage(jqxhr, textStatus, error, hint);
          });
      }
    },
    closeCustomMarker() {
      this.Map.balloon.close();
      this.Map.geoObjects.remove(this.customPlacemark);
      this.customMarkerTitle = null;
      this.customMarkerDescription = null;
      this.customMarkerEmail = null;
      this.updateCustomMarkerCategory = null;
      this.updateCustomMarkerSubcategories = [];
      this.customMarkerCoordinates = [0, 0];
      this.customPlacemark = null;
      this.isPermanentForm = false;
      this.openForm = false;
      this.progressBar = false;
      this.optimizedImgBlob = null;
      this.currImg = null;
      this.showAlert = false;
      this.mapCursor.remove();
    },
    saveCustomMarker() {
      this.Map.balloon.close();
      this.showAlert = false;
      const customMarkerTitle = this.customMarkerTitle;
      const customMarkerDescription = this.customMarkerDescription;
      const customMarkerEmail = this.customMarkerEmail;
      const customMarkerCategory = this.updateCustomMarkerCategory;

      if (!customMarkerCategory) {
        this.textAlert = `${this.$t("message.4")} --> ${this.$t("message.12")}`;
        this.showAlert = true;
        return;
      } else if (customMarkerTitle === null) {
        this.textAlert = `${this.$t("message.6")} --> ${this.$t("message.12")}`;
        this.showAlert = true;
        return;
      } else if (customMarkerDescription === null) {
        this.textAlert = `${this.$t("message.8")} --> ${this.$t("message.12")}`;
        this.showAlert = true;
        return;
      } else if (customMarkerEmail === null) {
        this.textAlert = `${this.$t("message.11")} --> ${this.$t(
          "message.12",
        )}`;
        this.showAlert = true;
        return;
      }

      this.progressBar = true;

      const fd = new FormData();
      fd.append("ymap", window.djeymMapID);
      fd.append("csrfmiddlewaretoken", window.djeymCSRFToken);
      fd.append("header", customMarkerTitle);
      fd.append("body", customMarkerDescription);
      fd.append("footer", "");
      fd.append("category", +customMarkerCategory);
      fd.append("user_email", customMarkerEmail);
      fd.append("icon_slug", "djeym-marker-default");
      fd.append("coordinates", JSON.stringify(this.customMarkerCoordinates));
      fd.append("active", false);
      fd.append("is_user_marker", true);

      if (this.currImg !== null) {
        fd.append("user_image", this.optimizedImgBlob, "pic.jpg");
      } else {
        fd.append("user_image", null);
      }

      this.updateCustomMarkerSubcategories.forEach((elem) => {
        fd.append("subcategories", +elem);
      });

      window.$.ajax({
        type: "POST",
        url: "/djeym/ajax-save-cusotm-marker/",
        data: fd,
        cache: false,
        processData: false,
        contentType: false,
        dataType: "json",
      })
        .done(() => {
          setTimeout(() => {
            this.closeCustomMarker();
            this.textAlert = this.$t("message.9");
            this.showAlert = true;
          }, 1000);
        })
        .fail((jqxhr, textStatus, error) => {
          setTimeout(() => {
            this.progressBar = false;
            const hint = "Ajax - Save custom marker.";
            this.ajaxErrorMessage(jqxhr, textStatus, error, hint);
          }, 1000);
        });
    },
    // Add Placemarks to manager.
    addPlacemarkTypeObjects(geoObjects) {
      this.globalObjMngPlacemark.add({
        type: "FeatureCollection",
        features: geoObjects,
      });
    },
    // Add Heat Points to manager.
    addHeatPoints(geoObjects) {
      if (this.isActiveHeatmap) {
        this.globalHeatPoints.features.push(geoObjects);
        this.globalHeatmap.setData(this.globalHeatPoints);
      }
    },
    // Add Polylines to manager.
    addPolylineTypeObjects(geoObjects) {
      this.globalObjMngPolyline.add({
        type: "FeatureCollection",
        features: geoObjects,
      });
    },
    // Add Polygons to manager.
    addPolygonTypeObjects(geoObjects) {
      this.globalObjMngPolygon.add({
        type: "FeatureCollection",
        features: geoObjects,
      });
    },
    // Start Map initialization.
    initMap(data) {
      const currentTile = data.currentTile;
      const randomTileUrl =
        currentTile !== null
          ? // eslint-disable-next-line no-new-func
          new Function("return " + currentTile.randomTileUrl)
          : null;

      const isTypeSelector = data.activeControls.includes("typeSelector");
      const activeControls = data.activeControls.filter(
        (title) => title !== "typeSelector",
      );
      const isRoundTheme = data.isRoundTheme;
      const heatmap = data.heatmap;

      // UPLOAD INDICATOR
      let spinTimers = [];
      const waitLoadContent = () => {
        // wait upload content to Balloon
        spinTimers[3] = setTimeout(() => {
          const loadIndicator = document.getElementById("djeymLoadIndicator");

          if (loadIndicator === null) {
            return;
          }

          loadIndicator.style.display = "block";

          const $images = window.$(
            "ymaps:regex(class, .*-balloon__content) img",
          );
          let imgLoaded = false;
          let counter = 0;

          if ($images.length === 0) {
            imgLoaded = true;
          } else {
            $images.each((idx, elem) => {
              if (elem.complete) {
                counter++;
              }
            });
            if (counter === $images.length) {
              imgLoaded = true;
            }
          }

          if (!imgLoaded) {
            spinTimers[2] = setTimeout(() => {
              waitLoadContent();
            }, 100);
          } else {
            window.$(".djeymUpdateInfoPreset").each((idx, elem) => {
              window.$(elem).trigger("click");
            });
            const modalLock = document.getElementById("djeymModalLock");
            if (modalLock !== null) {
              spinTimers[1] = setTimeout(() => {
                spinTimers[0] = setTimeout(() => {
                  modalLock.remove();
                }, 600);
                modalLock.style.opacity = 0;
              }, 200);
            }
          }
        }, 500);
      };

      // CUSTOM LAYOUTS
      // Custom layout for Balloon.
      const customBalloonContentLayout =
        window.djeymYMaps.templateLayoutFactory.createClass(
          '<div class="djeym-pos-relative djeym-fill-hight">' +
          '<div id="djeymModalLock"><div id="djeymLoadIndicator"></div></div>' +
          '<div class="djeym_ballon_header">{{ properties.balloonContentHeader|raw }}</div>' +
          '<div class="djeym_ballon_body">{{ properties.balloonContentBody|raw }}</div>' +
          '<div class="djeym_ballon_footer">{{ properties.balloonContentFooter|raw }}</div></div>',
        );
      // Custom layout for icon of Cluster.
      const customLayoutForClusterIcon =
        window.djeymYMaps.templateLayoutFactory.createClass(
          '<div class="djeym_layout_cluster_icon"><span style="background-color:' +
          data.colorBackgroundCountObjects +
          ";color:" +
          data.textColorCountObjects +
          ';">$[properties.geoObjects.length]</span></div>',
        );

      // CREATE A MAP
      const Map = new window.djeymYMaps.Map(
        "djeymYMapsID",
        {
          center: data.mapCenter,
          zoom: data.mapZoom,
          type: null,
          controls: isRoundTheme ? [] : activeControls,
        },
        {
          minZoom: currentTile !== null ? currentTile.minZoom : 0,
          maxZoom: currentTile !== null ? currentTile.maxZoom : 23,
          geoObjectHasBalloon: true,
          hasHint: false,
          geoObjectBalloonMinWidth: 322,
          geoObjectBalloonMaxWidth: 342,
          geoObjectBalloonMinHeight: window.djeymBalloonMinHeight,
          geoObjectBalloonPanelMaxMapArea: 0,
          geoObjectOpenBalloonOnClick: true,
        },
      );
      this.Map = Map;

      // Add map types.
      if (isTypeSelector) {
        // Add map types to TypeSelector.
        let typeSelector;
        if (isRoundTheme) {
          typeSelector = new window.djeymYMaps.control.TypeSelector({
            options: {
              layout: "round#listBoxLayout",
              size: "small",
              float: "none",
              position: {
                bottom: "40px",
                left: "10px",
              },
            },
          });
        } else {
          typeSelector = new window.djeymYMaps.control.TypeSelector();
          typeSelector.options.set(
            "panoramasItemMode",
            data.isPanorama ? "ifMercator" : "off",
          );
        }
        typeSelector.addMapType("yandex#map", 2);
        typeSelector.addMapType("yandex#satellite", 3);
        typeSelector.addMapType("yandex#hybrid", 4);
        // Create a map type for the current tile.
        if (currentTile !== null) {
          let currentTilLayer = function () {
            let layer = new window.djeymYMaps.Layer(randomTileUrl(), {
              projection: window.djeymYMaps.projection.sphericalMercator,
            });
            // Copyright.
            layer.getCopyrights = function () {
              return window.djeymYMaps.vow.resolve(currentTile.copyrights);
            };
            // The range of available sizes.
            layer.getZoomRange = function () {
              return window.djeymYMaps.vow.resolve([
                currentTile.minZoom,
                currentTile.maxZoom,
              ]);
            };
            return layer;
          };
          // Add a layer to the storage.
          window.djeymYMaps.layer.storage.add("tile#aerial", currentTilLayer);
          // Create map types.
          let currentTilMapType = new window.djeymYMaps.MapType(
            currentTile.title,
            ["tile#aerial"],
          );
          // Add map types in storage.
          window.djeymYMaps.mapType.storage.add(
            "tile#current",
            currentTilMapType,
          );
          typeSelector.addMapType("tile#current", 1);
          // Use custom current map type.
          Map.controls.add(typeSelector);
          Map.setType("tile#current", { checkZoomRange: true });
        } else {
          // Use default map type.
          Map.controls.add(typeSelector);
          Map.setType("yandex#map");
        }
      } else {
        if (currentTile !== null) {
          // Connect a third-party source of tiles.
          Map.layers.add(
            new window.djeymYMaps.Layer(randomTileUrl(), {
              projection: window.djeymYMaps.projection.sphericalMercator,
            }),
          );
          // Add Copyrights.
          Map.copyrights.add(currentTile.copyrights);
        } else {
          // Use default map type.
          Map.setType("yandex#map");
        }
      }

      // Use round theme for controls.
      if (isRoundTheme) {
        if (activeControls.includes("geolocationControl")) {
          let geolocationControl =
            new window.djeymYMaps.control.GeolocationControl({
              options: {
                layout: "round#buttonLayout",
                floatIndex: 4,
                size: "small",
              },
            });
          Map.controls.add(geolocationControl);
        }
        if (activeControls.includes("routeButtonControl")) {
          let customRouteButton = new window.djeymYMaps.control.Button({
            data: {
              iconType: "routes",
            },
            options: {
              layout: "round#buttonLayout",
              floatIndex: 2,
              size: "small",
            },
          });
          Map.controls.add(customRouteButton);
          Map.controls.add("routePanelControl", {
            visible: false,
            showHeader: true,
            floatIndex: 1,
            float: "left",
            top: "auto",
            right: "auto",
            bottom: "auto",
            left: "auto",
          });
          let routePanelControl = Map.controls.get("routePanelControl");
          customRouteButton.events.add("press", () => {
            if (routePanelControl.options.get("visible")) {
              routePanelControl.options.set("visible", false);
              routePanelControl.routePanel.state.set("fromEnabled", false);
            } else {
              routePanelControl.options.set("visible", true);
              routePanelControl.routePanel.state.set("fromEnabled", true);
            }
          });
        }
        if (activeControls.includes("searchControl")) {
          let searchControl = new window.djeymYMaps.control.SearchControl({
            options: {
              size: "small",
              float: "none",
              position: {
                top: -40,
              },
            },
          });
          let customSearchControl = new window.djeymYMaps.control.Button({
            data: {
              iconType: "loupe",
            },
            options: {
              layout: "round#buttonLayout",
              size: "small",
              floatIndex: 3,
              selectOnClick: false,
              float: "left",
            },
          });
          customSearchControl.events.add("press", () => {
            window
              .$(
                "ymaps:regex(class, ymaps-.+-float-button-icon_icon_magnifier)",
              )
              .trigger("click");
          });
          Map.controls.add(searchControl);
          Map.controls.add(customSearchControl);
        }
        if (activeControls.includes("trafficControl")) {
          let trafficControl = new window.djeymYMaps.control.TrafficControl({
            options: {
              visible: false,
            },
          });

          let customTrafficControl = new window.djeymYMaps.control.Button({
            data: {
              iconType: "traffic",
            },
            options: {
              layout: "round#buttonLayout",
              floatIndex: 1,
              size: "small",
              float: "right",
            },
          });
          customTrafficControl.events.add("press", () => {
            if (trafficControl.isTrafficShown()) {
              trafficControl.hideTraffic();
            } else {
              trafficControl.showTraffic();
            }
          });
          Map.controls.add(trafficControl);
          Map.controls.add(customTrafficControl);
        }
        if (activeControls.includes("fullscreenControl")) {
          let fullscreenControl =
            new window.djeymYMaps.control.FullscreenControl({
              data: {
                iconType: "expand",
              },
              options: {
                layout: "round#buttonLayout",
                size: "small",
                floatIndex: 2,
                selectOnClick: false,
              },
            });
          fullscreenControl.events.add("press", () => {
            if (!fullscreenControl.isSelected()) {
              Map.container.enterFullscreen();
            } else {
              Map.container.exitFullscreen();
            }
          });
          Map.container.events.add("fullscreenenter", () => {
            fullscreenControl.data.set({ iconType: "collapse" });
            fullscreenControl.select();
          });
          Map.container.events.add("fullscreenexit", () => {
            fullscreenControl.data.set({ iconType: "expand" });
            fullscreenControl.deselect();
          });
          Map.controls.add(fullscreenControl);
        }
        if (activeControls.includes("zoomControl")) {
          let zoomControl = new window.djeymYMaps.control.ZoomControl({
            options: {
              layout: "round#zoomLayout",
              size: "small",
            },
          });
          Map.controls.add(zoomControl);
        }
        if (activeControls.includes("rulerControl")) {
          let rulerControl = new window.djeymYMaps.control.RulerControl({
            options: {
              layout: "round#rulerLayout",
              size: "small",
              position: {
                bottom: "40px",
                right: "10px",
              },
            },
          });
          Map.controls.add(rulerControl);
        }
      } else {
        // Enable search by organization.
        if (
          activeControls.includes("searchControl") &&
          data.isSearchByOrganization
        ) {
          Map.controls
            .get("searchControl")
            .options.set("provider", "yandex#search");
        }
      }

      // Set up a heatmap.
      if (heatmap.isActive) {
        window.djeymYMaps.modules.require(["Heatmap"], (Heatmap) => {
          this.globalHeatPoints = {
            type: "FeatureCollection",
            features: [],
          };
          this.globalHeatmap = new Heatmap(this.globalHeatPoints, {
            radius: heatmap.radius,
            dissipating: heatmap.dissipating,
            opacity: heatmap.opacity,
            intensityOfMidpoint: heatmap.intensity,
            gradient: {
              0.1: heatmap.gradient.color1,
              0.2: heatmap.gradient.color2,
              0.7: heatmap.gradient.color3,
              1.0: heatmap.gradient.color4,
            },
          });
          this.globalHeatmap.setMap(Map);
        });
      }

      // ADD EVENTS TO THE MAP
      // Open Balloon - Run Preset
      Map.events.add("balloonopen", () => {
        for (let idx = 0, len = spinTimers.length; idx < len; idx++) {
          clearTimeout(spinTimers[idx]);
        }
        waitLoadContent();
      });
      // Restart Preset
      window
        .$(document)
        .on(
          "click",
          "ymaps:regex(class, .*-cluster-tabs__menu-item.*), " +
          "ymaps:regex(class, .*-cluster-carousel__pager-item.*), " +
          "ymaps:regex(class, .*-cluster-carousel__nav.*)",
          (event) => {
            event.stopPropagation();
            for (let idx = 0, len = spinTimers.length; idx < len; idx++) {
              clearTimeout(spinTimers[idx]);
            }
            waitLoadContent();
          },
        );

      // CREATE MANAGERS GEO OBJECTS
      const geoObjectBalloonOptions = {
        geoObjectHasBalloon: true,
        geoObjectHasHint: false,
        geoObjectBalloonMinWidth: 322,
        geoObjectBalloonMaxWidth: 342,
        geoObjectBalloonMinHeight: window.djeymBalloonMinHeight,
        geoObjectBalloonPanelMaxMapArea: 0,
        geoObjectBalloonContentLayout: customBalloonContentLayout,
        geoObjectOpenBalloonOnClick: false,
      };

      const clusterRadius = parseInt(
        Math.min.apply(null, data.cluster.size) / 2,
      );
      const objMngPlacemarkOptions = {
        clusterize: data.isClusterize,
        clusterHasBalloon: true,
        clusterHasHint: false,
        clusterIconContentLayout: data.isIconContentLayout
          ? customLayoutForClusterIcon
          : null,
        clusterBalloonItemContentLayout: customBalloonContentLayout,
        clusterDisableClickZoom: true,
        clusterOpenBalloonOnClick: false,
        showInAlphabeticalOrder: false,
        clusterBalloonPanelMaxMapArea: 0,
        clusterMaxZoom: Map.options.get("maxZoom"),
        gridSize: 128,
        margin: clusterRadius + 2,
        clusterBalloonContentLayout: data.balloonContentLayout,
        clusterIcons: [
          {
            href: data.cluster.url,
            size: data.cluster.size,
            offset: data.cluster.offset,
            shape: {
              type: "Circle",
              coordinates: [0, 0],
              radius: clusterRadius,
            },
          },
        ],
      };

      Object.assign(objMngPlacemarkOptions, geoObjectBalloonOptions);

      // Create a manager for Placemarks.
      this.globalObjMngPlacemark = new window.djeymYMaps.ObjectManager(
        objMngPlacemarkOptions,
      );

      // Create a manager for Polylines.
      this.globalObjMngPolyline = new window.djeymYMaps.ObjectManager(
        geoObjectBalloonOptions,
      );

      // Create a manager for Polygons.
      this.globalObjMngPolygon = new window.djeymYMaps.ObjectManager(
        geoObjectBalloonOptions,
      );

      // Cleaning content in a geo-object.
      const clearContentGeoObject = (geoObject) => {
        geoObject.properties.balloonContentHeader = "";
        geoObject.properties.balloonContentBody = "";
        geoObject.properties.balloonContentFooter = "";
        return geoObject;
      };

      // Ajax, uploading content for Cluster (balloonContent) - Header, Body and Footer.
      this.globalObjMngPlacemark.clusters.events.add("click", (event) => {
        Map.balloon.close(true);

        const objectId = event.get("objectId");
        const cluster = this.globalObjMngPlacemark.clusters.getById(objectId);
        const geoObjects = cluster.properties.geoObjects;
        const countObjs = geoObjects.length;
        const ids = [];

        for (let idx = 0; idx < countObjs; idx++) {
          ids.push(geoObjects[idx].properties.id);
        }

        for (let idx = 0; idx < countObjs; idx++) {
          this.globalObjMngPlacemark.clusters.balloon.setData(
            clearContentGeoObject(geoObjects[idx]),
          );
        }

        setTimeout(() => {
          this.globalObjMngPlacemark.clusters.balloon.open(objectId);
        }, 100);

        window.$.get("/djeym/ajax-balloon-content/", {
          ids: JSON.stringify(ids),
          objType: "Point",
          isPresets: "True",
        })
          .done(function (data) {
            for (let idx = 0, marker, content; idx < countObjs; idx++) {
              marker = geoObjects[idx];
              content = data[marker.properties.id];
              marker.properties.balloonContentHeader = content.header;
              marker.properties.balloonContentBody = content.body;
              marker.properties.balloonContentFooter = content.footer;
            }
            window
              .$("ymaps:regex(class, .*-cluster-tabs__menu-item.*)")
              .eq(0)
              .trigger("click");
          })
          .fail((jqxhr, textStatus, error) => {
            const err = `${textStatus} , ${error}`;
            const msg = `ERROR<br>Request Failed -> ${err}`;
            const hint = "Ajax - Uploading content for Cluster.";
            window.console.log(msg);
            this.textAlert = `${msg} <br>Hint -> ${hint}`;
            this.showAlert = true;
          });
      });

      /* Ajax, uploading content for geo objects (balloonsContent) -
         Header, Body and Footer. */
      const ajaxGetBalloonContent = (geoObject) => {
        Map.balloon.close(true);
        const geoObjectType = geoObject.geometry.type;

        setTimeout(() => {
          if (geoObjectType === "Point") {
            this.globalObjMngPlacemark.objects.balloon.open(geoObject.id);
          } else if (geoObjectType === "LineString") {
            this.globalObjMngPolyline.objects.balloon.open(geoObject.id);
          } else if (geoObjectType === "Polygon") {
            this.globalObjMngPolygon.objects.balloon.open(geoObject.id);
          }
        }, 100);

        window.$.get("/djeym/ajax-balloon-content/", {
          objID: geoObject.properties.id,
          objType: geoObjectType,
          isPresets: "True",
        })
          .done((data) => {
            geoObject.properties.balloonContentHeader = data.header;
            geoObject.properties.balloonContentBody = data.body;
            geoObject.properties.balloonContentFooter = data.footer;

            if (geoObjectType === "Point") {
              this.globalObjMngPlacemark.objects.balloon.setData(geoObject);
            } else if (geoObjectType === "LineString") {
              this.globalObjMngPolyline.objects.balloon.setData(geoObject);
            } else if (geoObjectType === "Polygon") {
              this.globalObjMngPolygon.objects.balloon.setData(geoObject);
            }
          })
          .fail((jqxhr, textStatus, error) => {
            const err = `${textStatus} , ${error}`;
            const msg = `ERROR<br>Request Failed -> ${err}`;
            const hint = "Ajax - Uploading content for geo objects.";
            window.console.log(msg);
            this.textAlert = `${msg} <br>Hint -> ${hint}`;
            this.showAlert = true;
          });
      };

      // Ajax, uploading content for "balloonContent" - Header, Body and Footer.
      this.globalObjMngPlacemark.objects.events.add("click", (event) => {
        const objectId = event.get("objectId");
        let geoObject = this.globalObjMngPlacemark.objects.getById(objectId);
        geoObject = clearContentGeoObject(geoObject);
        ajaxGetBalloonContent(geoObject);
      });
      this.globalObjMngPolyline.objects.events.add("click", (event) => {
        const objectId = event.get("objectId");
        let geoObject = this.globalObjMngPolyline.objects.getById(objectId);
        geoObject = clearContentGeoObject(geoObject);
        ajaxGetBalloonContent(geoObject);
      });
      this.globalObjMngPolygon.objects.events.add("click", (event) => {
        const objectId = event.get("objectId");
        let geoObject = this.globalObjMngPolygon.objects.getById(objectId);
        geoObject = clearContentGeoObject(geoObject);
        ajaxGetBalloonContent(geoObject);
      });

      // Add object manager to map.
      Map.geoObjects.add(this.globalObjMngPlacemark);
      Map.geoObjects.add(this.globalObjMngPolyline);
      Map.geoObjects.add(this.globalObjMngPolygon);

      // Run filtering by categories.
      this.refreshVisibilityGeoObjects();

      // AJAX - LOADING GEO OBJECTS TO MAP
      // Upload Placemarks.
      const loadPlacemarkGeoObjects = (offset) => {
        window.$.getJSON("/djeym/ajax-upload-placemarks/", {
          mapID: window.djeymMapID,
          offset: offset,
        })
          .done((data) => {
            setTimeout(() => {
              if (data.length > 0) {
                this.addPlacemarkTypeObjects(data);
                offset += 1000;
                loadPlacemarkGeoObjects(offset);
              } else {
                setTimeout(() => loadHeatPoints(0), 0);
              }
            }, 0);
          })
          .fail((jqxhr, textStatus, error) => {
            const err = `${textStatus} , ${error}`;
            const msg = `ERROR<br>Request Failed -> ${err}`;
            const hint = "Ajax - Load Placemarks.";
            window.console.log(msg);
            this.textAlert = `${msg} <br>Hint -> ${hint}`;
            this.showAlert = true;
          });
      };
      loadPlacemarkGeoObjects(0);

      // Upload Heat Points.
      const loadHeatPoints = (offset) => {
        window.$.getJSON("/djeym/ajax-upload-heat-points/", {
          mapID: window.djeymMapID,
          offset: offset,
        })
          .done((data) => {
            setTimeout(() => {
              if (data.length > 0) {
                this.addHeatPoints(data);
                offset += 1000;
                loadHeatPoints(offset);
              } else {
                setTimeout(() => loadPolylineGeoObjects(0), 0);
              }
            }, 0);
          })
          .fail((jqxhr, textStatus, error) => {
            const err = `${textStatus} , ${error}`;
            const msg = `ERROR<br>Request Failed -> ${err}`;
            const hint = "Ajax - Loading Thermal points.";
            window.console.log(msg);
            this.textAlert = `${msg} <br>Hint -> ${hint}`;
            this.showAlert = true;
          });
      };

      // Upload Polylines.
      const loadPolylineGeoObjects = (offset) => {
        window.$.getJSON("/djeym/ajax-upload-polylines/", {
          mapID: window.djeymMapID,
          offset: offset,
        })
          .done((data) => {
            setTimeout(() => {
              if (data.length > 0) {
                this.addPolylineTypeObjects(data);
                offset += 500;
                loadPolylineGeoObjects(offset);
              } else {
                setTimeout(() => loadPolygonGeoObjects(0), 0);
              }
            }, 0);
          })
          .fail((jqxhr, textStatus, error) => {
            const err = `${textStatus} , ${error}`;
            const msg = `ERROR<br>Request Failed -> ${err}`;
            const hint = "Ajax - Load Polylines.";
            window.console.log(msg);
            this.textAlert = `${msg} <br>Hint -> ${hint}`;
            this.showAlert = true;
          });
      };

      // Upload Polygons.
      const loadPolygonGeoObjects = (offset) => {
        window.$.getJSON("/djeym/ajax-upload-polygons/", {
          mapID: window.djeymMapID,
          offset: offset,
        })
          .done((data) => {
            setTimeout(() => {
              if (data.length > 0) {
                this.addPolygonTypeObjects(data);
                offset += 500;
                loadPolygonGeoObjects(offset);
              } else {
                setTimeout(() => {
                  if (window.$("#djeym-open-panel").length) {
                    this.createPanel = true; // Create Filter by Categories.
                  }
                  if (window.$("#djeym-add-marker").length) {
                    this.createForm = true; // Create Add Marker.
                  }
                  setTimeout(
                    () => {
                      if (this.tmpOpenPanel) {
                        this.openPanel = true;
                        this.isPermanentPanel = true;
                      }
                      window
                        .$(document)
                        .on("click", "#djeym-open-panel", () => {
                          this.openPanel = true;
                          this.isPermanentPanel = true;
                        });
                      window
                        .$(document)
                        .on("click", "#djeym-add-marker", () => {
                          if (!this.openForm) {
                            this.Map.balloon.close();
                            this.mapCursor = this.Map.cursors.push("arrow");
                            this.isPermanentPanel = false;
                            this.openPanel = false;
                            this.openForm = true;
                            this.isPermanentForm = true;
                            // Create custom marker.
                            this.customPlacemark =
                              new window.djeymYMaps.Placemark(
                                Map.getCenter(),
                                {
                                  hintContent: "",
                                  balloonContent: "",
                                },
                                {
                                  iconLayout: "default#image",
                                  iconImageHref: "/static/djeym/img/center.svg",
                                  iconImageSize: [32, 60],
                                  iconImageOffset: [-16, -60],
                                  draggable: true,
                                },
                              );
                            // Add 'drag' event for custom Placemark.
                            this.customPlacemark.events.add("drag", (event) => {
                              const coords = event
                                .get("target")
                                .geometry.getCoordinates();
                              this.customMarkerCoordinates = coords;
                            });
                            // Add custom Placemark on Map.
                            this.Map.geoObjects.add(this.customPlacemark);
                            // Help - How to specify the coordinates.
                            this.textAlert = this.$t("message.17");
                            this.showAlert = true;
                          }
                        });
                      // Add 'click' event for custom Placemark.
                      this.Map.events.add("click", (event) => {
                        if (this.customPlacemark !== null) {
                          const coords = event.get("coords");
                          this.customPlacemark.geometry.setCoordinates(coords);
                          this.customMarkerCoordinates = coords;
                        }
                      });
                    },
                    this.imgBgPanel !== undefined ? 1000 : 0,
                  );
                }, 0);
              }
            }, 0);
          })
          .fail((jqxhr, textStatus, error) => {
            const err = `${textStatus} , ${error}`;
            const msg = `ERROR<br>Request Failed -> ${err}`;
            const hint = "Ajax - Load Polygons.";
            window.console.log(msg);
            this.textAlert = `${msg} <br>Hint -> ${hint}`;
            this.showAlert = true;
          });
      };
    },
  },
  created() {
    // Add custom map size.
    this.widthMap = window.djeymWidthMap;
    this.heightMap = window.djeymHeightMap;
    // Show buttons - djeym-open-panel, djeym-add-marker
    if (window.djeymMapID !== undefined) {
      window.$(".djeym-button-bar").show();
    }
    // Ajax - Upload all settings.
    this.uploadSettings();
  },
};
</script>

<style scoped>
.djeym-ymap {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}
</style>
