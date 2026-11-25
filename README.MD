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

## 📌 1. Цель работы

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




## Шаг 1. Dockerfile
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

## Шаг 2. compose.yaml 

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

## Шаг 3. Файлы .env и .dockerignore  
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

## Шаг 4. Инициализация базы 
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

## docker compose config
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

## Шаг 5. Сборка и запуск
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
db-1  | This user must also own the server process.
db-1  |
db-1  | The database cluster will be initialized with locale "en_US.utf8".
db-1  | The default database encoding has accordingly been set to "UTF8".
db-1  | The default text search configuration will be set to "english".
db-1  |
db-1  | Data page checksums are disabled.
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
db-1  |
db-1  |
db-1  | Success. You can now start the database server using:
db-1  |
db-1  |     pg_ctl -D /var/lib/postgresql/data -l logfile start
db-1  |
db-1  | initdb: warning: enabling "trust" authentication for local connections
db-1  | initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
db-1  | waiting for server to start....2026-11-25 19:53:13.424 UTC [47] LOG:  starting PostgreSQL 17.11 (Debian 17.11-1.pgdg13+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
db-1  | 2026-11-25 19:53:13.427 UTC [47] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2026-11-25 19:53:13.431 UTC [50] LOG:  database system was shut down at 2026-11-25 19:53:13 UTC
db-1  | 2026-11-25 19:53:13.437 UTC [47] LOG:  database system is ready to accept connections
db-1  |  done
db-1  | server started
db-1  | CREATE DATABASE
db-1  |
db-1  |
db-1  | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init.sql
db-1  | CREATE TABLE
db-1  | INSERT 0 10
db-1  |
db-1  |
db-1  | waiting for server to shut down....2026-11-25 19:53:13.735 UTC [47] LOG:  received fast shutdown request
db-1  | 2026-11-25 19:53:13.736 UTC [47] LOG:  aborting any active transactions
db-1  | 2026-11-25 19:53:13.741 UTC [47] LOG:  background worker "logical replication launcher" (PID 53) exited with exit code 1
db-1  | 2026-11-25 19:53:13.742 UTC [48] LOG:  shutting down
db-1  | 2026-11-25 19:53:13.743 UTC [48] LOG:  checkpoint starting: shutdown immediate
db-1  | 2026-11-25 19:53:13.782 UTC [48] LOG:  checkpoint complete: wrote 935 buffers (5.7%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.020 s, sync=0.017 s, total=0.041 s; sync files=306, longest=0.002 s, average=0.001 s; distance=4279 kB, estimate=4279 kB; lsn=0/191D428, redo lsn=0/191D428
db-1  | 2026-11-25 19:53:13.789 UTC [47] LOG:  database system is shut down
db-1  |  done
db-1  | server stopped
db-1  |
db-1  | PostgreSQL init process complete; ready for start up.
db-1  |
db-1  | 2026-11-25 19:53:13.862 UTC [1] LOG:  starting PostgreSQL 17.11 (Debian 17.11-1.pgdg13+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
db-1  | 2026-11-25 19:53:13.863 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db-1  | 2026-11-25 19:53:13.864 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db-1  | 2026-11-25 19:53:13.866 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db-1  | 2026-11-25 19:53:13.870 UTC [65] LOG:  database system was shut down at 2026-11-25 19:53:13 UTC
db-1  | 2026-11-25 19:53:13.876 UTC [1] LOG:  database system is ready to accept connections
Container lab9-db-1 Healthy
app-1  |    city  sales  revenue
app-1  |  Алматы      4   900000
app-1  |  Астана      3   564000
app-1  | Шымкент      3   552000
app-1 exited with code 0
```