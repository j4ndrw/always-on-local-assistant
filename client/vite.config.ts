import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
      "./expressions.js": path.resolve(
        __dirname,
        "./src/monkey-patches/piper-wasm/expressions.js",
      ),
    },
  },
  optimizeDeps: {
    exclude: ['piper-wasm'],
  },
  build: {
    rollupOptions: {
      output: {
        assetFileNames: "assets/[name][extname]",
      },
    },
  },
});
