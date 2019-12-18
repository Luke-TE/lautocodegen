import copy
import smtplib
import ssl


class SMTPEmailSender:
    def __init__(self, port, host, host_email_addr, passwd):
        self._host_email_addr = host_email_addr
        self._interface = smtplib.SMTP(host, port)
        try:
            context = ssl.create_default_context()
            self._interface.starttls(context=context)
            self._interface.login(host_email_addr, passwd)
        except smtplib.SMTPException:
            raise Exception("Could not login.")

    def forward_email(self, old_email, recipient_email_addr):
        new_email = copy.deepcopy(old_email)
        new_email.replace_header("From", self._host_email_addr)
        new_email.replace_header("To", recipient_email_addr)
        self._interface.sendmail(self._host_email_addr, recipient_email_addr, new_email.as_string())

    def close(self):
        self._interface.quit()
