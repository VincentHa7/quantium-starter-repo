import pytest
import dash
import threading
from dash import html, dcc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from src.pink_morsels_dash import pink_dash


@pytest.fixture(scope="module")
def app():
    # Function to run the Dash app in a separate thread
    def run_app():
        pink_dash.run_server(debug=True, use_reloader=False)

    # Start the Dash app in a new thread
    app_thread = threading.Thread(target=run_app)
    app_thread.start()

    # Give the app some time to start up
    time.sleep(5)

    yield pink_dash

    # Ensure the app is stopped after tests are done
    app_thread.join()


@pytest.fixture(scope="module")
def driver():
    # Setup the WebDriver using ChromeDriverManager to avoid PhantomJS
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


def test_header_present(driver, app):
    # Test to check if the header is present
    app.layout
    driver.get("http://localhost:8050/")

    # Wait for the header to appear
    header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )

    assert "Pink Morsels Sales" in header.text, "Header text is missing or incorrect"


def test_visualization_present(driver, app):
    # Test to check if the graph is present
    app.layout
    driver.get("http://localhost:8050/")

    # Wait for the graph to appear
    graph = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'sales-graph'))
    )

    assert graph is not None, "Graph is not present in the layout"


def test_region_picker_present(driver, app):
    # Test to check if the region picker is present
    app.layout
    driver.get("http://localhost:8050/")

    # Wait for the region picker to appear
    region_picker = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'region-radio'))
    )

    assert region_picker is not None, "Region picker is missing in the layout"
