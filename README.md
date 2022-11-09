# Для запуска проекта на сервере необходимо

Операционная система: Ubuntu server 18

База данных: Postgres 11

Серсивысы: Redis 6

Django 3, python 3.7 >

```shell
python3 -m pip install virtualenv && python3 -m virtualenv venv && source venv/bin/activate
```
```shell
pip install -r requirements.txt
```

## Можно использовать docker-compose
В репозитории находится файл docker-compose.yml

## Для заполения fixture
Ипользуйте приведенные команды в заданном порядке

```bash
python manage.py loaddata shop/fixtures/characteristics.json
```
```bash
python manage.py loaddata shop/fixtures/category.json
```
```bash
python manage.py loaddata shop/fixtures/filled_characteristic.json
```
```bash
python manage.py loaddata users/fixtures/users.json
```
```bash
python manage.py loaddata shop/fixtures/shop.json
```
```bash
python manage.py loaddata shop/fixtures/products.json
```