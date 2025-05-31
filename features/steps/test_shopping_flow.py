import pytest
import asyncio
from pytest_bdd import scenarios, given, when, then
from utils.config import username, password, filtering_price
from utils.test_data import generate_checkout_details
from utils.test_utils import handle_errors
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.order_page import OrderPage
from locators.login_locators import LoginLocators
from locators.cart_locators import CartLocators

scenarios('../shopping_flow.feature')

def run_async(coroutine):
    return asyncio.get_event_loop().run_until_complete(coroutine)

@handle_errors
@given("the user is on SauceDemo login page")
def go_to_login_page(page):
    login_page = LoginPage(page)
    run_async(login_page.go_to(LoginLocators.LOGIN_URL))

@handle_errors
@when("the user logs in with valid credentials")
def login(page, context):
    login_page = LoginPage(page)
    result = run_async(login_page.login_and_verify(username, password))
    assert result
    context['login_page'] = login_page

@handle_errors
@then("the inventory page should be displayed")
def inventory_displayed(page):
    pass

@handle_errors
@when("the user filters products as per price criteria and add to the cart")
def filter_and_add_products(page, context):
    inventory_page = InventoryPage(page)
    selected_products = run_async(inventory_page.filter_product(max_price=filtering_price))
    context['selected_products'] = selected_products

@handle_errors
@then("the selected products should be in the cart")
def validate_cart(page, context):
    cart_page = CartPage(page, context.get('selected_products', []))
    run_async(cart_page.validate_cart())

@handle_errors
@when("the user continues shopping")
def continue_shopping(page):
    run_async(page.click(CartLocators.CONTINUE_SHOP))

@handle_errors
@when("the user checks out with valid checkout details")
def checkout(page, context):
    checkout_page = CheckoutPage(page)
    details = generate_checkout_details()
    context['checkout_details'] = details
    total_price = run_async(checkout_page.checkout(details))
    context['total_price'] = total_price
    assert total_price

@handle_errors
@then("the total price should be displayed")
def verify_total_price(context):
    assert 'total_price' in context and context['total_price'], "Total price is missing"

@handle_errors
@when("the user places the order")
def place_order(page):
    order_page = OrderPage(page)
    run_async(order_page.place_order())

@handle_errors
@then("the order confirmation message should be shown")
def verify_order_success(page):
    order_page = OrderPage(page)
    run_async(order_page.verify_order_success())

@handle_errors
@then("the user returns to the products page")
def return_home(page):
    order_page = OrderPage(page)
    run_async(order_page.return_to_home())