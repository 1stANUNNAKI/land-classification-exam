"""Captures the two required screenshots with Selenium + Edge.

6b_deployment_test.png       -> happy path (statement analyzed)
7c_error_handling_interface.png -> blank input error
"""
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVER_PATH = os.environ.get("MSEDGEDRIVER", r"C:\Users\070425\AppData\Local\Temp\opencode\msedgedriver\msedgedriver.exe")


def main():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,800")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Edge(service=webdriver.EdgeService(DRIVER_PATH), options=opts)
    try:
        driver.get("http://127.0.0.1:5000/")
        time.sleep(2)

        # --- 6b: deployment test (statement analyzed) ---
        textarea = driver.find_element(By.ID, "textToAnalyze")
        textarea.send_keys("I am so glad this happened")
        driver.find_element(By.CSS_SELECTOR, "button.btn").click()
        time.sleep(3)
        response = driver.find_element(By.ID, "system_response").text
        print("6b response:", response[:80])
        driver.get_screenshot_as_file(
            os.path.join(PROJECT_ROOT, "Task_6_flask_deployment", "6b_deployment_test.png")
        )

        # --- 7c: error handling (blank input) ---
        textarea.clear()
        driver.find_element(By.CSS_SELECTOR, "button.btn").click()
        time.sleep(2)
        response = driver.find_element(By.ID, "system_response").text
        print("7c response:", response[:80])
        driver.get_screenshot_as_file(
            os.path.join(PROJECT_ROOT, "Task_7_error_handling", "7c_error_handling_interface.png")
        )
        print("Screenshots saved.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()