# Plano de fontes e métricas

## Princípio

O projeto não procura replicar websites generalistas.

O objetivo é combinar dados de várias origens para construir métricas próprias,
testar hipóteses e estudar aspetos pouco observados do desempenho do Benfica.

## Fontes atuais

### FBref

Utilização:

- remates a favor
- remates contra
- remates enquadrados
- métricas de eficácia de remate
- dados de guarda-redes
- posse
- formação
- formação adversária
- capitão
- árbitro
- contexto competitivo

Método atual:

- exportação manual através de Share & Export
- importação e limpeza automáticas em R
- atualização após cada jogo

Limitações:

- acesso automático bloqueado em alguns pedidos
- sem API oficial usada neste projeto
- sem exportação estável da sequência cronológica dos golos por jogo
- cobertura variável conforme a tabela e a competição

### football-data.org

Utilização:

- calendário
- resultados
- jornadas
- adversários
- casa e fora
- plantel base
- dados pessoais básicos dos jogadores

Limitações:

- sem estatísticas detalhadas de jogo no plano gratuito
- sem alinhamentos e substituições no plano gratuito
- sem xG
- sem eventos

### Auditoria manual

Utilização:

- pertença real ao plantel
- reforços
- datas de chegada
- clubes anteriores
- posições detalhadas
- situações incertas
- equipa que marcou primeiro
- minuto do primeiro golo
- sequência cronológica dos golos, quando necessária

## Fontes a testar

### ClubElo

Objetivo:

- força do adversário antes de cada jogo
- dificuldade ajustada do calendário
- contextualização de resultados

### StatsBomb Open Data

Objetivo:

- desenvolver modelos experimentais
- testar métricas com dados de eventos
- estudar sequências, pressão, progressão e redes
- validar métodos antes da aplicação ao Benfica

### Fontes públicas pós-jogo

Objetivo:

- onze inicial
- substituições
- minutos
- remates
- posse
- cantos
- cartões
- xG quando disponível

## Blind spots prioritários

1. Familiaridade do onze
2. Continuidade por setor
3. Custo temporário de integração dos reforços
4. Dependência estrutural de jogadores
5. Efeito real das substituições
6. Capacidade de controlar vantagens
7. Volatilidade do desempenho
8. Resultado versus processo
9. Impacto do descanso e sequência de jogos
10. Diferença entre rotação numérica e rotação funcional

## Regra metodológica

Cada indicador deverá incluir:

- definição
- fórmula
- fonte dos dados
- pressupostos
- limitações
- versão do modelo

### FBref

Utilização:

- remates a favor
- remates contra
- remates enquadrados
- métricas de eficácia de remate
- dados de guarda-redes
- posse
- formação
- formação adversária
- capitão
- árbitro
- contexto competitivo

Método atual:

- exportação manual através de Share & Export
- importação e limpeza automáticas em R
- atualização após cada jogo

Limitações:

- acesso automático bloqueado em alguns pedidos
- sem API oficial usada neste projeto
- sem exportação estável da sequência cronológica dos golos por jogo
- sem tabela Goal and Shot Creation disponível para o Benfica nesta época
- cobertura variável conforme a tabela e a competição

## Resultado real versus desfecho sugerido pelo xG

### Objetivo

Identificar jogos em que o resultado final divergiu da categoria de resultado sugerida pela diferença de xG.

### Fonte

- xG do Sofascore
- resultado final da tabela canónica
- validação possível através do FotMob

### Fórmula

`diferença de xG = xG Benfica - xG adversário`

### Classificação provisória do xG

- diferença superior a `+0,25`: vitória sugerida pelo xG
- diferença entre `-0,25` e `+0,25`: empate sugerido pelo xG
- diferença inferior a `-0,25`: derrota sugerida pelo xG

### Variáveis produzidas

- `xg_result`
- `actual_result_points`
- `xg_result_points`
- `result_performance_gap`
- `result_xg_class`

### Interpretação

A métrica compara o resultado real com uma categoria derivada exclusivamente da diferença de xG.

Não representa uma avaliação completa do desempenho, porque não considera:

- evolução temporal do jogo
- estado do marcador
- qualidade do adversário
- expulsões
- contexto competitivo
- distribuição dos remates
- momento em que o xG foi produzido
- estratégia depois de obter vantagem

### Limitações

- limiar de `0,25` é uma decisão metodológica provisória
- pequenas alterações no limiar podem mudar a categoria de alguns jogos
- xG é um modelo probabilístico e não um resultado esperado determinístico
- a diferença de xG não distingue domínio constante de produção concentrada num curto período

### Estado

- versão: `v0.1`
- cobertura: 34 jogos da Liga Portugal 2025/26
- implementação: `python/calculate_result_performance_gap.py`
- saída: `data/processed/benfica_2025_26_result_performance_gap.csv`