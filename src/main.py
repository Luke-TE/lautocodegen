import os
import quopri
import time
from bs4 import BeautifulSoup
from imap.imap_email_getter import IMAPEmailGetter
from smtp.smtp_email_sender import SMTPEmailSender
from web.webpage_interface import WebpageInterface





def main():
    email = os.environ["EMAIL"]
    passwd = os.environ["PASS"]
    loyalty_url = os.environ["LOYALTY_URL"]
    stamps = os.environ["STAMPS"]

    email_getter = IMAPEmailGetter(email, passwd)

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
                    if new_email['Subject'] == "I love wasabi":
                        print(f"Email from {new_email['From']} is correct. Loyalty code with be sent.")

                        # email_sender = SMTPEmailSender(WASABI_EMAIL, passwd)
                        # web_browser = WebpageInterface()
                        # try:
                        #     send_loyalty_code(email_getter, email_sender, web_browser, new_email["From"])
                        # finally:
                        #     email_sender.close()
                        #     web_browser.close()

                    email_getter.delete_email("INBOX", uid)

            else:
                print("No emails. Sleeping...")
                time.sleep(5)

    finally:
        email_getter.close()


if __name__ == '__main__':
    main()
