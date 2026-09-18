import { expect, test } from '@playwright/test';

const token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJlMmUtdXNlciIsInJvbGUiOiJBVVRIT1JJVFkiLCJleHAiOjQxMDI0NDQ4MDB9.signature';

test.beforeEach(async ({ page }) => {
  await page.addInitScript((value) => window.localStorage.setItem('climax_access_token', value), token);
  await page.route('**/api/v1/**', async (route) => {
    const url = route.request().url();
    const data = url.includes('/users/me') ? { id: 'e2e-user', email: 'e2e@example.invalid', full_name: 'E2E Authority', role: 'AUTHORITY', preferred_language: 'en', is_active: true } : url.includes('/analytics/summary') ? { observations: 0, reports: 0, incidents: 0, alerts: 0, interventions: 0 } : url.includes('/weather') ? {} : [];
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: true, data, total: Array.isArray(data) ? data.length : undefined }) });
  });
});

for (const path of ['/dashboard', '/map', '/reports', '/alerts']) {
  test(`${path} fits a 375px viewport`, async ({ page }) => {
    await page.goto(path);
    await expect(page.locator('main')).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);
    await expect(page.locator('nav').last()).toBeVisible();
  });
}
