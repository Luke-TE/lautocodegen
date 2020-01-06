import logging
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

log = logging.getLogger("lautocodegen")
logging.basicConfig(level=logging.INFO)


class WebpageInterface:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self._initialize_driver()

    def _initialize_driver(self):
        self._driver = webdriver.Chrome(executable_path="lautocodegen/resources/chromedriver",
                                        chrome_options=self.chrome_options)

    def submit_form(self, field_dict: dict):
        """
        Submit a web form
        :param field_dict: A name-to-input-value dictionary of the form fields
        :return: None
        """
        field = None
        try:
            for (field_name, field_val) in field_dict.items():
                field = self._driver.find_element_by_id(field_name)
                field.clear()
                field.send_keys(field_val)

            field.send_keys(Keys.RETURN)
        except selenium.common.exceptions.NoSuchElementException:
            logging.error(f"The field {field.id} was not found.")

    def screenshot(self):
        """
        Save a test screenshot
        :return: None
        """
        self._driver.save_screenshot("test.png")

    def goto(self, webpage):
        """
        Have the chrome instance go to the webpage specified
        :param webpage: The url of the webpage
        :return: None
        """
        self._driver.get(webpage)

    def reset_browser(self):
        """
        Completely reset a browser
        :return: None
        """
        self._driver.delete_all_cookies()
        self._driver.refresh()
        self.close()
        self._initialize_driver()

    def close(self):
        """
        Close the browser
        :return: None
        """
        self._driver.close()
