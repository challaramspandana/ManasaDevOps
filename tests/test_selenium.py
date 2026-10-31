import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1365,900")
    browser = webdriver.Chrome(options=options)
    browser.get(BASE_URL)
    yield browser
    browser.quit()

def test_homepage_title(driver):
    assert "CampusConnect" in driver.title

def test_notice_board_heading(driver):
    assert "Notice board" in driver.page_source

def test_sample_notice_visible(driver):
    assert "Hackathon 2026 Registration" in driver.page_source

def test_notice_form_visible(driver):
    assert driver.find_element(By.ID, "notice-form").is_displayed()

def test_search_filters_notices(driver):
    driver.find_element(By.NAME, "search").send_keys("Hackathon")
    driver.find_element(By.CSS_SELECTOR, ".filters button[type='submit']").click()
    WebDriverWait(driver, 5).until(EC.url_contains("search=Hackathon"))
    assert "Hackathon 2026 Registration" in driver.page_source
    assert "Library Timings Update" not in driver.page_source

def test_health_endpoint(driver):
    driver.get(BASE_URL + "/health")
    assert '"status":"ok"' in driver.page_source.replace(" ", "")
