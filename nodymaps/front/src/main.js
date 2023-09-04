import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import i18n from "@/i18n";
import "@/assets/css/helpers.css";

// Global Config.
// https://vuejs.org/v2/api/index.html
if (process.env.NODE_ENV === "production") {
  Vue.config.productionTip = false;
  Vue.config.devtools = false;
  Vue.config.debug = false;
  Vue.config.silent = true;
}

new Vue({
  vuetify,
  i18n,
  render: (h) => h(App),
}).$mount("#djeym-app");
