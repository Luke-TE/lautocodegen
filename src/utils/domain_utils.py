import re


def get_domain(email_addr: str):
    domain_matcher = re.search(r"@(.+?)\.", email_addr)
    return domain_matcher.group(1)
