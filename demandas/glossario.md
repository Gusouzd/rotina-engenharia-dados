# Glossário

Termos já explicados pelo gestor. Quando um termo novo aparecer numa
demanda, ele é explicado uma vez em contexto e depois anotado aqui.

## Termos de time / empresa
<!-- ex: Sprint — período fixo de trabalho (aqui, X dias) onde o time entrega um conjunto de demandas -->
<!-- ex: SLA — prazo máximo combinado para resolver algo -->

## Termos técnicos de dados
<!-- ex: CDC (Change Data Capture) — técnica pra detectar o que mudou numa fonte de dados sem reprocessar tudo -->
<!-- ex: Upsert — operação que insere um registro novo ou atualiza se já existir -->

## Registrados na DE-001
- **Ticket (DE-00X)** — registro numérico de uma demanda, com contexto, critério de aceite e prazo; permite rastrear quem pediu o quê e quando.
- **PM (Product Manager)** — quem define prioridades e fala com o negócio; aqui, Ana.
- **Definition of Ready (DoR)** — checklist de que a demanda está clara o bastante pra começar (contexto, critério de aceite, prazo).
- **Definition of Done (DoD)** — checklist do que precisa estar pronto pra eu aprovar (erro tratado, dado validado, doc, teste).
- **SLA** — prazo máximo combinado pra entregar/resolver algo; aqui, sexta 20/11.
- **Sprint** — período fixo de trabalho (aqui, 2 semanas) em que o time se compromete com um conjunto de demandas.
- **Dimensão (dim_)** — tabela de apoio com atributos descritivos (ex: calendário de feriados), usada para enriquecer análises.
- **Idempotência** — rodar a mesma operação várias vezes dá o mesmo resultado que rodar uma; sem duplicar dados.
- **Upsert** — insere o registro se for novo, atualiza se já existir.
- **Backoff exponencial** — em retentativas, esperar mais a cada falha (1s, 2s, 4s…) para não sobrecarregar a fonte.
- **Dados brutos (raw)** — cópia fiel do que a fonte devolveu, guardada sem alteração, para poder reprocessar depois.
- **Ambiente virtual (venv)** — pasta isolada com o Python e as bibliotecas só deste projeto, para não misturar versões com outros projetos nem com o sistema.
- **requirements.txt** — lista das bibliotecas (e versões) que o projeto precisa; permite que qualquer pessoa ou servidor reproduza o mesmo ambiente com um comando.
- **Reprodutibilidade** — qualquer pessoa conseguir rodar o seu código do zero e obter o mesmo resultado, sem "na minha máquina funciona".
