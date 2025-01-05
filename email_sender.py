import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from settings import SMTP_SERVER, SMTP_PORT, EMAIL, PASSWORD, SENDER_NAME
from utils import validate_email


def send_email(
    recipient_email: str,
    recipient_name: str,
    email_body: str,
    subject: str
) -> None:
    """
    Sends an email to the specified recipient.

    Args:
        recipient_email (str): The recipient's email address.
        recipient_name (str): The recipient's name.
        email_body (str): The HTML content of the email.
        subject (str): The subject of the email.

    Returns:
        None
    """
    try:
        # Validate the recipient's email format
        if not validate_email(recipient_email):
            logging.error(f"Invalid email address: {recipient_email}. Email not sent.")
            return

        # Create the email message
        message = MIMEMultipart()
        message["From"] = formataddr((SENDER_NAME, EMAIL))
        message["To"] = formataddr((recipient_name, recipient_email))
        message["Subject"] = subject

        # Attach the email body
        message.attach(MIMEText(email_body, "html"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipient_email, message.as_string())

        logging.info(
            f"Email successfully sent to {recipient_name} ({recipient_email})."
        )

    except smtplib.SMTPAuthenticationError:
        logging.error(
            "SMTP Authentication Error: Invalid email or password. "
            "Please check your credentials."
        )
    except smtplib.SMTPConnectError:
        logging.error(
            "SMTP Connection Error: Unable to connect to the SMTP server. "
            "Check your SMTP settings."
        )
    except smtplib.SMTPRecipientsRefused:
        logging.error(
            f"Recipient refused: The email address {recipient_email} "
            "was rejected by the server."
        )
    except smtplib.SMTPException as e:
        logging.error(
            f"SMTP error occurred while sending email to {recipient_email}: {e}"
        )
    except Exception as e:
        logging.error(f"Unexpected error while sending email to {recipient_email}: {e}")
