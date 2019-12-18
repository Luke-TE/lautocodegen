import sys
import quopri
import time
from bs4 import BeautifulSoup
from imap_email_getter import IMAPEmailGetter
from smtp_email_sender import SMTPEmailSender
from webpage_interface import WebpageInterface

***REMOVED***_EMAIL = "***REMOVED***.official@outlook.com"
***REMOVED***_LINK = "http://***REMOVED***/***REMOVED***"
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
        print(f"Verification email {i + 1} sent.")


def verify_account_from_email(web_interface: WebpageInterface, email_content):
    parser = BeautifulSoup(email_content, 'html.parser')
    verify_link_elem = parser.find(name='a', text='Click here to verify')
    verify_link = verify_link_elem['href']
    web_interface.goto(verify_link)
    print("Account verified. Sending loyalty code...")


def main():
    with open("pass.txt", 'r') as f:
        passwd = f.readline()

    email_getter = IMAPEmailGetter(imap_port, imap_host, ***REMOVED***_EMAIL, passwd)
    email_sender = SMTPEmailSender(smtp_port, smtp_host, ***REMOVED***_EMAIL, passwd)
    web_browser = WebpageInterface()

    complete_loyalty_card(web_browser, ***REMOVED***_LINK, LOYALTY_CODE_STAMPS)
    verification_email = email_getter.get_mailbox_contents('VERIFICATION')[0]
    decoded_email = quopri.decodestring(verification_email.get_payload())
    verify_account_from_email(web_browser, decoded_email)
    time.sleep(.400)

    loyalty_code_email = email_getter.get_mailbox_contents('CODES')[0]
    email_sender.forward_email(loyalty_code_email, target_email_addr)
    print(f"Loyalty code sent to {target_email_addr}.")

    web_browser.close()
    email_sender.close()
    email_getter.close()


if __name__ == '__main__':
    target_email_addr = sys.argv[1]
    main()

# Useful links
# https://www.freecodecamp.org/news/send-emails-using-code-4fcea9df63f/
# https://docs.python.org/3/library/email.examples.html
# https://stackoverflow.com/questions/2717196/forwarding-an-email-with-python-smtplib
# https://realpython.com/python-send-email/
# https://stackoverflow.com/questions/1777264/using-python-imaplib-to-delete-an-email-from-gmail/3044555
