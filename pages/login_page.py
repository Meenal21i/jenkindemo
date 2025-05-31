from utils.base_page import BasePage
from utils.logging import logger
from locators.login_locators import LoginLocators

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    async def login(self, username, password):
        await self.go_to(LoginLocators.LOGIN_URL)
        await self.fill(LoginLocators.USERNAME_INPUT, username)
        await self.fill(LoginLocators.PASSWORD_INPUT, password)
        await self.click(LoginLocators.LOGIN_BUTTON)

    async def is_login_error_visible(self):
        return await self.is_visible(LoginLocators.ERROR_MESSAGE)

    async def verify_login_success(self):
        return await self.is_visible(LoginLocators.INVENTORY_LIST)

    async def perform_valid_login_and_verify(self, username, password):
        await self.login(username, password)
        assert not await self.is_login_error_visible(), "Login error shown for valid credentials"
        assert await self.verify_login_success(), "Inventory not visible after login"

    async def perform_invalid_login_and_verify(self, username, password):
        await self.login(username, password)
        assert await self.is_login_error_visible(), "Expected error message not found for invalid credentials"

    async def login_and_verify(self, username: str, password: str):
        await self.login(username, password)
        if await self.is_login_error_visible():
            logger.error("Login failed: Invalid credentials.")
            return False
        if not await self.verify_login_success():
            logger.error("Login failed: Could not verify successful login.")
            return False
        return True