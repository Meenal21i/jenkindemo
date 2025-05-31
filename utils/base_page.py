from utils.logging import logger
from playwright.async_api import Page, TimeoutError

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def go_to(self, url: str):
        await self.page.goto(url)

    async def click(self, selector: str):
        try:
            await self.page.click(selector)
        except TimeoutError:
            logger.error(f"Click failed: {selector}")
            raise

    async def fill(self, selector: str, value: str):
        try:
            await self.page.fill(selector, value)
        except TimeoutError:
            logger.error(f"Fill failed: {selector}")
            raise

    async def get_text(self, selector: str) -> str:
        try:
            element = await self.page.query_selector(selector)
            if not element:
                logger.warning(f"No element found for selector: {selector}")
                return ""
            text = await element.inner_text()
            return text
        except Exception as error_message:
            logger.error(f"Failed to get text from {selector}: {str(error_message)}")
            raise

    async def wait_for_selector(self, selector: str, timeout: int = 5000):
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
        except TimeoutError:
            logger.error(f"Timeout waiting for selector: {selector}")
            raise
        
    async def is_visible(self, selector: str) -> bool:
        try:
            element = await self.page.query_selector(selector)
            visible = element is not None and await element.is_visible()
            return visible
        except Exception as error_message:
            logger.error(f"Failed to check visibility of {selector}: {error_message}")
            return False