import { Locator, Page } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly formHeader: Locator;
  readonly usernameField: Locator;
  readonly passwordField: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.formHeader = page.getByRole('heading', { name: 'LIF Advisor' });
    this.usernameField = page.getByLabel('Username');
    this.passwordField = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign In' });
    this.page = page;
  }

  async goto() {
    await this.page.goto(`/`);
  }

  async login(username: string, password: string) {
    await this.usernameField.fill(username);
    await this.passwordField.fill(password);
    await this.submitButton.click();
  }
}