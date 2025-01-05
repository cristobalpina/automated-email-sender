import logging
import re


def validate_email(email: str) -> bool:
    """
    Validates the format of an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.match(email_regex, email))


def load_email_template(template_path: str) -> str:
    """
    Loads an email template from the specified path.

    Args:
        template_path (str): Path to the email template file.

    Returns:
        str: The raw content of the email template.
    """
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Error: The email template at '{template_path}' was not found.")
        return ""


def fill_email_template(template: str, context: dict) -> str:
    """
    Fills an email template with the provided context.

    Args:
        template (str): The raw email template with placeholders.
        context (dict): A dictionary of placeholder keys and their values.

    Returns:
        str: The filled email content.
    """
    for key, value in context.items():
        placeholder = f"{{{{{key}}}}}"  # e.g., {{recipient_name}}
        template = template.replace(placeholder, value)
    return template


def append_signature(email_body: str, signature_path: str) -> str:
    """
    Appends an HTML email signature to the given email body.

    Args:
        email_body (str): The main content of the email.
        signature_path (str): Path to the HTML signature file.

    Returns:
        str: The email body with the appended signature.
    """
    try:
        with open(signature_path, "r", encoding="utf-8") as signature_file:
            signature = signature_file.read()
        logging.debug(f"Email signature loaded from: {signature_path}")
        return email_body + signature
    except FileNotFoundError:
        logging.error(
            f"Signature file '{signature_path}' not found. "
            "Skipping signature (optional)."
        )
        return email_body  # Skip appending the signature.
    except Exception as e:
        logging.error(f"Error loading signature file from {signature_path}: {e}")
        return email_body  # Skip appending the signature.
