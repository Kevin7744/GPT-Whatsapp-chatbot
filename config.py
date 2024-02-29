import logging
import sys


class Config:
    #==== whatsapp tokens
    ACCESS_TOKEN="EAAFfj44wdZCgBO00UUfUF3UWnOfj45ZBdgSy3COiobEyZAPs7qWYNYhs56qYniL4ZBoSJLKQnilxOnHRiMwNaTVkRugZAcRgBf17QhzZCq4kTJQ9zlZAczvFIPrxb6kwteK3V6w9klF3VSM82hg3fiJVhBD4OG8lrYGBCZAluI81TNOFPBTTZBi0vAnWkpXYzX5lG"
    APP_ID="386545147213816"
    APP_SECRET="e2c59c7f9edbf20b6b65702ce55a4988"
    VERSION="v18.0"
    PHONE_NUMBER_ID="211741572019486"
    RECIPIENT_WAID="447484214653"
    VERIFY_TOKEN="BigBot"

    
    #==== open ai key
    OPENAI_API_KEY=""

    
    #==== air table tokens
    INVOICE_AIRTABLE_TOKEN="patLUzGHr4oT0lkUh.0e9c925fa198b2e7a724ab4c6dfa4ec7ee248bf478869a1cfb28644ed4d45e70"   #get one from (https://airtable.com/create/tokens) 
    INVOICE_AIRTABLE_BASE_ID="apppVyNr3bFxISzdh"     #get these from (https://airtable.com/developers/web/api/introduction)
    INVOICE_AIRTABLE_TABLE_ID="tblcPerxkuwSVgClR"
    INVOICE_AIRTABLE_FIELDS=['Bedrijf', 'Email', 'Telefoonnummer', 'Status Factuur', 'Laatst gewijzigd']
    
    INVENTORY_AIRTABLE_TOKEN="patXwbCXt6uxWu5nA.1f2c84b2f5527660c749df08b8e4b0793cbb8897718fac90e14baa1a078b45ad"
    INVENTORY_AIRTABLE_BASE_ID="appsVa1VFWimE95i5"
    INVENTORY_AIRTABLE_TABLE_ID="tblGX4ZGFVqWIuQnQ"
    INVENTORY_AIRTABLE_FIELDS=['product_ID', 'product', 'huidige_stock', 'minimum_stock', 'desired_order_quantity', 'kind of material', 'Lateed']
    
    
    #==== urls for make automations relate to outlook
    CREATE_OUTLOOK_EVENT_MAKE_URL = "https://hook.eu2.make.com/2vac9vg9yc2nywpk17tyi3ow49i4cbbm"
    CREATE_RECURING_OUTLOOK_EVENT_MAKE_URL = "https://hook.eu2.make.com/h84z6g84tsucc97o0zmatdpdut5me5sv"
    
    BUSINESS_NAME="Smart Sales"

    MAKE_URL="https://hook.eu2.make.com/vw98p11ebazn2vrkycat3ervuiyvzmla"
    AIRTABLE_API_KEY = "Bearer patl6VaEUWuUZgQqx.ea25f8a97617a28ffa599b3532ebaa2ac27da419456dc9a17b5596d5c38e6573"
    
    def configure_logging():
        """Configure the logging functionality"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            stream=sys.stdout
        )
        
#https://developers.facebook.com/docs/whatsapp/business-management-api/get-started#1--acquire-an-access-token-using-a-system-user-or-facebook-login
