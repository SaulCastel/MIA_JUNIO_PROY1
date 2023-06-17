from .ply.lex import lex, TOKEN
from .ply.yacc import yacc
from ..commands import *
from re import IGNORECASE

localState = {}

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
  localState['message'] = f'Error lexico en: <{t.value}>'
  t.lexer.skip(1)

lexer = lex(reflags=IGNORECASE)

def testLexer(data):
  lexer.input(data)
  
  for tok in lexer:
    print(tok)

def execCommand(command, params) -> str:
  if localState['configured']:
    try:
      return command(**params)
    except TypeError:
      return 'Parametro(s) invalido(s)'
  return 'El entorno no ha sido configurado'

def execLogging(result,p):
  log.updateLog(data=str(p[2]).strip('{}'),type='input',action=p[1],encrypt=localState['encrypt_log'])
  log.updateLog(data=result,type='output',action=p[1],encrypt=localState['encrypt_log'])
  localState['message'] = result

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
  result = ''
  try:
    localState.update(local.configure(**p[2]))
    result = 'Entorno configurado'
  except TypeError:
    result = 'Parametro(s) invalido(s)'
  except ValueError:
    result = 'Error en argumentos'
  execLogging(result, p)

def p_create(p):
  'create : CREATE params'
  if localState['type'] == 'local':
    execLogging(execCommand(local.create, p[2]), p)
  else:
    cloud = localState['cloud']
    execLogging(execCommand(cloud.create, p[2]), p)

def p_delete(p):
  'delete : DELETE params'
  if localState['type'] == 'local':
    execLogging(execCommand(local.delete, p[2]), p)
  else:
    cloud = localState['cloud']
    execLogging(execCommand(cloud.delete, p[2]), p)
  
def p_copy(p):
  'copy : COPY params'
  try:
    params = {
      'source': p[2]['from'],
      'dest': p[2]['to']
    }
  except KeyError:
    return execLogging('Parametro(s) invalido(s)', p)
  else:
    execLogging(execCommand(local.copy, params), p)

def p_transfer(p):
  'transfer : TRANSFER params'
  #Llamar metodo

def p_rename(p):
  'rename : RENAME params'
  if localState['type'] == 'local':
    execLogging(execCommand(local.rename, p[2]), p)
  else:
    cloud = localState['cloud']
    execLogging(execCommand(cloud.rename, p[2]), p)

def p_modify(p):
  'modify : MODIFY params'
  if localState['type'] == 'local':
    execLogging(execCommand(local.modify, p[2]), p)
  else:
    cloud = localState['cloud']
    execLogging(execCommand(cloud.modify, p[2]), p)

def p_add(p):
  'add : ADD params'
  execLogging(execCommand(local.add, p[2]), p)

def p_backup(p):
  'backup : BACKUP params'
  #Llamar metodo

def p_exec(p):
  'exec : EXEC params'
  globals()['localState'].update({'exec': True, 'exec_params': p[2]})

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
  if not p:
    localState['message'] = 'Comando invalido'
    return
  localState['message'] = f'Error de sintaxis en: <{p.value}>'

parser = yacc()

def interpretCommand(command:str, state:dict) -> dict:
  globals()['localState'] = state
  parser.parse(command)
  return localState