import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_add_to_cart(driver):
    # Login terlebih dahulu
    driver.get("https://www.saucedemo.com/v1/index.html")
    username = driver.find_element(By.ID, "user-name")
    username.send_keys("standard_user")
    password = driver.find_element(By.ID, "password") 
    password.send_keys("secret_sauce")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    time.sleep(10)
    assert "Products" in driver.page_source
    
     # Menambahkan beberapa produk ke cart menggunakan xpath
    cart_items = [
        '//*[@id="inventory_container"]/div/div[4]/div[3]/button',
        '//*[@id="inventory_container"]/div/div[5]/div[3]/button',
        '//*[@id="inventory_container"]/div/div[1]/div[3]/button'
    ]
    for item_xpath in cart_items:
        add_to_cart = driver.find_element(By.XPATH, item_xpath)
        add_to_cart.click()
        time.sleep(2)
    
    # Verifikasi jumlah produk yang berhasil ditambahkan
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "3"  # Karena kita menambahkan 3 item
    time.sleep(5)
    
    