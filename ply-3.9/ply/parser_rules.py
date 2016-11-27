from lexer_rules import tokens
from expressions import *

def p_pointarray(subexpr):
    'array_declaration : LBRACE point_list RBRACE'
    point_list = subexpressions[8]

def p_point_list_empty(subexpressions):
    'point_list :'
    subexpressions[0] = {"size": 0}


def p_point_list_non_empty(subexpressions):
    'point_list : point_list_non_empty' 
    subexpressions[0] = subexpressions[1]


def p_point_list_one(subexpressions):
    'point_list_non_empty : point'
    point_token = subexpressions[1]
    subexpressions[0] = {"size": 1, "type": point_token["type"]}


def p_point_list_append(subexpressions):
    'point_list_non_empty : point_list_non_empty COMMA point'
    point_token = subexpressions[3]
    sub_point_list = subexpressions[1]
    if sub_point_list["type"] != point_token["type"]:
        raise SemanticException("Incompatible type.")
    subexpressions[0] = {"size": sub_point_list["size"] + 1, "type": point_token["type"]}
    
def p_point(subexpressions):
	'poin_declaration: LPAREN INTEGER COMMA INTEGER RPAREN'
	#creo que estas verificaciones son al pedo
	first_point_token = subexpressions[1]
	second_point_token = subexpressions[3]
	if first_point_token["type"] != "int":
        raise SemanticException("Incompatible point type")
	if second_point_token["type"] != "int":
        raise SemanticException("Incompatible point type")

    subexpressions[0] = {"type": "point"}

#falta poder ponerle otro orden 
def p_size(size):
	'size_declaration: SIZE HEIGHT num COMMA WIDTH num' 
	first_num = subexpressions[2]
	second_num = subexpressions[5]
	if first_num["type"] != "int" && first_num["type"] != "float":
		raise SemanticException("Incompatible HEIGHT type")
	if second_num["type"] != "int" && second_num["type"] != "float":
		raise SemanticException("Incompatible WIDTH type")
	
	subexpressions[0] = {"type": "size"}

def p_rectangle(subexpressions):
	'rectangle_declaration: RECTANGLE UPPER_LEFT point COMMA HEIGHT num COMMA WIDTH num'
	point = subexpressions[2]
	first_num = subexpressions[5]
	second_num = subexpressions[8]
	if point["type"] != "point":
		raise SemanticException("Incompatible UPPER_LEFT type")
	if first_num["type"] != "int" && first_num["type"] != "float":
		raise SemanticException("Incompatible HEIGHT type")
	if second_num["type"] != "int" && second_num["type"] != "float":
		raise SemanticException("Incompatible WIDTH type")

	subexpressions[0] = {"type": "rectangle"}


def p_line(subexpressions):
	'line_declaration: LINE FROM point COMMA TO point'
	first_point = subexpressions[2]
	second_point = subexpressions[5]
	if first_point["type"] != "point":
		raise SemanticException("Incompatible FROM type")
	if second_point["type"] != "point":
		raise SemanticException("Incompatible TO type")

	subexpressions[0] = {"type": "line"}


def p_circle(subexpressions):
	'circle_declaration: CIRCLE CENTER point COMMA RADIUS num'
	point = subexpressions[2]
	number = subexpressions[5]
	if point["type"] != "point":
		raise SemanticException("Incompatible CENTER type")
	if number["type"] != "int" && number["type"] != "float":
		raise SemanticException("Incompatible RADIUS type")

	subexpressions[0] = {"type": "circle"}


def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
