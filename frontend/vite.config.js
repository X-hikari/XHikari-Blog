import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { prismjsPlugin } from 'vite-plugin-prismjs'
import Components from 'unplugin-vue-components/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';

// https://vite.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        frontend: 'src/main.js',
        admin: 'src/admin.js',
      },
    },
  },
  // 设置scss的api类型为modern-compiler
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern-compiler',
        silenceDeprecations: ['legacy-js-api'],
      }
    }
  },
  plugins: [
    prismjsPlugin({
      languages: 'all', // 语言
      plugins: ['line-numbers','show-language','copy-to-clipboard','inline-color'],
      theme: 'okaidia',// 主题
      css: true,
    }),
    vue(),
    vueDevTools(),
    Components({
      resolvers: [ElementPlusResolver()], // 使用 Element Plus 的按需加载
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: true,       // 监听 0.0.0.0，允许外部访问
    port: 5173,       // 端口号，和 docker 映射端口对应
    // cors: true,    // 如果需要跨域，可以打开这行
  },
})
