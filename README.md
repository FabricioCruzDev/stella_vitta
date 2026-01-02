# 💎 Sistema de Gestão de STELLA VITA (Atacado & Varejo)
Sistema para venda e gestão de estoque de semi-joias, desenvolvido com foco em performance e escalabilidade utilizando Python (FastAPI) e PostgreSQL.

🚀 Tecnologias Utilizadas
Linguagem: Python 3.12+

Gerenciador de Pacotes: UV (Astral)

Framework Web: FastAPI (Assíncrono)

Banco de Dados: PostgreSQL 16 (via Docker)

ORM: SQLAlchemy 2.0 (Modelagem declarativa)

Migrações: Alembic

Cache/Queue: Redis

Validação/Configuração: Pydantic V2 & Pydantic Settings

🏗️ Arquitetura do Banco de Dados
A modelagem foi desenhada para suportar variações de banho (Ouro, Prata, Ródio) e tabelas de preços distintas para Atacado e Varejo.

Principais Entidades:
Products: Nome, descrição e categoria.

Product Variants (SKU): Banho, peso, dimensões e estoque disponível.

Prices: Inteligência de preço baseada no tipo de cliente (Varejo/Atacado).

🛠️ Configuração do Ambiente
1. Requisitos Próximos
Docker e Docker Compose instalados.

UV (Gerenciador de pacotes Python).

2. Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto seguindo o modelo:

Snippet de código

# Banco de Dados
POSTGRES_USER=admin
POSTGRES_PASSWORD=sua_senha_secreta
POSTGRES_DB=joias_vendas
DATABASE_URL=postgresql+asyncpg://admin:sua_senha_secreta@localhost:5432/joias_vendas

# Segurança
SECRET_KEY=sua_chave_jwt_aleatoria
3. Executando o Projeto
Bash

# Subir Banco de Dados e Redis
docker compose up -d

# Instalar dependências
uv sync

# Rodar Migrações (Alembic)
uv run alembic upgrade head

# Iniciar Servidor de Desenvolvimento
uv run uvicorn app.main:app --reload
📅 Status do Cronograma (MVP)
[x] Semana 1: Setup de ambiente e Docker.

[x] Semana 1: Configuração de Segurança e .env.

[ ] Semana 2: Finalização dos Models e CRUD de Produtos.

[ ] Semana 3: Implementação de Autenticação JWT e RBAC.

🔒 Segurança e Boas Práticas
Pydantic Settings: Assegura que nenhuma credencial fique exposta no código fonte.

.gitignore: Configurado para ignorar .env, __pycache__ e diretórios de ambiente virtual.

Asyncpg: Driver assíncrono para garantir que o banco não seja um gargalo sob alta carga.