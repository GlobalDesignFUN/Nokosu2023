from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from decouple import config

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'token' : reset_password_token.key,
        'reset_password_url': "{}://{}/password/{}".format(
            instance.request.scheme,
            instance.request.get_host(),
            reset_password_token.key),
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for ".format(title="Your Website Title"),
        # message:
        email_plaintext_message,
        # from:
        config('EMAIL_ADD'),
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()