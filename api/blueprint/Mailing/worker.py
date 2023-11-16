import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import getenv
from api.blueprint.Mailing.temps import HTMLTemp
import json

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'unikrib'
APP_PASSWORD = getenv('AUTH_PASS')
SENDER_EMAIL = 'unikrib@gmail.com'


def perform_task(task_data):
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    task_data = json.loads(task_data)
    if task_data['type'] != 'newReport':
        RECIPIENT_EMAIL = task_data['email']

    if task_data['type'] == 'welcome':
        message['Subject'] = "Welcome " + task_data['first_name']
        content = MIMEText(HTMLTemp.welcome(task_data['first_name']), 'html')
        message.attach(content)
        try:
            smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_server.starttls()
            smtp_server.login(SMTP_USERNAME, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
            smtp_server.quit()
            print("Welcome mail sent to {RECIPIENT_EMAIL}")
        except Exception as e:
            print("An error has occured", e)
        
    elif task_data['type'] == 'verifyLink':
        message['Subject'] = "Verify your account " + task_data['first_name']
        code = task_data['code']
        message.attach(MIMEText(HTMLTemp.verifyLink(code, task_data['first_name'],
                        task_data['user_id']), 'html'))
        try:
            smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_server.starttls()
            smtp_server.login(SMTP_USERNAME, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
            smtp_server.quit()
            print("Verification mail sent to {RECIPIENT_EMAIL}")
        except Exception as e:
            print("An error has occured", e)

    elif task_data['type'] == 'sendOTP':
        message['Subject'] = "OTP verification "
        otp = task_data['otp']
        message.attach(MIMEText(HTMLTemp.otp(otp, task_data['first_name']), 'html'))
        try:
            smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_server.starttls()
            smtp_server.login(SMTP_USERNAME, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
            smtp_server.quit()
            print("An OTP has been sent to {RECIPIENT_EMAIL}")
        except Exception as e:
            print("An error has occured", e)

    elif task_data['type'] == 'resetCode':
        message['Subject'] = "Password change requested"
        otp = task_data['otp']
        message.attach(MIMEText(HTMLTemp.resetpassword(otp, task_data['first_name']), 'html'))
        try:
            smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_server.starttls()
            smtp_server.login(SMTP_USERNAME, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
            smtp_server.quit()
            print("An reset email has been sent to {RECIPIENT_EMAIL}")
        except Exception as e:
            print("An error has occured", e)
    
    elif task_data['type'] == 'inspected_request':
        message['Subject'] = "Request for inspection"
        message.attach(MIMEText(HTMLTemp.notifyAgent(task_data['first_name']), 'html'))
        try:
            smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_server.starttls()
            smtp_server.login(SMTP_USERNAME, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
            smtp_server.quit()
            print("An alert email has been sent to {RECIPIENT_EMAIL} for apartment inspection")
        except Exception as e:
            print("An error has occured", e)

    elif task_data['type'] == 'inspection_accepted':
        message['Subject'] = "Request for inspection approved"
        message.attach(MIMEText(HTMLTemp.requestAccepted(task_data['first_name'], task_data['itemId']), 'html'))
        try:
            smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_server.starttls()
            smtp_server.login(SMTP_USERNAME, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
            smtp_server.quit()
            print("A request-accepted email has been sent to {RECIPIENT_EMAIL}")
        except Exception as e:
            print("An error has occured", e)

    elif task_data['type'] == 'inspection_denied':
        message['Subject'] = "Request for inspection denied"
        message.attach(MIMEText(HTMLTemp.requestDenied(task_data['first_name']), 'html'))
        try:
            smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_server.starttls()
            smtp_server.login(SMTP_USERNAME, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
            smtp_server.quit()
            print("A request-denied email has been sent to {RECIPIENT_EMAIL}")
        except Exception as e:
            print("An error has occured", e)

    elif task_data['type'] == 'newReport':
        message['Subject'] = "A new report has been added"
        topic = task_data['topic']
        reporter = task_data['reporter']
        reported = task_data['reported']
        description = task_data['description']
        RECIPIENT_EMAIL = "unikrib@gmail.com"
        message.attach(MIMEText(HTMLTemp.newReport(topic, reporter, reported, description), 'html'))
        try:
            smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_server.starttls()
            smtp_server.login(SMTP_USERNAME, APP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
            smtp_server.quit()
            print("A new report has been added")
        except Exception as e:
            print("An error has occured", e)

    elif task_data['type'] == "prompt_deletion":
        pass

    del message
    return "Task completed"