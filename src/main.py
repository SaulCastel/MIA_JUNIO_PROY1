from parser import parser

command = 'cReate -naMe->adios.txt -pATh->/ -bOdy->"Ya me voy ajio ajio\n"'
command2 = 'delete -path->/ -name->adios.txt'

#parser.testLexer(command)
parser.interpretCommand(command)