IMPORT TABLE jogadores FROM "jogadores.csv";
IMPORT TABLE estatisticas FROM "estatisticas.csv";

PRINT TABLE jogadores;
PRINT TABLE estatisticas;

SELECT Nome, Clube FROM jogadores WHERE Posicao = "Avançado";
SELECT * FROM estatisticas WHERE Golos > 20;

CREATE TABLE top_goleadores SELECT * FROM estatisticas WHERE Golos > 20;
PRINT TABLE top_goleadores;

CREATE TABLE resumo FROM jogadores JOIN estatisticas USING(Id);
PRINT TABLE resumo;

DISCARD TABLE jogadores;
DISCARD TABLE estatisticas;
DISCARD TABLE top_goleadores;
DISCARD TABLE resumo;