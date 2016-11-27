tokens = [
#
'INTEGER', 'FLOAT', 'STRING','LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET','COMMA',
#inicios de funciones
    'SIZE','RECTANGLE','LINE','CIRCLE','POLYLINE','POLYGON','TEXT',
#parametros obligatorios
	'HEIGHT','WIDTH','UPPER_LEFT','FROM','TO','CENTER','RADIUS','RX','RY','TO','AT',

#parametros opcionales
	'FFAMILY','FSIZE','FILL','STROKE','STRWIDTH'
    ]



def t_INTEGER(token):
	r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
	number_type = "int"
    number_value = int(token.value)
	token.value = {"value": number_value, "type": number_type}
    return token


def t_FLOAT(token):
	r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'
	number_type = "float"
    number_value = float(token.value)
	token.value = {"value": number_value, "type": number_type}
    return token

def t_STRING(token):
	r'\"([^\\\n]|(\\.))*?\"'
	string_type = "string"
	string_value = token.value
	token.value = {"value": string_value, "type": string_type}
    return token


t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'

t_COMMA            = r','

t_FSIZE            = r'size '
t_RECTANGLE        = r'rectangle '
t_LINE             = r'line '
t_CIRCLE           = r'circle '
t_POLYLINE         = r'polyline '
t_POLYGON          = r'polygon '
t_TEXT             = r'text '


t_HEIGHT           = r'height:'
t_WIDTH            = r'width:'
t_UPPER_LEFT       = r'upper_left:'
t_FROM             = r'from:'
t_TO               = r'to:'
t_CENTER           = r'center:'
t_RADIUS           = r'radius:'
t_RX               = r'rx:'
t_RY               = r'ry:'
t_TO               = r'to:' 
t_AT               = r'at:'

t_FFAMILY          = r'font-family:'
t_FSIZE            = r'font-size:'
t_FILL             = r'fill'
t_STROKE           = r'stroke'
t_STRWIDTH         = r'stroke-width'


# Comment (C-Style)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

# Comment (C++-Style)
def t_CPPCOMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1
    return t

def t_NEWLINE(token):
    r"\n+"
    token.lexer.lineno += len(token.value)


def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
