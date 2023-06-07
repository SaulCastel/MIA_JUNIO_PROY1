from ply.lex import lex, TOKEN
from ply.yacc import yacc

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

tokens = ['ID','PATH','STRING'] + list(reserved.values())

literals = ['-','>']

id = r'[a-zA-Z_]+'

t_PATH = f'[.]?(/{id}?)+'

t_STRING = f'"[^"]*"'

t_ignore = ' \t'

@TOKEN(id)
def t_ID(t):
  t.type = reserved.get(t.value,'ID')
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += t.value.count("\n")

def t_error(t):
  print(f"Illegal charactaer '{t.value}'")
  t.lexer.skip(1)

lexer = lex()

def p_command(p):
  'command : configure'
  print('Analisis terminado sin problemas')

def p_configure(p):
  'configure : CONFIGURE params'
  print(p[1])
  print(p[2])
  #Llamar metodo configure con parametros obetenidos

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
              | STRING
              | PATH'''
  p[0] = p[1]

def p_error(p):
  print(f'Syntax error at {p.value}')

parser = yacc()

parser.parse("configure -type->local -encrypt_log->false -encrypt_read->false")