from bs4 import BeautifulSoup


class EmailParser:
    def __init__(self, email_content):
        self.parser = BeautifulSoup(email_content, 'html.parser')

    def find_url(self, text="Click here to verify"):
        return self.parser.find(name='a', text=text)['href']
