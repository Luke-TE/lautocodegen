import re
import os


def get_domain(email_addr: str):
    domain_matcher = re.search(r"@(.+?)\.", email_addr)
    return domain_matcher.group(1)


def get_abs_path(own_file, file_needed):
    directory = os.path.dirname(os.path.abspath(own_file))
    return os.path.join(directory, file_needed)