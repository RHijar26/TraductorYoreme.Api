# services/mail_service.py
from flask_mail import Mail, Message
from flask import render_template

from config import config 
# This assumes your app is initialized somewhere that provides 'mail' 
# or you initialize it in your main entry point.
mail = Mail()

def send_welcome_email(user_email, user_name,token):
    """
    Sends a welcome email to a specific user.
    """

    # Render the HTML template into a string
    html_content = render_template('welmcome_message.html', 
                                    name=user_name,
                                    verification_url=f"{config.set_password_url}?token={token}")
    
    msg = Message(
        subject="Welcome to our Community!",
        recipients=[user_email],        
        sender=config.mail_username  # Ensure 'sender' is explicitly set here
    )

    msg.html = html_content
    msg.body = "Welcome to our community! Please verify your email address by clicking the link below."
    
    mail.send(msg)