# 📚 Sistema de Gerenciamento de Biblioteca

## 🎓 Projeto Acadêmico - Professor Howard Roatti

### 👥 Equipe de Desenvolvimento
- **João Ricardo Alves**
- **Keven Leite Silva**
- **Maria Silva Santos**
- **Pedro Oliveira Costa**
- **Ana Paula Ferreira**

---

## 📋 Visão Geral do Projeto

Este projeto implementa um **Sistema de Gerenciamento de Biblioteca** completo, desenvolvido conforme as diretrizes específicas do edital do Professor Howard Roatti. O sistema simula uma interface real entre uma linguagem de programação e um Banco de Dados Relacional, executável em ambiente Linux.

### 🎯 Tema Escolhido
**Sistema de Gerenciamento de Livraria** - Controla livros, autores e pedidos, gerando relatórios de vendas por gênero e autor.

### 🛠️ Definições Técnicas
- **Banco de Dados**: PostgreSQL
- **Linguagem de Programação**: Python 3.x
- **Interface**: Console amigável com cores e formatação
- **⚠️ CONDIÇÃO CRÍTICA**: **PROIBIDO uso de ORM** - Todas as operações utilizam queries SQL manuais

---

## 🗄️ Estrutura do Banco de Dados

### 📊 Diagrama Relacional

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     AUTORES     │       │     LIVROS      │       │    PEDIDOS      │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id_autor (PK)   │◄──────┤ id_livro (PK)   │       │ id_pedido (PK)  │
│ nome_autor      │       │ titulo          │       │ data_pedido     │
│ nacionalidade   │       │ id_autor (FK)   │       │ nome_cliente    │
│ data_nascimento │       │ genero          │       │ email_cliente   │
│ biografia       │       │ ano_publicacao  │       │ valor_total     │
└─────────────────┘       │ preco           │       └─────────────────┘
                          │ quantidade_est. │                │
                          └─────────────────┘                │
                                   │                         │
                                   │                         │
                                   ▼                         ▼
                          ┌─────────────────────────────────────┐
                          │         ITENS_PEDIDO            │
                          ├─────────────────────────────────────┤
                          │ id_item (PK)                    │
                          │ id_pedido (FK) ─────────────────┤
                          │ id_livro (FK) ──────────────────┤
                          │ quantidade                      │
                          │ preco_unitario                  │
                          │ subtotal                        │
                          └─────────────────────────────────────┘
```

### 🔗 Relacionamentos
- **AUTORES** 1:N **LIVROS** (Um autor pode ter vários livros)
- **PEDIDOS** 1:N **ITENS_PEDIDO** (Um pedido pode ter vários itens)
- **LIVROS** 1:N **ITENS_PEDIDO** (Um livro pode estar em vários pedidos)

---

## ⚙️ Funcionalidades Implementadas

### 🖥️ Splash Screen (Tela de Inicialização)
- ✅ Nome da aplicação
- ✅ Nomes dos componentes do grupo
- ✅ Contagem de registros em todas as tabelas
- ✅ Status de conexão com o banco

### 🧭 Menu Principal
- ✅ **1. Relatórios**
- ✅ **2. Inserir Registros**
- ✅ **3. Remover Registros**
- ✅ **4. Atualizar Registros**
- ✅ **5. Sair**

### 📊 Relatórios
#### 1. Vendas por Gênero (GROUP BY)
```sql
SELECT 
    l.genero,
    COUNT(ip.id_item) as total_vendas,
    SUM(ip.quantidade) as quantidade_vendida,
    SUM(ip.subtotal) as valor_total_vendas
FROM livros l
INNER JOIN itens_pedido ip ON l.id_livro = ip.id_livro
GROUP BY l.genero
ORDER BY valor_total_vendas DESC
```

#### 2. Pedidos Detalhados (JOIN)
```sql
SELECT 
    p.id_pedido, p.data_pedido, p.nome_cliente,
    l.titulo, a.nome_autor, ip.quantidade,
    ip.preco_unitario, ip.subtotal
FROM pedidos p
INNER JOIN itens_pedido ip ON p.id_pedido = ip.id_pedido
INNER JOIN livros l ON ip.id_livro = l.id_livro
INNER JOIN autores a ON l.id_autor = a.id_autor
ORDER BY p.data_pedido DESC
```

### ➕ Inserir Registros
- ✅ **Autores**: Nome, nacionalidade, data nascimento, biografia
- ✅ **Livros**: Título, autor, gênero, ano, preço, estoque
- ✅ **Pedidos**: Cliente, email
- ✅ Validação de dados e relacionamentos
- ✅ Opção de inserir múltiplos registros

### ❌ Remover Registros
- ✅ Listagem de registros com ID e campo descritivo
- ✅ Seleção por ID
- ✅ Confirmação antes da remoção
- ✅ **Verificação de integridade referencial**:
  - Autor com livros não pode ser removido
  - Livro em pedidos não pode ser removido
  - Pedido remove itens automaticamente (CASCADE)

### ✏️ Atualizar Registros
- ✅ Listagem de registros existentes
- ✅ Seleção por ID
- ✅ Exibição dos dados atuais
- ✅ Entrada de novos dados (Enter mantém atual)
- ✅ Validação de relacionamentos
- ✅ Exibição do registro atualizado

---

## 🚀 Como Executar

### 📋 Pré-requisitos
- Python 3.x
- PostgreSQL
- Docker e Docker Compose (recomendado)

### 🔧 Instalação

1. **Clone o repositório**:
```bash
git clone <url-do-repositorio>
cd sistema-biblioteca
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Configure o banco de dados**:
```bash
# Usando Docker (recomendado)
docker-compose up -d

# Ou configure PostgreSQL manualmente e ajuste as variáveis em config/database.py
```

4. **Execute o sistema**:
```bash
python main.py
```

### 🌍 Variáveis de Ambiente
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydatabase
DB_USER=user
DB_PASSWORD=password
```

---

## 📁 Estrutura do Projeto

```
sistema-biblioteca/
├── main.py                 # Arquivo principal
├── requirements.txt        # Dependências Python
├── README_PROJETO.md       # Esta documentação
├── config/
│   └── database.py         # Configuração do banco
├── database/
│   └── schema.sql          # Script de criação das tabelas
├── models/
│   └── database_operations.py  # Operações CRUD sem ORM
├── views/
│   └── interface.py        # Interface do usuário
└── docker-compose.yml      # Configuração Docker
```

---

## 🔍 Exemplos de Queries SQL Utilizadas

### Inserção Manual (sem ORM)
```python
def inserir_autor(self, nome, nacionalidade, data_nascimento, biografia):
    query = """
        INSERT INTO autores (nome_autor, nacionalidade, data_nascimento, biografia)
        VALUES (%s, %s, %s, %s)
        RETURNING id_autor
    """
    cursor.execute(query, (nome, nacionalidade, data_nascimento, biografia))
```

### Consulta com JOIN
```python
def listar_livros(self):
    query = """
        SELECT l.id_livro, l.titulo, a.nome_autor, l.genero, l.preco, l.quantidade_estoque
        FROM livros l
        INNER JOIN autores a ON l.id_autor = a.id_autor
        ORDER BY l.titulo
    """
    cursor.execute(query)
```

### Verificação de Integridade
```python
def remover_autor(self, id_autor):
    # Verifica dependências antes de remover
    cursor.execute("SELECT COUNT(*) FROM livros WHERE id_autor = %s", (id_autor,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        return False, f"Não é possível remover. Autor possui {count} livro(s)."
```

---

## 🎨 Características da Interface

- **🌈 Cores e formatação** usando `colorama`
- **📊 Tabelas formatadas** com `tabulate`
- **🔄 Navegação intuitiva** com menus constantes
- **✅ Feedback visual** para operações
- **⚠️ Validação de entrada** com mensagens claras
- **🛡️ Tratamento de erros** robusto

---

## 📝 Conformidade com o Edital

### ✅ Requisitos Atendidos

- [x] **Simulação de interface real** entre linguagem e BD
- [x] **Executável em Linux**
- [x] **Interface amigável** (console com cores e formatação)
- [x] **PROIBIÇÃO DE ORM** - Apenas queries SQL manuais
- [x] **Mínimo 2 tabelas** com relacionamentos (4 tabelas implementadas)
- [x] **Diagrama relacional** com PKs, FKs e cardinalidades
- [x] **Script SQL** para criação das tabelas
- [x] **Splash screen** completo
- [x] **Menu principal** com todas as opções
- [x] **Relatórios** com GROUP BY e JOIN
- [x] **CRUD completo** para todas as entidades
- [x] **Verificação de integridade referencial**
- [x] **Confirmações** antes de operações destrutivas
- [x] **Contagem de registros** nas tabelas

### 🏆 Funcionalidades Extras Implementadas

- **🎨 Interface colorida** e profissional
- **📊 Tabelas formatadas** para melhor visualização
- **🔄 Navegação fluida** entre menus
- **💾 Dados de exemplo** pré-carregados
- **🐳 Containerização** com Docker
- **📚 Documentação completa**
- **🛡️ Tratamento robusto de erros**

---

## 👨‍🏫 Créditos Acadêmicos

**Professor**: Howard Roatti  
**Disciplina**: [Nome da Disciplina]  
**Instituição**: [Nome da Instituição]  
**Período**: 2024

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se o PostgreSQL está rodando
2. Confirme as credenciais de conexão
3. Execute `docker-compose up -d` para subir o ambiente
4. Verifique os logs com `docker-compose logs`

---

**🎯 Projeto desenvolvido com foco na excelência acadêmica e conformidade total com as diretrizes do edital.**