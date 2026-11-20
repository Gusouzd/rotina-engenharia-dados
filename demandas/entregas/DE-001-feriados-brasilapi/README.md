# DE-001 — Ingestão de feriados nacionais (BrasilAPI)

## Contexto
Analytics calcula dias úteis com planilha manual (já errou 2x). Ana (PM)
pediu uma tabela `dim_feriados` no PostgreSQL, alimentada por script, para
2025–2027, a partir de `https://brasilapi.com.br/api/feriados/v1/{ano}`.

## Critério de aceite
1. Script busca feriados de 2025, 2026 e 2027.
2. JSON bruto em `data/raw/feriados_{ano}.json`.
3. Tabela `dim_feriados` (PK `data`; `data`, `nome`, `tipo`, `ano`, `carregado_em`) no PostgreSQL via Docker Compose.
4. Idempotente (rodar 2x não duplica) — `ON CONFLICT DO UPDATE`.
5. Tratamento de erro (timeout, HTTP != 200, resposta vazia) + `logging` + retry com backoff (3 tentativas).
6. Validação antes de gravar (datas válidas, sem nulos, sem duplicatas); falhou = não grava o ano.
7. Credenciais via `.env`, fora do Git.
8. README final: subir banco, rodar, validar + query de conferência.
9. Teste pytest da função de validação.

Prazo: 20/11/2026.

## Contexto

A Ana necessitava de uma planilha com os feriados, pois estavam calculando os dias úteis nos relatórios de SLA, com uma planilha que era mantida a mão, e já saiu errada duas vezes. E necessitava de algo confiável direto no PostgreSQL.

## Stack utilizada

Python, pandas, SQLAlchemy, PostgreSQL (via Docker Compose), pytest

## Pré-requisitos
- Docker Desktop instalado e rodando
- Python 3.x instalado

## Como subir o ambiente

### 1. Clonar o repositório

git clone https://github.com/Gusouzd/rotina-engenharia-dados
cd rotina-engenharia-dados/demandas/entregas/DE-001-feriados-brasilapi

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=feriados_db

### 3. Subir o banco de dados (Docker Compose)

docker compose up -d

### 4. Instalar as dependências Python

pip install -r requirements.txt

## Como rodar o pipeline

python src/main.py

## Como validar que funcionou
Conecte no banco (via PgAdmin, DBeaver, ou `psql`) e rode:
```sql
SELECT COUNT(*) FROM dim_feriados;
```
É esperado 42 linhas no resultado desta query.

Pra confirmar a idempotência, rode o pipeline novamente — a contagem de linhas deve se manter igual, mas a coluna `carregado_em` das linhas deve ser atualizada.

## Como rodar os testes

pytest tests/

## Estrutura do projeto

├── src/
│   ├── capturar_feriados.py
│   ├── conectar_banco.py
│   ├── transformar.py
│   ├── validacao.py
│   ├── carregamento.py
│   └── main.py
├── tests/
│   └── test_validacao.py
├── data/raw/
├── docker-compose.yml
├── requirements.txt
├── README.md
├── venv/ (não versionado)
└── .env (não versionado)


## Decisões arquiteturais

1 - Como o pipeline é "tudo ou nada". Decidi limpar a pasta data/raw caso algum ano falhe. Ou seja, ou salva todos os JSONs, ou não salva nenhum.

2 - Mesmo o "ON CONFLICT" lidando com conflito de chave no banco, adicionei uma validação de duplicatas antes da carga. Isso garante que, se a API retornar duas vezes a mesma data no mesmo lote, o problema seja detectado e o pipeline interrompido, em vez de o ON CONFLICT silenciosamente absorver a inconsistência sem nenhum alerta.

3 - Resolvi colocar o que acontece com cada erro dentro do main.py para termos mais controle. Dentro das funções coloquei a maioria dos retornos como None, ou False, e só no main.py Coloco o return que irá pará-lo, e mostrar o motivo.