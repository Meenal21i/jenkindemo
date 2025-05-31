from utils.logging import logger
from utils.base_page import BasePage
from locators.cart_locators import CartLocators
from locators.inventory_locators import InventoryLocators

class CartPage(BasePage):
    def __init__(self, page, selected_products: list = None):
        super().__init__(page)
        self.selected_products = selected_products or []

    async def open_cart(self):
        await self.click(CartLocators.CART_ICON)

    async def get_cart_products(self) -> list:
        cart_items = await self.page.query_selector_all(InventoryLocators.ITEM_LINK)
        product_names = []
        for item in cart_items:
            name_element = await item.query_selector(InventoryLocators.ITEM_NAME)
            name = await name_element.inner_text()
            product_names.append(name)
        return product_names

    async def validate_cart(self):
        await self.open_cart()
        cart_product_names = await self.get_cart_products()
        if not cart_product_names:
            logger.warning("Cart is empty! No products found.")
            raise AssertionError("Cart is unexpectedly empty.")
        expected_names = [product["name"] for product in self.selected_products]
        if set(expected_names) != set(cart_product_names):
            logger.error(f"Cart validation failed.\nExpected: {expected_names}\nFound: {cart_product_names}")
            raise AssertionError("Mismatch between expected and actual cart contents.")

    async def assert_cart_matches_selected(self):
        await self.validate_cart()