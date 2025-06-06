### Фонд QRKot
Данный проект позволяет собирать пожертвование на благотворительные проекты для поддержки животных. Администратор может создавать благотворительные проекты, а пользователи могут сделать пожертвование на проекте по очереди их создания.

### Как запустить проект:
Cоздать и активировать виртуальное окружение:

#### для Linux
```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip

```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### для Windows
```
python -m venv env
```

```
source env/Scripts/activate
```

```
python -m pip install --upgrade pip

```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Для запуска
```
uvicorn app.main:app
```

## Авторы:
- Норенко Евгений
- norugin@gmail.com