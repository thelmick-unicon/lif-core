import { Locator, Page } from "@playwright/test";

export class ChatPage {
  readonly page: Page;
  readonly formHeader: Locator;
  readonly messageField: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.formHeader = page.getByRole('heading', { name: 'LIF Advisor' });
    this.messageField = page.getByLabel('Message');
    this.submitButton = page.getByRole('button', { name: 'Send Message'});
    this.page = page;
  }

  async goto() {
    await this.page.goto(`/`);
  }

  async sendMessage(message: string) {
    await this.messageField.fill(message);
    await this.submitButton.click();
  }
}