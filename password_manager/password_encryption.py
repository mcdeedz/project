import base64

def encrypt(password):
    encrypted_password = base64.b64encode(password.encode('utf-8'))
    return encrypted_password


def decrypt(password):
    decoded_password = (base64.b64decode(password)).decode("utf-8")
    return decoded_password
