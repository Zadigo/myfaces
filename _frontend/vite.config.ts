/// <reference types="vitest" />

import { resolve } from "path";
import { defineConfig, loadEnv } from "vite";

import vue from '@vitejs/plugin-vue';
import eslint from "vite-plugin-eslint";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const root = process.cwd();
  const env = loadEnv(mode, root);
  process.env = { ...process.env, ...env };

  return {    
    root,
    resolve: {
      alias: [
        {
          find: "@",
          replacement: resolve(__dirname, "src"),
        },
        {
          find: "src",
          replacement: resolve(__dirname, "src"),
        },
      ],
    },
    plugins: [vue(), eslint()],
    test: {
      globals: true,
      environment: "happy-dom",
    },
  };
});
