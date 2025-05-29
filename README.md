# Bank‑Sim — симуляция банковской системы

Курсовой проект на Python 3.10+ (SQLite + SQLAlchemy) с дружелюбным CLI на Click + Rich.

---

## Быстрая установка и запуск

```bash
# клонируем и переходим в каталог
$ git clone <repo_url> bank_sim
$ cd bank_sim

# создаём и активируем виртуальное окружение
$ python -m venv venv
$ source venv/bin/activate        # Windows: venv\Scripts\activate

# ставим пакет в editable‑режиме (установит все зависимости)
$ pip install -e .

# инициализируем базу (создаст bank.db)
$ bank initdb
```

После этого команда **`bank`** доступна из любого места (пока активирован `venv`).

---

## Дерево проекта

```
bank_sim/
├── cli.py              # CLI-группа Click (скрипт `bank`)
├── config.py           # .env / настройки
├── database.py         # engine + Session + init_db()
├── models/             # SQLAlchemy ORM‑модели (Client, Account, Transaction)
├── services/           # бизнес‑логика + очередь FIFO
└── ...
pyproject.toml          # dependencies + entry‑point bank
requirements.txt        # дублирует зависимости (Faculty)
```

---

## Список команд

| Команда                                      | Аргументы                | Что делает                                                                     |
| -------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------ |
| `bank initdb`                                | –                        | Создаёт таблицы в базе данных (запускать один раз)                             |
| `bank register <NAME>`                       | `NAME` — имя клиента     | Регистрирует нового клиента, выводит `id`                                      |
| `bank open <CLIENT_ID>`                      | `CLIENT_ID`              | Открывает счёт клиенту                                                         |
| `bank deposit <ACC_ID> <AMOUNT>`             | `ACC_ID`, `AMOUNT` (руб) | Пополняет счёт                                                                 |
| `bank withdraw <ACC_ID> <AMOUNT>`            | –                        | Снимает средства (ошибка при нехватке)                                         |
| `bank transfer <FROM_ACC> <TO_ACC> <AMOUNT>` | –                        | Перевод между счетами                                                          |
| `bank history <ACC_ID>`                      | –                        | Показать таблицу транзакций счёта                                              |
| `bank enqueue <CLIENT_ID>`                   | –                        | Поставить клиента в онлайн‑очередь                                             |
| `bank queue-list`                            | –                        | Показать текущую очередь (FIFO)                                                |
| `bank serve`                                 | –                        | Обслужить следующего в очереди                                                 |
| `bank shell`                                 | –                        | Интерактивный REPL: вводите те же команды без префикса `bank` (выйти — `exit`) |

Все команды поддерживают `--help`, например:

```bash
bank deposit --help
```

---

## Примеры полного сценария

```bash
# 1. Создаём клиента и счёт
bank register "Иван Иванов"        # ← id=1
bank open 1                         # ← счёт id=1

# 2. Работа с деньгами
bank deposit 1 1000
bank withdraw 1 250
bank history 1

# 3. Очередь обслуживания
bank enqueue 1
bank queue-list
bank serve
```
## Интерактивный режим (`bank shell`)

`bank shell` запускает REPL-консоль. Внутри неё вводятся те же команды,
что и в обычном CLI, **но без префикса `bank`**.  
Выход — `exit`, `quit`, `Ctrl-D` или `Ctrl-C`.

```bash
$ bank shell
bank> help              # список всех доступных под-команд
bank> register "Иван"
bank> open 1
bank> deposit 1 1500
bank> enqueue 1
bank> serve
bank> history 1
bank> queue-list
bank> exit
```


---

## Конфигурация через .env

| Переменная       | По умолчанию        | Назначение                          |
| ---------------- | ------------------- | ----------------------------------- |
| `BANK_DB_URL`    | `sqlite:///bank.db` | Строка подключения к БД             |
| `BANK_LOG_LEVEL` | `INFO`              | Уровень логов (DEBUG/INFO/WARNING…) |

Создайте файл `.env` рядом с `pyproject.toml`, например:

```dotenv
BANK_DB_URL=sqlite:///C:/temp/my_bank.db
BANK_LOG_LEVEL=DEBUG
```


### Требования курса выполнены

✔ классы **Client, Account, Transaction, BankQueue**
✔ операции **deposit, withdraw, transfer** с валидацией
✔ история транзакций (таблица Rich)
✔ очередь FIFO и команды `enqueue` / `serve`
✔ CLI + интерактивный `shell`
✔ установка одной командой `pip install -e .`

> Если нужно расширение функций или помощь — пишите мне в WhatsApp или Telegramm: @asanjs
