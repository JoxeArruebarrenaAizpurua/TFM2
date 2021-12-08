from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date
import requests, csv, time

with open('companiesList.csv', newline='') as file:
    reader = csv.reader(file)
    companiesList = list(reader)

DRIVER_PATH = '/Users/joxman/Library/Mobile Documents/com~apple~CloudDocs/Documents/Universidad/Cuarto/TFG/TFG/Datos/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.implicitly_wait(20)


counter = 0
for i in companiesList:
    selector = 531
    if counter > selector:
        driver.get('https://es.finance.yahoo.com/quote/' + i[1] + '/history?p=' + i[1])
        
        if counter == selector + 1:
           acceptCoockies = driver.find_element_by_name('agree')
           acceptCoockies.click()

        buttons = driver.find_elements_by_tag_name('ul')
        maxButton = buttons[7].find_elements_by_tag_name('li')
        maxButton[3].click()

        applyButton = driver.find_elements_by_tag_name('button')
        applyButton[4].click()

        downloadButton = driver.find_element_by_partial_link_text('Descargar')
        downloadButton.click()

    counter += 1
