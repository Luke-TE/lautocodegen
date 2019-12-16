import email
import imaplib


class IMAPEmailGetter:    
    def __init__(self, port, host, host_email_addr, passwd):
        self._interface = imaplib.IMAP4_SSL(host, port)
        try:
            self._interface.login(host_email_addr, passwd)
        except imaplib.IMAP4.error:
            raise Exception("Could not login.")

    def get_mailbox_contents(self, mailbox):
        typ, dat = self._interface.select(mailbox)
        if typ != 'OK':
            raise Exception(f"Could not open mailbox {mailbox}")

        typ, dat = self._interface.search(None, "ALL")
        if typ != 'OK':
            print(f"Mailbox {mailbox} is empty.")
            return

        emails = list()
        for email_num in dat[0].split():
            typ, dat = self._interface.fetch(email_num, '(RFC822)')
            if typ != 'OK':
                raise Exception(f"Failed to get message {email_num}")

            emails.append(email.message_from_bytes(dat[0][1]))

        return emails
        
    def close(self):
        self._interface.logout()
