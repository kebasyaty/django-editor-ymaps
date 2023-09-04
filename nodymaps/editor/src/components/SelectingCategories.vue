<!--
-------------------------------------
Component for selecting a categories.
-------------------------------------
-->
<template>
  <v-conteiner fluid>
    <div style="width: 422px; height: 500px; overflow: auto">
      <v-row dense justify="start" align="center" style="width: 422px">
        <v-col cols="12" class="pa-0">
          <v-card-subtitle class="py-0 font-italic">{{
            `-${$t("message.20")}`
          }}</v-card-subtitle>
        </v-col>
        <template v-for="item in categoryList">
          <v-col cols="1" :key="`icon-category-${item.id}`">
            <v-icon :color="item.color" class="pos-icon">{{
              item.icon
            }}</v-icon>
          </v-col>
          <v-col cols="11" :key="`switch-category-${item.id}`">
            <v-switch v-model="controls.category" inset :value="item.id.toString()" hide-details :label="item.title"
              class="mt-0" :color="colorControlsTheme"></v-switch>
          </v-col>
        </template>
        <v-col cols="12" class="pa-0">
          <v-card-subtitle class="pb-0 font-italic">{{
            `_${$t("message.21")}`
          }}</v-card-subtitle>
        </v-col>
        <template v-for="item in subcategoryList">
          <v-col cols="1" :key="`icon-subcategory-${item.id}`">
            <v-icon :color="item.color" class="pos-icon">{{
              item.icon
            }}</v-icon>
          </v-col>
          <v-col cols="11" :key="`switch-subcategory-${item.id}`">
            <v-switch v-model="controls.subcategories" multiple inset :value="item.id.toString()" hide-details
              :label="item.title" class="mt-0" :color="colorControlsTheme"></v-switch>
          </v-col>
        </template>
      </v-row>
    </div>
  </v-conteiner>
</template>

<script>
import { mapState, mapMutations } from "vuex";

export default {
  name: "SelectingCategories",
  data: () => ({
    categoryList: [],
    subcategoryList: [],
  }),
  computed: {
    ...mapState(["dataAction"]),
    ...mapState("categoryFilters", ["filters"]),
    ...mapState("generalSettings", ["colorControlsTheme"]),
    ...mapState("selectingCategories", ["controls"]),
  },
  methods: {
    ...mapMutations("selectingCategories", ["setCategory", "setSubcategories"]),
  },
  created() {
    // Initialization with Current Values.
    const currCategory = () => {
      let category = this.dataAction.category;
      return category !== null ? category.toString() : null;
    };
    this.setCategory(currCategory());
    this.setSubcategories(
      this.dataAction.subcategories.map((item) => item.toString()),
    );
    // Add Category Lists.
    switch (this.dataAction.geoType) {
      case "placemark":
        this.categoryList = this.filters.a;
        this.subcategoryList = this.filters.b;
        break;
      case "polyline":
        this.categoryList = this.filters.c;
        this.subcategoryList = this.filters.d;
        break;
      case "polygon":
        this.categoryList = this.filters.e;
        this.subcategoryList = this.filters.f;
        break;
    }
  },
  beforeDestroy() {
    // Restore Defaults.
    this.setCategory(null);
    this.setSubcategories([]);
  },
};
</script>

<style scoped>
.pos-icon {
  position: relative;
  top: 2px;
}
</style>
