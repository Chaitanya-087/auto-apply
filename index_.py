import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

firstname=''                        #Add your LastName
lastname=''                         #Add your FirstName
joblink=[]                          #Initialized list to store links
maxcount=100                        #Max daily apply quota for Naukri
keywords=['data engineering','java full stack']                       #Add you list of role you want to apply comma seperated
location = ''                       #Add your location/city name for within India or remote
applied =0                          #Count of jobs applied sucessfully
failed = 0                          #Count of Jobs failed
applied_list={
    'passed':[],
    'failed':[]
}                                           #Saved list of applied and failed job links for manual review
edgedriverfile = r'''./msedgedriver.exe'''  #Please add your filepath here
yournaukriemail = 'sparkscj234@gmail.com'
yournaukripass = ''

options = Options()
service = Service(edgedriverfile) 
params = "?experience=2&wfhType=0&glbl_qcrc=1019&glbl_qcrc=1028&ugTypeGid=12&cityTypeGid=17&cityTypeGid=97&cityTypeGid=134&cityTypeGid=139&cityTypeGid=183"

# try:
#     driver = webdriver.Edge(service=service, options=options)
#     driver.get('https://login.naukri.com/')
#     uname=driver.find_element(By.ID, 'usernameField')
#     uname.send_keys(yournaukriemail)
#     passwd=driver.find_element(By.ID, 'passwordField')
#     passwd.send_keys(yournaukripass)
#     passwd.send_keys(Keys.ENTER)

# except Exception as e:
#     print('Webdriver exception')
# time.sleep(10)
options = Options()
options.add_argument(r"user-data-dir=C:\\Users\\chait\\AppData\\Local\\Microsoft\\Edge\\User Data")
options.add_argument("profile-directory=Default")
options.add_argument("start-maximized"); 
options.add_argument("disable-infobars"); 
options.add_argument("--disable-extensions"); 
options.add_argument("--disable-gpu");
options.add_argument("--disable-dev-shm-usage"); 
service = Service(r'./msedgedriver.exe') 

driver = webdriver.Edge(service=service, options=options)
for k in keywords:
    url = "https://www.naukri.com/"+k.lower().replace(' ','-')+ "-jobs"+params
    driver.get(url)
    print(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,'html5lib')
    results = soup.find(class_='list')
    job_elems = results.find_all('article',class_='jobTuple bgWhite br4 mb-8')
    for job_elem in job_elems:
        joblink.append(job_elem.find('a',class_='title fw500 ellipsis').get('href'))

# TODO: check company site button "//*[@id="company-site-button"]" exists or not, if exists then save it by clicking save button next to it "//*[@id="root"]/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/a"
# TODO: else click on apply button "//*[@id="apply-button"]"

# for i in joblink:
#     time.sleep(3)
#     driver.get(i)   
#     if applied <=maxcount:
#         try:
#             time.sleep(3)
#             driver.find_element_by_xpath("//*[text()='Apply']").click()
#             time.sleep(2)
#             applied +=1
#             applied_list['passed'].append(i)
#             print('Applied for ',i, " Count", applied)

#         except Exception as e: 
#             failed+=1
#             applied_list['failed'].append(i)
#             print(e, "Failed " ,failed)
#         try:    
#             if driver.find_element_by_xpath("//*[text()='Your daily quota has been expired.']"):
#                 print('MAX Limit reached closing browser')
#                 driver.close()
#                 break
#             if driver.find_element_by_xpath("//*[text()=' 1. First Name']"):
#                 driver.find_element_by_xpath("//input[@id='CUSTOM-FIRSTNAME']").send_keys(firstname)
#             if driver.find_element_by_xpath("//*[text()=' 2. Last Name']"):
#                 driver.find_element_by_xpath("//input[@id='CUSTOM-LASTNAME']").send_keys(lastname);
#             if driver.find_element_by_xpath("//*[text()='Submit and Apply']"):
#                 driver.find_element_by_xpath("//*[text()='Submit and Apply']").click()
#         except:
#             pass
            
#     else:
#         driver.close()
#         break
# print('Completed applying closing browser saving in applied jobs csv')
# try:
#     driver.close()
# except:pass
# csv_file = "naukriapplied.csv"
# final_dict= dict ([(k, pd.Series(v)) for k,v in applied_list.items()])
# df = pd.DataFrame.from_dict(final_dict)
# df.to_csv(csv_file, index = False)