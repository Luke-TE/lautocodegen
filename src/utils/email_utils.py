import quopri


def decode_email(email):
    return quopri.decodestring(email.get_payload())

