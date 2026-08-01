# Dicionário da ficha pós-jogo

## Identificação

### match_id
Identificador do jogo na football-data.org.

### date
Data do jogo no formato AAAA-MM-DD.

### opponent
Nome do adversário conforme a base principal.

### venue
Local do jogo:

- Home
- Away

## Resultado

### goals_for
Golos marcados pelo Benfica.

### goals_against
Golos sofridos pelo Benfica.

## Posse

### possession_for
Percentagem de posse do Benfica, entre 0 e 100.

### possession_against
Percentagem de posse do adversário, entre 0 e 100.

A soma deverá ser aproximadamente 100.

## Remates

### shots_for
Total de remates do Benfica.

### shots_against
Total de remates do adversário.

### shots_on_target_for
Remates enquadrados do Benfica.

### shots_on_target_against
Remates enquadrados do adversário.

### shots_inside_box_for
Remates do Benfica dentro da área.

### shots_inside_box_against
Remates do adversário dentro da área.

## Qualidade das oportunidades

### big_chances_for
Grandes oportunidades atribuídas ao Benfica pela fonte escolhida.

### big_chances_against
Grandes oportunidades atribuídas ao adversário.

### xg_for
Golos esperados do Benfica.

### xg_against
Golos esperados do adversário.

O xG deve vir sempre da mesma fonte principal. Caso seja usada outra fonte, deve ser indicado em `data_source` ou `notes`.

## Bolas paradas

### corners_for
Cantos do Benfica.

### corners_against
Cantos do adversário.

## Composição da equipa

### lineup_changes
Número de alterações no onze inicial relativamente ao jogo anterior.

No primeiro jogo da época, deixar vazio.

### new_signings_starting
Número de reforços de 2026/27 no onze inicial.

### new_signings_minutes
Soma dos minutos jogados pelos reforços de 2026/27.

Exemplo:

- reforço A joga 90 minutos;
- reforço B joga 60 minutos;
- total = 150.

## Estado do resultado

### scored_first
Indica se o Benfica marcou o primeiro golo:

- TRUE
- FALSE

Num jogo 0-0, deixar vazio.

### minute_first_goal
Minuto do primeiro golo do jogo, independentemente da equipa.

Num jogo 0-0, deixar vazio.

## Expulsões

### red_card_for
Número de expulsões do Benfica.

### red_card_against
Número de expulsões do adversário.

## Proveniência e observações

### data_source
Fonte principal das estatísticas.

Exemplo:

- Sofascore
- FotMob
- UEFA
- Liga Portugal

### notes
Acontecimentos que possam distorcer a comparação:

- prolongamento;
- expulsão;
- lesão precoce;
- mudança tática;
- jogo interrompido;
- métricas divergentes entre fontes;
- valor estimado ou em falta.

## Regras gerais

- Nunca substituir um valor desconhecido por zero.
- Usar vazio para dados indisponíveis.
- Zero significa que a ocorrência foi medida e não aconteceu.
- Manter a mesma fonte principal sempre que possível.
- Registar mudanças de fonte.
- Não misturar xG de fornecedores diferentes sem identificação.
- Rever valores anómalos antes de os usar nos modelos.