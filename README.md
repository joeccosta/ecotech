# Ecotech: Plataforma de Gestão de Pedidos de Vestuário Sustentável

## 1. Contexto

A Ecotech é uma empresa de e-commerce focada em vestuário esportivo sustentável. O processo atual de gestão de pedidos baseado em planilhas apresenta limitações como:

- ausência de atualização em tempo real
- erros manuais frequentes
- dificuldade de rastreamento de pedidos
- baixa escalabilidade

Este projeto propõe um **Produto Mínimo Viável (PMV)** utilizando uma arquitetura moderna com **microsserviços** e **microfrontends**.

---

## 2. Arquitetura

```
[ Shell (single-spa) :9000 ]
        |
        |--- orders-mfe :8500
        |
        ↓
[ orders-service :8002 ] ----> [ PostgreSQL orders_db ]
[ users-service  :8001 ] ----> [ PostgreSQL users_db ]
```

### Princípios adotados

- baixo acoplamento entre serviços
- separação de responsabilidades
- escalabilidade independente

---

## 3. Backend

### 3.1 users-service
Responsável por autenticação e usuários:

- criação de usuários
- login (JWT)
- validação de credenciais

### 3.2 orders-service
Responsável por pedidos:

- criação de pedidos
- listagem
- filtro por status
- atualização de status
- rotas protegidas por JWT

### 3.3 Banco de Dados

Cada serviço possui seu próprio banco PostgreSQL:

- isolamento de dados
- independência de deploy

---

## 4. Frontend

Arquitetura baseada em **microfrontends com single-spa**.

### Shell
- orquestra os MFEs
- gerencia rotas

### orders-mfe
- criação de pedidos
- listagem
- atualização de status
- integração com orders-service

---

## 5. Autenticação (JWT)

### Fluxo

1. Login no `users-service`
2. Geração de JWT com:
   - `sub` (email do usuário)
   - `exp` (expiração)
3. Envio do token ao cliente

### Uso

```
Authorization: Bearer <token>
```

### Validação

- feita localmente em cada serviço
- não há chamada entre serviços
- depende de `SECRET_KEY` compartilhada

### Benefícios

- stateless
- escalável
- desacoplado

---

## 6. Tecnologias

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pytest

### Frontend
- React
- TypeScript
- single-spa

### Infra
- Docker
- Docker Compose

---

## 7. Execução

```bash
docker compose up --build
```

### Endpoints

- Frontend: http://localhost:9000
- Users API: http://localhost:8001/docs
- Orders API: http://localhost:8002/docs

---

## 8. Testes

Executar:

```bash
docker compose exec users-service pytest
docker compose exec orders-service pytest
```

### Cobertura atual

- autenticação (login, token válido/inválido)
- rotas protegidas (401)
- criação de pedidos (201)
- validação de payload (422)
- atualização de status

---

## 9. Decisões Técnicas

### JWT compartilhado
- simplicidade para MVP
- evita chamada entre serviços

### Bancos separados
- isolamento
- resiliência

### FastAPI
- produtividade
- tipagem forte

### Microfrontends
- deploy independente
- escalabilidade de equipes

---

## 10. Próximos Passos

- integração completa do login no frontend
- API Gateway / BFF
- logs estruturados
- observabilidade (tracing)
- uso de chave pública (RS256)
- testes no frontend

---

## 11. Status do Projeto

✔ Backend funcional (users + orders)
✔ Autenticação JWT entre serviços
✔ Testes automatizados passando
✔ Integração via Postman validada
✔ Ambiente dockerizado reproduzível

---

## 12. Conclusão

O projeto demonstra a implementação de uma arquitetura distribuída moderna com autenticação segura, testes automatizados e separação clara de responsabilidades, servindo como base sólida para evolução.