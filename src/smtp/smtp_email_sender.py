import copy
import json
import smtplib
import ssl
from utils.domain_utils import get_domain


class SMTPEmailSender:
    SMTP_PORT = 587

    def __init__(self, email_addr, passwd):
        self._host_email_addr = email_addr
        with open("src/smtp/smtp_servers.json") as json_file:
            hosts = json.load(json_file)
        domain = get_domain(email_addr)
        host = hosts.get(domain, "")
        self._interface = smtplib.SMTP(host, self.SMTP_PORT)
        try:
            context = ssl.create_default_context()
            self._interface.starttls(context=context)
            self._interface.login(email_addr, passwd)
        except smtplib.SMTPException:
            raise Exception("Could not login.")

    def forward_email(self, old_email, recipient_email_addr):
        new_email = copy.deepcopy(old_email)
        new_email.replace_header("From", self._host_email_addr)
        new_email.replace_header("To", recipient_email_addr)
        self._interface.sendmail(self._host_email_addr, recipient_email_addr, new_email.as_string())

    def close(self):
        self._interface.quit()
