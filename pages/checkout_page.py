from utils.base_page import BasePage
from utils.logging import logger
from locators.cart_locators import CartLocators
from locators.checkout_locators import CheckoutLocators

class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    async def go_to_checkout(self):
        await self.click(CartLocators.CART_ICON)
        await self.click(CheckoutLocators.CHECKOUT_BUTTON)

    async def fill_checkout_form(self, details: dict):
        await self.fill(CheckoutLocators.FIRSTNAME_INPUT, details["first_name"])
        await self.fill(CheckoutLocators.LASTNAME_INPUT, details["last_name"])
        await self.fill(CheckoutLocators.POSTCODE_INPUT, details["postal_code"])
        await self.click(CheckoutLocators.CONTINUE_CHECKOUT)

    async def get_total_price(self) -> str:
        return await self.get_text(CheckoutLocators.TOTAL_PRICE)

    async def checkout(self, details: dict) -> str:
        await self.go_to_checkout()
        await self.fill_checkout_form(details)
        total = await self.get_total_price()
        return total