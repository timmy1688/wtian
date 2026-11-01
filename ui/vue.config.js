const { defineConfig } = require('@vue/cli-service')

/** Local backend used by `npm run serve`; override with API_PROXY_TARGET */
const API_PROXY_TARGET = process.env.API_PROXY_TARGET || 'http://127.0.0.1:8000'

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: API_PROXY_TARGET,
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
    },
  },
})
