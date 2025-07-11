# Microsite Backend FastAPI Project

## How to setup project?
### Add environment variables file `.env`

```sh
cp .env.template .env
```

Modify the variables/credentials in the `.env` file.

### Start the server (Build & Up the docker images)

```sh
docker-compose up -d --build
```

### Migrate the database

```sh
docker-compose exec backend alembic upgrade head
```

The project setup has been successful. You can check the API Docs at http://127.0.0.1:8000/docs :)

## Development Commands

### Check the status of the docker containers

```sh
docker-compose ps -a
```

### Check logs of fastapi server

```sh
docker-compose logs -f --tail 10 backend
```

### Stop the server

```sh
docker-compose stop
```

### Down the server (-v option will remove volumes)

`WARNING`: By running below command, deletes the database also. You can get your data stored in the database back.

```sh
docker-compose down -v
```

## Alembic DB Migrations

Alembic is used for generating migrations for the database for the SQL Alchemy.

### Create a migration

You can the change the message `create user table` in the below command.

### Create an manual migration

```sh
docker-compose exec backend alembic revision -m "create user table"
```

### Create an autogenerate migration

```sh
docker-compose exec backend alembic revision --autogenerate -m [commit message]
```

### Running a Migration

```sh
docker-compose exec backend alembic upgrade head
```

### Downgrade last migration

```sh
docker-compose exec backend alembic downgrade -1
```

### Downgrade migration from the beginning

```sh
docker-compose exec backend alembic downgrade base
```
# docker compose exec postgres psql -U postgres -d demoproject
# docker compose exec backend alembic revision --autogenerate -m "initial"
# docker-compose exec backend alembic upgrade head