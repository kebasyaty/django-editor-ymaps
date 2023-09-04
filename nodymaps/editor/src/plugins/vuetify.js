import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

const opts = {
  theme: {
    defaultTheme: "dark",
    themes: {
      light: {
        accent: "#FF4081",
      },
      dark: {
        accent: "#FF4081",
      },
    },
  },
  icons: {
    iconfont: "mdi",
  },
};

export default new Vuetify(opts);
