import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import eslint from 'vite-plugin-eslint2'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(), 
    eslint({
      lintOnStart: true,
      cache: false
    })
  ],
})
