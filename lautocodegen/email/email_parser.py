from bs4 import BeautifulSoup


class EmailParser:
    def __init__(self, email_content):
        self.parser = BeautifulSoup(email_content, 'html.parser')

    def find_url(self, text="Click here to verify"):
        """
        Find a URL from the email
        :param text: The text of the URL element
        :return: The URL
        """
        return self.parser.find(name='a', text=text)['href']
