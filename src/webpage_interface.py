from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import chromedriver_binary  # Adds chromedriver binary to path


class WebpageInterface:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.initialize_driver()

    def initialize_driver(self):
        self._driver = webdriver.Chrome(chrome_options=self.chrome_options)

    def submit_form(self, field_dict: dict):
        field = None
        for (field_name, field_val) in field_dict.items():
            field = self._driver.find_element_by_id(field_name)
            field.clear()
            field.send_keys(field_val)
        field.send_keys(Keys.RETURN)

    def screenshot(self):
        self._driver.save_screenshot("test.png")

    def goto(self, webpage):
        self._driver.get(webpage)

    def reset_browser(self):
        self._driver.delete_all_cookies()
        self._driver.refresh()
        self.close()
        self.initialize_driver()

    def close(self):
        self._driver.close()
