import os 
import csv
from cql_grammar import *
from collections import OrderedDict

def carregar_csv(filename):
    # Se o caminho não for absoluto nem contiver uma subpasta, adiciona 'data/'
    if not os.path.isabs(filename) and not os.path.dirname(filename):
        filename = os.path.join("data", filename)
    try:
        with open(filename, encoding='utf-8') as f:
            lines = [
                l.strip() for l in f
                if l.strip() and not l.strip().startswith('--')
                       and not l.strip().startswith('{-')
            ]
        reader = csv.reader(lines)
        headers = next(reader)
        return [dict(zip(headers, row)) for row in reader]
    except Exception as e:
        print(f"Erro ao carregar o ficheiro CSV {filename}: {e}")
        return []

def salvar_csv(filename, data):
    if not data:
        print(f"{filename}: sem dados para guardar.")
        return

    if not os.path.isabs(filename) and not os.path.dirname(filename):
        filename = os.path.join("saida", filename)
    headers = list(data[0].keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data:
            writer.writerow([row.get(h, "") for h in headers])

def juntar_tabelas(t1, t2, col):
    result = []
    for r1 in t1:
        for r2 in t2:
            if r1.get(col) == r2.get(col):
                merged = OrderedDict(r1)
                merged.update(r2)
                result.append(dict(merged))
    return result

class Memory:
    def __init__(self):
        self.tables = {}
        self.procs = {}

    def store_table(self, name, data):
        self.tables[name] = data

    def get_table(self, name):
        return self.tables.get(name)

    def discard_table(self, name):
        return self.tables.pop(name, None) is not None

    def rename_table(self, old, new):
        if old in self.tables:
            self.tables[new] = self.tables.pop(old)
            return True
        return False

    def list_tables(self):
        return list(self.tables.keys())

    def store_proc(self, name, stmts):
        self.procs[name] = stmts

    def get_proc(self, name):
        return self.procs.get(name)

class Evaluator:
    def __init__(self, mem=None):
        self.mem = mem or Memory()

    def visit(self, node):
        method = f"visit_{type(node).__name__}"
        return getattr(self, method)(node)

    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_ImportTableNode(self, node):
        data = carregar_csv(node.filename)
        self.mem.store_table(node.name, data)
        print(f"Tabela '{node.name}' importada ({len(data)} linhas).")

    def visit_ExportTableNode(self, node):
        data = self.mem.get_table(node.name)
        salvar_csv(node.filename, data)
        print(f"Tabela '{node.name}' exportada para '{node.filename}'.")

    def visit_DiscardTableNode(self, node):
        ok = self.mem.discard_table(node.name)
        print("Descartada." if ok else "Não encontrada.")

    def visit_RenameTableNode(self, node):
        ok = self.mem.rename_table(node.old, node.new)
        print("Renomeada." if ok else "Falhou.")

    def visit_PrintTableNode(self, node):
        data = self.mem.get_table(node.name) or []
        self._print_result(data, f"Tabela: {node.name}")

    def visit_SelectNode(self, node):
        tbl = self.mem.get_table(node.table) or []
        rows = tbl
        if node.where:
            rows = [r for r in rows if self._check(r, node.where)]
        if node.columns != ['*']:
            rows = [ {c: r.get(c) for c in node.columns} for r in rows ]
        if node.limit:
            rows = rows[:node.limit.count]
        self._print_result(rows, f"SELECT de '{node.table}'")
        return rows

    def visit_CreateTableNode(self, node):
        src = node.source
        if isinstance(src, SelectNode):
            rows = self.visit(src)
        elif isinstance(src, JoinTableNode):
            left_tbl  = self.mem.get_table(src.left)  or []
            right_tbl = self.mem.get_table(src.right) or []
            rows = juntar_tabelas(left_tbl, right_tbl, src.column)
        else:
            rows = self.mem.get_table(src) or []
        self.mem.store_table(node.name, rows)
        print(f"Tabela '{node.name}' criada ({len(rows)} linhas).")

    def visit_ProcedureNode(self, node):
        self.mem.store_proc(node.name, node.statements)
        print(f"Procedimento '{node.name}' guardado.")

    def visit_CallProcedureNode(self, node):
        stmts = self.mem.get_proc(node.name) or []
        for s in stmts:
            self.visit(s)

    def _check(self, row, cond):
        lv = row.get(cond.left)
        rv = cond.right
        op = cond.op
        try:
            if op == '=':  return lv == rv
            if op == '<>': return lv != rv
            if op == '>':  return float(lv) > float(rv)
            if op == '<':  return float(lv) < float(rv)
            if op == '>=': return float(lv) >= float(rv)
            if op == '<=': return float(lv) <= float(rv)
            if op == 'AND':
                return self._check(row, cond.left) and self._check(row, cond.right)
        except:
            return False
        return False

    def _print_result(self, data, title="Resultado"):
        if not data:
            print(f"{title}: Sem resultados.")
            return
        columns = list(data[0].keys())
        header = " | ".join(columns)
        separator = "-" * len(header)
        print(f"\n{title}")
        print(separator)
        print(header)
        print(separator)
        for row in data:
            values = [str(row.get(c, "")) for c in columns]
            print(" | ".join(values))
        print(separator)
        print(f"Total: {len(data)} linhas\n")