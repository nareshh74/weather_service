import threading
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings


class EmailService(object):
    server = settings.EMAIL_SMTP_SERVER
    port = settings.EMAIL_PORT
    password = settings.EMAIL_PASSWORD
    sender_email = settings.EMAIL_SENDER_EMAIL

    def __init__(self):
        self.receiver_email_list = None
        self.msg = MIMEMultipart()
        self.msg['From'] = EmailService.sender_email

    def _add_subject(self, subject):
        self.msg['Subject'] = subject

    def _add_receiver_email(self, receiver_email):
        self.msg['To'] = receiver_email

    def _add_body(self, body):
        self.msg.attach(MIMEText(body, 'plain'))

    def _add_attachment(self, attachment_file):
        attachment = open(attachment_file, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition',
                     "attachment; filename= %s" % attachment_file)
        self.msg.attach(p)

    def send_email(self, receiver_email_list, subject="Weather Report", body="PFA.", attachment_file=None):
        thread = threading.Thread(target=self.send_email_to_users(
            receiver_email_list, subject, body, attachment_file), name="mail orchestrator")
        thread.setDaemon = True
        thread.run()

    def send_email_to_users(self, receiver_email_list, subject, body, attachment_file):

        def send_email_to_user(email_service_instance=None,
                               server=None,
                               port=None,
                               sender_email=None,
                               password=None,
                               receiver_email=None,
                               subject=None,
                               body=None,
                               attachment_file=None):
            email_service_instance._add_receiver_email(receiver)
            email_service_instance._add_subject(subject)
            email_service_instance._add_body(body)
            email_service_instance._add_attachment(attachment_file)
            text = email_service_instance.msg.as_string()
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)

        for receiver in receiver_email_list:
            send_email_to_user(email_service_instance=self,
                               server=self.server,
                               port=self.port,
                               sender_email=self.sender_email,
                               password=self.password,
                               receiver_email=receiver,
                               subject=subject,
                               body=body,
                               attachment_file=attachment_file)
