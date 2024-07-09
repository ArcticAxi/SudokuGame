# import required modules
from cryptography.fernet import Fernet

def create_key():
    # key generation
    key = Fernet.generate_key()

    # saves the key as a string in a file
    with open('filekey.key', 'wb') as filekey:
       filekey.write(key)
