import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const messages = {
  en: {
    message: {
      1: 'Places',
      2: 'Routes',
      3: 'Territories',
      4: 'Categories',
      5: 'Subcategories',
      6: 'Title',
      7: 'Upload image',
      8: 'Short description',
      9: 'The marker will appear on the map after successful moderation.',
      10: 'Save',
      11: 'Your E-mail',
      12: 'Required',
      13: 'Max 60 characters',
      14: 'Max 300 characters',
      15: 'Only JPG files',
      16: 'Close',
      17: '1. Click on the map in the right place.<br>2. If necessary, move the marker.',
      18: 'The File APIs are not fully supported in this browser.',
      19: 'Invalid address'
    }
  },
  ru: {
    message: {
      1: 'Места',
      2: 'Маршруты',
      3: 'Территории',
      4: 'Категории',
      5: 'Подкатегории',
      6: 'Название',
      7: 'Загрузите изображение',
      8: 'Краткое описание',
      9: 'Маркер появится на карте после успешной модерации.',
      10: 'Сохранить',
      11: 'Ваш E-mail',
      12: 'Обязательно',
      13: 'Макс. 60 символов',
      14: 'Макс. 300 символов',
      15: 'Только JPG файлы',
      16: 'Закрыть',
      17: '1. Кликните по карте в нужном месте.<br>2. Если необходимо, переместите маркер.',
      18: 'Файловые API не полностью поддерживаются в этом браузере.',
      19: 'Некорректный адрес'
    }
  }
}

let langCode = window.djeymLanguageCode.slice(0, 2)

if (!Object.keys(messages).includes(langCode)) {
  langCode = 'en'
}

const opts = {
  locale: langCode,
  messages
}

export default new VueI18n(opts)
