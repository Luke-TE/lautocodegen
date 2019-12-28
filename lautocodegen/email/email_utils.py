import quopri
import re


def decode_email(email):
    """
    Decode email using quoted printable
    :param email: The email to decode
    :return: The decoded email content
    """
    return quopri.decodestring(email.get_payload())


def get_domain(email_addr: str):
    """
    Extract the domain from an email address
    :param email_addr: The email address
    :return: The domain
    """
    domain_matcher = re.search(r"@(.+?)\.", email_addr)
    return domain_matcher.group(1)
