import quopri
import time
from bs4 import BeautifulSoup
from imap.imap_email_getter import IMAPEmailGetter
from smtp.smtp_email_sender import SMTPEmailSender
from web.webpage_interface import WebpageInterface

***REMOVED***_EMAIL = "***REMOVED***.official@outlook.com"
***REMOVED***_LINK = "http://thy.ng/CQL027756"
LOYALTY_CODE_STAMPS = 7


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
    web_interface.reset_browser()
    web_interface.goto(verify_link)
    print("Account verified. Sending loyalty code...")


def generate_loyalty_code(web_interface: WebpageInterface, email_getter: IMAPEmailGetter):
    complete_loyalty_card(web_interface, ***REMOVED***_LINK, LOYALTY_CODE_STAMPS)
    time.sleep(3)
    verification_email = email_getter.get_mailbox_contents('VERIFICATION')[-1]
    decoded_email = quopri.decodestring(verification_email.get_payload())
    verify_account_from_email(web_interface, decoded_email)
    time.sleep(3)


def send_loyalty_code(email_getter, email_sender, web_browser, target_email_addr):
    loyalty_code_emails = email_getter.get_mailbox_contents('CODES')
    if not loyalty_code_emails:
        generate_loyalty_code(web_browser, email_getter)
    uid, loyalty_code_email = loyalty_code_emails[-1]
    email_sender.forward_email(loyalty_code_email, target_email_addr)
    email_getter.delete_email("CODES", uid)
    print(f"Loyalty code sent to {target_email_addr}.")


def main():
    with open("pass.txt", 'r') as f:
        passwd = f.readline()

    email_getter = IMAPEmailGetter(***REMOVED***_EMAIL, passwd)

    try:
        while True:
            junk_emails = email_getter.get_mailbox_contents('JUNK')
            for uid, _ in junk_emails:
                email_getter.copy_email("JUNK", "INBOX", uid)
                email_getter.delete_email("JUNK", uid)
                print("Email detected in junk. Moved to inbox.")

            new_emails = email_getter.get_mailbox_contents('INBOX')

            if new_emails:
                print("Processing emails.")
                for uid, new_email in new_emails:
                    if new_email['Subject'] == "I love ***REMOVED***":
                        print(f"Email from {new_email['From']} is correct. Loyalty code with be sent.")

                        email_sender = SMTPEmailSender(***REMOVED***_EMAIL, passwd)
                        web_browser = WebpageInterface()
                        try:
                            send_loyalty_code(email_getter, email_sender, web_browser, new_email["From"])
                        finally:
                            email_sender.close()
                            web_browser.close()

                    email_getter.delete_email("INBOX", uid)

            else:
                print("No emails. Sleeping...")
                time.sleep(5)

    finally:
        email_getter.close()


if __name__ == '__main__':
    main()
