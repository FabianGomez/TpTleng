import ply.lex as lex

"""
Lista de tokens

El analizador léxico de PLY (al llamar al método lex.lex()) va a buscar
para cada uno de estos tokens una variable "t_TOKEN" en el módulo actual.

t_TOKEN puede ser:

- Una expresión regular
- Una función cuyo docstring sea una expresión regular (bizarro).

En el segundo caso, podemos hacer algunas cosas "extras", como quedarnos
con algún valor de ese elemento.

"""
tokens = [
#
'NUMBER', 'STRING','LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET','COMMA', 'EQUAL',
#inicios de funciones
    'SIZE','RECTANGLE','LINE','CIRCLE','ELLIPSE','POLYLINE','POLYGON','TEXT',
#parametros obligatorios
    'HEIGHT','WIDTH','ULEFT','FROM','CENTER','RADIUS','RX','RY','TO', 'T', 'AT', 'POINTS',

#parametros opcionales
'FFAMILY','FSIZE','FILL','STROKE','STRWIDTH'
    ]



def t_NUMBER(token):
    #primera parte es para integers y la segunda para floats
    r'\d+\.\d+|\d+'
    # Floats y integers son el mismo token. 
    if token.value.isdigit():
        number_value = int(token.value)
    else:
        number_value = float(token.value)
        
    number_type = "number"
    token.value = {"value": number_value, "type": number_type}
    return token

def t_STRING(token):
    r'\"([^\\\n]|(\\.))*\"'
    string_type = "string"
    #removemos las comillas obligatorias
    string_value = token.value[1:-1]
    token.value = {"value": string_value, "type": string_type}
    return token


t_POINTS           = r'points'
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_EQUAL            = r'='
t_COMMA            = r','

t_SIZE             = r'size '
t_RECTANGLE        = r'rectangle '
t_LINE             = r'line '
t_CIRCLE           = r'circle '
t_ELLIPSE          = r'ellipse '
t_POLYLINE         = r'polyline '
t_POLYGON          = r'polygon '
t_TEXT             = r'text '


t_HEIGHT           = r'height'
t_WIDTH            = r'width'
t_ULEFT            = r'upper_left'
t_FROM             = r'from'
t_CENTER           = r'center'
t_RADIUS           = r'radius'
t_RX               = r'rx'
t_RY               = r'ry'
t_TO               = r'to'
t_AT               = r'at'
t_T                = r't'

t_FFAMILY          = r'font-family'
t_FSIZE            = r'font-size'
t_FILL             = r'fill'
t_STROKE           = r'stroke'
t_STRWIDTH         = r'stroke-width'


def t_NEWLINE(token):
    r"\n+"
    token.lexer.lineno += len(token.value)
    
t_ignore = " \t"

def t_error(t):
    print("ERROR")
    pass

# Build the lexer
lexer = lex.lex()

def apply(string):
    u"""Aplica el análisis léxico al string dado."""
    lex.input(string)

    return list(lexer)
