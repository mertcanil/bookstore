import os
from models.user import User
from services.hash import generate_hash
from services.mail import send_mail_queued
from services.exception import BasicException
from services.auth import login_manager
from flask_login import login_user

def create_user(user):
    try:
        if User.objects(email=user.email).first() == None:
            user.password = str(generate_hash(user.password))
            user.save()

            mail_msg = f"Hello {user.firstname} {user.lastname}, welcome to the bookstore\nYour new account was successfully created!"
            send_mail_queued(os.environ.get("MAIL_SENDER"), [user.email], "Your new bookstore account", mail_msg)
    except Exception as e:
        raise BasicException(message = str(e), HTTPCode = 400)

def delete_user(user_id):
    try:
        user = User.objects.get(id=user_id).first()
        user.delete()

        mail_msg = f"Hello {user.firstname} {user.lastname},\nYour account was successfully deleted!"
        send_mail_queued(os.environ.get("MAIL_SENDER"), [user.email], "Bookstore account deleted", mail_msg) 
    except Exception as e:
        raise BasicException(message = str(e), HTTPCode = 400)

@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id).first()

def signin_user(email, password):
    try:
        user = User.objects(email=email, password=generate_hash(password)).first()
        if user:
            login_user(user)
    except Exception as e:
        raise BasicException(message = str(e), HTTPCode = 400)