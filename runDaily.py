from gCode_scraper import run
from email_me import send
import os
from dotenv import load_dotenv

# This is the driver program from scripts that I want to schedule daily
# results can be sent as an email
load_dotenv()
send(os.getenv('EMAIL_RECIPIENT'), 'AUC gCode Changes', run())
