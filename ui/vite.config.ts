import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
// NOTE: Keeping it plugin-free for now; vite handles TS/JSX out of the box
export default defineConfig({
  plugins: [react()]
});
