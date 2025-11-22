import { test, expect } from '@playwright/test';
import { LoginPage } from '../fixtures/login-page';
import { ChatPage } from '../fixtures/chat-page';

const SIXTY_SECONDS = 60 * 1000;

test.describe('Chat Interface', { tag: ['@ui', '@chat'] }, () => {
  test.beforeEach(async ({ page }) => {
      const loginPage = new LoginPage(page);
      await loginPage.goto();

      const username = process.env.E2E_USERNAME;
      const password = process.env.E2E_PASSWORD;

      if (!username || !password) {
        throw new Error('E2E_USERNAME and E2E_PASSWORD must be set as environment variables.');
      }

      await loginPage.login(username, password);
  });

  test('page displays', async ({ page }) => {
    test.setTimeout(SIXTY_SECONDS); // wait up to 60 seconds for entire test
    const chatPage = new ChatPage(page);

    // form header should be visible
    await expect(chatPage.formHeader).toBeVisible();
    // message field should be visible
    await expect(chatPage.messageField).toBeVisible();
    // message submit button should be visible
    await expect(chatPage.submitButton).toBeVisible();
    // wait for bot to type
    await chatPage.page.getByTestId('typing').waitFor({ state: 'hidden', timeout: SIXTY_SECONDS });
    // bot should send welcoming messages
    // wait for bot to type
    const botMessages = chatPage.page.locator('[data-testid="message-item"][data-isbot="true"]');
    // Wait until the bot has sent at least 1 message
    await expect.poll(async () => await botMessages.count(), {
      message: 'Waiting for bot messages',
      timeout: SIXTY_SECONDS, // wait up to 60 seconds
    }).toBeGreaterThanOrEqual(1);
  });

  test('can send message to bot', async ({ page}) => {
    test.setTimeout(SIXTY_SECONDS); // wait up to 60 seconds for entire test
    const chatPage = new ChatPage(page);

    // wait for bot to type
    await chatPage.page.getByTestId('typing').waitFor({ state: 'hidden', timeout: SIXTY_SECONDS });
    const botMessages = chatPage.page.locator('[data-testid="message-item"][data-isbot="true"]');
    // Wait until the bot has sent at least 1 message
    await expect.poll(async () => await botMessages.count(), {
      message: 'Waiting for bot messages',
    }).toBeGreaterThanOrEqual(1);
    await chatPage.page.getByTestId('typing').waitFor({ state: 'hidden', timeout: SIXTY_SECONDS });
    const welcomeCount = await botMessages.count()

    await chatPage.sendMessage('Test message');

    // user message to bot should display
    const userMessageItem = await chatPage.page.locator('[data-testid="message-item"][data-isbot="false"]');
    await expect(userMessageItem).toBeVisible();

    // Wait until the bot has sent a reply
    await expect.poll(async () => await botMessages.count(), {
      message: 'Waiting for new bot messages',
      timeout: SIXTY_SECONDS, // wait up to 60 seconds
    }).toBeGreaterThanOrEqual(welcomeCount + 1);
  });
});
