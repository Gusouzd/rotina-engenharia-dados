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

## Como rodar
_(a preencher por Gustavo)_
