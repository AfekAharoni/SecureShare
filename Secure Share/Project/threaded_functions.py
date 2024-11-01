import os
from pymongo import MongoClient
import time

mongodb_access = MongoClient("mongodb+srv://Afek:DHR9H03J@secureshare.tus0w.mongodb.net/"
                             "AfekDropBox?retryWrites=true&w=majority")
users_db = mongodb_access.AfekDropBox.users
PATH = os.getcwd() + "\\files"


def count_files():
    """
    This function count the number of files in the upload folder
    :return: count
    :rtype: int
    """
    files = os.listdir(PATH)
    files.remove("to_download")
    for file in files:
        if not os.path.isfile(f"{PATH}\\{file}") or "." not in file:
            files.remove(file)
    return len(files)


def count_users():
    """
    This function count the number of users in db (users registered)
    :return: count
    :rtype: int
    """
    count = 0
    for line in users_db.find():
        count = count + 1
    return count


def uploaded_without_password():

    """
    This function checks if someone upload a file to the site but exit from the password page,
    If there is a file but there is not password - it will be removed from the site
    """
    print("[THREADING - Remover] Start scanning for files without password...")
    while True:
        files = os.listdir(PATH)
        files.remove("to_download")
        for file in files:
            if not os.path.isfile(f"{PATH}\\{file}") or "." not in file:
                files.remove(file)
        files_password = os.listdir(f"{PATH}\\password")
        time.sleep(120) # If he uploads a file but for 2 minutes seconds he didn't upload a password for it, it will be removed
        for file in files:
            flag = False
            for password in files_password:
                if str(password) == str(file):
                    flag = True
            if flag == False:
                os.remove(f"{PATH}\\{file}")
                print(f"[THREADING - Remover] {file} was a file without password, removed automatically. ")


def remove_decrypted_files():
    """
    This function checks if there is a decrypted file in 'to_download' file
    If there is a file, it will be removed.
    """
    print("[THREADING - Remover] Start scanning for decrypted files...")
    while True:
        time.sleep(120)
        files = os.listdir(f"{PATH}\\to_download")
        for file in files:
            try:
                os.remove(f"{PATH}\\to_download\\{file}")
                print(f"[THREADING - Remover] {file} was a decrypted file, removed automatically.")
            except:
                pass
