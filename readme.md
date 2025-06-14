Claro! Um bom `README.md` é a porta de entrada do seu projeto. Ele deve explicar o que o projeto faz, quais tecnologias usa e, mais importante, como executá-lo.

Criei um `README.md` completo e bem estruturado para o seu projeto. Você só precisa criar um arquivo chamado `README.md` na pasta raiz do seu projeto (`meu_projeto_completo/`) e colar o conteúdo abaixo.

---

# 📚 Sistema de Gerenciamento de Biblioteca com Docker

Este projeto consiste em um Sistema de Gerenciamento de Biblioteca completo, desenvolvido com Python/Flask e conteinerizado com Docker e Docker Compose. A aplicação permite cadastrar, listar, emprestar, devolver e excluir livros de um acervo, com todos os dados persistidos em um banco de dados PostgreSQL.

O ambiente é orquestrado para subir múltiplos serviços, incluindo a aplicação web, o banco de dados e ferramentas de administração, demonstrando uma arquitetura de microsserviços local.


*(Recomendação: Tire um screenshot da sua aplicação rodando e substitua o link acima pelo caminho da sua imagem)*

## ✨ Funcionalidades

-   **Cadastro de Livros**: Adicione novas obras ao acervo com título, autor e número de exemplares.
-   **Listagem do Acervo**: Visualize todos os livros disponíveis, com status de disponibilidade (disponível, poucos, esgotado).
-   **Empréstimo e Devolução**: Registre o empréstimo de um livro para um leitor e processe sua devolução.
-   **Exclusão de Livros**: Remova livros do acervo (com validação para não permitir a exclusão de livros emprestados).
-   **Interface Responsiva**: Layout moderno e funcional desenvolvido com **Tailwind CSS**.
-   **Persistência de Dados**: Os dados são armazenados de forma definitiva e não se perdem ao reiniciar os contêineres.

## 🛠️ Arquitetura e Tecnologias Utilizadas

O projeto utiliza uma arquitetura baseada em contêineres, orquestrada pelo `docker-compose.yml`, que define e conecta os seguintes serviços:

-   **`web` (Aplicação Principal)**:
    -   **Backend**: Python 3.9 com **Flask**
    -   **Servidor WSGI**: **Gunicorn**
    -   **Frontend**: HTML5, **Tailwind CSS**

-   **`db` (Banco de Dados)**:
    -   **SGBD**: **PostgreSQL 13**

-   **`adminer` (Gerenciador de Banco de Dados)**:
    -   Uma ferramenta leve para administração gráfica do banco de dados PostgreSQL.

-   **`portainer` (Gerenciador de Contêineres)**:
    -   Uma interface gráfica para gerenciar o ambiente Docker (contêineres, volumes, redes).

-   **Orquestração**:
    -   **Docker** e **Docker Compose**

## 🚀 Como Executar o Projeto

### Pré-requisitos

Antes de começar, certifique-se de que você tem o **Docker** e o **Docker Compose** instalados na sua máquina.

-   [Instalar Docker](https://docs.docker.com/get-docker/)
-   [Instalar Docker Compose](https://docs.docker.com/compose/install/) (geralmente já vem com o Docker Desktop).

### Passos para a Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/JoaoRicardoAlves/CloudC3.git
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd CloudC3
    ```

3.  **Suba os contêineres:**
    Execute o comando abaixo para construir as imagens e iniciar todos os serviços em segundo plano (`-d`).
    ```bash
    docker-compose up --build -d
    ```
    Aguarde um momento até que todos os serviços estejam em execução.

## 🌐 Acessando os Serviços

Após a execução do `docker-compose up`, os seguintes serviços estarão disponíveis:

#### 1. Sistema de Biblioteca
-   **URL**: [http://localhost:8080](http://localhost:8080)
-   **Descrição**: A aplicação principal onde você pode gerenciar os livros.

#### 2. Adminer (Gerenciador do Banco de Dados)
-   **URL**: [http://localhost:8081](http://localhost:8081)
-   **Descrição**: Para visualizar e gerenciar as tabelas `books` e `loans` diretamente.
-   **Credenciais de Login**:
    -   **Sistema**: `PostgreSQL`
    -   **Servidor**: `db`
    -   **Usuário**: `user`
    -   **Senha**: `password`
    -   **Banco de dados**: `mydatabase`

#### 3. Portainer (Gerenciador de Contêineres)
-   **URL**: [https://localhost:9443](https://localhost:9443)
-   **Descrição**: Para gerenciar de forma gráfica todos os contêineres do projeto.
-   **Primeiro Acesso**:
    1.  O navegador exibirá um aviso de segurança. Clique em "Avançado" e "Continuar para localhost".
    2.  Crie uma conta de administrador (usuário e senha).
    3.  Selecione o ambiente **Docker** local para gerenciar.

## ⚙️ Comandos Úteis do Docker Compose

-   **Verificar o status dos contêineres:**
    ```bash
    docker-compose ps
    ```

-   **Visualizar os logs de um serviço (ex: a aplicação web):**
    ```bash
    docker-compose logs -f web
    ```

-   **Parar e remover todos os contêineres:**
    ```bash
    docker-compose down
    ```

-   **Parar e remover contêineres E VOLUMES (apaga todos os dados):**
    Use este comando para uma limpeza completa e para recomeçar do zero.
    ```bash
    docker-compose down -v
    ```

## 📂 Estrutura do Projeto

```
.
├── app/                  # Contém todo o código da aplicação Flask
│   ├── app.py            # Lógica principal, rotas e conexão com o BD
│   ├── Dockerfile        # Instruções para construir a imagem da aplicação
│   ├── requirements.txt  # Dependências Python
│   └── templates/
│       └── index.html    # O template HTML da interface
├── docker-compose.yml    # Arquivo principal que orquestra todos os serviços
└── README.md             # Este arquivo
```

---

Feito por [João Ricardo Alves, Keven Leite](https://github.com/JoaoRicardoAlves).
