from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from util import getJobData
import json
from string import Template
from collections import deque
from driver import Driver as driver
import os

seen_jobs = set()
count = 0
maxcount = float('inf')

if os.path.exists("jobs.jsonl"):
    with open("jobs.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            try:
                job = json.loads(line)
                job_id = job.get("job_id")
                if job_id:
                    seen_jobs.add(job_id)
            except Exception:
                continue

def parsePage(soup) -> bool:
    global count
    if count >= maxcount:
        return False

    job_elems = soup.find_all('div', class_='srp-jobtuple-wrapper')
    with open("jobs.jsonl", "a", encoding="utf-8") as f:
        for job_elem in job_elems:
            job_data = getJobData(str(job_elem))
            if job_data:
                job_id = job_data.get("job_id")
                if job_id in seen_jobs:
                    continue
                seen_jobs.add(job_id)
                json.dump(job_data, f, ensure_ascii=False)
                f.write("\n")
                count += 1  
    return True

keywords = ['data engineering', 'java full stack']    

URL = Template(
    "https://www.naukri.com/$keyword-jobs-$p?experience=2&wfhType=0&wfhType=2&wfhType=3&glbl_qcrc=1019&glbl_qcrc=1028&ugTypeGid=12&cityTypeGid=17&cityTypeGid=97&cityTypeGid=134&cityTypeGid=139&cityTypeGid=183"
)

if __name__ == "__main__":
    try:
        urls = []
        for keyword in keywords:
            url = URL.substitute(keyword=keyword.lower().replace(' ', '-'), p=1)
            urls.append(url)
            driver.get(url)
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'styles_pages__v1rAK'))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            page_elem = soup.find('div', class_='styles_pages__v1rAK')
            if page_elem:
                pages = page_elem.find_all('a')
                for i in range(2, len(pages) + 1):
                    url = URL.substitute(keyword=keyword.lower().replace(' ', '-'), p=i)
                    urls.append(url)
                
        for url in urls:
            print(url)
            driver.get(url)
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'srp-jobtuple-wrapper'))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            success = parsePage(soup)
            if not success: 
                break

        print(f"Saved {count} new jobs to jobs.jsonl")

    except Exception as e:
        print('Error:', e)

    finally:
        print('Done')
        driver.quit()
