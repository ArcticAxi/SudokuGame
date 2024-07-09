# import required modules
from cryptography.fernet import Fernet
import os

def encrypt_files():
    # opening the key
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # using the key
    fernet = Fernet(key)

    # loading all documents in raw_texts
    all_files = os.listdir("raw_texts/")
    raw_text_files = filter(lambda x: x[-4:] == '.txt', all_files)

    # for each .txt in raw_texts, encrypt
    for raw_text in raw_text_files:
        print(raw_text)
        # opening the original file to encrypt
        with open('./raw_texts/' + raw_text, 'rb') as file:
            original = file.read()

        # encrypting the file
        encrypted = fernet.encrypt(original)

        # opening the file in write mode and
        # writing the encrypted data
        with open('./encrypted_texts/' + raw_text, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
