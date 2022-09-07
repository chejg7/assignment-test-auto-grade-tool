import os
from dotenv import load_dotenv
from selenium import webdriver
from openpyxl import load_workbook

load_dotenv()

TARGET_EXCEL_FILE = os.environ.get("TARGET_EXCEL_FILE")
# CHROME_DRIVER =

wb = load_workbook(TARGET_EXCEL_FILE, data_only=True)
ws = wb["Sheet1"]

for row in ws:
    url = row[2].value
    if url == "url":
        continue
    ox_list = []

    for index in range(23):
        ox_list.append(row[index + 5].value)
    print(ox_list)
