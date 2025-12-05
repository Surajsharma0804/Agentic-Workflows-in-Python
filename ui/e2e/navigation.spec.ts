import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('API documentation is accessible', async ({ page }) => {
    await page.goto('/api/docs');
    
    // Swagger UI should load
    await expect(page.locator('.swagger-ui, #swagger-ui')).toBeVisible({ timeout: 10000 });
  });

  test('404 page handles unknown routes', async ({ page }) => {
    const response = await page.goto('/this-route-does-not-exist-12345');
    
    // Should either redirect to home or show 404
    const url = page.url();
    const is404 = response?.status() === 404;
    const redirectedHome = url.endsWith('/') || url.includes('/login');
    
    expect(is404 || redirectedHome).toBeTruthy();
  });

  test('Static assets load correctly', async ({ page }) => {
    await page.goto('/');
    
    // Check that CSS is loaded
    const styles = await page.locator('link[rel="stylesheet"], style').count();
    expect(styles).toBeGreaterThan(0);
    
    // Check that JavaScript is loaded
    const scripts = await page.locator('script[src]').count();
    expect(scripts).toBeGreaterThan(0);
  });
});
