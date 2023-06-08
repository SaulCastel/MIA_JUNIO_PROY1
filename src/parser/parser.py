from .ply.lex import lex, TOKEN
from .ply.yacc import yacc
import commands

reserved = {
  'configure': 'CONFIGURE',
  'create': 'CREATE',
  'delete': 'DELETE',
  'copy': 'COPY',
  'transfer': 'TRANSFER',
  'rename': 'RENAME',
  'modify': 'MODIFY',
  'add': 'ADD',
  'backup': 'BACKUP',
  'exec': 'EXEC'
}

tokens = ['ID','PATH','STRING','FILE'] + list(reserved.values())

literals = ['-','>']

id = r'[0-9a-zA-Z_]+'

fileRegex = f'{id}[.]{id}'

path = f'([.]*\/({id})?)+'

t_STRING = r'"[^"]*"'

t_ignore = ' \t'

@TOKEN(path)
def t_PATH(t):
  return t

@TOKEN(fileRegex)
def t_FILE(t):
  return t

@TOKEN(id)
def t_ID(t):
  t.type = reserved.get(t.value,'ID')
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += t.value.count("\n")

def t_error(t):
  print(f"Illegal character '{t.value}'")
  t.lexer.skip(1)

lexer = lex()

def testLexer(data):
  lexer.input(data)
  
  for tok in lexer:
    print(tok)

def p_command(p):
  '''command  : configure
              | create
              | delete
              | copy
              | transfer
              | rename
              | modify
              | add
              | backup
              | exec'''

def p_configure(p):
  'configure : CONFIGURE params'
  #Llamar metodo

def p_create(p):
  'create : CREATE params'
  commands.create(**p[2])

def p_delete(p):
  'delete : DELETE params'
  #Llamar metodo

def p_copy(p):
  'copy : COPY params'
  #Llamar metodo

def p_transfer(p):
  'transfer : TRANSFER params'
  #Llamar metodo

def p_rename(p):
  'rename : RENAME params'
  #Llamar metodo

def p_modify(p):
  'modify : MODIFY params'
  #Llamar metodo

def p_add(p):
  'add : ADD params'
  #Llamar metodo

def p_backup(p):
  'backup : BACKUP params'
  #Llamar metodo

def p_exec(p):
  'exec : EXEC params'
  #Llamar metodo

def p_params(p):
  'params : params param'
  p[0] = {**p[1], **p[2]}

def p_simgle_param(p):
  'params : param'
  p[0] = p[1]

def p_param(p):
  'param : "-" ID "-" ">" argument'
  p[0] = {p[2]: p[5]}

def p_argument(p):
  '''argument : ID
              | PATH
              | FILE'''
  p[0] = p[1]

def p_argument_string(p):
  'argument : STRING'
  p[0] = p[1].strip('"')

def p_error(p):
  print(f'Syntax error at {p.value}')

parser = yacc()

def interpretCommand(command:str):
  parser.parse(command)