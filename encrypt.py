#  based on https://github.com/robee/Simple-Encrypt-Decrypt-for-Pycrypto/blob/master/encryption.py
import binascii
import hashlib
from Crypto.Cipher import AES

def encrypt(plain_text, secret_key):
    """encrypts a plain text string using the given secret_key"""
    key = hashlib.sha256(secret_key).digest()
    encobj = AES.new(key, AES.MODE_ECB)
    str_length = len(plain_text) + (16 - (len(plain_text) % 16))
    padded = plain_text.rjust(str_length, '~')
    encrypted_text = encobj.encrypt(padded)
    return encrypted_text.encode('hex')
    
def decrypt(encrypted_text, secret_key):
    """decrypts an encrypted string using the given secret_key"""
    key = hashlib.sha256(secret_key).digest()
    encobj = AES.new(key, AES.MODE_ECB)
    decrypted_text = encobj.decrypt(binascii.unhexlify(encrypted_text))
    stripped_text = decrypted_text.lstrip('~')
    return stripped_text
