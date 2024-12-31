import pytest
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Setup logging
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Logging initialization
setup_logging()

# Fixture untuk browser dengan opsi headless
@pytest.fixture
def browser(request):
    chrome_options = Options()
    headless_mode = request.config.getoption("--headless")
    
    # Set opsi headless
    if headless_mode:
        chrome_options.add_argument("--headless=new")  # Disarankan untuk Chrome terbaru
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

    # Initialize driver with error handling
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize browser driver: {e}")
        pytest.fail("Browser initialization failed")

    # Set User-Agent untuk headless mode
    if headless_mode:
        try:
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
            })
        except Exception as e:
            logging.warning(f"Failed to set User-Agent: {e}")
    
    # Log informasi versi
    try:
        logging.info(f"Chrome version: {driver.capabilities.get('browserVersion')}")
        logging.info(f"ChromeDriver version: {driver.capabilities.get('chrome').get('chromedriverVersion')}")
    except Exception as e:
        logging.warning(f"Failed to retrieve version info: {e}")
    
    logging.info(f"Starting browser session in {'headless' if headless_mode else 'normal'} mode")

    yield driver

    logging.info(f"Closing browser session")
    driver.quit()

# Add custom pytest options
def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )

# Hooks for pytest-bdd
try:
    from pytest_bdd import before_scenario, after_scenario

    @before_scenario
    def pytest_bdd_before_scenario(request, feature, scenario):
        logging.info(f"Running scenario: {scenario.name}")

    @after_scenario
    def pytest_bdd_after_scenario(request, feature, scenario):
        logging.info(f"Finished scenario: {scenario.name}")
except ImportError:
    logging.warning("pytest-bdd not installed, skipping related hooks.")

# Capture failure screenshots
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        if driver:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"failure_{item.name}_{timestamp}.png"
            try:
                driver.save_screenshot(screenshot_name)
                logging.error(f"Test failed! Screenshot saved as {screenshot_name}")
            except Exception as e:
                logging.error(f"Failed to save screenshot: {e}")

# Context fixture for shared data
@pytest.fixture
def context():
    return {}
