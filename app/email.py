from flask import current_app, render_template
# from . import mail
from flask_mail import Message
import sendgrid
import os
from sendgrid.helpers.mail import *


def send_email(**kwargs):
    app = current_app._get_current_object()
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email('brian.weinfeld@gmail.com')
    to_email = Email('brian.weinfeld@gmail.com')
    subject = "Personal Website Form Submission"
    content = Content('text/plain', render_template('static/email/email.txt', **kwargs))
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())