import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random 
import string
class EmailService():
    def random_passcode(self,length):
        characters = string.ascii_letters + string.digits + '!@#$&*'
        random_passwords = ''.join(random.choice(characters) for _ in range(length))
        return random_passwords
    def send_email(self, to_email,user_name,user_password):
        EMAIL_SERVER = 'smtp.gmail.com'
        EMAIL_PORT = 587  # or the appropriate port for your email server
        EMAIL_USERNAME = 'nicky123.test@gmail.com'
        EMAIL_PASSWORD = 'ikngaokmmaotrrux'
        url = "http://3.6.86.197:82/account/login"
        body = "Dear " +user_name + ",\n\nWelcome to Roboxa." + "\n\nPlease find below your login credentials: " + "\n\nUsername: " + to_email + "\nPassword: "+ user_password + "\n\nTo access your account, please visit our website at "+ url +" and log in using the provided credentials."
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = to_email 
        msg['Subject'] = "User Credentials"
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
            return "Password sent to the Registerd mail id."