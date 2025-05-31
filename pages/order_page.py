from utils.base_page import BasePage
from utils.logging import logger
from locators.order_locators import OrderLocators

class OrderPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    async def place_order(self):
        await self.click(OrderLocators.FINISH_BUTTON)

    async def verify_order_success(self, expected_message: str = "Thank you for your order!"):
        await self.wait_for_selector(OrderLocators.THANKYOU_HEADER)
        confirmation_text = await self.get_text(OrderLocators.THANKYOU_HEADER)
        if expected_message not in confirmation_text:
            logger.error(f"Expected confirmation text '{expected_message}' not found. Actual: '{confirmation_text}'")
            raise AssertionError("Order confirmation failed.")

    async def return_to_home(self):
        await self.click(OrderLocators.BACK_HOME)