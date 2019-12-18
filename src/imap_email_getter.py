import email
import re
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
            return []

        emails = list()
        email_ids = dat[0]
        email_id_list = email_ids.split()
        for email_id in email_id_list:
            typ, dat = self._interface.fetch(email_id, '(UID RFC822)')
            if typ != 'OK':
                raise Exception(f"Failed to get message {email_id}")

            pattern_uid = re.compile(r'(?<=UID )(\d+)')
            uid = pattern_uid.findall(str(dat[0][0]))[0]
            emails.append((uid, email.message_from_bytes(dat[0][1])))

        return emails

    def delete_email(self, mailbox, uid):
        self._interface.select(mailbox)
        self._interface.uid('STORE', str(uid), "+FLAGS", "\\Deleted")

    def copy_email(self, source_mailbox, target_mailbox, uid):
        self._interface.select(source_mailbox)
        self._interface.uid('COPY', uid, target_mailbox)

    def close(self):
        self._interface.logout()
