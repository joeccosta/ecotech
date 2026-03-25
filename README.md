# Ecotech: Plataforma de Gestão de Pedidos de Vestuário Sustentável

![users-service](https://github.com/joeccosta/ecotech/actions/workflows/ci-users.yml/badge.svg?branch=main)
![orders-service](https://github.com/joeccosta/ecotech/actions/workflows/ci-orders.yml/badge.svg?branch=main)
![shell](https://github.com/joeccosta/ecotech/actions/workflows/ci-shell.yml/badge.svg?branch=main)
![orders-mfe](https://github.com/joeccosta/ecotech/actions/workflows/ci-orders-mfe.yml/badge.svg?branch=main)
![login-mfe](https://github.com/joeccosta/ecotech/actions/workflows/ci-login-mfe.yml/badge.svg?branch=main)


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
[ login-mfe :8501 ]
        |
        ↓
[ Shell (single-spa) :9000 ]
        |
        |--- orders-mfe :8500
        |
        ↓
[ orders-service :8002 ] ----> [ PostgreSQL orders_db ]
        |
        └-------------------> [ MongoDB ecotech_logs ]
        |
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
- filtro por ID do pedido (query param `order_id`)
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
- filtros por status e ID do pedido
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

### 5.1 Autenticação no Frontend (Microfrontends)

Além da validação no backend, o frontend implementa **controle de acesso por token (JWT)** para impedir navegação direta às rotas dos microfrontends.

#### Estratégia adotada

- o token JWT é armazenado no `localStorage` após login
- cada MFE verifica localmente se o usuário está autenticado
- em caso negativo, ocorre redirecionamento para o `login-mfe`

#### Proteções implementadas

- bloqueio de acesso direto ao `shell` (`:9000`) (pendente)
- bloqueio de acesso direto ao `orders-mfe` (`:8500`)
- redirecionamento automático para login quando não autenticado
- redirecionamento para o shell quando o usuário já está autenticado

#### Responsabilidade por camada

- **Frontend (MFE):** controle de navegação e experiência do usuário
- **Backend (services):** validação real de segurança via JWT (401 Unauthorized)

Essa abordagem segue o princípio de **defesa em profundidade**, combinando validação visual no frontend com proteção efetiva no backend.

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
- MongoDB (logs estruturados)

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

## 7.1 Variáveis de Ambiente (.env)

O projeto utiliza um arquivo `.env` na raiz para configuração dos serviços.

### Banco de dados

```
USERS_DB_NAME=users_db
USERS_DB_USER=...
USERS_DB_PASSWORD=...

ORDERS_DB_NAME=orders_db
ORDERS_DB_USER=...
ORDERS_DB_PASSWORD=...
```

### Autenticação (JWT)

```
SECRET_KEY=ecotech-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Observações

- `SECRET_KEY` deve ser **idêntica em todos os serviços**
- `ALGORITHM` deve ser consistente (ex: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` define o tempo de expiração do token

Sem esse alinhamento, a validação do JWT entre microsserviços falhará (erro 401).

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
- listagem de pedidos (200)
- atualização de status
- validação de payload (422)


---

## 8.1 Integração Contínua (CI)

O projeto utiliza GitHub Actions para execução automática de testes a cada `push` ou `pull request` na branch principal.

![users-service](https://github.com/joeccosta/ecotech/actions/workflows/ci-users.yml/badge.svg?branch=main)
![orders-service](https://github.com/joeccosta/ecotech/actions/workflows/ci-orders.yml/badge.svg?branch=main)
![shell](https://github.com/joeccosta/ecotech/actions/workflows/ci-shell.yml/badge.svg?branch=main)
![orders-mfe](https://github.com/joeccosta/ecotech/actions/workflows/ci-orders-mfe.yml/badge.svg?branch=main)
![login-mfe](https://github.com/joeccosta/ecotech/actions/workflows/ci-login-mfe.yml/badge.svg?branch=main)
### Pipeline

- execução de testes do `users-service`
- execução de testes do `orders-service`
- validação do ambiente via Docker
- pipelines independentes para cada serviço (`users-service`, `orders-service`)
- pipelines independentes para cada microfrontend (`shell`, `orders-mfe`, `login-mfe`)
- execução automática de testes a cada `push` ou `pull request`

### Benefícios

- garantia de integridade do código a cada alteração
- detecção precoce de falhas
- padronização do processo de build e teste

### Status

O status da pipeline pode ser acompanhado pelo badge no topo deste documento.

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

## 9.1 Logs Estruturados (MongoDB)

O projeto implementa logs estruturados persistidos em MongoDB como camada complementar ao banco relacional.

### Objetivo

- registrar eventos de negócio e técnicos
- permitir rastreabilidade de requisições
- facilitar debugging e observabilidade

### Arquitetura

```
[ orders-service ] ---> [ MongoDB (ecotech_logs.logs) ]
```

### Implementação

- handler customizado (`mongo_logger.py`)
- integração com o sistema de logging padrão do Python
- inserção automática de documentos no MongoDB via `emit()`

### Estrutura do log

Exemplo de documento armazenado:

```json
{
  "timestamp": "2026-03-24T15:50:00Z",
  "level": "INFO",
  "service": "orders-service",
  "event": "orders_listed",
  "message": "orders_listed",
  "request_id": "uuid",
  "status_filter": "pending",
  "order_id_filter": 12,
  "result_count": 120
}
```

### Variáveis de ambiente

```
MONGO_URI=mongodb://logs-mongo:27017
MONGO_DB_NAME=ecotech_logs
```

### Debug opcional

Para inspecionar logs durante desenvolvimento:

```
DEBUG_MONGO_LOGGER=true
```

Isso imprime no console o documento antes da inserção.

### Benefícios

- separação entre dados transacionais e observabilidade
- suporte a análise posterior (logs históricos)
- base para evolução com tracing e métricas

---

## 10. Próximos Passos

- centralizar autenticação em um módulo compartilhado entre MFEs
- implementar ProtectedRoute reutilizável
- adicionar logout global no shell com contexto de usuário
- persistir informações do usuário (ex: nome) no frontend
- implementar refresh token e controle de expiração
- considerar uso de armazenamento seguro (ex: httpOnly cookies)
- integração completa do login no frontend
- API Gateway / BFF
- logs estruturados
- observabilidade (tracing)
- uso de chave pública (RS256)
- testes no frontend

---

## 11. Status do Projeto

### Entregas concluídas

- backend funcional com `users-service` e `orders-service`
- autenticação JWT entre serviços, com rotas protegidas e validação local do token
- testes automatizados no backend cobrindo autenticação, validações e atualização de status
- integração validada via Postman e frontend
- ambiente dockerizado reproduzível com serviços isolados
- persistência de logs estruturados no MongoDB para o `orders-service`
- pipeline de CI com GitHub Actions validando automaticamente os testes dos microsserviços

### Funcionalidades já implementadas

- criação, listagem e filtros de pedidos (status e ID)
- atualização de status de pedidos
- cadastro e login de usuários
- propagação de autenticação entre microsserviços
- logging estruturado no console e no MongoDB
- proteção de rotas no frontend com verificação de autenticação (JWT) e redirecionamento automático

### Estado atual da arquitetura

- microsserviços com bancos PostgreSQL separados
- microfrontend `orders-mfe` integrado ao `orders-service`
- shell com `single-spa` para orquestração do frontend
- MongoDB como camada complementar de observabilidade

### Próxima evolução natural

- integrar completamente o fluxo de login ao frontend
- replicar a persistência de logs estruturados no `users-service`
- ampliar observabilidade com tracing e correlação entre serviços

---

## 12. Conclusão

O projeto demonstra a implementação de uma arquitetura distribuída moderna com autenticação segura, testes automatizados e separação clara de responsabilidades, servindo como base sólida para evolução.