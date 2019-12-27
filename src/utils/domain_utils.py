import re


def get_domain(email_addr: str):
    domain_pattern = "@(.+?)\\."
    domain_matcher = re.search(domain_pattern, email_addr)
    return domain_matcher.group(1)
