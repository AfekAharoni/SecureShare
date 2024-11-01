import smtplib
from email.message import EmailMessage
import os
SRC_MAIL = "secureshare.il@gmail.com"
PASSWORD = "fjkbifn3o4h40"


def send_register_mail(dst_mail, username, password):
    """
    This function send register mail details
    :param dst_mail: destination mail
    :param username: username
    :param password: decrypted password
    """
    msg = EmailMessage()
    msg['subject'] = "Your Secure Share Account Has Been Created"
    msg['to'] = dst_mail
    msg['from'] = SRC_MAIL
    msg.add_alternative(get_register_content(username, password), subtype='html')
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SRC_MAIL, PASSWORD)
    server.send_message(msg)
    server.quit()


def send_password_mail(dst_email, username, password):
    """
    This function send 'forgot password' mail details
    :param dst_email: destination mail
    :param username: username
    :param password: decrypted password
    """
    msg = EmailMessage()
    msg['subject'] = "Forgot Your Password? Here It Is."
    msg['to'] = dst_email
    msg['from'] = SRC_MAIL
    msg.add_alternative(get_password_content(username, password), subtype='html')
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SRC_MAIL, PASSWORD)
    server.send_message(msg)
    server.quit()


def send_new_password_mail(dst_email, username, password):
    """
    This function send 'change password' mail details
    :param dst_email: destination mail
    :param username: username
    :param password: decrypted password
    """
    msg = EmailMessage()
    msg['subject'] = "Password Changed - New Account Details"
    msg['to'] = dst_email
    msg['from'] = SRC_MAIL
    msg.add_alternative(get_new_password_content(username, password), subtype='html')
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SRC_MAIL, PASSWORD)
    server.send_message(msg)
    server.quit()


def get_register_content(username, password):
    """
    This function read content of register mail and change its username and password
    :param username: username
    :param password: password
    :return: mail
    :rtype: str
    """
    with open(os.getcwd() + "\\mail_templates\\register_mail.html", "r") as f:
        msg = f.read()
    msg = msg.replace("{name}", username)
    msg = msg.replace("{password}", password)
    msg = msg.replace("â’¸", "Ⓒ")
    return msg


def get_password_content(username, password):
    """
    This function read content of 'forgot password' mail and change its username and password
    :param username: username
    :param password: password
    :return: mail
    :rtype: str
    """
    with open(os.getcwd() + "\\mail_templates\\password_mail.html", "r") as f:
        msg = f.read()
    msg = msg.replace("{name}", username)
    msg = msg.replace("{password}", password)
    msg = msg.replace("â’¸", "Ⓒ")
    return msg


def get_new_password_content(username, password):
    """
    This function read content of 'change password' mail and change its username and password
    :param username: username
    :param password: password
    :return: mail
    :rtype: str
    """
    with open(os.getcwd() + "\\mail_templates\\new_password.html", "r") as f:
        msg = f.read()
    msg = msg.replace("{name}", username)
    msg = msg.replace("{password}", password)
    msg = msg.replace("â’¸", "Ⓒ")
    return msg