import smtplib
import ssl
import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(recipient, subject, body):
    """
    Reusable function to send an email from a dummy account. 
    The body param can be html as a string.
    """
    # Set up connection to gmail
    user = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD') # use gmail app password
    smtp_server = 'smtp.gmail.com'
    port = 465  # for SSL
    context = ssl.create_default_context()
    # Create email message object
    msg = MIMEMultipart()
    msg['From'] = 'Automated Message'
    msg['To'] = recipient
    msg['Subject'] = subject
    # If body is None, email won't send and exit function
    try:
        msg.attach(MIMEText(body, 'html'))
    except:
        logging.info('No email sent')
        return
    # Sends email logging success or faillure
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(user, password)
            server.sendmail(user, recipient, msg.as_string())

        logging.info('Email Sent to %s' % recipient)
    except Exception as e:
        logging.warn('email failed\n%s' % e)
