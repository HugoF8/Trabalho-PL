Licenciatura em Engenharia de Sistemas Informáticos 2024-25 

# 📄 Trabalho de Processamento de Linguagens

Este projeto implementa um interpretador para a linguagem **CQL (Comma Query Language)**, uma linguagem simples de consulta e manipulação de dados tabulares em ficheiros `.csv`. O interpretador foi desenvolvido em **Python 3** com recurso à biblioteca **PLY** (Python Lex-Yacc).

---

## Grupo *21*
| Número | Nome             |
|--------|------------------|
| 26747  | Gonçalo Figueiredo |
| 25431  | Hugo Azevedo       |
| 25434  | Tiago Castro       |

---

## ⚙️ Requisitos

- Python 3.10 ou superior
- [PLY](https://www.dabeaz.com/ply/) (`pip install ply`)

---

## ✅ Funcionalidades Suportadas

A linguagem CQL permite a execução das seguintes instruções:

- `IMPORT TABLE nome FROM "ficheiro.csv";`
- `EXPORT TABLE nome AS "ficheiro.csv";`
- `DISCARD TABLE nome;`
- `RENAME TABLE antigo novo;`
- `PRINT TABLE nome;`
- `SELECT col1, col2 FROM tabela [WHERE condição] [LIMIT n];`
- `SELECT * FROM tabela;`
- `CREATE TABLE nome SELECT ...;` (com ou sem WHERE/LIMIT)
- `CREATE TABLE nome FROM tabela1 JOIN tabela2 USING(coluna);`
- `PROCEDURE nome DO ... END;`
- `CALL nome;`

---

## 📁 Estrutura do Projeto

```plaintext
Trabalho-PL/
├── main.py             # Ponto de entrada do interpretador
├── cql_lexer.py        # Analisador léxico da linguagem CQL (PLY)
├── cql_grammar.py      # Analisador sintático + AST (PLY)
├── cql_eval.py         # Avaliador semântico (interpretação da AST)
├── README.md           # Este ficheiro
│
├── input/              # Scripts CQL (.fca)
│   └── exemplo.fca     # Script de exemplo com todas as funcionalidades
│
├── data/               # Dados de entrada (.csv)
│   ├── estacoes.csv
│   └── observacoes.csv
│
└── saida/              # Ficheiros criados por EXPORT TABLE
    └── est.csv         # (exemplo exportado pela execução)



---

## 📌 Conclusão do Projeto

Este trabalho permitiu consolidar os conhecimentos de **análise léxica, sintática e semântica** no contexto de linguagens formais, através do desenvolvimento completo de um **interpretador funcional**.

O projeto cobre todos os requisitos propostos, incluindo:

- A definição de uma **gramática concreta** e geração da **AST**;
- A implementação de um **interpretador com suporte a queries, joins, procedimentos e manipulação de tabelas**;
- O suporte completo a **comentários de linha** (`-- ...`) e **comentários multilinha** (`{- ... -}`);
- A capacidade de importar e exportar dados reais de ficheiros `.csv`, e de realizar consultas condicionais e com limite de resultados.
