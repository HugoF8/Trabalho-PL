from ply import yacc
from cql_lexer import CQLLexer


# Árvore Sintática Abstrata
class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class ImportTableNode(ASTNode):
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

class ExportTableNode(ASTNode):
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

class DiscardTableNode(ASTNode):
    def __init__(self, name):
        self.name = name

class RenameTableNode(ASTNode):
    def __init__(self, old, new):
        self.old = old
        self.new = new

class PrintTableNode(ASTNode):
    def __init__(self, name):
        self.name = name

class SelectNode(ASTNode):
    def __init__(self, columns, table, where, limit):
        self.columns = columns
        self.table = table
        self.where = where
        self.limit = limit

class ConditionNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class LimitNode(ASTNode):
    def __init__(self, count):
        self.count = count

class CreateTableNode(ASTNode):
    def __init__(self, name, source):
        self.name = name
        self.source = source

class JoinTableNode(ASTNode):
    def __init__(self, left, right, column):
        self.left = left
        self.right = right
        self.column = column

class ProcedureNode(ASTNode):
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

class CallProcedureNode(ASTNode):
    def __init__(self, name):
        self.name = name


# Gramática
class CQLGrammar:
    tokens = CQLLexer.tokens

    def __init__(self):
        self.lexer = CQLLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

    # Programa
    def p_program(self, p):
        "program : statements"
        p[0] = ProgramNode(p[1])

    def p_statements(self, p):
        """statements : statements statement
                      | statement"""
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    # Statements
    def p_statement_import(self, p):
        "statement : IMPORT TABLE IDENTIFIER FROM STRING SEMICOLON"
        p[0] = ImportTableNode(p[3], p[5])

    def p_statement_export(self, p):
        "statement : EXPORT TABLE IDENTIFIER AS STRING SEMICOLON"
        p[0] = ExportTableNode(p[3], p[5])

    def p_statement_discard(self, p):
        "statement : DISCARD TABLE IDENTIFIER SEMICOLON"
        p[0] = DiscardTableNode(p[3])

    def p_statement_rename(self, p):
        "statement : RENAME TABLE IDENTIFIER IDENTIFIER SEMICOLON"
        p[0] = RenameTableNode(p[3], p[4])

    def p_statement_print(self, p):
        "statement : PRINT TABLE IDENTIFIER SEMICOLON"
        p[0] = PrintTableNode(p[3])

    def p_statement_select(self, p):
        "statement : SELECT select_columns FROM IDENTIFIER where_clause limit_clause SEMICOLON"
        p[0] = SelectNode(p[2], p[4], p[5], p[6])

    def p_select_columns_asterisk(self, p):
        "select_columns : ASTERISK"
        p[0] = ['*']

    def p_select_columns_list(self, p):
        "select_columns : column_list"
        p[0] = p[1]

    def p_column_list(self, p):
        """column_list : IDENTIFIER
                       | column_list COMMA IDENTIFIER"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_where_clause(self, p):
        """where_clause : WHERE condition
                        | empty"""
        p[0] = p[2] if p[1] else None

    def p_condition(self, p):
        """condition : IDENTIFIER EQUALS value
                     | IDENTIFIER NOTEQUAL value
                     | IDENTIFIER GT value
                     | IDENTIFIER LT value
                     | IDENTIFIER GE value
                     | IDENTIFIER LE value
                     | condition AND condition"""
        if len(p) == 4 and isinstance(p[2], str):
            p[0] = ConditionNode(p[1], p[2], p[3])
        else:
            p[0] = ConditionNode(p[1], 'AND', p[3])

    def p_limit_clause(self, p):
        """limit_clause : LIMIT NUMBER
                        | empty"""
        p[0] = LimitNode(p[2]) if len(p) == 3 else None

    def p_value(self, p):
        """value : NUMBER
                 | STRING"""
        p[0] = p[1]

    def p_statement_create(self, p):
        """
        statement : CREATE TABLE IDENTIFIER select_source SEMICOLON
                  | CREATE TABLE IDENTIFIER SELECT select_columns FROM IDENTIFIER where_clause limit_clause SEMICOLON
        """
        # Se for a forma com SELECT inline
        if len(p) > 5 and p[4] == 'SELECT':
            cols   = p[5]
            table  = p[7]
            where  = p[8]
            limit  = p[9]
            p[0] = CreateTableNode(p[3], SelectNode(cols, table, where, limit))
        else:
            # Forma antiga: CREATE TABLE nome FROM ... (ou JOIN ...)
            p[0] = CreateTableNode(p[3], p[4])

    def p_select_source(self, p):
        """select_source : FROM IDENTIFIER
                         | FROM IDENTIFIER JOIN IDENTIFIER USING LPAREN IDENTIFIER RPAREN"""
        if len(p) == 3:
            p[0] = p[2]
        else:
            p[0] = JoinTableNode(p[2], p[4], p[7])

    def p_statement_procedure(self, p):
        """statement : PROCEDURE IDENTIFIER DO statements END
                  | PROCEDURE IDENTIFIER DO statements END SEMICOLON"""
        p[0] = ProcedureNode(p[2], p[4])

    def p_statement_call(self, p):
        "statement : CALL IDENTIFIER SEMICOLON"
        p[0] = CallProcedureNode(p[2])

    def p_empty(self, p):
        "empty :"
        p[0] = None

    def p_error(self, p):
        if p:
            raise SyntaxError(f"Sintaxe inválida: token {p.value!r} (tipo {p.type}) na linha {p.lineno}")
        else:
            raise SyntaxError("Sintaxe inválida no ficheiro")

    def parse(self, text):
        return self.parser.parse(text, lexer=self.lexer.lexer)


def create_parser():
    return CQLGrammar()
