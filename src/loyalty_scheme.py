import asyncio
from imap.imap_email_getter import IMAPEmailGetter
from smtp.smtp_email_sender import SMTPEmailSender
from utils.email_parser import EmailParser
from utils.email_utils import decode_email
from web.webpage_interface import WebpageInterface


class LoyaltyScheme:
    def __init__(self, stamps: int, loyalty_url: str, web_interface: WebpageInterface):
        self.stamps_required = stamps
        self.loyalty_signup_url = loyalty_url
        self.web_browser = web_interface

    async def complete_loyalty_card(self, email_addr: str):
        for i in range(1, self.stamps_required + 1):
            await self.add_stamp(email_addr)
            # self.verify_account(email_content)  # only needed for some schemes
            print(f"Verification email {i} sent.")

    async def add_stamp(self, email_addr):
        self.web_browser.goto(self.loyalty_signup_url)
        field_data = {'Email': email_addr}
        self.web_browser.submit_form(field_data)
        self.web_browser.reset_browser()

    async def verify_account(self, email_getter: IMAPEmailGetter, verf_mailbox):
        verification_email = email_getter.get_mailbox_contents(verf_mailbox)[-1]
        decoded_email = decode_email(verification_email)
        parser = EmailParser(decoded_email)
        verify_link = parser.find_url()

        self.web_browser.reset_browser()
        self.web_browser.goto(verify_link)
        print("Account verified. Sending loyalty code...")

    async def generate_loyalty_code(self, email_getter: IMAPEmailGetter, verf_mailbox):
        await self.complete_loyalty_card(email_getter.email_addr)
        await asyncio.sleep(3)
        await self.verify_account(email_getter, verf_mailbox)
        await asyncio.sleep(3)

    async def send_loyalty_code(self,
                          email_getter: IMAPEmailGetter,
                          email_sender: SMTPEmailSender,
                          target_email_addr: str,
                          verf_mailbox="VERIFICATION",
                          code_mailbox="CODES"):
        # Get all loyalty codes
        loyalty_code_emails = email_getter.get_mailbox_contents(code_mailbox)
        if not loyalty_code_emails:
            # If no remaining, loyalty codes, generate a new one
            await self.generate_loyalty_code(email_getter, verf_mailbox)
            loyalty_code_emails = email_getter.get_mailbox_contents(code_mailbox)

        # Send the oldest loyalty code
        uid, loyalty_code_email = loyalty_code_emails[-1]
        email_sender.forward_email(loyalty_code_email, target_email_addr)
        email_getter.delete_email("CODES", uid)
        print(f"Loyalty code sent to {target_email_addr}.")