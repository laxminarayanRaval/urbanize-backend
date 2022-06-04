from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

import os


class Util:
    @staticmethod
    def send_mail(data):
        mail_template = 'emails/send_verification_mail.html'
        subject = f"Attention {data['mail_to_name']}!, You Requested Password Reset Link."
        body = get_template(mail_template).render(
            {'user': data['mail_to_name'], 'link': data['reset_link']})
        email = EmailMessage(subject=subject, body=body,
                             from_email=os.environ.get('EMAIL_HOST_USER'), to=[data['mail_to_email']],
                             reply_to=[os.environ.get('EMAIL_HOST_USER')])  # {"email":"hitesh@popcornfly.com"}
        email.content_subtype = "html"
        email.send()
