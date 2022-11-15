import datetime
import random
import string

from django.conf import settings
from phonenumber_field.phonenumber import PhoneNumber

from logisticproject.container import Container
from logisticproject.exceptions import BadeRequestException
from users.models import ConfirmPhone, ConfirmPassword


class SendSmsVerificationCode:
    """
    Создание кода подтверждения номера телефона
    и отправка его по смс
    """

    def __init__(self, phone: str):
        self._phone = self._validate_phone(phone)
        self._sender = Container.get_service_send_sms()

    def send(self):
        code = self._generate_code()
        confirm_phone, created = ConfirmPhone.objects.get_or_create(code=code, phone=self._phone)

        if not created:
            confirm_phone.code = code
            confirm_phone.save()

        response = self._sender.send(self._phone.split('+')[1], code)
        if response['status'] != 'accepted':
            raise BadeRequestException(message='Internal service error', code='service_error')
        return response

    def send_for_password(self):
        code = self._generate_code()
        expired_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
        try:
            confirm_password = ConfirmPassword.objects.get(phone=self._phone, expired_time__gte=datetime.datetime.now())
            confirm_password.code = code
            confirm_password.save()
        except:
            confirm_password = ConfirmPassword.objects.create(code=code, phone=self._phone, expired_time=expired_time)

        response = self._sender.send(self._phone.split('+')[1], code)
        if settings.DEBUG:
            if response['status'] != 'accepted':
                raise BadeRequestException(message='not enough credits', code='service_error')
        else:
            if response == b'not enough credits':
                raise BadeRequestException(message='not enough credits', code='service_error')
            if not '=accepted' in str(response):
                raise BadeRequestException(message='Internal service error', code='service_error')
        return response

    def _validate_phone(self, phone: str) -> str:
        if phone != '' and phone is not None:
            phone = PhoneNumber.from_string(phone_number=phone, region='RU').as_e164
            return phone
        else:
            raise ValueError('Phone number is valid')

    def _generate_code(self) -> str:
        if settings.DEBUG:
            return '1111'
        code = "".join(random.choice(string.digits) for i in range(4))
        return code
