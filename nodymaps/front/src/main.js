import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import i18n from '@/i18n'
import '@/assets/css/helpers.css'

Vue.config.productionTip = false

new Vue({
  vuetify,
  i18n,
  render: h => h(App)
}).$mount('#djeym-app')
