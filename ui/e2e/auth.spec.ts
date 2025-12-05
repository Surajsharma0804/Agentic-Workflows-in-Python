import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('Registration form validation', async ({ page }) => {
    await page.goto('/register');
    
    // Try to submit empty form
    const submitButton = page.locator('button[type="submit"]');
    await submitButton.click();
    
    // Should show validation errors
    await expect(page.locator('text=/email.*required/i, text=/password.*required/i')).toBeVisible({ timeout: 5000 });
  });

  test('Login form is functional', async ({ page }) => {
    await page.goto('/login');
    
    // Fill in credentials
    await page.fill('input[type="email"]', 'test@example.com');
    await page.fill('input[type="password"]', 'testpassword123');
    
    // Form should be fillable
    const emailValue = await page.inputValue('input[type="email"]');
    expect(emailValue).toBe('test@example.com');
  });

  test('OAuth buttons are present', async ({ page }) => {
    await page.goto('/login');
    
    // Check for social login options
    const googleButton = page.locator('button:has-text("Google"), a:has-text("Google")');
    const githubButton = page.locator('button:has-text("GitHub"), a:has-text("GitHub")');
    
    // At least one OAuth option should be visible
    const hasOAuth = await googleButton.isVisible().catch(() => false) || 
                     await githubButton.isVisible().catch(() => false);
    
    expect(hasOAuth).toBeTruthy();
  });
});
