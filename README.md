# Ecotech: Plataforma de Gestão de Pedidos de vestuário Ecofriendly

## 1. Contexto do Problema

Uma empresa de e-commerce de vestuário esportivo sustentável (Ecotech) enfrenta dificuldades operacionais ao gerenciar pedidos por meio de planilhas.

Esse processo apresenta limitações importantes:
- ausência de atualização em tempo real
- alta propensão a erros manuais
- dificuldade de rastreamento do status dos pedidos
- baixa escalabilidade

Este projeto propõe um Produto Mínimo Viável (PMV) para resolver esse problema utilizando uma arquitetura moderna baseada em **microsserviços** no backend e **microfrontends** no frontend.

---

## 2. Arquitetura da Solução

A solução foi projetada com separação clara de responsabilidades e baixo acoplamento entre componentes.

### 2.1 Visão Geral

```
[ Shell (single-spa) :9000 ]
        |
        |--- orders-mfe :8500
        |
        ↓
[ orders-service :8002 ] ----> [ PostgreSQL orders_db ]
[ users-service  :8001 ] ----> [ PostgreSQL users_db ]
```

---

## 3. Backend (Microsserviços)

A aplicação backend é composta por serviços independentes, cada um responsável por um domínio específico.

### 3.1 orders-service
Responsável pela gestão de pedidos:
- criação de pedidos
- listagem de pedidos
- filtro por status
- atualização de status

### 3.2 users-service
Responsável pela gestão de usuários:
- criação de usuários
- listagem de usuários
- consulta por ID

### 3.3 Persistência
Cada serviço possui seu próprio banco de dados PostgreSQL:
- isolamento de dados
- independência entre serviços
- alinhamento com boas práticas de microsserviços

---

## 4. Frontend (Microfrontends)

O frontend utiliza arquitetura de microfrontends com **single-spa**.

### 4.1 Shell (Root Config)
- responsável por orquestrar os MFEs
- gerencia rotas e composição
- não contém lógica de negócio

### 4.2 orders-mfe
- listagem de pedidos
- filtro por status
- criação de pedidos
- atualização de status
- integração direta com o orders-service

---

## 5. Tecnologias Utilizadas

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pytest

### Frontend
- React
- single-spa
- TypeScript

### Infraestrutura
- Docker
- Docker Compose

---

## 6. Como Executar o Projeto

Na raiz do projeto:

```bash
docker compose up --build
```

### Acessos

- Shell (frontend): http://localhost:9000
- Orders API (docs): http://localhost:8002/docs
- Users API (docs): http://localhost:8001/docs

---

## 7. Funcionalidades Implementadas

- Criação de pedidos
- Listagem de pedidos
- Filtro por status
- Atualização de status
- Criação e listagem de usuários
- Testes automatizados no backend

---

## 8. Decisões Técnicas

### FastAPI
Escolhido por:
- rapidez no desenvolvimento
- tipagem forte com Pydantic
- documentação automática via Swagger

### Microfrontends com single-spa
- composição em runtime
- independência entre equipes
- possibilidade de deploy isolado

### Bancos separados por serviço
- evita acoplamento
- aumenta a resiliência
- permite evolução independente

### Docker Compose
- simplifica execução local
- reproduz ambiente completo com um único comando

---

## 9. Qualidade e Testes

- Testes automatizados com Pytest
- Cobertura dos principais endpoints do orders-service
- Validação de cenários de erro (status inválido, recurso inexistente)

---

## 10. Próximos Passos (Evoluções Possíveis)

- Autenticação JWT compartilhada
- API Gateway / BFF
- Comunicação assíncrona (RabbitMQ ou Kafka)
- Observabilidade (logs estruturados, tracing)
- Cache com Redis
- Testes no frontend

---

## 11. Considerações Finais

Este projeto demonstra a construção de um sistema distribuído com separação clara de responsabilidades, integração entre frontend e backend e uso de práticas modernas de desenvolvimento.

O foco foi a entrega de um PMV funcional, priorizando clareza arquitetural, simplicidade e capacidade de evolução.