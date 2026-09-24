from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from cachetools import cached, TTLCache
from selenium import webdriver
import os


@cached(cache=TTLCache(maxsize=1024, ttl=60*60))  # Cache for 1 hour
def get_timetable(username: str, password: str) -> str:
    scraper = _KUCampusScraper()
    try:
        scraper.login(username, password)
        timetable_html = scraper.get_timetable()
        return timetable_html
    finally:
        scraper.close()


class _KUCampusScraper:
    def __init__(self):
        if selenium_url := os.getenv("SELENIUM_URL"):
            self.driver = webdriver.Remote(
                command_executor=selenium_url,
                options=webdriver.ChromeOptions(),
            )
        else:
            self.driver = webdriver.Chrome()

    def login(self, username: str, password: str):
        self.driver.get('https://campus.ku.de/Evt_Pages/Login.aspx')

        username_input = self.driver.find_element(By.ID, 'ctl00_WebPartManager1_gwpLogin1_Login1_LoginMask_UserName')
        password_input = self.driver.find_element(By.ID, 'ctl00_WebPartManager1_gwpLogin1_Login1_LoginMask_Password')
        username_input.send_keys(username)
        password_input.send_keys(password)

        login_button = self.driver.find_element(By.ID, 'ctl00_WebPartManager1_gwpLogin1_Login1_LoginMask_LoginButton')
        login_button.click()

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mainTitle'))
        )

    def get_timetable(self):
        self.driver.get('https://campus.ku.de/cst_pages/meinstundenplanstudent.aspx')

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, 'ctl00_WebPartManager1_gwpMeinStundenplanStudent_MeinStundenplanStudent_btnSearch2'))
        )

        timetable_button = self.driver.find_element(By.ID, 'ctl00_WebPartManager1_gwpMeinStundenplanStudent_MeinStundenplanStudent_btnSearch2')
        timetable_button.click()

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_WebPartManager1_ResultatAnzeigenWP1"]/div/div[1]/a'))
        )

        self.driver.get('https://campus.ku.de/cst_pages/meinstundenplanstudent.aspx?tabkey=webtab_cst_lektionenstudent&Print=true')

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="print_content"]'))
        )

        return self.driver.find_element(By.XPATH, '//*[@id="print_content"]').get_attribute("innerHTML")

    def close(self):
        self.driver.quit()
