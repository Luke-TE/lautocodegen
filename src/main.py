import os
import time
from imap.imap_email_getter import IMAPEmailGetter
from loyalty_scheme import LoyaltyScheme
from smtp.smtp_email_sender import SMTPEmailSender
from web.webpage_interface import WebpageInterface


def main():
    email = os.environ["EMAIL"]
    passwd = os.environ["PASS"]
    loyalty_url = os.environ["LOYALTY_URL"]
    stamps = os.environ["STAMPS"]
    secret_code = os.environ["SECRET_CODE"]

    email_getter = IMAPEmailGetter(email, passwd)
    web_browser = WebpageInterface()
    try:
        loyalty_scheme = LoyaltyScheme(stamps, loyalty_url, web_browser)

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
                    if new_email['Subject'] == secret_code:
                        print(f"Email from {new_email['From']} is correct. Loyalty code with be sent.")

                        email_sender = SMTPEmailSender(email, passwd)
                        try:
                            loyalty_scheme.send_loyalty_code(email_getter, email_sender, new_email["From"])
                        finally:
                            email_sender.close()
                    else:
                        print(f"Email did not have the subject {secret_code}.")

                    email_getter.delete_email("INBOX", uid)

            else:
                print("No emails. Sleeping...")
                time.sleep(5)

    finally:
        email_getter.close()
        web_browser.close()


if __name__ == '__main__':
    main()
