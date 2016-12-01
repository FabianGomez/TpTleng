from lexer_rules import tokens
from expressions import *

def p_pointarray(subexpr):
    'array_declaration : LBRACE point_list RBRACE'
    sub_point_list = subexpressions[2]
    subexpressions[0] = {"size": sub_point_list["size"] + 1, "type": point_token["type"] + 'list'}

def p_point_list_empty(subexpressions):
    'point_list :'
    subexpressions[0] = {"size": 0,"type": "point"}


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
	first_point_token = subexpressions[2]
	second_point_token = subexpressions[4]
	if first_point_token["type"] != "int":
        raise SemanticException("Incompatible point type")
	if second_point_token["type"] != "int":
        raise SemanticException("Incompatible point type")

    subexpressions[0] = {"type": "point"}


def p_args_lambda(subexpressions):
	'args :'
	subexpressions[0] = {}

def p_args_list(subexpressions):
	'args : args_list'
	subexpressions[0] = subexpressions[1]

def p_args_list_one(subexpressions):
	'args_list : args_declaration'
	subexpressions[0] = subexpressions[1]

def p_args_append(subexpressions):
	'args_list : args_list COMMA args_declaration'
	subexpressions[0] = subexpressions[1].update(subexpressions[3])

def p_args_terminal_height(subexpressions):
	'args_declaration : HEIGHT num'
	num = subexpressions[2]
	if num["type"] != "int" && num["type"] != "float":
		raise SemanticException("Incompatible HEIGHT type")

	subexpressions[0] = {"HEIGHT":True,"HEIGHT_value":num["value"]}

def p_args_terminal_width(subexpressions):
	'args_declaration : WIDTH num'
	num = subexpressions[2]

	if num["type"] != "int" && num["type"] != "float":
		raise SemanticException("Incompatible WIDTH type")

	subexpressions[0] = {"WIDTH":True,"WIDTH_value":num["value"]}

def p_args_terminal_upper(subexpressions):
	'args_declaration : UPPER_LEFT point'
	point = subexpressions[2]

	if point["type"] != "point":
		raise SemanticException("Incompatible UPPER_LEFT type")

	subexpressions[0] = {"UPPER_LEFT":True,"UPPER_LEFT_value":point["value"]}

def p_args_terminal_from(subexpressions):
	'args_declaration : FROM point'
	point = subexpressions[2]

	if point["type"] != "point":
		raise SemanticException("Incompatible FROM type")

	subexpressions[0] = {"FROM":True,"FROM_value":point["value"]}

def p_args_terminal_to(subexpressions):
	'args_declaration : TO point'
	point = subexpressions[2]

	if point["type"] != "point":
		raise SemanticException("Incompatible TO type")

	subexpressions[0] = {"TO":True,"TO_value":point["value"]}

def p_args_terminal_center(subexpressions):
	'args_declaration : CENTER point'
	point = subexpressions[2]

	if point["type"] != "point":
		raise SemanticException("Incompatible CENTER type")

	subexpressions[0] = {"CENTER":True,"CENTER_value":point["value"]}

def p_args_terminal_at(subexpressions):
	'args_declaration : AT point'
	point = subexpressions[2]

	if point["type"] != "point":
		raise SemanticException("Incompatible AT type")

	subexpressions[0] = {"AT":True,"AT_value":point["value"]}

def p_args_terminal_radius(subexpressions):
	'args_declaration : RADIUS num'
	num = subexpressions[2]

	if num["type"] != "int" && num["type"] != "float":
		raise SemanticException("Incompatible RADIUS type")

	subexpressions[0] = {"RADIUS":True,"RADIUS_value":num["value"]}

def p_args_terminal_rx(subexpressions):
	'args_declaration : RX num'
	num = subexpressions[2]

	if num["type"] != "int" && num["type"] != "float":
		raise SemanticException("Incompatible RX type")

	subexpressions[0] = {"RX":True,"RX_value":num["value"]}

def p_args_terminal_ry(subexpressions):
	'args_declaration : RY num'
	num = subexpressions[2]

	if num["type"] != "int" && num["type"] != "float":
		raise SemanticException("Incompatible RY type")

	subexpressions[0] = {"RY":True,"RY_value":num["value"]}

def p_args_terminal_points(subexpressions):
	'args_declaration : POINTS points'
	points = subexpressions[2]

	if points["type"] != "pointlist" :
		raise SemanticException("Incompatible POINTS type")

	subexpressions[0] = {"POINTS":True,"POINTS_value":points["value"]}

def p_args_terminal_t(subexpressions):
	'args_declaration : T STRING'
	string = subexpressions[2]
	subexpressions[0] = {"T":True,"T_value":string["value"]}


def p_args_terminal_font_family(subexpressions):
	'args_declaration : FFAMILY STRING'
	string = subexpressions[2]
	subexpressions[0] = {"FFAMILY":True,"FFAMILY_value":string["value"]}

def p_args_terminal_font_size(subexpressions):
	'args_declaration : FSIZE STRING'
	string = subexpressions[2]
	subexpressions[0] = {"FSIZE":True,"FSIZE_value":string["value"]}



def p_argsextra_lambda(subexpressions):
	'argsextra :'
	subexpressions[0] = {}

def p_argsextra_list(subexpressions):
	'argsextra : argsextra_list'
	subexpressions[0] = subexpressions[1]

def p_argsextra_list_one(subexpressions):
	'argsextra_list : argsextra_declaration'
	subexpressions[0] = subexpressions[1]

def p_argsextra_append(subexpressions):
	'argsextra_list : argsextra_list COMMA argsextra_declaration'
	listargs = subexpressions[1]
	argsE = subexpressions[3]
	if(listargs.has_key[argsE["value"]])
		raise SemanticException("Double args")
		
	subexpressions[0] = subexpressions[1].update(subexpressions[3])

def p_argsextra_terminal_fill(subexpressions):
	'argsextra_declaration : FILL'
	
	subexpressions[0] = {"FILL":True,"value":"FILL"}

def p_argsextra_terminal_stroke(subexpressions):
	'argsextra_declaration : STROKE'
	
	subexpressions[0] = {"STROKE":True,"value":"STROKE"}

def p_argsextra_terminal_strwidth(subexpressions):
	'argsextra_declaration : STRWIDTH'
	
	subexpressions[0] = {"STRWIDTH":True,"value":"STRWIDTH"}



def p_size(subexpressions):
	'size_declaration: SIZE args args_extra' 
	args = subexpressions[2]
	if !(args.has_key["HEIGHT"] && args.has_key["WIDTH"]):
		raise SemanticException("Incopatible size args")
	if len(args) > 4
		raise SemanticException("Incopatible size args")
	
	subexpressions[0] = {"type": "size","size":True}



def p_rectangle(subexpressions):
	'rectangle_declaration: RECTANGLE args args_extra'
	args = subexpressions[2]

	if !(args.has_key["UPPER_LEFT"] &&args.has_key["HEIGHT"] && args.has_key["WIDTH"]):
		raise SemanticException("Incopatible rectangle args")
	if len(args) > 6
		raise SemanticException("Incopatible rectangle args")

	subexpressions[0] = {"type": "rectangle"}


def p_line(subexpressions):
	'line_declaration: LINE args args_extra'
	args = subexpressions[2]
	if !(args.has_key["FROM"] &&args.has_key["TO"]):
		raise SemanticException("Incopatible line args")
	if len(args) > 4
		raise SemanticException("Incopatible line args")

	subexpressions[0] = {"type": "line"}


def p_circle(subexpressions):
	'circle_declaration: CIRCLE args args_extra'
	args = subexpressions[2]

	if !(args.has_key["CENTER"] &&args.has_key["RADIUS"]):
		raise SemanticException("Incopatible circle args")
	if len(args) > 4
		raise SemanticException("Incopatible circle args")

	subexpressions[0] = {"type": "circle"}

def p_ellipse(subexpressions):
	'ellipse_declaration: ELLIPSE args args_extra'
	args = subexpressions[2]

	if !(args.has_key["CENTER"] &&args.has_key["RX"]&&args.has_key["RY"]):
		raise SemanticException("Incopatible ellipse args")
	if len(args) > 6
		raise SemanticException("Incopatible ellipse args")

	subexpressions[0] = {"type": "ellipse"}

def p_polyline(subexpressions):
	'polyline_declaration: POLYLINE args args_extra'
	args = subexpressions[2]

	if !(args.has_key["POINTS"]):
		raise SemanticException("Incopatible polyline args")
	if len(args) > 2
		raise SemanticException("Incopatible polyline args")

	subexpressions[0] = {"type": "polyline"}

def p_polygon(subexpressions):
	'polygon_declaration: POLYGON args args_extra'
	args = subexpressions[2]

	if !(args.has_key["POINTS"]):
		raise SemanticException("Incopatible polygon args")
	if len(args) > 2
		raise SemanticException("Incopatible polygon args")

	subexpressions[0] = {"type": "polygon"}

def p_text(subexpressions):
	'text_declaration: TEXT args args_extra'
	args = subexpressions[2]

	if !(args.has_key["T"] &&args.has_key["AT"]):
		raise SemanticException("Incopatible text args")
	if len(args) > 4
		raise SemanticException("Incopatible text args")
	if len(args_text) > 4
		raise SemanticException("Incopatible extra text args")

	subexpressions[0] = {"type": "text"}



def p_funciones_lambda(subexpressions):
	'f_declaration: '

def p_funciones_lambda(subexpressions):
	'f_declaration: function f_declaration'
	rec = subexpressions[2]
	fun = subexpressions[1]
	if !(rec.has_key["size"] && fun.has_key["size"]):
		raise SemanticException("Incopatible function declaration")
	subexpressions[0] = subexpressions[1].update(subexpressions[2])



def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
