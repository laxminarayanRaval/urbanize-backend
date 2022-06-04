from django.core.mail import EmailMessage
import os


class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(subject=data['mail_sub'], body=data['mail_body'],
                             from_email=os.environ.get('EMAIL_HOST_USER'), to=[data['mail_to']])
        email.send()
