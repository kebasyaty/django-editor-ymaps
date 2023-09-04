<!--
-----------------------------------
Component for creating Heat Points.
-----------------------------------
-->
<template>
  <v-conteiner fluid>
    <v-row>
      <v-col class="py-0" cols="12">
        <v-text-field v-model="updateTitle" :label="$t('message.94')" :placeholder="$t('message.94')"
          :hint="$t('message.96')" clearable dense full-width counter maxlength="60"
          :color="colorControlsTheme"></v-text-field>
      </v-col>
      <v-col class="py-0" cols="12">
        <v-text-field id="id-djeym-weight" v-model="updateWeight" :label="$t('message.95')"
          :placeholder="$t('message.95')" hint="0 ... 2147483647" clearable dense full-width maxlength="10"
          :rules="rulesWeight()" :color="colorControlsTheme"></v-text-field>
      </v-col>
    </v-row>
  </v-conteiner>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
  name: "ContextmenuHeatPoint",
  data: () => ({
    transTitle: [94, 95],
  }),
  computed: {
    ...mapState("contextmenuHeatPoint", ["title", "weight"]),
    ...mapState("generalSettings", ["colorControlsTheme"]),
    updateTitle: {
      get() {
        return this.title;
      },
      set(text) {
        this.setTitle(text);
      },
    },
    updateWeight: {
      get() {
        return this.weight;
      },
      set(num) {
        this.setWeight(num);
      },
    },
  },
  methods: {
    ...mapMutations("contextmenuHeatPoint", ["setTitle", "setWeight"]),
    ...mapActions("contextmenuHeatPoint", ["restoreDefaults"]),
    // Rules
    rulesWeight() {
      return [
        (val) => /^\d+$/.test(val) || this.$t("message.92"),
        (val) => +val <= 2147483647 || `${this.$t("message.99")} - 2147483647`,
      ];
    },
  },
  created() {
    // Restore Defaults
    this.restoreDefaults();
  },
};
</script>
