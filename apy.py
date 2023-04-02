from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# create a webdriver object for Chrome
driver = webdriver.Chrome()

# navigate to the webpage
driver.get('https://www.sofi.com/banking/savings-account/')

# wait for the page to load completely
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "APY")]')))
text = driver.find_element(By.TAG_NAME, 'body').text

# use regex to find all the floats in the text
floats = re.findall(r'\b\d+\.\d+\b', text)

# print the list of floats
print(floats)

# close the browser
driver.quit()