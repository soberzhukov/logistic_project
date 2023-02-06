# Для запуска проекта на сервере необходимо

Операционная система: Ubuntu server 22

База данных: Postgres 15

Django 4, python 3.10 

```shell
python3 -m pip install virtualenv && python3 -m virtualenv venv && source venv/bin/activate
```
```shell
pip install -r requirements.txt
```
### Перезапуск работы сервера
```shell
supervisorctl restart all
```
---
## Для заполнения fixture

- Заполнить базу стран и городов
```bash
./manage.py cities_light --force-all
```
- Заполнить базу кастомными данными "Валюта"
```bash
python manage.py loaddata payment/fixtures/currency.json
```
---
## Описание сущностей

- ***logisticproject*** - основное приложение
  - settings - файл настроек
  - celeryapp - файл подключения celery 
  - urls - файл подключения остальных urls 

- ***common*** - общее приложение, отсюда наследуются order и offer
- ***order*** - приложение с логикой, относящейся к заказам
- ***offer*** - приложение с логикой, относящейся к предложениям
- ***selection*** - приложение с логикой, относящейся к подборкам order и offer
- ***contract*** - приложение с логикой, относящейся к контрактам
- ***payment*** - приложение с логикой, относящейся к оплате
- ***chat*** - приложение с логикой, относящейся к оплате
- ***users*** - приложение с логикой, относящейся к пользователю

- ***requirements.txt*** - файл зависимостей
- ***.env*** -файл с переменными, которые импортируются в settings

