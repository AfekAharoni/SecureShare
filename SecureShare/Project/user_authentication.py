from email_validator import validate_email, EmailNotValidError
import re

global errors


def email_valid(errors, email):
    """
    This function checks if the email inserted is valid
    :param errors: global errors argument
    :param email: email
    """
    try:
        validate_email(email)
    except EmailNotValidError as e:
        errors.append(str(e))


def username_valid(errors, user):
    """
    This function checks if the user inserted is valid
    :param errors: global errors argument
    :param user: user
    """
    if not(str(user)).isalpha():
        errors.append("Username is not valid, please enter a valid username.")
    if len(str(user)) > 10:
        errors.append("Username must be in maximum 10 characters.")


def password_valid(errors, password):
    """
    This function checks if the password inserted is valid
    :param errors: global errors argument
    :param password: password
    """
    if (len(str(password))) < 6:
        errors.append("Password must be at least 6 characters.")
    if not re.search("[a-z]", password):
        errors.append("Password must include lowercase letters.")
    if not re.search("[A-Z]", password):
        errors.append("Password must include uppercase letters.")
    if not re.search("[0-9]", password):
        errors.append("Password must include numbers.")


def get_errors(username, password, email):
    """
    This function checks the errors of the username, password and email isnerted
    :param username: username
    :param password: password
    :param email: email
    :return: errors
    :rtype: list
    """
    errors = []
    email_valid(errors, email)
    username_valid(errors, username)
    password_valid(errors, password)
    return errors
