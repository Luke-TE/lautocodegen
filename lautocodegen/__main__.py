import asyncio
import json
import logging
import os
from lautocodegen.email.imap_email_getter import IMAPEmailGetter
from lautocodegen.email.smtp_email_sender import SMTPEmailSender
from lautocodegen.web.loyalty_scheme import LoyaltyScheme
from lautocodegen.web.webpage_interface import WebpageInterface

log = logging.getLogger()
logging.basicConfig(level=logging.INFO)


async def main():
    email_getter = IMAPEmailGetter(email, passwd)
    web_browser = WebpageInterface()

    try:
        loyalty_scheme = LoyaltyScheme(stamps, loyalty_url, web_browser)

        # Endless loop for sending loyalty codes
        while True:
            # Move junk emails to inbox
            junk_emails = email_getter.get_mailbox_contents('JUNK')
            for uid, _ in junk_emails:
                email_getter.copy_email("JUNK", "INBOX", uid)
                email_getter.delete_email("JUNK", uid)
                log.debug("Email detected in junk. Moved to inbox.")

            new_emails = email_getter.get_mailbox_contents('INBOX')
            if new_emails:
                log.debug("Processing emails...")
                email_sender = SMTPEmailSender(email, passwd)
                tasks = list()

                try:
                    # Process each email in inbox
                    for uid, new_email in new_emails:
                        log.debug(f"New email from {new_email['From']}")
                        if new_email['Subject'] == secret_code:
                            # Schedule task for sending (and generating) loyalty codes
                            log.debug(f"Email has the subject {secret_code}. Loyalty code will be sent.")
                            tasks.append(asyncio.create_task(
                                loyalty_scheme.send_loyalty_code(email_getter, email_sender, new_email["From"])))
                        else:
                            log.debug(f"Email did not have the subject {secret_code}.")

                        email_getter.delete_email("INBOX", uid)

                    # Generate and send all loyalty codes asynchronously
                    log.debug("Sending loyalty codes now...")
                    await asyncio.gather(*tasks)

                finally:
                    email_sender.close()

            else:
                # Wait as no emails currently
                log.debug("No emails. Sleeping...")
                await asyncio.sleep(5)

    finally:
        email_getter.close()
        web_browser.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Start bot for completing loyalty codes.")
    parser.add_argument('--verbose', action='store_true', help='Output commands')
    parser.add_argument("--json", action='store_true', help="Use variables from a json")
    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    # Get environment variables

    if args.json:
        with open("lautocodegen/resources/envs.json") as json_file:
            env_vars = json.load(json_file)
    else:
        env_vars = os.environ

    email = env_vars["LCG_EMAIL"]
    passwd = env_vars["LCG_PASS"]
    loyalty_url = env_vars["LCG_LOYALTY_URL"]
    stamps = env_vars["LCG_STAMPS"]
    secret_code = env_vars["LCG_SECRET_CODE"]

    asyncio.run(main())
