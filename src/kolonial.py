import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class Kolonial:
    START_URL = "https://kolonial.no/"
    LOGIN_URL = "https://kolonial.no/bruker/logg-inn/"
    LOGOUT_URL = "https://kolonial.no/bruker/logg-ut/"

    def __init__(self, username, password, chromedriver="chromedriver", headless=True):
        self.username = username
        self.password = password

        self.selector = {
            "menu_item_login": "//li[@class='menu-item-login']",
            "account_dropdown": "//a[@id='account-dropdown']",
            "username": "//input[@id='id_username']",
            "password": "//input[@id='id_password']",
            "login_button": "//input[@type='submit']",
            "logout_button": "//a[@id='log-out-link']",
            "delivery_tracker": "//div[@class='delivery-tracker']",
            "dt_title": "//h4",
            "dt_status": "//h5",
        }

        options = ChromeOptions()
        options.add_argument("user-data-dir=selenium")

        if headless:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        self.driver = Chrome(chromedriver, options=options)
        self.driver.set_window_size(1200, 600)

    def logged_in(self):
        self.driver.get(Kolonial.LOGIN_URL)

        try:
            self.driver.find_element_by_xpath("//body[contains(@class,'logged-in')]")

            return True
        except NoSuchElementException:
            return False

    def login(self):
        driver = self.driver
        driver.get(Kolonial.LOGIN_URL)

        driver.find_element_by_xpath(self.selector["username"]).send_keys(self.username)
        driver.find_element_by_xpath(self.selector["password"]).send_keys(self.password)
        driver.find_element_by_xpath(self.selector["login_button"]).click()

    def logout(self):
        self.driver.get(Kolonial.START_URL)
        time.sleep(2)
        self.driver.find_element_by_xpath(self.selector["account_dropdown"]).click()

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.selector["logout_button"]))
        ).click()

    def quit(self):
        self.driver.close()
        self.driver.quit()

    def delivery_tracker(self):
        driver = self.driver
        data = {}

        if not self.logged_in():
            self.login()

        driver.get(Kolonial.START_URL)

        try:
            delivery_tracker_title = driver.find_elements_by_xpath(
                self.selector["delivery_tracker"] + self.selector["dt_title"]
            )[0].text

            data["title"] = delivery_tracker_title
        except Exception:
            data["title"] = ""

        try:
            delivery_tracker_status = driver.find_elements_by_xpath(
                self.selector["delivery_tracker"] + self.selector["dt_status"]
            )[0].text

            data["status"] = delivery_tracker_status
        except Exception:
            data["status"] = ""

        return data
