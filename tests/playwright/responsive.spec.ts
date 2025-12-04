import { test, expect, Page } from '@playwright/test'
import { mkdir } from 'fs/promises'
import { join } from 'path'

/**
 * Comprehensive Responsive Testing Suite
 * Tests all breakpoints from XS Phone (320