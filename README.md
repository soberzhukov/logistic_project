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

## Для заполнения fixture

- Заполнить базу стран и городов
```bash
./manage.py cities_light --force-all
```
- Заполнить базу кастомными данными "Валюта"
```bash
python manage.py loaddata payment/fixtures/currency.json
```

