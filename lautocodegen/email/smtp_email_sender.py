import copy
import json
import smtplib
import ssl
from lautocodegen.email.email_utils import get_domain


class SMTPEmailSender:
    PORT = 587
    servers_path = "lautocodegen/resources/smtp_servers.json"

    def __init__(self, email_addr, passwd):
        """
        Create an SMTP connection
        :param email_addr: The email address to use in the connection
        :param passwd: The password for the account
        """
        self._host_email_addr = email_addr
        with open(self.servers_path) as json_file:
            hosts = json.load(json_file)
        domain = get_domain(email_addr)
        host = hosts.get(domain, "")
        self._conn = smtplib.SMTP(host, self.PORT)
        try:
            context = ssl.create_default_context()
            self._conn.starttls(context=context)
            self._conn.login(email_addr, passwd)
        except smtplib.SMTPException:
            raise Exception("Could not login.")

    def forward_email(self, old_email, recipient_email_addr):
        """
        Forward an email to a recipient
        :param old_email: The email to be forwarded
        :param recipient_email_addr: The recipient of the forwarded email
        :return: None
        """
        new_email = copy.deepcopy(old_email)
        new_email.replace_header("From", self._host_email_addr)
        new_email.replace_header("To", recipient_email_addr)
        self._conn.sendmail(self._host_email_addr, recipient_email_addr, new_email.as_string())

    def close(self):
        """
        Close the SMTP connection
        :return: None
        """
        self._conn.quit()
