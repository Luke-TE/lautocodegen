import re
import os


def get_domain(email_addr: str):
    """
    Extract the domain from an email address
    :param email_addr: The email address
    :return: The domain
    """
    domain_matcher = re.search(r"@(.+?)\.", email_addr)
    return domain_matcher.group(1)


def get_abs_path(own_file, file_needed):
    """
    Get absolute path of file in same directory
    :param own_file: __file__ of caller
    :param file_needed: The file required
    :return: The absolute path of the file required
    """
    directory = os.path.dirname(os.path.abspath(own_file))
    return os.path.join(directory, file_needed)