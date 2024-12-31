import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    # Setup: Menginisialisasi browser (Chrome)
    driver = webdriver.Chrome()
    yield driver
    # Teardown: Menutup browser setelah pengujian selesai
    driver.quit()

def test_login_valid(driver):
    driver.get("https://www.saucedemo.com/v1/index.html")
    username = driver.find_element(By.ID, "user-name")
    username.send_keys("standard_user")
    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    time.sleep(10)
    assert "Products" in driver.page_source

def test_login_invalid(driver):
    driver.get("https://www.saucedemo.com/v1/index.html")
    username = driver.find_element(By.ID, "user-name")
    username.send_keys("locked_out_user")
    password = driver.find_element(By.ID, "password")
    password.send_keys("secret_sauce")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    time.sleep(10)
    assert "Epic sadface: Sorry, this user has been locked out." in driver.page_source




