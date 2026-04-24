// @ts-check
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 120000,
  expect: {
    timeout: 15000,
  },
  use: {
    headless: true,
    viewport: { width: 1366, height: 768 },
    screenshot: 'only-on-failure',
    video: 'off',
    trace: 'on-first-retry',
  },
  reporter: [['list']],
});
