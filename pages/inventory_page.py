from utils.base_page import BasePage
from utils.logging import logger
from locators.inventory_locators import InventoryLocators
from utils.config import filtering_price

class InventoryPage(BasePage):
    async def get_affordable_products(self, max_price: float = filtering_price) -> list:
        product_elements = await self.page.query_selector_all(InventoryLocators.ITEM_LINK)
        selected_products = []
        for item in product_elements:
            price_el = await item.query_selector(InventoryLocators.ITEM_PRICE)
            price_text = await price_el.inner_text()
            price = float(price_text.replace('$', ''))
            if price < max_price:
                name_el = await item.query_selector(InventoryLocators.ITEM_NAME)
                name = await name_el.inner_text()
                selected_products.append({
                    "name": name,
                    "price": price,
                    "element": item
                })
        return selected_products

    async def add_to_cart(self, products: list):
        for product in products:
            add_button = await product["element"].query_selector(InventoryLocators.ADD_TO_CART)
            await add_button.click()

    async def filter_product(self, max_price: float = filtering_price):
        products = await self.get_affordable_products(max_price)
        await self.add_to_cart(products)
        return products

    async def assert_affordable_products_and_add(self, max_price: float = filtering_price):
        products = await self.get_affordable_products(max_price)
        assert products, f"No products found under ${max_price}"
        await self.add_to_cart(products)
        return products