"""Web scraping plugin using Playwright."""
from typing import Dict, Any, List, Optional
from pathlib import Path
import asyncio
import structlog

from ..base import PluginBase

logger = structlog.get_logger()


class WebScraperPlugin(PluginBase):
    """
    Advanced web scraping using Playwright.
    
    Features:
    - JavaScript rendering
    - Screenshot capture
    - Element extraction
    - Form interaction
    - Wait for dynamic content
    """
    
    name = "web_scraper"
    
    def __init__(self, params: Dict[str, Any], audit=None):
        super().__init__(params, audit=audit)
        self.url = params.get("url")
        self.selectors = params.get("selectors", {})
        self.screenshot = params.get("screenshot", False)
        self.screenshot_path = params.get("screenshot_path", "screenshot.png")
        self.wait_for = params.get("wait_for")  # Selector to wait for
        self.timeout = params.get("timeout", 30000)  # 30 seconds
        self.headless = params.get("headless", True)
    
    def plan(self) -> List[Dict[str, Any]]:
        actions = [
            {"action": "navigate", "url": self.url},
        ]
        
        if self.wait_for:
            actions.append({"action": "wait_for_selector", "selector": self.wait_for})
        
        if self.selectors:
            actions.append({"action": "extract_data", "selectors": list(self.selectors.keys())})
        
        if self.screenshot:
            actions.append({"action": "screenshot", "path": self.screenshot_path})
        
        return actions
    
    def execute(self) -> Dict[str, Any]:
        """Execute web scraping."""
        try:
            # Try to use Playwright if available
            return asyncio.run(self._execute_with_playwright())
        except ImportError:
            logger.warning("playwright_not_installed", falling_back="requests")
            return self._execute_with_requests()
        except Exception as e:
            logger.error("web_scraper_failed", error=str(e))
            return {"status": "error", "message": str(e)}
    
    async def _execute_with_playwright(self) -> Dict[str, Any]:
        """Execute using Playwright for full browser automation."""
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()
            
            try:
                # Navigate to URL
                await page.goto(self.url, timeout=self.timeout)
                
                # Wait for specific element if specified
                if self.wait_for:
                    await page.wait_for_selector(self.wait_for, timeout=self.timeout)
                
                # Extract data using selectors
                extracted_data = {}
                for key, selector in self.selectors.items():
                    try:
                        element = await page.query_selector(selector)
                        if element:
                            extracted_data[key] = await element.inner_text()
                    except Exception as e:
                        logger.warning("selector_failed", key=key, error=str(e))
                        extracted_data[key] = None
                
                # Take screenshot if requested
                screenshot_path = None
                if self.screenshot:
                    await page.screenshot(path=self.screenshot_path)
                    screenshot_path = self.screenshot_path
                
                # Get page title and URL
                title = await page.title()
                final_url = page.url
                
                if self.audit:
                    self.audit.record({
                        "plugin": self.name,
                        "url": self.url,
                        "selectors_extracted": len(extracted_data),
                        "screenshot": screenshot_path is not None
                    })
                
                return {
                    "status": "ok",
                    "url": final_url,
                    "title": title,
                    "data": extracted_data,
                    "screenshot": screenshot_path
                }
            
            finally:
                await browser.close()
    
    def _execute_with_requests(self) -> Dict[str, Any]:
        """Fallback to simple requests-based scraping."""
        import requests
        from bs4 import BeautifulSoup
        
        try:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract data using CSS selectors
            extracted_data = {}
            for key, selector in self.selectors.items():
                try:
                    element = soup.select_one(selector)
                    if element:
                        extracted_data[key] = element.get_text(strip=True)
                except Exception as e:
                    logger.warning("selector_failed", key=key, error=str(e))
                    extracted_data[key] = None
            
            if self.audit:
                self.audit.record({
                    "plugin": self.name,
                    "url": self.url,
                    "method": "requests",
                    "selectors_extracted": len(extracted_data)
                })
            
            return {
                "status": "ok",
                "url": self.url,
                "title": soup.title.string if soup.title else None,
                "data": extracted_data,
                "method": "requests_fallback"
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
