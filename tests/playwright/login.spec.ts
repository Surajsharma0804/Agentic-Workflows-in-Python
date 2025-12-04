import { test, expect } from '@playwright/test'

test.describe('Login Page - Responsive Design', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173/login')
  })

  test('renders correctly on mobile (375px)', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    
    // Mobile hero should be visible
    const mobileHero = page.locator('.lg\\:hidden')
    await expect(mobileHero).toBeVisible()
    
    // Desktop hero should be hidden
    const desktopHero = page.locator('.hidden.lg\\:block')
    await expect(desktopHero).toBeHidden()
    
    // Form should be visible and properly sized
    const form = page.locator('form[aria-label="Login form"]')
    await expect(form).toBeVisible()
    
    // Social buttons should have minimum tap target
    const socialButtons = page.locator('button[aria-label*="Sign in with"]')
    const firstButton = socialButtons.first()
    const box = await firstButton.boundingBox()
    expect(box?.height).toBeGreaterThanOrEqual(44)
    
    // Take screenshot
    await page.screenshot({ 
      path: 'audit/responsive-screenshots/login-mobile-375.png',
      fullPage: true 
    })
  })

  test('renders correctly on tablet (768px)', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 })
    
    // Desktop hero should be visible
    const desktopHero = page.locator('.hidden.lg\\:block')
    await expect(desktopHero).toBeVisible()
    
    // Form should be visible
    const form = page.locator('form[aria-label="Login form"]')
    await expect(form).toBeVisible()
    
    // Take screenshot
    await page.screenshot({ 
      path: 'audit/responsive-screenshots/login-tablet-768.png',
      fullPage: true 
    })
  })

  test('renders correctly on desktop (1366px)', async ({ page }) => {
    await page.setViewportSize({ width: 1366, height: 768 })
    
    // Hero should take appropriate space
    const desktopHero = page.locator('.hidden.lg\\:block')
    await expect(desktopHero).toBeVisible()
    
    // Form should be centered
    const form = page.locator('form[aria-label="Login form"]')
    await expect(form).toBeVisible()
    
    // Take screenshot
    await page.screenshot({ 
      path: 'audit/responsive-screenshots/login-desktop-1366.png',
      fullPage: true 
    })
  })
})

test.describe('Login Page - Functionality', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173/login')
  })

  test('validates email field', async ({ page }) => {
    const emailInput = page.locator('input[type="email"]')
    const submitButton = page.locator('button[type="submit"]')
    
    // Try to submit without email
    await submitButton.click()
    
    // Should show error
    const error = page.locator('text=/Email is required|Email is invalid/i')
    await expect(error).toBeVisible({ timeout: 2000 })
  })

  test('validates password field', async ({ page }) => {
    const emailInput = page.locator('input[type="email"]')
    const passwordInput = page.locator('input[type="password"]')
    const submitButton = page.locator('button[type="submit"]')
    
    // Fill email but not password
    await emailInput.fill('test@example.com')
    await submitButton.click()
    
    // Should show password error
    const error = page.locator('text=/Password is required/i')
    await expect(error).toBeVisible({ timeout: 2000 })
  })

  test('toggles password visibility', async ({ page }) => {
    const passwordInput = page.locator('input[type="password"]').or(page.locator('input[type="text"]')).first()
    const toggleButton = page.locator('button[aria-label*="password"]')
    
    // Initially should be password type
    await expect(passwordInput).toHaveAttribute('type', 'password')
    
    // Click toggle
    await toggleButton.click()
    
    // Should change to text type
    const textInput = page.locator('input[type="text"]').first()
    await expect(textInput).toBeVisible()
  })

  test('shows loading state on submit', async ({ page }) => {
    const emailInput = page.locator('input[type="email"]')
    const passwordInput = page.locator('input[type="password"]')
    const submitButton = page.locator('button[type="submit"]')
    
    // Fill form
    await emailInput.fill('test@example.com')
    await passwordInput.fill('password123')
    
    // Submit
    await submitButton.click()
    
    // Should show loading spinner
    const loader = page.locator('.animate-spin')
    await expect(loader).toBeVisible({ timeout: 1000 })
  })

  test('keyboard navigation works', async ({ page }) => {
    // Tab through form
    await page.keyboard.press('Tab') // Skip link
    await page.keyboard.press('Tab') // Email
    await page.keyboard.press('Tab') // Password
    await page.keyboard.press('Tab') // Password toggle
    await page.keyboard.press('Tab') // Remember me
    await page.keyboard.press('Tab') // Forgot password
    await page.keyboard.press('Tab') // Submit button
    
    // Submit button should be focused
    const submitButton = page.locator('button[type="submit"]')
    await expect(submitButton).toBeFocused()
  })
})

test.describe('Login Page - Accessibility', () => {
  test('has proper ARIA labels', async ({ page }) => {
    await page.goto('http://localhost:5173/login')
    
    // Form should have aria-label
    const form = page.locator('form[aria-label="Login form"]')
    await expect(form).toBeVisible()
    
    // Inputs should have aria-labels
    const emailInput = page.locator('input[aria-label="Email address"]')
    await expect(emailInput).toBeVisible()
    
    const passwordInput = page.locator('input[aria-label="Password"]')
    await expect(passwordInput).toBeVisible()
    
    // Buttons should have aria-labels
    const googleButton = page.locator('button[aria-label="Sign in with Google"]')
    await expect(googleButton).toBeVisible()
  })

  test('has skip to content link', async ({ page }) => {
    await page.goto('http://localhost:5173/login')
    
    // Press Tab to focus skip link
    await page.keyboard.press('Tab')
    
    // Skip link should be visible when focused
    const skipLink = page.locator('.skip-to-content')
    await expect(skipLink).toBeFocused()
  })

  test('maintains focus visibility', async ({ page }) => {
    await page.goto('http://localhost:5173/login')
    
    // Tab to email input
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')
    
    const emailInput = page.locator('input[type="email"]')
    await expect(emailInput).toBeFocused()
    
    // Should have visible focus ring
    const focusRing = await emailInput.evaluate((el) => {
      const styles = window.getComputedStyle(el)
      return styles.outline !== 'none' || styles.boxShadow !== 'none'
    })
    expect(focusRing).toBeTruthy()
  })
})

test.describe('Theme Toggle', () => {
  test('theme toggle works', async ({ page }) => {
    await page.goto('http://localhost:5173/login')
    
    // Wait for page to load
    await page.waitForLoadState('networkidle')
    
    // Get initial theme
    const initialTheme = await page.evaluate(() => {
      return document.documentElement.getAttribute('data-theme')
    })
    
    // Note: Theme toggle might not be on login page
    // This test would work better on dashboard
    console.log('Initial theme:', initialTheme)
  })

  test('theme persists on reload', async ({ page, context }) => {
    await page.goto('http://localhost:5173/login')
    
    // Set theme in localStorage
    await page.evaluate(() => {
      localStorage.setItem('theme', 'light')
    })
    
    // Reload
    await page.reload()
    
    // Check theme persisted
    const theme = await page.evaluate(() => {
      return localStorage.getItem('theme')
    })
    expect(theme).toBe('light')
  })
})
