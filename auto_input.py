import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import load_workbook

load_dotenv()

TARGET_EXCEL_FILE = os.environ.get("TARGET_EXCEL_FILE")
LOGIN_URL = os.environ.get("LOGIN_URL")
LOGIN_ID = os.environ.get("LOGIN_ID")
LOGIN_PW = os.environ.get("LOGIN_PW")

driver = webdriver.Chrome("chromedriver")
driver.get(LOGIN_URL)
driver.find_element(By.ID, "user_email").send_keys(LOGIN_ID)
driver.find_element(By.ID, "user_password").send_keys(LOGIN_PW)
driver.find_element(By.NAME, "commit").click()

wb = load_workbook(TARGET_EXCEL_FILE, data_only=True)
ws = wb["Sheet1"]

for row in ws:
    url = row[2].value

    if url == "url":
        continue

    driver.get(url)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/a[2]").click()
    driver.implicitly_wait(3)

    for index in range(24):
        ox_value = row[index + 5].value

        if ox_value == "O":
            evaluation_item_xpath = (
                f'//*[@id="evaluation_sheet_result_evaluation_sheet_item_results_attributes_{index}_grade_high"]'
            )
        else:
            evaluation_item_xpath = (
                f'//*[@id="evaluation_sheet_result_evaluation_sheet_item_results_attributes_{index}_grade_low"]'
            )

        element = driver.find_element(By.XPATH, evaluation_item_xpath)
        driver.execute_script("arguments[0].click();", element)

    elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[4]/div/div/form/div[3]/input")
    driver.execute_script("arguments[0].click();", elements[-1])
    driver.implicitly_wait(3)
