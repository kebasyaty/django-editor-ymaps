/*
 * Module for the Help.vue component.
 */

export default {
  namespaced: true,
  state: {
    controls: {
      version: window.djeymVersion,
      requirements: {
        python: window.djeymPythonVersion,
        django: window.djeymDjangoVersion,
        vue: window.djeymVueVersion,
        vuetify: window.djeymVuetifyVersion,
      },
      links: [
        {
          icon: "language-python",
          title: "PyPI",
          link: "https://pypi.org/project/django-editor-ymaps/",
        },
        {
          icon: "github",
          title: "GitHub",
          link: "https://github.com/kebasyaty/django-editor-ymaps",
        },
        {
          icon: "email-outline",
          title: "Feedback",
          link: "mailto:kebasyaty@gmail.com?subject=DjEYM",
        },
        {
          icon: "license",
          title: "License",
          link: "https://github.com/kebasyaty/django-editor-ymaps/blob/master/LICENSE",
        },
      ],
    },
  },
  getters: {},
  mutations: {},
  actions: {},
};
