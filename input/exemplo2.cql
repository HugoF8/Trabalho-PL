IMPORT TABLE jogadores FROM "jogadores.csv";
IMPORT TABLE estatisticas FROM "estatisticas.csv";
PRINT TABLE jogadores;
PRINT TABLE estatisticas;

SELECT Nome, Clube FROM jogadores WHERE Posicao = "Avançado";

CREATE TABLE top_goleadores SELECT * FROM estatisticas WHERE Golos > 20;
CREATE TABLE top_assistencias SELECT * FROM estatisticas WHERE Assistencias > 10;

PROCEDURE resumo_por_clube DO
    SELECT * FROM jogadores WHERE Idade > 30 AND Clube ="Inter Miami";
    CREATE TABLE completo FROM jogadores JOIN estatisticas USING(Id);
    PRINT TABLE completo;
END
CALL resumo_por_clube;

DISCARD TABLE jogadores;
DISCARD TABLE estatisticas;
DISCARD TABLE top_goleadores;
DISCARD TABLE top_assistencias;
