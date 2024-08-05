from rest_framework.response import Response
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework import status
from email.mime.base import MIMEBase
from django.conf import settings
from email import encoders

import smtplib


# create a function to send email

def send_email(subject, message, recipient_list, cc, attachment=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = ", ".join(recipient_list)
        msg['Cc'] = ", ".join(cc)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()
        server.sendmail(settings.EMAIL_HOST_USER, recipient_list, msg.as_string())
        if cc:
            server.sendmail(settings.EMAIL_HOST_USER, cc, msg.as_string())
        server.quit()
        return Response({'message': 'Mail sent successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

