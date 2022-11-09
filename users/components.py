from polly_style.settings import Iqsms_login, Iqsms_password
from .services import ServiceSendSms


class SenderSms:
    def __init__(self, send_sms: ServiceSendSms):
        self._send_sms = send_sms

    def send(self, phone: str, text: str) -> dict:
        return self._send_sms(Iqsms_login, Iqsms_password).send(phone, text)
