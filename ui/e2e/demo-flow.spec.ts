import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('Competition Demo Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should complete full demo workflow @demo', async ({ page }) => {
    // Step 1: Navigate to login
    await expect(page).toHaveTitle(/Agentic Workflows/)
    
    // Step 2: Register new user
    await page.click('text=Register')
    await page.fill('input[name="email"]', 'demo@example.com')
    await page.fill('input[name="password"]', 'SecurePass123!')
    await page.fill('input[name="confirmPassword"]', 'SecurePass123!')
    await page.click('button[type="submit"]')
    
    // Step 3: Verify dashboard loads
    await expect(page.locator('h1')).toContainText('Welcome')
    await expect(page.locator('[data-testid="stat-card"]')).toHaveCount(4)
    
    // Step 4: Navigate to workflow runner
    await page.click('text=Run New Workflow')
    await expect(page).toHaveURL(/.*\/run/)
    
    // Step 5: Select and run workflow
    await page.selectOption('select[name="workflow"]', 'file_organizer')
    await page.fill('textarea[name="spec"]', JSON.stringify({
      name: 'Demo Workflow',
      tasks: []
    }))
    await page.click('button:has-text("Run Workflow")')
    
    // Step 6: Verify execution
    await expect(page.locator('[data-testid="execution-status"]')).toBeVisible()
    
    // Step 7: Check audit logs
    await page.click('text=Audit')
    await expect(page.locator('[data-testid="audit-entry"]')).toHaveCount.greaterThan(0)
    
    // Step 8: View DAG
    await page.click('text=DAG')
    await expect(page.locator('[data-testid="dag-canvas"]')).toBeVisible()
  })

  test('should have accessible navigation @a11y', async ({ page }) => {
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    expect(accessibilityScanResults.violations).toEqual([])
  })

  test('should be keyboard navigable @a11y', async ({ page }) => {
    // Tab through main navigation
    await page.keyboard.press('Tab')
    await expect(page.locator(':focus')).toBeVisible()
    
    // Verify skip link
    await page.keyboard.press('Tab')
    const skipLink = page.locator('[href="#main-content"]')
    if (await skipLink.isVisible()) {
      await expect(skipLink).toBeFocused()
    }
  })

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    
    // Verify mobile menu
    await page.click('[aria-label="Open menu"]')
    await expect(page.locator('[role="dialog"]')).toBeVisible()
    
    // Verify content is readable
    const fontSize = await page.locator('body').evaluate(
      (el) => window.getComputedStyle(el).fontSize
    )
    expect(parseInt(fontSize)).toBeGreaterThanOrEqual(14)
  })

  test('should handle errors gracefully', async ({ page }) => {
    // Simulate network error
    await page.route('**/api/**', (route) => route.abort())
    
    await page.goto('/run')
    
    // Verify error boundary or error message
    await expect(
      page.locator('text=/error|failed|unable/i')
    ).toBeVisible({ timeout: 5000 })
  })

  test('should load within performance budget', async ({ page }) => {
    const startTime = Date.now()
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    const loadTime = Date.now() - startTime
    
    // Should load in under 3 seconds
    expect(loadTime).toBeLessThan(3000)
    
    // Check bundle size via performance API
    const performanceMetrics = await page.evaluate(() => {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
      return {
        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
      }
    })
    
    expect(performanceMetrics.domContentLoaded).toBeLessThan(1500)
  })
})

test.describe('Workflow Execution', () => {
  test.beforeEach(async ({ page }) => {
    // Login helper
    await page.goto('/login')
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password')
    await page.click('button[type="submit"]')
    await page.waitForURL('/')
  })

  test('should execute dry-run successfully', async ({ page }) => {
    await page.goto('/run')
    
    await page.selectOption('select[name="workflow"]', 'file_organizer')
    await page.click('button:has-text("Dry Run")')
    
    await expect(page.locator('[data-testid="dry-run-result"]')).toBeVisible()
    await expect(page.locator('text=/success|completed/i')).toBeVisible()
  })

  test('should show real-time execution logs', async ({ page }) => {
    await page.goto('/run')
    
    await page.selectOption('select[name="workflow"]', 'http_task')
    await page.click('button:has-text("Run Workflow")')
    
    // Verify logs appear
    const logsContainer = page.locator('[data-testid="execution-logs"]')
    await expect(logsContainer).toBeVisible()
    
    // Verify log entries stream in
    await expect(logsContainer.locator('[data-testid="log-entry"]')).toHaveCount.greaterThan(0)
  })
})

test.describe('Plugin Management', () => {
  test('should display all available plugins', async ({ page }) => {
    await page.goto('/plugins')
    
    const pluginCards = page.locator('[data-testid="plugin-card"]')
    await expect(pluginCards).toHaveCount.greaterThan(0)
    
    // Verify plugin details
    const firstPlugin = pluginCards.first()
    await expect(firstPlugin.locator('[data-testid="plugin-name"]')).toBeVisible()
    await expect(firstPlugin.locator('[data-testid="plugin-description"]')).toBeVisible()
  })

  test('should filter plugins by search', async ({ page }) => {
    await page.goto('/plugins')
    
    await page.fill('input[placeholder*="Search"]', 'file')
    
    const visiblePlugins = page.locator('[data-testid="plugin-card"]:visible')
    await expect(visiblePlugins).toHaveCount.greaterThan(0)
    
    // Verify all visible plugins match search
    const pluginNames = await visiblePlugins.locator('[data-testid="plugin-name"]').allTextContents()
    pluginNames.forEach(name => {
      expect(name.toLowerCase()).toContain('file')
    })
  })
})
