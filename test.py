from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

options = Options()
service = Service('./msedgedriver.exe') 

driver = webdriver.Edge(service=service, options=options)
driver.get('https://login.naukri.com/')
