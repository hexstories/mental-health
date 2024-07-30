from django.core.mail import send_mail


def send_email(subject, message, recipient, fail_silently=False):
   msg = send_mail(subject, message, from_email="kwakuasihene@gmail.com", to = [recipient])
   return msg.send(fail_silently=fail_silently)
   