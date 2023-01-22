from logisticproject.celeryapp import app
from users.actions import SendSmsVerificationCode


@app.task
def send_code_for_confirm_phone(phone):
    SendSmsVerificationCode(phone).send()


@app.task
def send_code_for_confirm_password(phone):
    SendSmsVerificationCode(phone).send_for_password()


@app.task
def send_code_for_mail(mail):
    SendSmsVerificationCode('+79999999999').send_for_mail(mail)