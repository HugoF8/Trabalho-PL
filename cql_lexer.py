# cql_lexer.py

import ply.lex as lex
import re

class CQLLexer:
    """Analisador léxico para a linguagem CQL (Comma Query Language)."""

    # Lista de nomes de tokens
    tokens = [
        'IDENTIFIER',
        'STRING',
        'NUMBER',
        'SEMICOLON',
        'COMMA',
        'LPAREN',
        'RPAREN',
        'ASTERISK',
        'EQUALS',
        'NOTEQUAL',
        'GT',
        'LT',
        'GE',
        'LE',
        'DOT',
        'AND',
    ]

    # Lista de palavras reservadas
    reserved = {
        'import': 'IMPORT',
        'export': 'EXPORT',
        'table': 'TABLE',
        'from': 'FROM',
        'as': 'AS',
        'call': 'CALL',
        'discard': 'DISCARD',
        'rename': 'RENAME',
        'print': 'PRINT',
        'select': 'SELECT',
        'where': 'WHERE',
        'limit': 'LIMIT',
        'create': 'CREATE',
        'join': 'JOIN',
        'using': 'USING',
        'procedure': 'PROCEDURE',
        'do': 'DO',
        'end': 'END',
    }

    # Junta os tokens das palavras reservadas
    tokens = tokens + list(reserved.values())

    # Definições de expressões regulares para tokens
    t_SEMICOLON = r';'
    t_COMMA     = r','
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_ASTERISK  = r'\*'
    t_EQUALS    = r'='
    t_NOTEQUAL  = r'<>'
    t_GT        = r'>'
    t_LT        = r'<'
    t_GE        = r'>='
    t_LE        = r'<='
    t_DOT       = r'\.'
    t_AND       = r'[Aa][Nn][Dd]'

    # Ignora espaços em branco e tabs
    t_ignore = ' \t\n'

    def t_COMMENT(self, t):
        r'--.*|{\-[\s\S]*?\-}'
        pass

    def t_STRING(self, t):
        r'\"([^\\\"]|(\\.))*\"'
        t.value = t.value[1:-1]
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def t_IDENTIFIER(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        t.type = self.reserved.get(t.value.lower(), 'IDENTIFIER')
        return t

    def t_error(self, t):
        raise SyntaxError(f"Illegal character {t.value[0]!r}")

    def build(self, **kwargs):
        """Cria o lexer com base neste módulo."""
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    def input(self, data):
        self.lexer.input(data)

    def get_tokens(self, data):
        """Retorna a lista de tokens para uma string de entrada."""
        self.input(data)
        toks = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            toks.append(tok)
        return toks


def create_lexer():
    return CQLLexer().build()


def test_lexer():
    data = """
    -- Comentário de linha
    IMPORT TABLE estacoes FROM "estacoes.csv";
    SELECT * FROM observacoes WHERE Temperatura > 22;
    {- Comentário
       multilinha -}
    """
    lex = create_lexer()
    for tok in lex.input(data) or []:
        print(tok)


if __name__ == "__main__":
    test_lexer()
