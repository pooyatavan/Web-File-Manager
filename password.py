import hashlib, binascii

def PassGenerate(username, password):
    username = username.upper()
    password = password.upper()
    username = hashlib.sha256(username.encode('utf-8'))
    username = username.hexdigest().upper()
    EmailPassword = username + ":" + password.upper()
    EmailPassword = hashlib.sha256(EmailPassword.encode('utf-8')).hexdigest().upper()
    EmailPassword = binascii.unhexlify(EmailPassword)[::-1]
    FinalPass = str(EmailPassword.hex()).upper()
    return FinalPass