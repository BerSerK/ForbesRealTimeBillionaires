from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Table:
    def __init__(self,driver):
        self.driver = driver
        self.wait_time = 10
        self.wait = WebDriverWait(self.driver, self.wait_time)

        # Accept Cookies
        acceptButton = "//button[@class='trustarc-agree-btn'][@id='truste-consent-button']"
        try:
            if self.driver.find_element_by_xpath(acceptButton).is_displayed():
                self.wait.until(EC.element_to_be_clickable((By.XPATH,acceptButton))).click()
            else:
                self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[@title="TrustArc Cookie Consent Manager"]')))
                self.wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='call']"))).click()
        except Exception as e:
            print ("Error accept cookies = " + str(e))
            self.driver.quit()
            return False

    def get_table_header(self):
        column_info = []
        columns =  self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class = 'scrolly-table']"
                                                                                    "//tr[@class = 'ng-table-sort-header']/th")))
        for column in columns:
            column_info.append(str(column.text))
        return column_info

    def get_table_body(self,index=None):
        elem_num = 25 # which is number of row loaded for each scroll
        incrament_num = 10 # increment of elem_num and sleep time is depend on the internet load speed.
        max_elem = 2000 # this can be change regarding the max rank number in page.
        
        index = max_elem if index == "all" or index >= max_elem else index
        if index > elem_num:
            try:
                for _ in range(int((index-elem_num)/incrament_num)+1):
                    elem_xpath = "//table[@class = 'ng-scope ng-table']//tr[@class = 'base ng-scope'][" + str(elem_num) + "]"
                    elem = self.driver.find_element_by_xpath(elem_xpath)
                    self.driver.execute_script("arguments[0].scrollIntoView();", elem)
                    elem_num += incrament_num
                    self.driver.implicitly_wait(3) # can be changed regarding internet load speed
            except Exception as e:
                print ("Error scrolling down web element = " + str(e))
                self.driver.quit()
                return False
        
        elements = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class = 'ng-scope ng-table']"
                                                                                    "//tr[@class = 'base ng-scope']{}"
                                                                                    .format("[{}]".format(index) if index and index < max_elem else ""))))
        columns = self.get_table_header()
        table_map = {}
        for element in elements:
            current_index = index if index and index < max_elem else elements.index(element) + 1
            each_line_map = {}
            for column in columns:
                value = element.find_element_by_xpath("//tr[@class = 'base ng-scope'][{}]"
                                                    "/td[@ng-repeat = 'column in columns'][{}]"
                                                    .format(current_index, columns.index(column) + 1 )).text
                each_line_map.update({column: str(value)})
            table_map.update({current_index: each_line_map})

        return table_map


if "__main__" == __name__:

    chrome_exe_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    url = "http://www.forbes.com/real-time-billionaires"

    chrome_options = webdriver.ChromeOptions()
    # TODO : Headless mode is not working yet.
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(executable_path=chrome_exe_path, options=chrome_options )
    driver.get(url)

    table = Table(driver)

    print (table.get_table_body(index=20))

    driver.quit()