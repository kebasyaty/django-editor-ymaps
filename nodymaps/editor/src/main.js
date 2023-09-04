import Vue from "vue";
import App from "@/App.vue";
import i18n from "@/locales/i18n";
import vuetify from "@/plugins/vuetify";
import "@/assets/css/helpers.css";
import store from "@/store";
import VueCroppie from "vue-croppie";
import "croppie/croppie.css";

// Global Config.
// https://vuejs.org/v2/api/index.html
if (process.env.NODE_ENV === "production") {
  Vue.config.productionTip = false;
  Vue.config.devtools = false;
  Vue.config.debug = false;
  Vue.config.silent = true;
}

Vue.use(VueCroppie);

new Vue({
  i18n,
  vuetify,
  store,
  render: (h) => h(App),
}).$mount("#djeym-app");
