---
mode: 'agent'
tools: ['codebase', 'githubRepo', 'runCommands', 'search', 'searchResults', 'terminalLastCommand', 'usages']
description: 'Documentação completa do backend em português'
---
# 🧠 INSTRUCTIONS FOR COPILOT

You're going to generate **complete backend project documentation** in **Portuguese**.  
You must **thoroughly scan the entire codebase**, understanding the actual implementation to reflect real decisions and structure.

---

## 🔍 Your Mission

Generate documentation that explains the following **in detail and in Portuguese**:

---

### ✅ 1. **Tecnologias Utilizadas**
- Detalhe **quais tecnologias e linguagens foram usadas em cada microserviço** (ex: Node.js, FastAPI, Spring Boot, PostgreSQL, MongoDB, Redis, Kafka, etc.)
- Inclua bibliotecas relevantes (ex: Sequelize, Prisma, SQLAlchemy, JWT, Passport, etc.)
- Mencione ferramentas de orquestração e deploy utilizadas (ex: Docker, Kubernetes, etc.)

---

### ✅ 2. **Estrutura dos Microserviços**
- Liste todos os microserviços presentes no projeto.
- Explique o **papel de cada um** e sua **responsabilidade única**.
- Descreva se são stateless ou stateful.

---

### ✅ 3. **Estrutura de Pastas**
- Mostre a estrutura de pastas de cada microserviço, com foco em padrões como:
  - `controller/`, `service/`, `repository/`
  - ou `api/`, `domain/`, `infra/`, etc.
- Explique o propósito de cada camada/pasta e como elas se comunicam.

---

### ✅ 4. **Sincronização entre Bancos de Dados**
- Explique como cada microserviço gerencia seu banco.
- Se existe um banco por serviço (Database per Service pattern).
- Como os dados são sincronizados entre serviços:
  - via eventos assíncronos (Kafka, RabbitMQ, etc.)
  - ou chamadas diretas (REST, gRPC)
- Como foi resolvido o problema de consistência eventual.

---

### ✅ 5. **Autenticação e Autorização**
- Descreva como funciona a autenticação no sistema:
  - Há um `auth-service`?
  - Ele gera tokens JWT? Com que payload?
- Explique o processo de **validação de token pelos outros serviços**.
- Como funciona o **refresh token**?
- Detalhe o uso de OAuth2/OpenID Connect, se houver.
- Diferencie entre usuários internos (admin/sistemas) e externos (clientes/app).
- **Explique também como funciona a autenticação social** (Google, GitHub, etc.)
  - Quais provedores foram implementados
  - Como os dados do usuário social são mapeados/salvos no sistema

---

### ✅ 6. **Arquitetura Geral**
- Desenhe (ou descreva textualmente) a arquitetura de alto nível.
- Explique o fluxo de requisições, chamadas entre serviços, uso de mensageria/eventos.
- Mencione se há um API Gateway e qual sua função.
- Detalhe como a arquitetura garante escalabilidade, isolamento e resiliência.

---

### (Opcional) ✅ 7. Observabilidade e Monitoramento
- Como são tratados os logs?
- Se há tracing distribuído (ex: OpenTelemetry, Jaeger).
- Healthchecks, circuit breakers, dashboards.

---

## ❗ Output Requirements
- Return everything **in Portuguese**
- Use **títulos organizados e exemplos reais**
- Não invente tecnologias — use somente o que estiver realmente presente no código
- Seja **completo e técnico**, como se fosse para um time de devs experientes ou documentação oficial

---

### 🧠 Reminder

**Scan minuciosamente todo o código-fonte** antes de escrever qualquer coisa.  
A documentação deve refletir **exatamente o que foi implementado** no projeto.

