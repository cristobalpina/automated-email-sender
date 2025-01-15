import logging
import pandas as pd
from email_sender import send_email
from typing import Tuple
from utils import (
    append_signature,
    load_email_template,
    fill_email_template,
    validate_email
)
from excel_handler import load_excel_data
from settings import (
    TEMPLATE_PATH,
    DATA_PATH,
    EMAIL_SUBJECT,
    HTML_SIGNATURE_PATH,
    CC_EMAIL,
    CC_NAME
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


def process_row(
    index: int,
    row: pd.Series,
    raw_template: str,
    sent_count: int,
    skipped_count: int
) -> Tuple[int, int]:
    """
    Process a single row of data from the Excel file.

    Args:
        index (int): The index of the current row.
        row (pd.Series): The data in the current row.
        raw_template (str): The raw email template.
        sent_count (int): The number of emails successfully sent.
        skipped_count (int): The number of emails skipped.

    Returns:
        Tuple[int, int]: The updated sent and skipped counts
    """
    logging.debug(f"Processing row {index + 1}.")

    # Extract relevant data from the row
    context = {
        key: str(row[key]) for key in row.index if f"{{{{{key}}}}}" in raw_template
    }

    # Extract recipient's email and name, skip if either is missing
    recipient_email = row.get("EMAIL")
    recipient_name = row.get("NAME")
    if not recipient_email or not recipient_name:
        logging.warning(
            f"Missing email or name for the recipient in row {index + 1}. "
            f"Row data: {row.to_dict()}"
        )
        skipped_count += 1
        return sent_count, skipped_count

    if not validate_email(recipient_email):
        logging.warning(
            f"Invalid email address for {recipient_name} ({recipient_email}). "
            "Skipping this recipient."
        )
        skipped_count += 1
        return sent_count, skipped_count

    # Fill the email template
    email_body = fill_email_template(raw_template, context)
    logging.debug(f"Filled email template for {recipient_name}.")

    # Append the email signature
    email_body = append_signature(email_body, HTML_SIGNATURE_PATH)
    logging.debug(f"Appended signature to the email for {recipient_name}.")

    # Confirm before sending
    logging.info(f"Preparing to send email to: {recipient_name} ({recipient_email})")

    confirmation = input("Do you want to send this email? (yes/no): ").strip().lower()

    if confirmation != "yes":
        logging.info(f"Skipped sending email to {recipient_name} ({recipient_email}).")
        skipped_count += 1
        return sent_count, skipped_count

    # Send the email
    try:
        send_email(
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            email_body=email_body,
            subject=EMAIL_SUBJECT,
            cc_email=CC_EMAIL if CC_EMAIL else None,
            cc_name=CC_NAME if CC_NAME else None
        )
        sent_count += 1
    except Exception as e:
        skipped_count += 1
        logging.error(f"Failed to send the email to {recipient_email}. Details: {e}")

    return sent_count, skipped_count


def main():
    """
    Main function to send personalized emails based on data from an Excel file.
    """
    logging.info("Starting the email sending process.")

    sent_count = 0
    skipped_count = 0

    # Load the email template
    raw_template = load_email_template(TEMPLATE_PATH)
    if not raw_template:
        logging.error("Exiting due to template loading failure.")
        return

    logging.info(f"Loaded email template from {TEMPLATE_PATH}.")

    # Load the Excel data
    data = load_excel_data(DATA_PATH)
    if data is None or data.empty:
        logging.error("Exiting due to data loading failure.")
        return

    logging.info(f"Loaded data from {DATA_PATH}. Total rows: {len(data)}")

    # Iterate through each row in the Excel data
    for index, row in data.iterrows():
        sent_count, skipped_count = process_row(
            index, row, raw_template, sent_count, skipped_count
        )
    logging.info(
        f"Email sending process completed. Sent: {sent_count}, Skipped: {skipped_count}"
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        logging.info("Process interrupted by user. Exiting...")
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        logging.info("Exiting the program.")
