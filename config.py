# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # WhatsApp tokens and IDs
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    APP_ID = os.getenv('APP_ID')
    APP_SECRET = os.getenv('APP_SECRET')
    PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
    RECIPIENT_WAID = os.getenv('RECIPIENT_WAID')
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

    # OpenAI key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Airtable tokens and IDs
    INVOICE_AIRTABLE_TOKEN = os.getenv('INVOICE_AIRTABLE_TOKEN')
    INVOICE_AIRTABLE_BASE_ID = os.getenv('INVOICE_AIRTABLE_BASE_ID')
    INVOICE_AIRTABLE_TABLE_ID = os.getenv('INVOICE_AIRTABLE_TABLE_ID')
    INVENTORY_AIRTABLE_TOKEN = os.getenv('INVENTORY_AIRTABLE_TOKEN')
    INVENTORY_AIRTABLE_BASE_ID = os.getenv('INVENTORY_AIRTABLE_BASE_ID')
    INVENTORY_AIRTABLE_TABLE_ID = os.getenv('INVENTORY_AIRTABLE_TABLE_ID')

    # Make.com (Integromat) URLs
    CREATE_OUTLOOK_EVENT_MAKE_URL = os.getenv('CREATE_OUTLOOK_EVENT_MAKE_URL')
    CREATE_RECURING_OUTLOOK_EVENT_MAKE_URL = os.getenv('CREATE_RECURING_OUTLOOK_EVENT_MAKE_URL')
    MAKE_URL = os.getenv('MAKE_URL')

    # Business Name
    BUSINESS_NAME = os.getenv('BUSINESS_NAME')

    # Configure logging
    @staticmethod
    def configure_logging():
        import logging
        import sys

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            stream=sys.stdout
        )
