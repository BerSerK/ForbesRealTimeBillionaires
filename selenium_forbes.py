from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time


chrome_exe_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
url = "http://www.forbes.com/real-time-billionaires"

#creating driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(executable_path=chrome_exe_path, options=chrome_options )
wait = WebDriverWait(driver, 10)
driver.get(url)

# Accept cookies
acceptButton = "//button[@class='trustarc-agree-btn'][@id='truste-consent-button']"
try:
    if driver.find_element_by_xpath(acceptButton).is_displayed():
        wait.until(EC.element_to_be_clickable((By.XPATH,acceptButton))).click()
    else:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@title="TrustArc Cookie Consent Manager"]')))
        wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='call']"))).click()
except Exception as e:
    print ("Error accept cookies = " + str(e))
    driver.quit()

# Get Table Header
column_info = []
columns = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class = 'scrolly-table']//tr[@class = 'ng-table-sort-header']")))
for column in columns:
    column_info.append(str(column.text))
print (column_info)

# Scroll the table
try:
    elem_num = 25 # which is number of row loaded for each scroll
    for _ in range(50):
        elem_str = "//table[@class = 'ng-scope ng-table']//tr[@class = 'base ng-scope'][" + str(elem_num) + "]"
        elem = driver.find_element_by_xpath(elem_str)
        driver.execute_script("arguments[0].scrollIntoView();", elem)
        # increment of elem_num and sleep time is depend on the internet load speed. 
        elem_num += 10
        time.sleep(1)
except Exception as e:
    print ("Error scrolling down web element = " + str(e))
    driver.quit()

elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class = 'ng-scope ng-table']//tr[@class = 'base ng-scope']")))
# for element in elements:
#     print(element.text)
print(elements[-1].text)

driver.quit()