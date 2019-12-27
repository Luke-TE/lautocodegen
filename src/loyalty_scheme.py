from bs4 import BeautifulSoup
from web.webpage_interface import WebpageInterface


class LoyaltyScheme:
    def __init__(self, stamps: int, loyalty_url: str, web_interface: WebpageInterface):
        self.stamps_required = stamps
        self.loyalty_signup_url = loyalty_url
        self.web_browser = web_interface

    def complete_loyalty_card(self, email_addr: str):
        for i in range(1, self.stamps_required + 1):
            self.add_stamp(email_addr)
            self.verify_account_from_email(email_content)  # not needed for W
            print(f"Verification email {i} sent.")

    def add_stamp(self, email_addr):
        self.web_browser.goto(self.loyalty_signup_url)
        field_data = {'Email': email_addr}
        self.web_browser.submit_form(field_data)
        self.web_browser.reset_browser()

    def verify_account_from_email(self, email_content):
        parser = BeautifulSoup(email_content, 'html.parser')
        verify_link_elem = parser.find(name='a', text='Click here to verify')
        verify_link = verify_link_elem['href']
        self.web_browser.reset_browser()
        self.web_browser.goto(verify_link)
        print("Account verified. Sending loyalty code...")

    # def generate_loyalty_code(self, IMAPEmailGetter):
    #     complete_loyalty_card(web_interface, WASABI_LINK, LOYALTY_CODE_STAMPS)
    #     time.sleep(3)
    #     verification_email = email_getter.get_mailbox_contents('VERIFICATION')[-1]
    #     decoded_email = quopri.decodestring(verification_email.get_payload())
    #     verify_account_from_email(web_interface, decoded_email)
    #     time.sleep(3)
    #
    # def send_loyalty_code(self, email_getter, email_sender, target_email_addr):
    #     loyalty_code_emails = email_getter.get_mailbox_contents('CODES')
    #     if not loyalty_code_emails:
    #         generate_loyalty_code(web_browser, email_getter)
    #     uid, loyalty_code_email = loyalty_code_emails[-1]
    #     email_sender.forward_email(loyalty_code_email, target_email_addr)
    #     email_getter.delete_email("CODES", uid)
    #     print(f"Loyalty code sent to {target_email_addr}.")