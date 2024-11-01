from cryptography.fernet import Fernet


def generate_key():
    """
    This function generating a key for the encrypt and decrypt process
    """
    key = Fernet.generate_key()
    with open("pass.key", "wb") as key_file:
        key_file.write(key)


def call_key():
    """
    This function returns the key generated
    """
    return open("pass.key", "rb").read()


def encrypt_file(file_data):
    """
    This function encrypt data insert
    :param file_data: data of file
    :return: encrypted file_data
    """
    key = call_key()
    key_create = Fernet(key)
    encrypted_file_data = key_create.encrypt(file_data)
    return encrypted_file_data


def decrypt_file(file_data):
    """
    This function decrypt data insert
    :param file_data: data of file
    :return: decrypted file_data
    """
    key = call_key()
    key_create = Fernet(key)
    decrypted_file_data = key_create.decrypt(file_data)
    return decrypted_file_data
