from django.conf import settings

from users.components import SenderSms
from users.services import DevelopSendSms, Iqsms


class Container:

    @staticmethod
    def get_service_send_sms() -> SenderSms:
        if settings.DEBUG:
            return SenderSms(DevelopSendSms)
        else:
            return SenderSms(Iqsms)

