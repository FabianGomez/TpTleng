import ply.yacc as yacc
import collections

from lexer import tokens

# Clases para las funciones
Size = collections.namedtuple('Size', 'width height optional')
Rectangle = collections.namedtuple('Rectangle', 'width height upper_left optional')
# from es una palabra reservada del lenguaje por eso hacemos froM
Line = collections.namedtuple('Line', 'froM to optional')
Circle = collections.namedtuple('Circle', 'center radius optional')
Ellipse = collections.namedtuple('Ellipse', 'center rx ry optional')
Polyline = collections.namedtuple('Polyline', 'points optional')
Polygon = collections.namedtuple('Polygon', 'points optional')
# los opcionales de text pueden tener dos mas que son especificos
Text = collections.namedtuple('Text', 't at optional')

# Clases intermedias
fPrima = collections.namedtuple('fPrima', 'f1 f2')
Point = collections.namedtuple('Point', 'x y')

# un argumento es una tupla (nombreArgumento, valor)

# argList es un diccionario 

# Funciones auxiliares
# por como se construye argList sabemos que args no tendra mas de un valor para la misma clave
def hasArg(argname, args):
    if not(argname in args.keys()):
        raise SemanticException("Argumento obligatorio no encontrado: " + str(argname))
        
def getOptionalArgs(args, isText):
    res = {}
    if "fill" in args.keys():
        res["fill"] = args["fill"]
    if "stroke" in args.keys():
        res["stroke"] = args["stroke"]
    if "stroke-width" in args.keys():
        res["stroke-width"] = args["stroke-width"]
    
    if isText:
        if "font-family" in args.keys():
            res["font-family"] = args["font-family"]
        if "font-size" in args.keys():
            res["font-size"] = args["font-size"]
            
    return res

# Producciones
# Producciones FPrima
def p_funciones_lambda(subexpressions):
    'fPrima : '
    pass

def p_funciones(subexpressions):
    'fPrima : f fPrima'
    rec = subexpressions[2]
    fun = subexpressions[1]
    subexpressions[0] = fPrima(f1=subexpressions[1], f2=subexpressions[2])

# Producciones ArgList
def p_arglist_arg(subexpressions):
    'arglist : arg'
    (k,v) = subexpressions[1]
    subexpressions[0] = {k : v}
    
def p_arglist(subexpressions):
    'arglist : arglist COMMA arg'
    (k,v) = subexpressions[3]
    # arglist es un diccionario de argumentos
    # no puede aparecer mas de una vez el mismo argumento
    if k in subexpressions[1].keys():
        raise SemanticException("El argumento " + str(k) +  " aparece mas de una vez")
    
    # agregamos el nuevo argumento
    subexpressions[1][k]=v
    subexpressions[0] = subexpressions[1]

# Producciones Arg
def p_arg_height(subexpressions):
    'arg : HEIGHT EQUAL NUMBER'
    print(subexpressions[3])
    subexpressions[0] = ("height", subexpressions[3]["value"])

def p_arg_width(subexpressions):
    'arg : WIDTH EQUAL NUMBER'
    subexpressions[0] = ("width", subexpressions[3]["value"])

def p_arg_upperLeft(subexpressions):
    'arg : ULEFT EQUAL point'
    subexpressions[0] = ("upper_left", subexpressions[3])

def p_arg_from(subexpressions):
    'arg : FROM EQUAL point'
    subexpressions[0] = ("from", subexpressions[3])
    
def p_arg_to(subexpressions):
    'arg : TO EQUAL point'
    subexpressions[0] = ("to", subexpressions[3])

def p_arg_center(subexpressions):
    'arg : CENTER EQUAL point'
    subexpressions[0] = ("center", subexpressions[3])

def p_arg_radius(subexpressions):
    'arg : RADIUS EQUAL NUMBER'
    subexpressions[0] = ("radius", subexpressions[3]["value"])

def p_arg_rx(subexpressions):
    'arg : RX EQUAL NUMBER'
    subexpressions[0] = ("rx",subexpressions[3]["value"])
    
def p_arg_ry(subexpressions):
    'arg : RY EQUAL NUMBER'
    subexpressions[0] = ("ry",subexpressions[3]["value"])
    
def p_arg_points(subexpressions):
    'arg : POINTS EQUAL pointarray'
    subexpressions[0] = ("points", subexpressions[3])
    
def p_pointarray(subexpressions):
    'pointarray : LBRACKET pointlist RBRACKET'
    subexpressions[0] = subexpression[2]

def p_pointlist_point(subexpressions):
    'pointlist : point'
    subexpressions[0] = [subexpressions[1]]

def p_pointlist(subexpressions):
    'pointlist : point COMMA pointlist'
    subexpressions[0] = [subexpression[1]] ++ subexpressions[3]
    
def p_arg_at(subexpressions):
    'arg : AT EQUAL point'
    subexpressions[0] = ("at", subexpressions[3])

def p_arg_t(subexpressions):
    'arg : T EQUAL STRING'
    subexpressions[0] = ("t", subexpressions[3]["value"])

def p_arg_font_family(subexpressions):
    'arg : FFAMILY EQUAL STRING'
    subexpressions[0] = ("font-family", subexpressions[3]["value"])

def p_arg_font_size(subexpressions):
    'arg : FSIZE EQUAL STRING'
    subexpressions[0] = ("font-size", subexpressions[3]["value"])
        
def p_f_size(subexpressions):
    'f : SIZE arglist' 
    args = subexpressions[2]
    
    hasArg("width", args)
    hasArg("height", args)    

    subexpressions[0] = Size(args["width"], args["height"], getOptionalArgs(args, False)) 

    
def p_f_rectangle(subexpressions):
    'f : RECTANGLE arglist' 
    args = subexpressions[2]
    
    hasArg("width", args)
    hasArg("height", args)    
    hasArg("upper_left", args)
    
    subexpressions[0] = Rectangle(args["width"], args["height"], args["upper_left"], getOptionalArgs(args, False)) 

def p_f_line(subexpressions):
    'f : LINE arglist' 
    args = subexpressions[2]
    
    hasArg("from", args)
    hasArg("to", args)
    
    subexpressions[0] = Line(args["froM"], args["to"], getOptionalArgs(args, False)) 

def p_f_circle(subexpressions):
    'f : CIRCLE arglist' 
    args = subexpressions[2]
    
    hasArg("center", args)
    hasArg("radius", args)
    
    subexpressions[0] = Circle(args["center"], args["radius"], getOptionalArgs(args, False)) 
    
def p_f_ellipse(subexpressions):
    'f : ELLIPSE arglist' 
    args = subexpressions[2]
    
    hasArg("center", args)
    hasArg("rx", args)
    hasArg("ry", args)
    
    subexpressions[0] = Ellipse(args["center"], args["rx"], args["ry"], getOptionalArgs(args, False))

def p_f_polyline(subexpressions):
    'f : POLYLINE arglist' 
    args = subexpressions[2]
    
    hasArg("points", args)

    subexpressions[0] = Polyline(args["points"], getOptionalArgs(args, False))
    
def p_f_polygon(subexpressions):
    'f : POLYGON arglist' 
    args = subexpressions[2]
    
    hasArg("points", args)
    
    subexpressions[0] = Polygon(args["points"], getOptionalArgs(args, False))

def p_f_text(subexpressions):
    'f : TEXT arglist' 
    args = subexpressions[2]
    
    hasArg("t", args)
    hasArg("at", args)
    
    subexpressions[0] = Polygon(args["points"], getOptionalArgs(args, True))
          
def p_point(subexpressions):
    'point : LPAREN NUMBER COMMA NUMBER RPAREN'
    subexpressions[0] = (subexpressions[2], subexpressions[4])
                                                           
# Build the parser
parser = yacc.yacc(debug=True)

def parse(str):
    """Dado un string, me lo convierte a SVG."""
    return parser.parse(str)
