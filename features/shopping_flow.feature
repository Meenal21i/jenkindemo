Feature: SauceDemo Shopping Flow

  Scenario: User logs in, selects products under price filter, adds to cart, checks out, and places order
    Given the user is on SauceDemo login page
    When the user logs in with valid credentials
    Then the inventory page should be displayed

    When the user filters products as per price criteria and add to the cart
    Then the selected products should be in the cart

    When the user continues shopping
    And the user checks out with valid checkout details
    Then the total price should be displayed

    When the user places the order
    Then the order confirmation message should be shown
    And the user returns to the products page