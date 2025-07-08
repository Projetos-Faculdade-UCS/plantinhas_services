# 📚 Documentação Completa do Backend - Plantinhas Services

## 1. **Tecnologias Utilizadas**

### **Framework Principal**
- **Django 5.2.1** - Framework web Python utilizado em todos os microserviços
- **Django REST Framework 3.16.0** - Para criação de APIs RESTful
- **Python 3.x** - Linguagem de programação principal

### **Banco de Dados**
- **PostgreSQL 17 Alpine** - Banco de dados relacional principal
- **psycopg2-binary 2.9.10** - Driver PostgreSQL para Python
- **Padrão Database per Service** - Cada microserviço possui seu próprio banco

### **Autenticação e Autorização**
- **JWT (JSON Web Tokens)** com algoritmo **RS256**
- **djangorestframework-simplejwt 5.5.0** - Para geração e validação de tokens JWT
- **jwcrypto 1.5.6** - Para manipulação de chaves criptográficas
- **Google OAuth2** - Para autenticação social com Google
- **google-auth 2.38.0** - Biblioteca para validação de tokens Google

### **Infraestrutura e Deploy**
- **Docker & Docker Compose** - Para orquestração dos serviços
- **Gunicorn 23.0.0** - Servidor WSGI para produção
- **Nginx** - Proxy reverso (configurado nos deployments)

### **Bibliotecas Auxiliares**
- **django-cors-headers 4.7.0** - Para configuração de CORS
- **django-environ 0.12.0** - Para gerenciamento de variáveis de ambiente
- **django-filter 25.1** - Para filtros avançados nas APIs
- **django-storages 1.14.6** - Para armazenamento de arquivos
- **Pillow 11.2.1** - Para manipulação de imagens
- **sentry-sdk 2.28.0** - Para monitoramento de erros
- **djangorestframework-camel-case 1.4.2** - Para conversão de nomenclatura
- **drf-standardized-errors 0.14.1** - Para padronização de erros

### **Biblioteca de Autenticação Compartilhada**
- **plantinhas_auth_lib** - Biblioteca interna para autenticação entre serviços

---

## 2. **Estrutura dos Microserviços**

### **🔐 Auth Service (Porta 8001)**
- **Responsabilidade**: Autenticação, autorização e gerenciamento de usuários
- **Banco**: `auth_db` (PostgreSQL - Porta 5431)
- **Principais entidades**: User, GoogleOAuth
- **Tipo**: Stateless (tokens JWT)

### **🌿 Catálogo Service (Porta 8002)**
- **Responsabilidade**: Gerenciamento do catálogo de plantas e categorias
- **Banco**: `catalogo_db` (PostgreSQL - Porta 5432)  
- **Principais entidades**: Planta, Categoria, SubCategoria, SugestaoPlanta
- **Tipo**: Stateless

### **🎯 Habilidades Service (Porta 8003)**
- **Responsabilidade**: Controle de XP, níveis e progressão dos usuários
- **Banco**: `habilidades_db` (PostgreSQL - Porta 5433)
- **Principais entidades**: Habilidade, HabilidadeUser
- **Tipo**: Stateful (mantém estado de progressão)

### **🌱 Plantios Service (Porta 8004)**
- **Responsabilidade**: Gerenciamento de ciclos de plantio e problemas
- **Banco**: `plantios_db` (PostgreSQL - Porta 5434)
- **Principais entidades**: Plantio, Problema
- **Tipo**: Stateful (acompanha ciclo de vida dos plantios)

### **📚 Tutoriais & Tarefas Service (Porta 8005)**
- **Responsabilidade**: Gerenciamento de tutoriais e tarefas periódicas
- **Banco**: `tutoriais_tarefas_db` (PostgreSQL - Porta 5435)
- **Principais entidades**: Tarefa, TarefaHabilidade, CronFrequencia
- **Tipo**: Stateful (gerencia agendamentos)

---

## 3. **Estrutura de Pastas**

Todos os microserviços seguem uma estrutura padrão Django organizada em camadas:

```
<serviço>/
├── apps/                    # Aplicações Django
│   ├── core/               # Funcionalidades centrais
│   └── <dominio>/          # Lógica específica do domínio
│       ├── api/            # Endpoints da API
│       │   ├── serializers.py
│       │   └── views.py
│       ├── models.py       # Modelos de dados
│       ├── services.py     # Lógica de negócio
│       └── tests/          # Testes unitários
├── common/                 # Código compartilhado
│   ├── constants.py
│   ├── generics.py
│   ├── helpers.py
│   ├── mixins.py
│   ├── models.py
│   └── serializers.py
├── config/                 # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements/           # Dependências
│   ├── common.txt
│   ├── local.txt
│   └── production.txt
├── docker-compose.yml      # Orquestração local
├── Dockerfile.dev          # Imagem para desenvolvimento
└── manage.py              # CLI do Django
```

### **Camadas de Arquitetura**

1. **API Layer** (`api/`): Endpoints REST, serializers, validações
2. **Service Layer** (services.py): Lógica de negócio, integrações
3. **Model Layer** (models.py): Modelos de dados, relacionamentos
4. **Common Layer** (`common/`): Código reutilizável entre apps

---

## 4. **Sincronização entre Bancos de Dados**

### **Padrão Database per Service**
- Cada microserviço possui seu **banco PostgreSQL independente**
- **Isolamento total** de dados entre serviços
- **Autonomia** para evoluir esquemas independentemente

### **Sincronização via Referências Externas**
Os serviços **não fazem JOIN** entre bancos. Instead, utilizam **referências por ID**:

```python
# Exemplo no serviço Plantios
class Plantio(models.Model):
    planta_id = models.IntegerField()    # Referência ao Catálogo
    user_id = models.IntegerField()      # Referência ao Auth
    # ... outros campos
```

### **Integrações Síncronas**
- **Autenticação**: Via JWT tokens validados em tempo real
- **Consultas**: Chamadas HTTP entre serviços quando necessário
- **Validação**: Verificação de existência via APIs

### **Consistência Eventual**
- **Sem transações distribuídas** (evita complexidade)
- **Tolerância a falhas** através de retry e circuit breaker
- **Reconciliação** via background jobs quando necessário

---

## 5. **Autenticação e Autorização**

### **🔐 Serviço de Autenticação Central**
O serviço **Auth** é responsável por:
- Geração e validação de tokens JWT
- Gerenciamento de usuários
- Autenticação social (Google OAuth2)
- Fornecimento de chaves públicas JWKS

### **🗝️ Tokens JWT (RS256)**
```json
{
  "user_id": 123,
  "exp": 1641234567,
  "token_type": "access",
  "jti": "abc123..."
}
```

**Configuração JWT:**
- **Algoritmo**: RS256 (chave assimétrica)
- **Access Token**: 60 minutos
- **Refresh Token**: 1 dia
- **Chave Privada**: Apenas no Auth Service
- **Chave Pública**: Distribuída via JWKS endpoint

### **🔑 Processo de Autenticação**

#### **1. Login Admin (username/password)**
```http
POST /auth/api/v1/login/
{
  "username": "admin",
  "password": "senha123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
  "exp": 1641234567
}
```

#### **2. Autenticação Google OAuth2**
```http
POST /auth/api/v1/google/
Authorization: Bearer <google_id_token>
```

**Processo:**
1. Cliente envia token Google ID
2. Auth Service valida token com Google
3. Cria/atualiza usuário baseado nos dados do Google
4. Retorna tokens JWT próprios

### **🛡️ Validação de Tokens pelos Serviços**

Cada serviço valida tokens JWT através da biblioteca **plantinhas_auth_lib**:

```python
# Configuração nos settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "plantinhas_auth_lib.authenticators.PlantinhasAuthenticator",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

### **🔄 Refresh Token**
```http
POST /auth/api/token/refresh/
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9..."
}
```

### **🌐 Autenticação Social Google**

**Provedores Implementados:**
- **Google OAuth2** via `google-auth` library

**Fluxo de Autenticação:**
1. Frontend obtém `id_token` do Google
2. Envia token para `/auth/api/v1/google/`
3. Auth Service valida token com Google APIs
4. Extrai dados do usuário (email, nome, foto)
5. Cria/atualiza usuário no banco local
6. Retorna tokens JWT próprios

**Mapeamento de Dados:**
```python
{
    "user_id": google_sub,
    "email": google_email,
    "name": google_name,
    "picture": google_picture,
    "given_name": google_given_name,
    "family_name": google_family_name
}
```

### **📍 Endpoint JWKS**
```http
GET /auth/.well-known/jwks.json
```

Retorna chave pública para validação de tokens pelos outros serviços.

---

## 6. **Arquitetura Geral**

### **🏗️ Padrão de Arquitetura**
**Microserviços com Communication Pattern síncrono**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Load Balancer │
│   (SPA/Mobile)  │◄──►│   (Nginx)       │◄──►│   (Opcional)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
            ┌───────▼───┐   ┌───▼───┐   ┌───▼───┐
            │   Auth    │   │Catálogo│   │Habilid│
            │ :8001     │   │ :8002  │   │ :8003 │
            │           │   │        │   │       │
            └─────┬─────┘   └───┬────┘   └───┬───┘
                  │             │            │
            ┌─────▼─────┐ ┌─────▼─────┐ ┌────▼────┐
            │ auth_db   │ │catalogo_db│ │habilid_db│
            │ :5431     │ │ :5432     │ │ :5433   │
            └───────────┘ └───────────┘ └─────────┘

            ┌───────────┐   ┌─────────────┐
            │ Plantios  │   │Tutoriais    │
            │ :8004     │   │Tarefas :8005│
            └─────┬─────┘   └─────┬───────┘
                  │               │
            ┌─────▼─────┐   ┌─────▼─────┐
            │plantios_db│   │tutoriais_db│
            │ :5434     │   │ :5435     │
            └───────────┘   └───────────┘
```

### **🔀 Fluxo de Requisições**

1. **Cliente** → **API Gateway (Nginx)** → **Microserviço específico**
2. **Token JWT** validado por cada serviço independentemente
3. **Consultas entre serviços** via HTTP quando necessário
4. **Rede compartilhada** `shared-network` para comunicação interna

### **📊 Comunicação entre Serviços**

**Exemplo de integração típica:**
```python
# Serviço Plantios consultando Catálogo
def criar_plantio(planta_id, user_id):
    # 1. Validar se planta existe no catálogo
    planta = catalogo_service.get_planta(planta_id)
    
    # 2. Criar plantio local
    plantio = Plantio.objects.create(
        planta_id=planta_id,
        user_id=user_id,
        # ... outros campos
    )
    
    # 3. Notificar serviço de habilidades (opcional)
    habilidades_service.add_xp(user_id, 'plantio', 10)
    
    return plantio
```

### **🛡️ Características de Resiliência**

1. **Isolamento de Falhas**: Falha em um serviço não afeta outros
2. **Tolerância a Falhas**: Circuit breaker pattern implementado
3. **Escalabilidade Horizontal**: Cada serviço pode escalar independentemente
4. **Database per Service**: Evita gargalos de banco compartilhado

### **🔄 Estratégias de Deploy**

**Desenvolvimento (Docker Compose):**
```bash
# Inicia todos os serviços
docker-compose up -d

# Serviços disponíveis:
# - auth:8001
# - catalogo:8002  
# - habilidades:8003
# - plantios:8004
# - tutoriais_tarefas:8005
```

**Produção (Kubernetes/Docker Swarm):**
- Cada serviço como deployment independente
- Services para descoberta de serviços
- Ingress para roteamento externo
- Persistent Volumes para bancos de dados

---

## 7. **Observabilidade e Monitoramento**

### **📊 Logs**
- **Structured Logging** em todos os serviços
- **Centralized Logging** via Sentry
- **Request/Response Logging** para auditoria

### **🔍 Monitoramento de Erros**
- **Sentry SDK** integrado em todos os serviços
- **Error Tracking** em tempo real
- **Performance Monitoring** de requests

### **❤️ Health Checks**
- **Django Health Check** endpoint `/health/`
- **Database Connectivity** verificada
- **Service Dependencies** monitoradas

### **📈 Métricas**
- **Response Times** por endpoint
- **Error Rates** por serviço
- **Database Connection Pool** status
- **JWT Token Validation** metrics

---

## 🎯 **Resumo da Arquitetura**

A plataforma Plantinhas utiliza uma **arquitetura de microserviços moderna** com:

✅ **Separação clara de responsabilidades** entre serviços
✅ **Autenticação centralizada** com JWT e OAuth2
✅ **Database per Service** para isolamento de dados
✅ **Comunicação síncrona** via HTTP/REST
✅ **Containerização** com Docker para portabilidade
✅ **Monitoramento integrado** com Sentry
✅ **Escalabilidade horizontal** independente por serviço

Esta arquitetura garante **alta disponibilidade**, **fácil manutenção** e **capacidade de evolução** independente de cada componente do sistema.

Similar code found with 1 license type