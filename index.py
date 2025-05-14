from time import sleep
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from driver import Driver as driver


apply_button_xpath = "//*[(@id='apply-button')]"
company_site_button_xpath = "//*[(@id = 'company-site-button')]"
save_button_xpath = "//*[(@class = 'styles_save-job-button__WLm_s')]"

with open("./data/jobs.jsonl", "r", encoding="utf-8") as f:
    for line in f.readlines():
        job = json.loads(line)
        link = job.get("link","")
        isApplyFound = True
        if link:
            driver.get(link)
            sleep(5)
            try:
                apply_button = driver.find_element(By.XPATH,apply_button_xpath)
                if apply_button:
                    apply_button.click()
                    sleep(5)
                    try:
                        element = driver.find_element(By.CLASS_NAME, "_chatBotContainer")
                        print("Element with class '_chatBotContainer' is present.")
                        help = input("Enter `P` to proceed with the application, or any other key to skip: ")
                        if help.lower() == 'p':
                            print("Proceeding with the application.")
                        else: 
                            save_button = driver.find_element(By.XPATH,save_button_xpath)
                            if save_button:
                                save_button.click()
                            continue
                    except NoSuchElementException:
                        print("Element with class '_chatBotContainer' is not present.")
                        
            except NoSuchElementException as e:
                isApplyFound = False
                print(f"Apply button was not found")
                
            if not isApplyFound:            
                try:
                    save_button = driver.find_element(By.XPATH,save_button_xpath)
                    if save_button:
                        save_button.click()
                except NoSuchElementException as e:
                    print(f"Save button not found")
                    print("No apply button found, skipping to next job.")
                    continue
            sleep(5)