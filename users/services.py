import random
import string
from abc import ABC, abstractmethod
from urllib.parse import urlencode
from urllib.request import Request, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener

from django.utils import timezone


class Iqsms:
    """класс для использования сервиса iqsms.ru через GET-запросы"""

    __host = 'gate.iqsms.ru'
    __sender = 'MediaGramma'

    def __init__(self, api_login, api_password):
        self.login = api_login
        self.password = api_password

    def __sendRequest(self, uri, params=None):
        url = self.__getUrl(uri, params)
        request = Request(url)
        passman = HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, self.login, self.password)
        authhandler = HTTPBasicAuthHandler(passman)
        try:
            opener = build_opener(authhandler)
            data = opener.open(request).read()
            return data
        except IOError as e:
            return e.code

    def __getUrl(self, uri, params=None):
        url = "https://%s/%s/" % (self.getHost(), uri)
        paramStr = ''
        if params is not None:
            for k, v in params.copy().items():
                if v is None:
                    del params[k]
            paramStr = urlencode(params)
        return "%s?%s" % (url, paramStr)

    def getHost(self):
        """Return current requests host """
        return self.__host

    def setHost(self, host):
        """Changing default requests host """
        self.__host = host

    def send(self, phone, text,
             statusQueueName=None, scheduleTime=None, wapurl=None):
        """Отправить sms"""
        params = {'phone': phone,
                  'text': text,
                  'sender': self.__sender,
                  'statusQueueName': statusQueueName,
                  'scheduleTime': scheduleTime,
                  'wapurl': wapurl
                  }
        return self.__sendRequest('send', params)

    def status(self, id):
        """Retrieve sms status by it's id """
        params = {'id': id}
        return self.__sendRequest('status', params)

    def statusQueue(self, statusQueueName, limit=5):
        """Retrieve latest statuses from queue """
        params = {'statusQueueName': statusQueueName, 'limit': limit}
        return self.__sendRequest('statusQueue', params)

    def credits(self):
        """Узнать текущий баланс"""
        return self.__sendRequest('credits')

    def senders(self):
        """Получить список доступных подписей"""
        return self.__sendRequest('senders')


def generate_code():
    return ''.join(random.choice(string.digits) for _ in range(8))


def is_interval_passed(confirm):
    if timezone.now() > confirm.time_initial_send_sms + timezone.timedelta(minutes=1):
        return True
    else:
        return False


def in_the_list_of_exclude_numbers(phone_number):
    """
    Проверка номера телефона на вхождение
    в список исключенных номеров
    """
    phone_numbers = ('+79991119999')
    state = False
    if phone_number in phone_numbers:
        state = True
    return state


class ServiceSendSms(ABC):

    @abstractmethod
    def send(self, phone: str, text: str):
        pass


class DevelopSendSms(ServiceSendSms):
    def __init__(self, *args, **kwargs):
        pass

    def send(self, phone: str, text: str):
        return {'id': '213213', 'status': 'accepted'}
