from django.core.mail import EmailMessage

import os


class Util:
    @staticmethod
    def send_mail(data):
        subject = data['mail_sub']
        body = data['mail_body']
        try:
            email = EmailMessage(subject=subject, body=body,
                                 from_email=os.environ.get('EMAIL_HOST_USER'), to=[data['to_email']],
                                 reply_to=[os.environ.get('EMAIL_HOST_USER')])
            email.content_subtype = "html"
            email.send()
        except Exception as e:
            print("--=-------=-------", e, "-------=-------=--")
