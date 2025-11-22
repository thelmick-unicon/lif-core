# End to End testing

[Playwright](https://playwright.dev/) was chosen to facilitate testing the UI end to end with the backend services.

First install the dependencies with

```shell
npm install
```

Next run the playwright install which will download the chromium browser used by playwright to run tests

```shell
npx playwright install
```

To run the tests locally you need to define the following ENVs

```shell
export E2E_USERNAME="atsatrian_lifdemo@stateu.edu"
export E2E_PASSWORD="liffy4life!"
export BASE_URL="localhost:5174/"
```

After starting up the UI and backend, execute the tests with

```shell
npm run test
```
