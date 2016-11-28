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
    point_token = subexpressions[2]
    sub_point_list = subexpressions[0]
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

def p_args_lambda(subexpressions):
	'args_declaration :'

def p_args_append(subexpressions):
	'args_declaration : args_declaration COMMA args'
	subexpressions[0] = subexpressions[0].update(subexpressions[2])

def p_args_terminal_height(subexpressions):
	'args_declaration : HEIGHT num'
	num = subexpressions[1]
	if num["type"] != "int" && num["type"] != "float":
		raise SemanticException("Incompatible HEIGHT type")

	subexpressions[0] = {"HEIGHT":True,"HEIGHT_value":num["value"]}

def p_args_terminal_width(subexpressions):
	'args_declaration : WIDTH num'
	num = subexpressions[1]

	if num["type"] != "int" && num["type"] != "float":
		raise SemanticException("Incompatible WIDTH type")

	subexpressions[0] = {"WIDTH":True,"WIDTH_value":num["value"]}

#def p_size(subexpressions):
#	'size_declaration: SIZE HEIGHT num COMMA WIDTH num' 
#	first_num = subexpressions[2]
#	second_num = subexpressions[5]
#	if first_num["type"] != "int" && first_num["type"] != "float":
#		raise SemanticException("Incompatible HEIGHT type")
#	if second_num["type"] != "int" && second_num["type"] != "float":
#		raise SemanticException("Incompatible WIDTH type")
	
#	subexpressions[0] = {"type": "size"}

#intento de curry
def p_size(subexpressions):
	'size_declaration: SIZE args args_extra' 
	args = subexpressions[1]
	if !(args.has_key["HEIGHT"] && args.has_key["WIDTH"]):
		raise SemanticException("Incopatible size args")
	if len(args) > 4
		raise SemanticException("Incopatible size args")
	
	subexpressions[0] = {"type": "size","size":True}


#def p_rectangle(subexpressions):
#	'rectangle_declaration: RECTANGLE UPPER_LEFT point COMMA HEIGHT num COMMA WIDTH num'
#	point = subexpressions[2]
#	first_num = subexpressions[5]
#	second_num = subexpressions[8]
#	if point["type"] != "point":
#		raise SemanticException("Incompatible UPPER_LEFT type")
#	if first_num["type"] != "int" && first_num["type"] != "float":
#		raise SemanticException("Incompatible HEIGHT type")
#	if second_num["type"] != "int" && second_num["type"] != "float":
#		raise SemanticException("Incompatible WIDTH type")

#	subexpressions[0] = {"type": "rectangle"}


def p_rectangle(subexpressions):
	'rectangle_declaration: RECTANGLE args args_extra'
	args = subexpressions[1]

	if !(args.has_key["UPPER_LEFT"] &&args.has_key["HEIGHT"] && args.has_key["WIDTH"]):
		raise SemanticException("Incopatible rectangle args")
	if len(args) > 6
		raise SemanticException("Incopatible rectangle args")

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
