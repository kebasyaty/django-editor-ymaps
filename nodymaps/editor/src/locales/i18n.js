import Vue from "vue";
import VueI18n from "vue-i18n";
import en from "@/locales/lang/en";
import ru from "@/locales/lang/ru";

Vue.use(VueI18n);

const messages = {
  en,
  ru,
};

let langCode = window.djeymLanguageCode.slice(0, 2);

if (!Object.keys(messages).includes(langCode)) {
  langCode = "en";
}

const opts = {
  locale: langCode,
  fallbackLocale: "en",
  messages,
};

export default new VueI18n(opts);
