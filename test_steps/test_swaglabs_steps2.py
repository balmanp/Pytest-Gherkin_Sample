import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Import feature file
scenarios('../features/swaglabs copy.feature')
def test_swaglabs(browser):
    pass

# Fixtures
@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)

# Given steps
@given('I am on the login page')
def login_page(browser):
    browser.get('https://www.saucedemo.com/v1/index.html')

@given('I am logged in')
def logged_in(browser):
    login_page(browser)
    browser.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys("standard_user")
    browser.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()

@given('I have items in cart')
def add_to_cart(browser):
    browser.find_element(By.CSS_SELECTOR, ".inventory_item:nth-child(1) .btn_primary").click()

# When steps
@when(parsers.parse('I enter "{username}" as username'))
def enter_username(browser, username):
    browser.find_element(By.CSS_SELECTOR, "*[data-test=\"username\"]").send_keys(username)

@when(parsers.parse('I enter "{password}" as password'))
def enter_password(browser, password):
    browser.find_element(By.CSS_SELECTOR, "*[data-test=\"password\"]").send_keys(password)

@when('I click the login button')
def click_login(browser):
    browser.find_element(By.ID, "login-button").click()

@when('I add an item to cart')
def add_item_to_cart(browser):
    browser.find_element(By.CSS_SELECTOR, ".inventory_item:nth-child(1) .btn_primary").click()

@when('I click the cart icon')
def click_cart(browser):
    browser.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()

@when('I click checkout')
def click_checkout(browser):
    browser.find_element(By.CSS_SELECTOR, ".checkout_button").click()

@when('I enter shipping information')
def enter_shipping_info(browser):
    browser.find_element(By.CSS_SELECTOR, "*[data-test=\"firstName\"]").send_keys("selenium")
    browser.find_element(By.CSS_SELECTOR, "*[data-test=\"lastName\"]").send_keys("test")
    browser.find_element(By.CSS_SELECTOR, "*[data-test=\"postalCode\"]").send_keys("12345")

@when('I click continue')
def click_continue(browser):
    browser.find_element(By.CSS_SELECTOR, ".cart_button").click()

@when('I click finish')
def click_finish(browser):
    browser.find_element(By.CSS_SELECTOR, ".cart_button").click()

@when('I click the menu button')
def click_menu(browser):
    browser.find_element(By.CSS_SELECTOR, ".bm-burger-button > button").click()

@when('I click the logout link')
def click_logout(browser, wait):
    logout_link = wait.until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    logout_link.click()

# Then steps
@then('I should be on the inventory page')
def verify_inventory_page(browser):
    assert "inventory" in browser.current_url

@then(parsers.parse('the cart badge should show "{number}"'))
def verify_cart_badge(browser, number):
    cart_badge = browser.find_element(By.CSS_SELECTOR, ".shopping_cart_badge")
    assert cart_badge.text == number

@then('I should see order confirmation')
def verify_order_confirmation(browser, wait):
    success_message = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".complete-header"))
    )
    assert "THANK YOU" in success_message.text

@then('I should be back on the login page')
def verify_login_page(browser):
    assert "index.html" in browser.current_url

os.environ['HEADLESS'] = 'True'