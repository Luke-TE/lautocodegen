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

    def forward_email(self, loyalty_code_email, recipient_email_addr):
        self._interface.sendmail(self._host_email_addr, recipient_email_addr, loyalty_code_email.as_string())

    def close(self):
        self._interface.quit()
