from parser import parser

command = 'create -name->adios.txt -path->../archivos/ -body->"Ya me voy ajio ajio\n"'

#parser.testLexer(command)
parser.interpretCommand(command)