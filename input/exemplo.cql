-- A. Configuração de tabelas de dados
IMPORT TABLE estacoes FROM "estacoes.csv";
IMPORT TABLE observacoes FROM "observacoes.csv";
PRINT TABLE estacoes;
PRINT TABLE observacoes;
EXPORT TABLE estacoes AS "est.csv";
RENAME TABLE estacoes est;
PRINT TABLE est;

-- B. Execução de queries sobre tabelas de dados
SELECT * FROM observacoes;
SELECT DataHoraObservacao, Id FROM observacoes;
SELECT * FROM observacoes WHERE Temperatura > 22;
SELECT * FROM observacoes WHERE Temperatura < 22 AND Radiacao > 600;
SELECT * FROM observacoes LIMIT 2;

-- C. Criação de novas tabelas de dados e -- D. procedimentos
CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 15;

PROCEDURE atualizar_observacoes DO
  CREATE TABLE completo FROM est JOIN observacoes USING(Id);
  PRINT TABLE completo;
END

CALL atualizar_observacoes;

-- Descartar Tabelas
DISCARD TABLE observacoes;
DISCARD TABLE est;
DISCARD TABLE completo;
DISCARD TABLE mais_quentes;

-- E. Comentários
{-
Os comentários apenas de uma linha são precedidos por -- (todo o texto seguinte é ignorado).
-}