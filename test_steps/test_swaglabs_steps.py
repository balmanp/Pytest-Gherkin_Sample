from pytest_bdd import scenario, given, when, then, parsers
import pandas as pd
from selenium.webdriver.common.by import By
import time

@scenario('../features/swaglabs.feature', 'Successful purchase with valid user')
def test_swaglabs(driver):
    pass

@given('I am on the login page')
def login_page(driver):
    driver.get("https://www.saucedemo.com/v1/")
    assert "https://www.saucedemo.com/v1/" in driver.current_url

@when(parsers.parse('I login with valid credentials from excel "{excel_path}"'))
def login_with_excel(driver, excel_path):
    data = pd.read_excel(excel_path, 'Sheet1')
    user_data = data.to_dict('records')[0]  # Mengambil data pertama
    
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username.send_keys(user_data['user'])
    password.send_keys(user_data['password'])
    login_button.click()
    time.sleep(2)

@then('I should be on the inventory page')
def verify_inventory_page(driver):
    assert "inventory.html" in driver.current_url
    inventory_list = driver.find_element(By.CLASS_NAME, "inventory_list")
    assert inventory_list.is_displayed()

@when('I add 3 items to cart')
def add_items_to_cart(driver):
    cart_items = [
        '//*[@id="inventory_container"]/div/div[4]/div[3]/button',
        '//*[@id="inventory_container"]/div/div[5]/div[3]/button',
        '//*[@id="inventory_container"]/div/div[1]/div[3]/button'
    ]
    
    for item_xpath in cart_items:
        add_to_cart = driver.find_element(By.XPATH, item_xpath)
        add_to_cart.click()
        time.sleep(1)
    
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "3"

@when('I proceed to checkout')
def proceed_to_checkout(driver):
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    cart_badge.click()
    assert "cart.html" in driver.current_url
    
    checkout_button = driver.find_element(By.CLASS_NAME, "checkout_button")
    checkout_button.click()
    assert "checkout-step-one.html" in driver.current_url

@when('I fill checkout information')
def fill_checkout_info(driver):
    first_name = driver.find_element(By.ID, "first-name")
    last_name = driver.find_element(By.ID, "last-name")
    postal_code = driver.find_element(By.ID, "postal-code")

    first_name.send_keys("User101")
    last_name.send_keys("Doodle")
    postal_code.send_keys("123456")

    continue_button = driver.find_element(By.CLASS_NAME, "cart_button")
    continue_button.click()
    assert "checkout-step-two.html" in driver.current_url

    finish_button = driver.find_element(By.CLASS_NAME, "cart_button")
    finish_button.click()

@then('I should see order confirmation')
def verify_order_confirmation(driver):
    assert "checkout-complete.html" in driver.current_url

@then('I logout from the system')
def logout(driver):
    menu_button = driver.find_element(By.CLASS_NAME, "bm-burger-button")
    menu_button.click()
    time.sleep(1)
    
    logout_button = driver.find_element(By.ID, "logout_sidebar_link")
    logout_button.click()
    assert "https://www.saucedemo.com/v1/index.html" in driver.current_url
