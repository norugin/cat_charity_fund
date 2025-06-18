# QRkot

![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?logo=sqlite&logoColor=white)
---

Это учебный проект на базе фреймворка **FastAPI**. 

Данный проект позволяет собирать пожертвование на благотворительные проекты для поддержки животных. Администратор может создавать благотворительные проекты, а пользователи могут сделать пожертвование на проекте по очереди их создания. 

### Проекты

Администратор может публиковать несколько проектов, нуждающихся в спонсировании, с указанием необходимой суммы. После того как сборы были проведены, проект автоматически закрывается. Просматривать открытые проекты могут все пользователи.

### Пожертвования

Зарегестрированные пользователи могут вносить пожертвования. Все инвестиции распределяются между проектами в порядке очереди. Пользователь может просматривать только свои собственные пожертвования.

### Отчёт

В проекте есть возможность автоматического формирования отчета в Гугл таблице, в котором перечислены осортированные проекты, которые уже были закрыты.

## Стек технологий:
- Python 3.9
- FastAPI v.0.78.0
- SQLite
- SQLAlchemy
- Alembic
- Google API


## Подготовка к работе:


Клонируйте репозиторий

```shell
git clone https://github.com/norugin/cat_charity_fund.git
cd cat_charity_fund
```


Создайте и активируйте виртуальное окружение

```shell
# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip

# Windows
python -m venv venv
source venv/scripts/activate
python -m pip install --upgrade pip
```

Установите зависимости из файла <code>requirements.txt</code>

```shell
pip install -r requirements.txt
```

Запустите программу
```shell
uvicorn app.main:app 
```


## Документация
После запуска программы документация будет доступна по адресам:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Авторы: 

- Норенко Евгений 

- norugin@gmail.com 