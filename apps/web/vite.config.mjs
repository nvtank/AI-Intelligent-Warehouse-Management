import { defineConfig } from "vitest/config";

export default defineConfig({
  envDir: "../..",
  test: {
    environment: "node",
    clearMocks: true,
    restoreMocks: true,
    unstubGlobals: true,
  },
});
