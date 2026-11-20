# Demanda em andamento

## DE-001 — Ingestão de feriados nacionais (BrasilAPI) para a tabela `dim_feriados`
- Aberto em: 16/11/2026 | Prazo (SLA): sexta, 20/11/2026, fim do dia
- Nível: júnior (demanda guiada — onboarding)
- Solicitante: Ana (PM de dados) | Revisor: Rafael (Tech Lead)
- Status: em revisão — ajustes solicitados (20/11/2026)

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

### Revisão 1 — 20/11/2026 (gestor)
**Resultado: NÃO aprovado ainda — 4 ajustes obrigatórios, 3 recomendados.**
Verificado: pytest 4/4 ok; 14 feriados por ano = 42 linhas (bate com o README); `.env` e `venv/` fora do Git.

Obrigatórios:
1. Decisão 1 (tudo ou nada) só vale em um dos dois caminhos de falha. Em `capturar_feriados.py`, "falhou após 3 tentativas" limpa `data/raw`; "resposta vazia" retorna sem limpar. Além disso, apagar a pasta inteira destrói uma carga anterior boa por causa de uma falha pontual. Pense: como garantir "tudo ou nada" sem perder o que já estava lá?
2. `conectar_banco.py` ignora `POSTGRES_DB` do `.env` e fixa `feriados_db`, host e porta no código. Se o `.env` de alguém diferir, o compose cria um banco e o script conecta em outro.
3. Comentário do passo 4 em `main.py` diz que a validação de duplicatas é feita pelo ON CONFLICT — contradiz a sua decisão 2 e o `validacao.py`. Comentário errado é pior que nenhum.
4. README: o `git clone` + `cd` não funciona como escrito; `conftest.py` aparece na estrutura mas não existe; o bloco "Como rodar" do template ficou vazio acima do seu conteúdo; documente a porta 5433.

Recomendados (não bloqueiam, mas Rafael vai perguntar):
- Retry: dorme também depois da última tentativa (espera inútil), e repete até em 404/400, onde tentar de novo não adianta. Qual erro merece retry e qual não?
- `criar_conexao()` não conecta de verdade (`create_engine` é preguiçoso), então o "Pipeline abortado: falha na conexão" nunca dispara. Como você testaria a conexão cedo?
- `iterrows` + um `execute` por linha: ok com 42 linhas, mas procure como mandar o lote de uma vez.

Pontos fortes: decisão 2 bem fundamentada; pipeline em módulos; carga numa única transação; testes cobrindo os 3 casos de erro.

### Revisão 2 — 20/11/2026 (gestor)
**Resultado: quase aprovado — 2 pendências pequenas.** Os 4 obrigatórios e os 3 recomendados foram corrigidos (conferido no código, commit 2eb2d17): captura só grava depois de todos os anos validados; retry sem sleep inútil e sem repetir 4xx; `SELECT 1` no início; carga em lote; conexão via `.env`.

Pendências:
1. **Regressão silenciosa:** `carregamento.py` agora cria `carregado_em DATE` (antes era `TIMESTAMPTZ`). Reexecutar no mesmo dia não muda nada, então o teste de idempotência do README ("`carregado_em` deve ser atualizado") deixa de ser verificável. Além disso, `CREATE TABLE IF NOT EXISTS` não altera a tabela que já existe no seu volume Docker. Corrija e explique como lidou com a tabela existente.
2. **README desatualizado:** a decisão 1 ainda descreve "limpar `data/raw`", que não é mais o comportamento. O bloco "Contexto" está duplicado e o critério de aceite do template continua colado no topo.

Observação (não bloqueia): 429 (rate limit) é 4xx mas merece retry; vale pensar nisso. E `logging.basicConfig` aparece em 3 módulos — só o primeiro a rodar vale; configure só no `main.py`.
