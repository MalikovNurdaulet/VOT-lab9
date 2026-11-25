<div align="center">

# 🐋 Лабораторная работа 9

### Docker Compose: запуск многоконтейнерного приложения

`Дисциплина «Облачные технологии и виртуализация»` · `продолжение лабораторной № 8 «Dockerfile` · `собственный образ»`


**Студент:** Маликов Нурдаулет  
**Тема:** Docker Compose  
**Специальность:** Прикладная статистика и Data Science  
**Проверил(а):** Тихонова О. А.  
**Репозиторий:** [MalikovNurdaulet/VOT-lab9](https://github.com/MalikovNurdaulet/VOT-lab9)

</div>

## 1. Цель работы

Научиться описывать, запускать и управлять многоконтейнерным приложением с помощью 
Docker Compose: организовывать взаимодействие сервисов, хранить данные PostgreSQL в 
томе, передавать настройки через переменные окружения и проверять работоспособность 
системы.

## 2. Задачи работы
- изучить структуру файла compose.yaml;
- описать два сервиса: PostgreSQL и Python-приложение;
- использовать собственный Dockerfile из лабораторной № 8;
- настроить взаимодействие контейнеров по имени сервиса;
- организовать постоянное хранение данных PostgreSQL;
- использовать файл .env для настройки приложения;
- настроить healthcheck и зависимости сервисов;
- изучить команды docker compose up, down, logs, ps, exec, run;
- проверить сохранность данных после перезапуска;
- выполнить самостоятельное изменение конфигурации

## 3. Теоретические сведения 
### 3.2. Dockerfile, Docker Engine и Docker Compose 
| Инструмент | Назначение |
|---|---|
| Dockerfile | Описывает, как собрать образ приложения  | 
| Docker Engine  | Создаёт и запускает контейнеры |
| Docker Compose  | Управляет несколькими взаимосвязанными сервисами  |

### 3.3. Что такое сервис 
```bash
services: 
    db `база данных PostgreSQL из готового образа`: 
        image: postgres:17 
    app: 
        build: .
```
db = `база данных PostgreSQL из готового образа`  
app = `наше Python-приложение, образ которого собирается из Dockerfile.`

### 3.4. Структура файла compose.yaml
```bash
services: 
    db: 
        image: postgres:17 
        environment: 
            POSTGRES_PASSWORD: student123 
        volumes:
            - pgdata:/var/lib/postgresql/data 
    app: 
        build: . 
        depends_on: 
        - db 
volumes: 
    pgdata:
```

### 3.5. Сети Docker Compose
```bash
    ports: - "127.0.0.1:5433:5432"
```
5433 = `порт компьютера`  
5432 = ` порт внутри контейнера.`  

### 3.6. Хранение данных: volumes и bind mounts
```bash
services: 
    db: 
        image: postgres:17 
        volumes:
            - pgdata:/var/lib/postgresql/data 
    volumes: 
        pgdata: 
```
### 3.7. Переменные окружения и файл .env
```bash
environment: 
    POSTGRES_DB: shop 
    POSTGRES_USER: postgres 
    POSTGRES_PASSWORD: ${DB_PASSWORD}
```
DB_PASSWORD = ` student123`

### 3.8. Порядок запуска и healthcheck 
```bash
environment: 
    image: postgres:17 
    healthcheck: 
        test: ["CMD-SHELL", "pg_isready -h 127.0.0.1 -U postgres -d shop"] 
        interval: 5s 
        timeout: 3s 
        retries: 10
```
### 3.9. Жизненный цикл проекта  
| Команда | Назначение |
|---|---|
| docker compose up | Создать и запустить сервис  | 
| docker compose up -d | Запустить в фоновом режиме |
| docker compose up --build | Собрать образы и запустить сервисы  |
| docker compose up  ps -a | Показать контейнеры проекта, включая завершённые  | 
| docker compose up logs | Просмотреть журналы |
| docker compose up exec db sh | Выполнить команду в работающем контейнере  |
| docker compose up run --rm app | Запустить разовый контейнер сервиса   | 
| docker compose up stop | Остановить контейнеры без удаления  |
| docker compose up down | Остановить и удалить контейнеры и сети проекта  |
| docker compose up down v | Дополнительно удалить именованные тома проекта и анонимные тома  | 

## 4. Архитектура приложения 
![Архитектура приложения](assets/image.png)


## 5. Подготовка проекта
### Структура проекта:
```text
lab9/
├── compose.yaml
├── Dockerfile 
├── requirements.txt 
├── report.py 
├── db_report.py 
├── init.sql 
├── .env 
└── .dockerignore 
```



# 🐧 Linux server
## Система
- Ubuntu 24.04 LTS
- В качестве виртуальной машины использован облачный VPS-сервер с операционной системой Ubuntu 24.04 LTS. Доступ к серверу осуществляется удалённо по протоколу SSH.V
- 2 vCPU · 4 GB RAM · 40 GB SSD · 200 Mbps




### Шаг 1. Dockerfile
```console
root@hiplet-123755:~# mkdir lab9
root@hiplet-123755:~# ls
errors.log  lab7  lab8  lab9  linux_lab  listing.txt  project  tasks.txt  tgbot

root@hiplet-123755:~/lab9# nano Dockerfile
root@hiplet-123755:~/lab9# cat Dockerfile
    FROM python:3.12-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY report.py db_report.py ./
    CMD ["python", "db_report.py"]
```

### Шаг 2. compose.yaml 

```console
root@hiplet-123755:~/lab9# nano compose.yaml
root@hiplet-123755:~/lab9# cat compose.yaml
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: shop
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -h 127.0.0.1 -U postgres -d shop"]
      interval: 5s
      timeout: 3s
      retries: 10
  app:
    build: .
    environment:
      DATABASE_URL: postgresql+psycopg2://postgres:${DB_PASSWORD}@db:5432/shop
    depends_on:
      db:
        condition: service_healthy
volumes:
  pgdata:
```

### Шаг 3. Файлы .env и .dockerignore  
```console
root@hiplet-123755:~/lab9# nano .env
root@hiplet-123755:~/lab9# cat .env
    DB_PASSWORD=student123

root@hiplet-123755:~/lab9# nano .dockerignore
root@hiplet-123755:~/lab9# cat .dockerignore
    .env
    .git
    __pycache__/
    *.pyc    
```

### Шаг 4. Инициализация базы 
```console
root@hiplet-123755:~/lab9# nano init.sql
root@hiplet-123755:~/lab9# cat init.sql
    CREATE TABLE sales (
        id      SERIAL PRIMARY KEY,
        city    TEXT,
        product TEXT,
        amount  INTEGER
    );
    INSERT INTO sales (city, product, amount) VALUES
        ('Алматы',  'Ноутбук',  350000),
        ('Астана',  'Телефон',  180000),
        ('Алматы',  'Наушники',  25000),
        ('Шымкент', 'Телефон',  175000),
        ('Астана',  'Ноутбук',  360000),
        ('Алматы',  'Телефон',  185000),
        ('Шымкент', 'Наушники',  22000),
        ('Астана',  'Наушники',  24000),
        ('Алматы',  'Ноутбук',  340000),
        ('Шымкент', 'Ноутбук',  355000);  
```

### docker compose config
```console
root@hiplet-123755:~/lab9# docker compose config
name: lab9
services:
  app:
    environment:
      DATABASE_URL: postgresql+psycopg2://postgres:student123@db:5432/shop
    networks:
      default: null
    build:
      context: /root/lab9
      dockerfile: Dockerfile
    depends_on:
      db:
        condition: service_healthy
        required: true
  db:
    environment:
      POSTGRES_DB: shop
      POSTGRES_PASSWORD: student123
      POSTGRES_USER: postgres
    image: postgres:17
    networks:
      default: null
    volumes:
      - type: volume
        source: pgdata
        target: /var/lib/postgresql/data
        volume: {}
      - type: bind
        source: /root/lab9/init.sql
        target: /docker-entrypoint-initdb.d/init.sql
        read_only: true
        bind: {}
    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -h 127.0.0.1 -U postgres -d shop
      timeout: 3s
      interval: 5s
      retries: 10
networks:
  default:
    name: lab9_default
volumes:
  pgdata:
    name: lab9_pgdata
```

## 6. Запуск приложения
### Шаг 5. Сборка и запуск
```console
root@hiplet-123755:~/lab9# docker compose up --build
    [+] Building 33.3s (12/12) FINISHED
    => [internal] load local bake definitions                                                                         0.0s
    => => reading from stdin 454B                                                                                     0.0s
    => [internal] load build definition from Dockerfile                                                               0.0s
    => => transferring dockerfile: 216B                                                                               0.0s
    => [internal] load metadata for docker.io/library/python:3.12-slim                                                1.0s
    => [internal] load .dockerignore                                                                                  0.0s
    => => transferring context: 72B                                                                                   0.0s
    => [1/5] FROM docker.io/library/python:3.12-slim@sha256:191083cdf6c7bda8c76158983163ead5d5cf7b77cf3033e805bb0f52  2.1s
    => => resolve docker.io/library/python:3.12-slim@sha256:191083cdf6c7bda8c76158983163ead5d5cf7b77cf3033e805bb0f52  0.0s
    => => sha256:286d8c291daa64125703b22c3d009462bcae0b630eaa16ad5b934502c4917233 248B / 248B                         0.1s
    => => sha256:e3e428093f5e80791498526d73a46eabf0e69575dc10897cf47aa99120e41712 12.12MB / 12.12MB                   0.3s
    => => sha256:30cf67d7101c07c55eef20970bc403fbde5f8600c2c4c38b4881a2da4fffb0b6 1.29MB / 1.29MB                     0.4s
    => => sha256:40748add9f4f6f944f334cbfc286590d6e93f60fb06f6ee7ffa1b894080ad861 29.84MB / 29.84MB                   0.6s
    => => extracting sha256:40748add9f4f6f944f334cbfc286590d6e93f60fb06f6ee7ffa1b894080ad861                          0.9s
    => => extracting sha256:30cf67d7101c07c55eef20970bc403fbde5f8600c2c4c38b4881a2da4fffb0b6                          0.1s
    => => extracting sha256:e3e428093f5e80791498526d73a46eabf0e69575dc10897cf47aa99120e41712                          0.5s
    => => extracting sha256:286d8c291daa64125703b22c3d009462bcae0b630eaa16ad5b934502c4917233                          0.0s
    => [internal] load build context                                                                                  0.0s
    => => transferring context: 997B                                                                                  0.0s
    => [2/5] WORKDIR /app                                                                                             0.2s
    => [3/5] COPY requirements.txt .                                                                                  0.0s
    => [4/5] RUN pip install --no-cache-dir -r requirements.txt                                                      16.3s
    => [5/5] COPY report.py db_report.py ./                                                                           0.1s
    => exporting to image                                                                                            13.5s
    => => exporting layers                                                                                            9.4s
    => => exporting manifest sha256:0e6abc3b105c0b241a84e92581768128782b1fb10889e932c6e501d76f848243                  0.0s
    => => exporting config sha256:c86ae590656e14c1baa9f193970491ecd3bb84b45f81ab35f97a356cdbfbf02b                    0.0s
    => => exporting attestation manifest sha256:8c30542db1d1d3e75da565a757a38dc3a112f6936c3c4d97656226fd1495c76d      0.0s
    => => exporting manifest list sha256:9c937f80ec07399884c7d5b6dc3b6ab64076f50895ed2a8ce12cf363e85278ec             0.0s
    => => naming to docker.io/library/lab9-app:latest                                                                 0.0s
    => => unpacking to docker.io/library/lab9-app:latest                                                              4.0s
    => resolving provenance for metadata file                                                                         0.0s
    [+] up 5/5
    ✔ Image lab9-app       Built                                                                                      33.4s
    ✔ Network lab9_default Created                                                                                     0.0s
    ✔ Volume lab9_pgdata   Created                                                                                     0.0s
    ✔ Container lab9-db-1  Created                                                                                     0.4s
    ✔ Container lab9-app-1 Created                                                                                     0.0s
    Attaching to app-1, db-1
    Container lab9-db-1 Waiting
    db-1  | The files belonging to this database system will be owned by user "postgres".
    ...
    db-1  |
    db-1  | fixing permissions on existing directory /var/lib/postgresql/data ... ok
    db-1  | creating subdirectories ... ok
    db-1  | selecting dynamic shared memory implementation ... posix
    db-1  | selecting default "max_connections" ... 100
    db-1  | selecting default "shared_buffers" ... 128MB
    db-1  | selecting default time zone ... Etc/UTC
    db-1  | creating configuration files ... ok
    db-1  | running bootstrap script ... ok
    db-1  | performing post-bootstrap initialization ... ok
    db-1  | syncing data to disk ... ok
    ...
    db-1  | server started
    ...
    db-1  | 2026-11-25 19:53:13.876 UTC [1] LOG:  database system is ready to accept connections

    Container lab9-db-1 Healthy
    app-1  |    city  sales  revenue
    app-1  |  Алматы      4   900000
    app-1  |  Астана      3   564000
    app-1  | Шымкент      3   552000
    app-1 exited with code 0
```


### Шаг 6. Изучение сервисов 
```console
root@hiplet-123755:~# cd lab9
root@hiplet-123755:~/lab9# docker compose ps -a
    NAME         IMAGE         COMMAND                  SERVICE   CREATED         STATUS                     PORTS
    lab9-app-1   lab9-app      "python db_report.py"    app       3 minutes ago   Exited (0) 3 minutes ago
    lab9-db-1    postgres:17   "docker-entrypoint.s…"   db        3 minutes ago   Up 3 minutes (healthy)     5432/tcp

root@hiplet-123755:~/lab9# docker compose logs db
    db-1  | The files belonging to this database system will be owned by user "postgres".
    ...
    db-1  | server started
    db-1  | CREATE DATABASE
    db-1  | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init.sql
    db-1  | CREATE TABLE
    db-1  | INSERT 0 10
    ...
    db-1  | 2026-11-25 19:53:13.876 UTC [1] LOG:  database system is ready to accept connections

root@hiplet-123755:~/lab9# docker compose logs app
    app-1  |    city  sales  revenue
    app-1  |  Алматы      4   900000
    app-1  |  Астана      3   564000
    app-1  | Шымкент      3   552000

root@hiplet-123755:~/lab9# docker compose images
    CONTAINER           REPOSITORY          TAG                 PLATFORM            IMAGE ID            SIZE                CREATED
    lab9-app-1          lab9-app            latest              linux/amd64         9c937f80ec07        431MB               4 minutes ago
    lab9-db-1           postgres            17                  linux/amd64         3b0cda93be7c        640MB               4 weeks ago
```


- `Контейнер lab9-db-1` — работает в состоянии healthy и готов принимать подключения;
- `Контейнер lab9-app-1` — успешно завершился с кодом Exited (0);
- `lab9-app` — составляет 431 МБ;
- `postgres:17` — 640 МБ;

### Шаг 7. Повторный запуск отчёта
```console
root@hiplet-123755:~/lab9# docker compose run --rm app
    [+] run 1/1
    ✔ Container lab9-db-1 Running                                                                                                                                                                                0.0s
    Container lab9-db-1 Waiting
    Container lab9-db-1 Healthy
    Container lab9-app-run-fa6b7d38c9b9 Creating
    Container lab9-app-run-fa6b7d38c9b9 Created
    city  sales  revenue
    Алматы      4   900000
    Астана      3   564000
    Шымкент      3   552000
```

## 7. Повторный запуск отчёта 
### Подключитесь к базе: 
```console
root@hiplet-123755:~/lab9# docker compose exec db psql -U postgres -d shop
    psql (17.11 (Debian 17.11-1.pgdg13+2))
    Type "help" for help.
    shop=# INSERT INTO sales (city, product, amount) 
    VALUES ('Астана', 'Монитор', 95000); 
    \q
```

### Добавьте новую продажу и выйдите командой \q: 
```console
root@hiplet-123755:~/lab9# docker compose exec db psql -U postgres -d shop
    psql (17.11 (Debian 17.11-1.pgdg13+2))
    Type "help" for help.

    shop=# SELECT * FROM sales;
    id |  city   | product  | amount
    ----+---------+----------+--------
    1 | Алматы  | Ноутбук  | 350000
    2 | Астана  | Телефон  | 180000
    3 | Алматы  | Наушники |  25000
    4 | Шымкент | Телефон  | 175000
    5 | Астана  | Ноутбук  | 360000
    6 | Алматы  | Телефон  | 185000
    7 | Шымкент | Наушники |  22000
    8 | Астана  | Наушники |  24000
    9 | Алматы  | Ноутбук  | 340000
    10 | Шымкент | Ноутбук  | 355000
    11 | Астана  | Монитор  |  95000
    (11 rows)

    shop=#
    \q
```

### Остановите проект и запустите его заново:  
```console
root@hiplet-123755:~/lab9# docker compose down
    [+] down 3/3
    ✔ Container lab9-app-1 Removed                                                                                                                                                                               0.0s
    ✔ Container lab9-db-1  Removed                                                                                                                                                                               0.1s
    ✔ Network lab9_default Removed                                                                                                                                                                               0.1s
root@hiplet-123755:~/lab9# docker compose up -d db
    [+] up 2/2
    ✔ Network lab9_default Created                                                                                                                                                                               0.0s
    ✔ Container lab9-db-1  Started                                                                                                                                                                               0.2s
root@hiplet-123755:~/lab9# docker compose run --rm app
    [+] run 1/1
    ✔ Container lab9-db-1 Running                                                                                                                                                                                0.0s
    Container lab9-db-1 Waiting
    Container lab9-db-1 Healthy
    Container lab9-app-run-c80b270ab5eb Creating
    Container lab9-app-run-c80b270ab5eb Created
    city  sales  revenue
    Алматы      4   900000
    Астана      4   659000
    Шымкент      3   552000
```

## 8. Самостоятельное задание 
### 📌 1. Добавьте в таблицу sales ещё пять продаж. Учтите, что init.sql не выполняется повторно: либо добавьте строки через psql, либо измените init.sql и пересоздайте том командой docker compose down -v. Объясните, какой способ вы выбрали и почему.
```console
root@hiplet-123755:~/lab9# docker compose exec db psql -U postgres -d shop
    psql (17.11 (Debian 17.11-1.pgdg13+2))
    Type "help" for help.

    shop=# INSERT INTO sales (city, product, amount) VALUES
        ('Алматы', 'Монитор', 55000),
        ('Астана', 'Ноутбук', 40000),
        ('Шымкент', 'Телефон', 15000),
        ('Алматы', 'Наушники', 30000),
        ('Астана', 'Монитор', 20000);
    INSERT 0 5
    shop=# SELECT * FROM sales;
    id |  city   | product  | amount
    ----+---------+----------+--------
    1 | Алматы  | Ноутбук  | 350000
    2 | Астана  | Телефон  | 180000
    3 | Алматы  | Наушники |  25000
    4 | Шымкент | Телефон  | 175000
    5 | Астана  | Ноутбук  | 360000
    6 | Алматы  | Телефон  | 185000
    7 | Шымкент | Наушники |  22000
    8 | Астана  | Наушники |  24000
    9 | Алматы  | Ноутбук  | 340000
    10 | Шымкент | Ноутбук  | 355000
    11 | Астана  | Монитор  |  95000
    12 | Алматы  | Монитор  |  55000
    13 | Астана  | Ноутбук  |  40000
    14 | Шымкент | Телефон  |  15000
    15 | Алматы  | Наушники |  30000
    16 | Астана  | Монитор  |  20000
    (16 rows)

    shop=# SELECT COUNT(*) FROM sales;
    count
    -------
        16
    (1 row)

    shop=#
    \q
```
### ✅способ добавления записей через psql, поскольку он проще и позволяет сохранить существующие данные без удаления тома и повторной инициализации базы данных


### 📌 2. Измените db_report.py, чтобы он мог выводить выручку по товарам.
```console
root@hiplet-123755:~/lab9# nano db_report.py
root@hiplet-123755:~/lab9# cat db_report.py
    import os
    import pandas as pd
    from sqlalchemy import create_engine

    url = os.environ["DATABASE_URL"]
    engine = create_engine(url)

    group_by = os.getenv("GROUP_BY", "city")

    if group_by not in ["city", "product"]:
        raise ValueError("GROUP_BY must be city or product")

    query = f"""
    SELECT
        {group_by},
        COUNT(*) AS sales,
        SUM(amount) AS revenue
    FROM sales
    GROUP BY {group_by}
    ORDER BY revenue DESC
    """
    print(pd.read_sql(query, engine).to_string(index=False))

root@hiplet-123755:~/lab9# docker compose run --rm app
    [+] run 1/1
    ✔ Container lab9-db-1 Running                                                                                                                                                                                0.0s
    Container lab9-db-1 Waiting
    Container lab9-db-1 Healthy
    Container lab9-app-run-71858d679227 Creating
    Container lab9-app-run-71858d679227 Created
    city  sales  revenue
    Алматы      6   985000
    Астана      6   719000
    Шымкент      4   567000
```

### 📌 3. Добавьте переменную окружения GROUP_BY со значениями city или product и объявите её в compose.yaml, например GROUP_BY: ${GROUP_BY:-city}. 
```console
root@hiplet-123755:~/lab9# nano compose.yaml
root@hiplet-123755:~/lab9# cat compose.yaml
    services:
    db:
        image: postgres:17
        environment:
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: ${DB_PASSWORD}
        POSTGRES_DB: shop
        volumes:
        - pgdata:/var/lib/postgresql/data
        - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
        healthcheck:
        test: ["CMD-SHELL", "pg_isready -h 127.0.0.1 -U postgres -d shop"]
        interval: 5s
        timeout: 3s
        retries: 10

    app:
        build: .
        environment:
        DATABASE_URL: postgresql+psycopg2://postgres:${DB_PASSWORD}@db:5432/shop
        GROUP_BY: ${GROUP_BY:-city}
        depends_on:
        db:
            condition: service_healthy

    volumes:
    pgdata:

root@hiplet-123755:~/lab9# docker compose run --rm app
    [+] run 1/1
    ✔ Container lab9-db-1 Running                                                                                                                                                                                0.0s
    Container lab9-db-1 Waiting
    Container lab9-db-1 Healthy
    Container lab9-app-run-369efa3aa264 Creating
    Container lab9-app-run-369efa3aa264 Created
    city  sales  revenue
    Алматы      6   985000
    Астана      6   719000
    Шымкент      4   567000
```

### 📌 4. Пересоберите образ после изменения кода (docker compose build app) и проверьте оба варианта отчёта, например docker compose run --rm -e GROUP_BY=product app.
```console
root@hiplet-123755:~/lab9# docker compose build app
    [+] Building 1.0s (12/12) FINISHED
    => [internal] load local bake definitions                                                                                                                                                                   0.0s
    => => reading from stdin 454B                                                                                                                                                                               0.0s
    => [internal] load build definition from Dockerfile                                                                                                                                                         0.0s
    => => transferring dockerfile: 216B                                                                                                                                                                         0.0s
    => [internal] load metadata for docker.io/library/python:3.12-slim                                                                                                                                          0.7s
    => [internal] load .dockerignore                                                                                                                                                                            0.0s
    => => transferring context: 72B                                                                                                                                                                             0.0s
    => [1/5] FROM docker.io/library/python:3.12-slim@sha256:191083cdf6c7bda8c76158983163ead5d5cf7b77cf3033e805bb0f5296f51b4b                                                                                    0.0s
    => => resolve docker.io/library/python:3.12-slim@sha256:191083cdf6c7bda8c76158983163ead5d5cf7b77cf3033e805bb0f5296f51b4b                                                                                    0.0s
    => [internal] load build context                                                                                                                                                                            0.0s
    => => transferring context: 576B                                                                                                                                                                            0.0s
    => CACHED [2/5] WORKDIR /app                                                                                                                                                                                0.0s
    => CACHED [3/5] COPY requirements.txt .                                                                                                                                                                     0.0s
    => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                                          0.0s
    => [5/5] COPY report.py db_report.py ./                                                                                                                                                                     0.0s
    => exporting to image                                                                                                                                                                                       0.1s
    => => exporting layers                                                                                                                                                                                      0.0s
    => => exporting manifest sha256:e6a7c6fc1f29cfd11295a645bf51e9fd56b453c038f849cd821aa47dfc724c3b                                                                                                            0.0s
    => => exporting config sha256:4cfc3986d3d343fa2437e896a02864e4a7b0a3e4b0dba2ecc235cf1faaafd955                                                                                                              0.0s
    => => exporting attestation manifest sha256:599d229241fa7f20194362cb31d7bf090bcc51200c812c95feaabf686ee47d2a                                                                                                0.0s
    => => exporting manifest list sha256:99f40420ff202f205ebcfa9fd49c268a7bf3f220705021c718a9b616cc659876                                                                                                       0.0s
    => => naming to docker.io/library/lab9-app:latest                                                                                                                                                           0.0s
    => => unpacking to docker.io/library/lab9-app:latest                                                                                                                                                        0.0s
    => resolving provenance for metadata file                                                                                                                                                                   0.0s
    [+] build 1/1
    ✔ Image lab9-app Built                                                                                                                                                                                       1.1s
root@hiplet-123755:~/lab9# docker compose run --rm -e GROUP_BY=city app
    [+] run 1/1
    ✔ Container lab9-db-1 Running                                                                                                                                                                                0.0s
    Container lab9-db-1 Waiting
    Container lab9-db-1 Healthy
    Container lab9-app-run-7d1bf33ac248 Creating
    Container lab9-app-run-7d1bf33ac248 Created
    city  sales  revenue
    Алматы      6   985000
    Астана      6   719000
    Шымкент      4   567000
root@hiplet-123755:~/lab9# docker compose run --rm -e GROUP_BY=product app
    [+] run 1/1
    ✔ Container lab9-db-1 Running                                                                                                                                                                                0.0s
    Container lab9-db-1 Waiting
    Container lab9-db-1 Healthy
    Container lab9-app-run-493010c1c81c Creating
    Container lab9-app-run-493010c1c81c Created
    product  sales  revenue
    Ноутбук      5  1445000
    Телефон      4   555000
    Монитор      3   170000
    Наушники      4   101000
```

### 📌 5. Продемонстрируйте, что после docker compose down данные сохраняются. 
```console
root@hiplet-123755:~/lab9# docker compose down
    [+] down 2/2
    ✔ Container lab9-db-1  Removed                                                                                                                                                                               0.1s
    ✔ Network lab9_default Removed                                                                                                                                                                               0.1s
root@hiplet-123755:~/lab9# docker compose up -d db
    [+] up 2/2
    ✔ Network lab9_default Created                                                                                                                                                                               0.0s
    ✔ Container lab9-db-1  Started                                                                                                                                                                               0.2s
root@hiplet-123755:~/lab9# docker compose run --rm -e GROUP_BY=city app
    [+] run 1/1
    ✔ Container lab9-db-1 Running                                                                                                                                                                                0.0s
    Container lab9-db-1 Waiting
    Container lab9-db-1 Healthy
    Container lab9-app-run-290a099ba49a Creating
    Container lab9-app-run-290a099ba49a Created
    city  sales  revenue
    Алматы      6   985000
    Астана      6   719000
    Шымкент      4   567000
root@hiplet-123755:~/lab9# docker compose run --rm -e GROUP_BY=product app
    [+] run 1/1
    ✔ Container lab9-db-1 Running                                                                                                                                                                                0.0s
    Container lab9-db-1 Waiting
    Container lab9-db-1 Healthy
    Container lab9-app-run-3199bd931e3d Creating
    Container lab9-app-run-3199bd931e3d Created
    product  sales  revenue
    Ноутбук      5  1445000
    Телефон      4   555000
    Монитор      3   170000
    Наушники      4   101000
```




## 9. Контрольные вопросы 
### ❓1. Чем Docker Compose отличается от Dockerfile? 
- **Dockerfile** описывает процесс сборки образа приложения
- **Docker Compose** управляет запуском и взаимодействием контейнеров через compose.yaml

### ❓2. Что описывает раздел services? 
- сервисы приложения
- образы
- переменные окружения
- сетевые настройки
- параметры запуска

### ❓3. Чем build отличается от image? 
- **build** собирает образ на основе Dockerfile
- **image** использует готовый Docker-образ

### ❓4. Почему приложение подключается к db, а не к localhost? 
- **Docker Compose** автоматически создаёт общую сеть
- Адрес db указывает на контейнер PostgreSQL

### ❓5. Зачем нужен healthcheck? 
- проверяет состояние и готовность сервиса

### ❓6. Чем depends_on отличается от healthcheck? 
- **depends_on** определяет зависимости и порядок запуска сервисов
- **healthcheck** проверяет их работоспособность.

### ❓7. Что происходит при docker compose down? 
- Команда останавливает и удаляет контейнеры и сети проекта. Именованные тома и образы сохраняются

### ❓8. Чем docker compose down -v отличается от обычного down? 
- Удаляет именованные тома, объявленные в конфигурации проекта, и подключённые анонимные тома
- В результате данные PostgreSQL, хранящиеся в томе pgdata, будут потеряны

### ❓9. Почему init.sql не выполняется при каждом запуске? 
- Файл **init.sql** выполняется только при первой инициализации пустого каталога данных

### ❓10. В чём отличие docker compose run от docker compose exec?
- **docker compose run** создаёт новый контейнер сервиса для выполнения отдельной задачи
- **docker compose exec** выполняет команду внутри уже работающего контейнера без создания нового
