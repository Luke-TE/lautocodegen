import sys
import quopri
from getpass import getpass
from bs4 import BeautifulSoup
from imap_email_getter import IMAPEmailGetter
from smtp_email_sender import SMTPEmailSender
from webpage_interface import WebpageInterface

***REMOVED***_EMAIL = "***REMOVED***.official@outlook.com"
***REMOVED***_LINK = "http://thy.ng/CQL027756"
LOYALTY_CODE_STAMPS = 7

smtp_host = "smtp.office365.com"
smtp_port = 587

imap_host = "outlook.office365.com"
imap_port = 993


def complete_loyalty_card(web_interface: WebpageInterface, url: str, stamps: int):
    for i in range(stamps):
        web_interface.goto(url)
        field_data = {'Email': ***REMOVED***_EMAIL}
        web_interface.submit_form(field_data)
        web_interface.reset_browser()
        print("Email sent.")


def verify_account_from_email(web_interface: WebpageInterface, email_content):
    parser = BeautifulSoup(email_content, 'html.parser')
    verify_link_elem = parser.find(name='a', text='Click here to verify')
    verify_link = verify_link_elem['href']
    web_interface.goto(verify_link)


def main():
    passwd = getpass()
    imap_interface = IMAPEmailGetter(imap_port, imap_host, ***REMOVED***_EMAIL, passwd)
    smtp_interface = SMTPEmailSender(smtp_port, smtp_host, ***REMOVED***_EMAIL, passwd)
    web_interface = WebpageInterface()

    complete_loyalty_card(web_interface, ***REMOVED***_LINK, LOYALTY_CODE_STAMPS)
    verification_email = imap_interface.get_mailbox_contents('VERIFICATION')[0]
    decoded_email = quopri.decodestring(verification_email.get_payload())
    verify_account_from_email(web_interface, decoded_email)
    loyalty_code_email = imap_interface.get_mailbox_contents('CODES')[0]
    smtp_interface.forward_email(loyalty_code_email, target_email)

    web_interface.close()
    smtp_interface.close()
    imap_interface.close()


if __name__ == '__main__':
    target_email = sys.argv[1]
    main()
