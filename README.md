# Plantinhas Services Monorepo

Este repositório monolítico (monorepo) reúne todos os microserviços que compõem a plataforma Plantinhas. Cada serviço é responsável por uma parte específica da aplicação, promovendo modularidade, escalabilidade e organização.

## Serviços Disponíveis

### 1. Auth
- **Diretório:** `auth/`
- **Descrição:** Serviço de autenticação, autorização e gerenciamento de usuários.
- **Principais entidades:** User

### 2. Catálogo de Plantas
- **Diretório:** `catalogo/`
- **Descrição:** Gerenciamento do catálogo de espécies de plantas, categorias e filtros de busca.
- **Principais entidades:** Planta, Categoria

### 3. Operações de Plantio
- **Diretório:** `plantios/`
- **Descrição:** Criação e rastreamento de ciclos de plantio, registro e tratamento de problemas nas plantações.
- **Principais entidades:** Plantio, Problema

### 4. Tutoriais & Tarefas
- **Diretório:** `tutoriais_tarefas/`
- **Descrição:** Gerenciamento de tutoriais de plantio, agendamento de tarefas periódicas e definição de requisitos de perícia.
- **Principais entidades:** TutorialPlantio, Tarefa, Pericia

### 5. Habilidades & Progressão
- **Diretório:** `habilidades/`
- **Descrição:** Controle de experiência (XP), níveis, habilidades e progressão dos usuários.
- **Principais entidades:** Habilidade, Pericia

---

Cada serviço possui seu próprio README detalhando suas funcionalidades, entidades e responsabilidades. Para mais informações sobre cada serviço, consulte o respectivo diretório.

> Este monorepo faz parte do ecossistema Plantinhas. Para dúvidas, sugestões ou contribuições, consulte a documentação técnica ou entre em contato com os mantenedores.
