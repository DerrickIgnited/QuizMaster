import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  vue: {
    template: {
      compilerOptions: {
        isCustomElement: (tag) => tag.startsWith('spline-viewer')
      }
    }
  }
})
