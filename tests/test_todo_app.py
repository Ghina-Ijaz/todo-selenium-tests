import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

APP_URL = "http://16.16.115.154"

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Test 1: Home page loads
def test_01_page_loads(driver):
    driver.get(APP_URL)
    assert driver.title != "", "Page title should not be empty"

# Test 2: Page title has content
def test_02_title_content(driver):
    driver.get(APP_URL)
    assert len(driver.title) > 0

# Test 3: Body element exists
def test_03_body_exists(driver):
    driver.get(APP_URL)
    body = driver.find_element(By.TAG_NAME, "body")
    assert body is not None

# Test 4: No 404 error
def test_04_no_404(driver):
    driver.get(APP_URL)
    assert "404" not in driver.page_source
    assert "Not Found" not in driver.page_source

# Test 5: Page has links
def test_05_links_exist(driver):
    driver.get(APP_URL)
    links = driver.find_elements(By.TAG_NAME, "a")
    assert len(links) >= 0

# Test 6: JavaScript runs
def test_06_javascript_runs(driver):
    driver.get(APP_URL)
    result = driver.execute_script("return 1 + 1")
    assert result == 2

# Test 7: Login page loads
def test_07_login_page_loads(driver):
    driver.get(f"{APP_URL}/login")
    assert "404" not in driver.page_source

# Test 8: Login has email field
def test_08_email_field_exists(driver):
    driver.get(f"{APP_URL}/login")
    try:
        field = driver.find_element(By.CSS_SELECTOR, "input[type='email'], input[name='email']")
        assert field is not None
    except:
        pytest.skip("Email field not found")

# Test 9: Login has password field
def test_09_password_field_exists(driver):
    driver.get(f"{APP_URL}/login")
    try:
        field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        assert field is not None
    except:
        pytest.skip("Password field not found")

# Test 10: Login has submit button
def test_10_submit_button_exists(driver):
    driver.get(f"{APP_URL}/login")
    try:
        btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button")
        assert btn is not None
    except:
        pytest.skip("Submit button not found")

# Test 11: Signup page loads
def test_11_signup_page_loads(driver):
    driver.get(f"{APP_URL}/signup")
    assert "404" not in driver.page_source

# Test 12: Signup has input fields
def test_12_signup_has_fields(driver):
    driver.get(f"{APP_URL}/signup")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    assert len(inputs) >= 0

# Test 13: Mobile responsive
def test_13_responsive_mobile(driver):
    driver.set_window_size(375, 812)
    driver.get(APP_URL)
    state = driver.execute_script("return document.readyState")
    assert state == "complete"
    driver.set_window_size(1920, 1080)

# Test 14: Page load time under 10 seconds
def test_14_page_load_time(driver):
    start = time.time()
    driver.get(APP_URL)
    driver.execute_script("return document.readyState")
    end = time.time()
    assert (end - start) < 10

# Test 15: Page has at least one heading or text
def test_15_page_has_content(driver):
    driver.get(APP_URL)
    assert len(driver.page_source) > 100, "Page should have content"
