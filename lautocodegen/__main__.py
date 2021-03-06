import asyncio
import json
import logging
import os
import sentry_sdk
from lautocodegen.email.imap_email_getter import IMAPEmailGetter
from lautocodegen.email.smtp_email_sender import SMTPEmailSender
from lautocodegen.web.loyalty_scheme import LoyaltyScheme
from lautocodegen.web.webpage_interface import WebpageInterface

log = logging.getLogger("lautocodegen")
logging.basicConfig(level=logging.INFO)


async def main():
    email_getter = None
    web_browser = WebpageInterface()

    try:
        loyalty_scheme = LoyaltyScheme(stamps, loyalty_url, web_browser)

        # Endless loop for sending loyalty codes
        while True:
            # Refresh the IMAP Connection after every loop
            email_getter = IMAPEmailGetter(user_email, passwd)

            # Move junk emails to inbox
            email_getter.move_junk_emails_to_inbox()

            new_emails = email_getter.get_mailbox_contents('INBOX')
            if new_emails:
                log.debug("Processing emails...")
                email_sender = SMTPEmailSender(user_email, passwd, sender_email)
                tasks = list()

                try:
                    # Process each email in inbox
                    for uid, new_email in new_emails:
                        log.debug(f"New email from {new_email.get('From', 'Unknown Sender')}")
                        if secret_code in new_email.get('Subject', ''):
                            # Schedule task for sending (and generating) loyalty codes
                            log.debug(f"Email has the subject {secret_code}. Loyalty code will be sent.")
                            tasks.append(asyncio.create_task(
                                loyalty_scheme.send_loyalty_code(email_getter,
                                                                 email_sender,
                                                                 new_email.get('From', 'Unknown Sender'))))
                        else:
                            log.debug(f"Email did not have the subject {secret_code}.")

                        email_getter.delete_email("INBOX", uid)

                    # Generate and send all loyalty codes asynchronously
                    log.debug("Sending loyalty codes now...")
                    await asyncio.gather(*tasks)

                except Exception as e:
                    log.warning(f"Error received: {str(e)}")

                finally:
                    email_sender.close()

            else:
                # Wait as no emails currently
                log.debug("No emails. Sleeping...")
                await asyncio.sleep(5)

            # CLose IMAP session after every loop
            email_getter.close()

    except Exception as e:
        log.warning(f"Error received: {str(e)}")

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
        with open("lautocodegen/resources/env_vars.json") as json_file:
            env_vars = json.load(json_file)
    else:
        env_vars = os.environ

    user_email = env_vars["LCG_USER"]
    sender_email = env_vars["LCG_SENDER"]
    passwd = env_vars["LCG_PASS"]
    loyalty_url = env_vars["LCG_LOYALTY_URL"]
    stamps = int(env_vars["LCG_STAMPS"])
    secret_code = env_vars["LCG_SECRET_CODE"]
    sentry_dsn = env_vars.get("LCG_SENTRY_DSN", "")

    if sentry_dsn != "":
        sentry_sdk.init(sentry_dsn)

    asyncio.run(main())
