import logging
import email
import json
import re
import imaplib
from lautocodegen.email.email_utils import get_domain

log = logging.getLogger("lautocodegen")
logging.basicConfig(level=logging.INFO)


class IMAPEmailGetter:
    PORT = 993
    servers_path = "lautocodegen/resources/imap_servers.json"

    def __init__(self, email_addr, passwd):
        """
        Create an IMAP connection
        :param email_addr: The email address to use in the connection
        :param passwd: The password for the account
        """
        self.email_addr = email_addr

        # Get the appropriate imap server
        with open(self.servers_path) as json_file:
            hosts = json.load(json_file)
        domain = get_domain(email_addr)
        host = hosts.get(domain, "")

        # Create the connection
        self._conn = imaplib.IMAP4_SSL(host, self.PORT)
        try:
            self._conn.login(email_addr, passwd)
        except imaplib.IMAP4.error:
            raise Exception("Could not login.")

    def get_mailbox_contents(self, mailbox):
        """
        Get the contents of a specific mailbox
        :param mailbox: The name of the mailbox (upper-case)
        :return: List of uid-email tuples in the mailbox
        """
        # Open mailbox
        typ, dat = self._conn.select(mailbox)
        if typ != 'OK':
            raise Exception(f"Could not open mailbox {mailbox}")

        # Get all emails from mailbox
        typ, dat = self._conn.search(None, "ALL")
        if typ != 'OK':
            log.debug(f"Mailbox {mailbox} is empty.")
            return []

        emails = list()
        email_ids = dat[0]
        email_id_list = email_ids.split()
        for email_id in email_id_list:
            # Try to fetch email from the mailbox
            typ, dat = self._conn.fetch(email_id, '(UID RFC822)')
            if typ != 'OK':
                raise Exception(f"Failed to get message {email_id}")

            # Extract the UID from the email
            uid = re.findall(r"(?<=UID )(\d+)", str(dat[0][0]))[0]
            # Add email content to the emails list
            emails.append((uid, email.message_from_bytes(dat[0][1])))

        return emails

    def delete_email(self, mailbox, uid):
        """
        Delete an email from a mailbox, specified by the UID
        :param mailbox: The mailbox from which to delete the email
        :param uid: The UID of the email to delete
        :return: None
        """
        self._conn.select(mailbox)
        self._conn.uid('STORE', str(uid), "+FLAGS", "\\Deleted")
        self._conn.expunge()

    def copy_email(self, source_mailbox, target_mailbox, uid):
        """
        Copy an email from one mailbox to another, specified by the UID
        :param source_mailbox: The email's original mailbox
        :param target_mailbox: The email's destination mailbox
        :param uid: THe UID of the email to copy
        :return: None
        """
        self._conn.select(source_mailbox)
        self._conn.uid('COPY', uid, target_mailbox)

    def move_junk_emails_to_inbox(self):
        """
        Move all emails in the junk mailbox to the inbox
        :return: None
        """
        junk_emails = self.get_mailbox_contents('JUNK')
        for uid, _ in junk_emails:
            self.copy_email("JUNK", "INBOX", uid)
            self.delete_email("JUNK", uid)
            log.debug("Email detected in junk. Moved to inbox.")

    def close(self):
        """
        Close the IMAP connection
        :return: None
        """
        self._conn.logout()
