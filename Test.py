import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# Constants
CHROME_URL = "https://accountable-triage.cs.jhu.edu/"
DELAY_AFTER_REFRESH = 2
INPUT_DELAY = 0.7
SUBMIT_DELAY = 7
PARTICIPANT_COUNT = 500

def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    return chrome_options

def navigate_or_refresh(driver, iteration):
    if iteration == 0:
        driver.get(CHROME_URL)
    else:
        driver.refresh()
        time.sleep(DELAY_AFTER_REFRESH)

def input_participant_ids(driver, num_list):
    for index, pid in enumerate(num_list):
        if index <= 2:
            input_field = driver.find_element(By.XPATH, f"//ol[@id='ids']/li[{index + 1}]/input")
        else:
            addrow_button = driver.find_element(By.ID, "addRow")
            addrow_button.click()
            WebDriverWait(driver, 1)
            input_field = driver.find_element(By.XPATH, f"//ol[@id='ids']/li[{index + 1}]/input")
        
        input_field.send_keys(pid)
        time.sleep(INPUT_DELAY)

    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    time.sleep(SUBMIT_DELAY)

def tampering_resistance_test_1(driver):
    for i in range(10):
        num_list = [i+1 for i in range(PARTICIPANT_COUNT)]
        random.seed(i)
        random.shuffle(num_list)
        
        navigate_or_refresh(driver, i)
        input_participant_ids(driver, num_list)

def tampering_resistance_test_2(driver):
    for i in range(10):
        random.seed(i)
        
        num_list = [j+1 for j in range(PARTICIPANT_COUNT)]
        random_remove = random.choices(num_list, k=5)
        for k in random_remove:
            num_list.remove(k)
        
        num_list2 = [l+1 for l in range(PARTICIPANT_COUNT, 2*PARTICIPANT_COUNT)]
        rand = random.choices(num_list2, k=5)
        num_list.extend(rand)
        random.shuffle(num_list)
        
        navigate_or_refresh(driver, i)
        input_participant_ids(driver, num_list)

        
def run_tampering_resistance_test_1():
    chrome_options = set_chrome_options()
    with webdriver.Chrome(options=chrome_options) as driver:
        tampering_resistance_test_1(driver)

def run_tampering_resistance_test_2():
    chrome_options = set_chrome_options()
    with webdriver.Chrome(options=chrome_options) as driver:
        tampering_resistance_test_2(driver)

def main():
    choice = input("Which Tamper resistance test do you want to run? (Enter 1 for Test 1, 2 for Test 2): ")
    if choice == "1":
        run_tampering_resistance_test_1()
    elif choice == "2":
        run_tampering_resistance_test_2()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()