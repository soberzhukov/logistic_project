import uuid

from django.db import models
from django.utils import timezone


class MainChat(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    executor = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='mainchat_executor', verbose_name='Исполнитель')
    customer = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='mainchat_customer', verbose_name='Заказчик')
    items_chat = models.ManyToManyField('ItemChat', related_name='mainchats')

    def __str__(self):
        return f"Chat {self.executor} - {self.customer}"

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class ItemChat(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    contract = models.ForeignKey('contract.Contract', related_name='items_chat', on_delete=models.CASCADE,
                                verbose_name='Контракт')
    messages = models.ManyToManyField('ChatMessage', related_name='items_chat',
                                      blank=True, verbose_name='Сообщения')
    date_created = models.DateTimeField('Дата создания', default=timezone.now, blank=True)

    def __str__(self):
        return f"Item chat {self.contract}"

    class Meta:
        verbose_name = 'Предмет чата'
        verbose_name_plural = 'Предмет чата'


class ChatMessage(models.Model):
    STATUS_SENT = 'sent'
    STATUS_READ = 'read'
    STATUS_ERROR = 'error'

    STATUS_CHOICES = [
        (STATUS_SENT, 'отправлено'),
        (STATUS_READ, 'прочитано'),
        (STATUS_ERROR, 'ошибка')
    ]



    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField('Текст')
    date_created = models.DateTimeField('Дата создания', default=timezone.now, blank=True)
    status = models.CharField('Статуc', max_length=250, choices=STATUS_CHOICES, default=STATUS_SENT)
    chat_files = models.ManyToManyField('common.File', related_name='chat_messages', blank=True, null=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='chat_messages')

    def __str__(self):
        return f"Message {self.items_chat.last()}"

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'
        ordering = ('-date_created',)
