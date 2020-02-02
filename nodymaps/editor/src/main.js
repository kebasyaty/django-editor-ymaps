import Vue from 'vue'
import App from '@/App.vue'
import i18n from '@/i18n'
import vuetify from '@/plugins/vuetify'
import '@/assets/css/helpers.css'
import store from '@/store'
import VueCroppie from 'vue-croppie'
import 'croppie/croppie.css'

Vue.config.productionTip = false

Vue.use(VueCroppie)

new Vue({
  i18n,
  vuetify,
  store,
  render: h => h(App)
}).$mount('#djeym-app')
