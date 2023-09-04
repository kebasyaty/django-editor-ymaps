const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  parallel: false,
  transpileDependencies: ["vuetify"],
  publicPath: "/",
  configureWebpack: {
    resolve: {
      modules: [],
      fallback: {
        fs: false,
        tls: false,
        net: false,
        path: false,
        zlib: false,
        http: false,
        https: false,
        stream: false,
        crypto: false,
      },
    },
    plugins: [],
  },
});
