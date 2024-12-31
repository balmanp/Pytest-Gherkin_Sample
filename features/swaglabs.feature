Feature: Swaglabs Shopping Flow
    As a user
    I want to login and purchase items
    So that I can complete shopping process

    Scenario: Successful purchase with valid user
        Given I am on the login page
        When I login with valid credentials from excel "data/user.xlsx"
        Then I should be on the inventory page
        When I add 3 items to cart
        And I proceed to checkout
        And I fill checkout information
            | firstName | lastName | postalCode |
            | User101  | Doodle   | 123456     |
        Then I should see order confirmation
        And I logout from the system
