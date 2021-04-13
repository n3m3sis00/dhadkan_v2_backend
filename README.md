## Setup Database

#### Using Docker
```bash
docker run --name dhadkan_db -v "$(pwd)/database:/var/lib/postgresql" -e POSTGRES_USER=dhadkan -e POSTGRES_PASSWORD=dhadkan -d postgres
```

## Start Server without [PROD]

```bash
docker build --tag server_dhadkan .
docker run --env-file ./.env --link dhadkan_db:dhadkan_db -p 8000:8000 -it --name cont_dhadkan server_dhadkan python manage.py runserver 0.0.0.0:8000 
```

## Start Server without [DEV]

```bash
docker build --tag server_dhadkan .
docker run --env-file ./.env --link dhadkan_db:dhadkan_db -p 8000:8000 -v $(pwd):/app -it --name cont_dhadkan server_dhadkan python manage.py runserver 0.0.0.0:8000 
```