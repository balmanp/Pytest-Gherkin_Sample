Feature: Swag Labs E-commerce Functionality
    As a user
    I want to be able to login, shop, and checkout
    So that I can purchase items from the store

    Background:
        Given I am on the login page

    Scenario: Successful login
        When I enter "standard_user" as username
        And I enter "secret_sauce" as password
        And I click the login button
        Then I should be on the inventory page

    Scenario: Add items to cart
        Given I am logged in
        When I add an item to cart
        Then the cart badge should show "1"

    Scenario: Complete checkout process
        Given I am logged in
        And I have items in cart
        When I click the cart icon
        And I click checkout
        And I enter shipping information
            | firstname | lastname | zipcode |
            | selenium | test     | 12345   |
        And I click continue
        And I click finish
        Then I should see order confirmation

    Scenario: Successful logout
        Given I am logged in
        When I click the menu button
        And I click the logout link
        Then I should be back on the login page