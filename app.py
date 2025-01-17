from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import csv
from openpyxl import load_workbook

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome(
    executable_path="C:\drivers\chromedriver_win32\chromedriver.exe", options=options
)
driver.get("https://inecnigeria.org/elections/polling-units/")
# driver.maximize_window()

states = driver.find_element(By.ID, "statePoll")
state_options = states.find_elements(By.TAG_NAME, "option")


# THESE WILL HOLD THE VARIABLES THAT WILL BE LATER PUSHED TO THE EXCEL ROWS
state_name = ""
lga_name = ""
ward_name = ""

# THIS LOOPS THROUGH THE STATES
for state_option in state_options[35:]:
    state_name = state_option.text
    # print(state_option.text)
    state_option.click()
    time.sleep(2)

    wait = WebDriverWait(driver, 10)
    lgas = wait.until(EC.presence_of_element_located((By.ID, "lgaPoll")))
    wait = WebDriverWait(lgas, 10)
    lgas_options = wait.until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "option"))
    )

    # THIS LOOPS THROUGH THE LOCAL GOVERNMENT
    for lga_option in lgas_options[1:]:
        lga_name = lga_option.text
        # print(lga_option.text)
        lga_option.click()
        time.sleep(2)

        # wards = driver.find_element(By.ID, "wardPoll")
        wait = WebDriverWait(driver, 10)
        wards = wait.until(EC.presence_of_element_located((By.ID, "wardPoll")))
        wait = WebDriverWait(wards, 10)
        ward_options = wait.until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "option"))
        )

        # THIS LOOPS THROUGH THE WARDS IN EACH LOCAL GOVERNMENT
        time.sleep(0.5)
        for ward_option in ward_options[1:]:
            time.sleep(0.1)
            ward_name = ward_option.text
            # print(ward_option.text)
            # THIS CREATES AN EMPTY LIST THAT I WILL APPEND THE DATA THAT I WILL LATER PUSH TO EACH ROW OF THE EXCEL FILE
            excel_list = []
            # THIS THEN APPENDS THE VALUES AT EVERY ITERATION
            excel_list.append(ward_name)
            excel_list.append(lga_name)
            excel_list.append(state_name)
            
            # TRYING THE CSV WAY
            excel_tup = tuple(excel_list)

            f = open("details2.csv", "a", newline="")
            writer = csv.writer(f)
            writer.writerow(excel_tup)
            f.close()
            
            # wb = load_workbook('details.xlsx')
            # ws = wb.active
            # ws.append(excel_list)
            # wb.save('details.xlsx')
            # ward_option.click()


driver.quit()

