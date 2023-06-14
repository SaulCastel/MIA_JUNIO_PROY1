from .ply.lex import lex, TOKEN
from .ply.yacc import yacc
from commands import *
from re import IGNORECASE

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

id = r'([0-9a-zA-Z_]+)'

fileRegex = f'({id}[.]{id})'

string = r'("[^"]*")'

path = f'([/]({string}|{fileRegex}|{id}))+[/]?'

t_ignore = ' \t'

@TOKEN(path)
def t_PATH(t):
  t.value = t.value.replace('"','')
  return t

@TOKEN(fileRegex)
def t_FILE(t):
  return t

@TOKEN(id)
def t_ID(t):
  t.value = t.value.lower()
  t.type = reserved.get(t.value,'ID')
  return t

@TOKEN(string)
def t_STRING(t):
  return t

def t_newline(t):
  r'[\r\n]'
  t.lexer.lineno += 1

def t_error(t):
  print(f"Illegal character '{t.value}'")
  t.lexer.skip(1)

lexer = lex(reflags=IGNORECASE)

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
  log.updateLog(data=str(p[2]).strip('{}'),type='input',action=p[1])
  output = local.create(**p[2])
  log.updateLog(data=output,type='output',action=p[1])

def p_delete(p):
  'delete : DELETE params'
  log.updateLog(data=str(p[2]).strip('{}'),type='input',action=p[1])
  output = local.delete(**p[2])
  log.updateLog(data=output,type='output',action=p[1])

def p_copy(p):
  'copy : COPY params'
  #Llamar metodo

def p_transfer(p):
  'transfer : TRANSFER params'
  #Llamar metodo

def p_rename(p):
  'rename : RENAME params'
  log.updateLog(data=str(p[2]).strip('{}'),type='input',action=p[1])
  output = local.rename(**p[2])
  log.updateLog(data=output,type='output',action=p[1])

def p_modify(p):
  'modify : MODIFY params'
  log.updateLog(data=str(p[2]).strip('{}'),type='input',action=p[1])
  output = local.modify(**p[2])
  log.updateLog(data=output,type='output',action=p[1])

def p_add(p):
  'add : ADD params'
  log.updateLog(data=str(p[2]).strip('{}'),type='input',action=p[1])
  output = local.add(**p[2])
  log.updateLog(data=output,type='output',action=p[1])

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