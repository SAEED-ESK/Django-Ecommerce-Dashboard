from django.core.mail import send_mail
from django.conf import settings

import threading

class EmailThread(threading.Thread):
    def __init__(self, subject, message, from_email, recipient_list):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        try:
            send_mail(
                self.subject,
                self.message,
                self.from_email,
                self.recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Exception sending email: {e}")

def send_async_email(subject, message, recipient_list):
    EmailThread(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list).start()