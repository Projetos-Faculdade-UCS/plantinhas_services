---
mode: 'agent'
tools: ['codebase', 'githubRepo', 'runCommands', 'search']
description: 'Template para geração de Pull Requests seguindo convenções do projeto'
---

# 🚀 TEMPLATE PARA PULL REQUEST

Este template deve ser usado para gerar Pull Requests que seguem as convenções estabelecidas no projeto Plantinhas Services.

---

## 📋 FORMATO DO TÍTULO

O título deve seguir o padrão **Conventional Commits** com **gitmoji**:

```
<gitmoji> <tipo>(escopo): <descrição>
```

### Exemplos de títulos:
- `✨ feat(api): adiciona endpoints para gerenciamento de plantios`
- `🐛 fix(auth): corrige validação de tokens JWT`
- `📝 docs(readme): atualiza documentação dos microserviços`
- `♻️ refactor(serializers): melhora estrutura dos serializers`
- `🔧 chore(docker): atualiza configurações do Docker`

---

## 📝 ESTRUTURA DA DESCRIÇÃO

A descrição do PR deve incluir obrigatoriamente as seguintes seções:

### 🎯 **Resumo das Alterações**
Breve descrição do que foi implementado, corrigido ou melhorado.

### 📋 **Checklist de Alterações**
Liste todas as principais mudanças usando checkboxes:
- [x] Feature X implementada
- [x] Bug Y corrigido  
- [x] Documentação Z atualizada

### 🔧 **Microserviços Afetados**
Liste quais microserviços foram modificados:
- [ ] **Auth** - Autenticação e autorização
- [ ] **Catálogo** - Gerenciamento de plantas e categorias  
- [ ] **Plantios** - Operações de plantio e acompanhamento
- [ ] **Tutoriais & Tarefas** - Gestão de tutoriais e tarefas
- [ ] **Habilidades** - Sistema de progressão e XP
- [ ] **Docker/Config** - Configurações gerais

### 🧪 **Testes**
Descreva como as alterações foram testadas:
- [ ] Testes unitários executados
- [ ] Testes de integração validados
- [ ] Validação manual realizada
- [ ] Endpoints testados via Postman/Insomnia

### 📚 **Documentação**
- [ ] README.md atualizado (se necessário)
- [ ] Documentação da API atualizada
- [ ] Comentários no código adicionados

### ⚠️ **Breaking Changes**
Se houver mudanças que quebram compatibilidade:
- [ ] Não há breaking changes
- [ ] Breaking changes documentados abaixo

### 🔗 **Issues Relacionadas**
- Closes #123
- Fixes #456
- Related to #789

---

## 🎨 GITMOJIS RECOMENDADOS

| Emoji | Tipo | Descrição |
|-------|------|-----------|
| ✨ | feat | Nova funcionalidade |
| 🐛 | fix | Correção de bug |
| 📝 | docs | Documentação |
| 🔧 | chore | Tarefas de manutenção |
| ♻️ | refactor | Refatoração de código |
| 🎨 | style | Melhorias de formatação |
| ⚡ | perf | Melhorias de performance |
| 🧪 | test | Adição/correção de testes |
| 🔒 | security | Correções de segurança |
| 🚀 | deploy | Deploy e CI/CD |

---

## ✅ CRITÉRIOS PARA APROVAÇÃO

- [ ] Código segue os padrões estabelecidos
- [ ] Testes estão passando
- [ ] Documentação está atualizada
- [ ] Não há conflitos de merge
- [ ] Review aprovado por pelo menos 1 reviewer
- [ ] Pipeline de CI passou com sucesso

---

## 🔄 FLUXO DE DESENVOLVIMENTO

1. **Feature Branch** → **Develop** (PR de desenvolvimento)
2. **Develop** → **Main** (PR de release)

**Importante**: PRs para `main` devem consolidar múltiplas features e representar uma release estável.