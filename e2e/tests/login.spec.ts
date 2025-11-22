import { test, expect } from '@playwright/test';
import { LoginPage } from '../fixtures/login-page';
import { ChatPage } from '../fixtures/chat-page';

test.describe('Login Form', { tag: ['@ui', '@login'] }, () => {
  test('page displays', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    // Page title matches for LIF Advisor Demo
    await expect(loginPage.page).toHaveTitle(/LIF Advisor/);

    // Check that Login Form header is displayed
    await expect(loginPage.formHeader).toBeVisible();

    // Check that Login Form Username field is displayed
    await expect(loginPage.usernameField).toBeVisible();

    // Check that Login Form Password field is displayed
    await expect(loginPage.passwordField).toBeVisible();

    // Check that the Sign In button is displayed and enabled
    await expect(loginPage.submitButton).toBeVisible();
    await expect(loginPage.submitButton).toBeEnabled();
  });

  test('can login successfully with valid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    const username = process.env.E2E_USERNAME;
    const password = process.env.E2E_PASSWORD;

    if (!username || !password) {
      throw new Error('E2E_USERNAME and E2E_PASSWORD must be set as environment variables.');
    }

    await loginPage.login(username, password);

    // confirm login is success and bot chat loads
    const chatPage = new ChatPage(page);

    await expect(chatPage.messageField).toBeVisible();
  });
});
