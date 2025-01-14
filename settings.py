from dotenv import find_dotenv, load_dotenv
import os
import logging
import sys

# Load environment variables from the .env file with override
dotenv_path = find_dotenv()
if dotenv_path:
    print(f"Loading .env file from: {dotenv_path}")
else:
    print("No .env file found")
load_dotenv(dotenv_path, override=True)

# SMTP Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SENDER_NAME = os.getenv("SENDER_NAME")

# File paths and other settings
HTML_SIGNATURE_PATH = os.getenv(
    "HTML_SIGNATURE_PATH", "assets/signatures/sample_signature.html"
)
TEMPLATE_PATH = os.getenv("TEMPLATE_PATH", "assets/email_templates/sample_email.html")
EMAIL_SUBJECT = os.getenv(
    "EMAIL_SUBJECT", "Personalized Email from Automated Email Sender"
)
DATA_PATH = os.getenv("DATA_PATH", "assets/example_data.xlsx")


# Validate critical environment variables
def validate_config():
    """Validate that all required configuration variables are set."""

    missing_vars = []

    # Validate critical variables
    for var, name in [
        (SMTP_SERVER, "SMTP_SERVER"),
        (SMTP_PORT, "SMTP_PORT"),
        (EMAIL, "EMAIL"),
        (PASSWORD, "PASSWORD"),
        (SENDER_NAME, "SENDER_NAME")
    ]:
        if not var:
            missing_vars.append(name)

    # Log and exit if any required variables are missing
    if missing_vars:
        missing_vars_str = ', '.join(missing_vars)
        logging.error(f"Missing required environment variables: {missing_vars_str}")
        sys.exit(1)


# Convert SMTP_PORT to an integer (with error handling)
try:
    SMTP_PORT = int(SMTP_PORT)
except (TypeError, ValueError):
    logging.error("SMTP_PORT must be a valid integer.")
    sys.exit(1)

# Validate configuration
validate_config()
