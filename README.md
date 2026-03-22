# ecotech
# Ecotech

Projeto de estudo com arquitetura de microserviços e microfrontends usando:

- FastAPI
- PostgreSQL
- Docker Compose

## Serviços

- users-service → porta 8001
- orders-service → porta 8002

## Bancos

- users-db → porta 5433
- orders-db → porta 5434

## Como subir

```bash
docker compose up --build

Documentação
	•	http://localhost:8001/docs
	•	http://localhost:8002/docs