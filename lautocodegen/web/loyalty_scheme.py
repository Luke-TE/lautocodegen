import asyncio
import logging
from lautocodegen.email.email_parser import EmailParser
from lautocodegen.email.email_utils import decode_email
from lautocodegen.email.imap_email_getter import IMAPEmailGetter
from lautocodegen.email.smtp_email_sender import SMTPEmailSender
from lautocodegen.web.webpage_interface import WebpageInterface

log = logging.getLogger()


class LoyaltyScheme:
    def __init__(self, stamps: int, loyalty_url: str, web_interface: WebpageInterface):
        """
        Create a new loyalty scheme
        :param stamps: The number of stamps to receive the loyalty code
        :param loyalty_url: The URL of the loyalty scheme
        :param web_interface: The headless web browser to use
        """
        self.stamps_required = stamps
        self.loyalty_signup_url = loyalty_url
        self.web_browser = web_interface

    async def complete_loyalty_card(self, email_addr: str):
        """
        Add all required loyalty stamps and complete the loyalty card
        :param email_addr: The email to complete the loyalty card with
        :return: None
        """
        for i in range(1, self.stamps_required + 1):
            await self._add_stamp(email_addr)
            log.debug(f"Verification email {i} sent.")
            # self.verify_account(email_getter)  # only needed for some schemes

    async def _add_stamp(self, email_addr):
        """
        Add a single stamp to the loyalty card
        :param email_addr: The email to add the stamp with
        :return: None
        """
        self.web_browser.goto(self.loyalty_signup_url)
        field_data = {'Email': email_addr}
        self.web_browser.submit_form(field_data)
        self.web_browser.reset_browser()

    async def verify_account(self, email_getter: IMAPEmailGetter, verf_mailbox):
        """
        Verify an email account using the topmost verification email
        :param email_getter: The email connection to use
        :param verf_mailbox: The mailbox to get the verification email from
        :return: None
        """
        verification_email = email_getter.get_mailbox_contents(verf_mailbox)[-1]
        decoded_email = decode_email(verification_email)
        parser = EmailParser(decoded_email)
        verify_link = parser.find_url()

        self.web_browser.reset_browser()
        self.web_browser.goto(verify_link)
        log.debug("Account verified. Sending loyalty code...")

    async def generate_loyalty_code(self, email_getter: IMAPEmailGetter, verf_mailbox):
        """
        Generate a loyalty code email
        :param email_getter: The email connection to use
        :param verf_mailbox: The mailbox to get the verification email from
        :return: None
        """
        await self.complete_loyalty_card(email_getter.email_addr)
        await asyncio.sleep(3)
        await self.verify_account(email_getter, verf_mailbox)
        await asyncio.sleep(3)

    async def send_loyalty_code(self, email_getter: IMAPEmailGetter, email_sender: SMTPEmailSender,
                                target_email_addr: str, verf_mailbox="VERIFICATION", code_mailbox="CODES"):
        """
        Completely verify and send a loyalty code to an email
        :param email_getter: The IMAP email connection to use
        :param email_sender: The SMTP email connection to use
        :param target_email_addr: The email to send the loyalty code to
        :param verf_mailbox: The mailbox to get the verification email from
        :param code_mailbox: The mailbox to get the loyalty code email from
        :return: None
        """
        # Get all loyalty codes
        loyalty_code_emails = email_getter.get_mailbox_contents(code_mailbox)
        if not loyalty_code_emails:
            # If no remaining, loyalty codes, generate a new one
            await self.generate_loyalty_code(email_getter, verf_mailbox)
            loyalty_code_emails = email_getter.get_mailbox_contents(code_mailbox)

        # Send the oldest loyalty code
        uid, loyalty_code_email = loyalty_code_emails[-1]
        email_sender.forward_email(loyalty_code_email, target_email_addr)
        email_getter.delete_email(code_mailbox, uid)
        log.info(f"Loyalty code sent to {target_email_addr}.")