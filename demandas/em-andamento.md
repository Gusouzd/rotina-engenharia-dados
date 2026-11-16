# Demanda em andamento

## DE-001 — Ingestão de feriados nacionais (BrasilAPI) para a tabela `dim_feriados`
- Aberto em: 16/11/2026 | Prazo (SLA): sexta, 20/11/2026, fim do dia
- Nível: júnior (demanda guiada — onboarding)
- Solicitante: Ana (PM de dados) | Revisor: Rafael (Tech Lead)
- Status: aberto

### Contexto de negócio
A Equipe de Analytics precisa calcular "dias úteis" nos relatórios de SLA de
entrega e hoje faz isso com uma planilha de feriados mantida na mão (que já
saiu errada duas vezes). Ana quer que isso vire uma tabela confiável no
PostgreSQL, atualizada por um script, para os anos de 2025 a 2027.

Fonte: BrasilAPI — `GET https://brasilapi.com.br/api/feriados/v1/{ano}`
(pública, sem chave). Retorna lista de `{date, name, type}`.

### Critério de aceite (Definition of Ready / Done)
1. Script Python que busca os feriados de 2025, 2026 e 2027.
2. Dados brutos salvos em `data/raw/feriados_{ano}.json` (como vieram da API).
3. Tabela `dim_feriados` no PostgreSQL (via Docker Compose) com PK em `data`
   e colunas `data`, `nome`, `tipo`, `ano`, `carregado_em`.
4. **Idempotente**: rodar o script 2x seguidas não duplica nem quebra
   (use `INSERT ... ON CONFLICT DO UPDATE`).
5. Tratamento de erro: timeout, status HTTP != 200 e resposta vazia, com
   `logging` (nada de `print`). Retry com espera crescente (3 tentativas).
6. Validação antes de gravar: datas válidas, sem nulos, sem duplicata na
   resposta; se falhar, não grava nada daquele ano.
7. Credenciais do banco via `.env` (nada hardcoded; `.env` fora do Git).
8. README com: como subir o banco, como rodar, como validar. E ao menos
   uma query de conferência (ex: quantos feriados por ano).
9. Teste: pelo menos um teste automatizado da função de validação (pytest).

### Pontos de pesquisa (só o necessário)
- **Idempotência / upsert**: termo para buscar — "PostgreSQL INSERT ON
  CONFLICT DO UPDATE".
- **Retry com backoff exponencial**: pode implementar na mão com um loop —
  entender o conceito vale mais que usar biblioteca.
- Docs da BrasilAPI: https://brasilapi.com.br/docs (seção Feriados).

### Como entregar
Código em `demandas/entregas/DE-001-feriados-brasilapi/`. Me avise com um
resumo das decisões que tomou (por que X e não Y) — é isso que Rafael vai
perguntar na revisão.
