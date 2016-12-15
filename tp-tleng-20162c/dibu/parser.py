#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import ply.yacc as yacc
import collections

import svgwrite
from .expressions import *

from .lexer import tokens
from .lexer import reset

optArgs = ["stroke", "stroke-width", "fill", "style"]
arguments = {"size":{"mandatory":["height", "width"],"optional":optArgs },
             "rectangle":{"mandatory":["upper_left", "width", "height"],"optional":optArgs},
             "line":{"mandatory":["from", "to"],"optional":optArgs},
             "circle":{"mandatory":["center", "radius"],"optional":optArgs},
             "ellipse":{"mandatory":["center", "rx", "ry"],"optional":optArgs},
             "polyline":{"mandatory":["points"],"optional":optArgs},
             "polygon":{"mandatory":["points"],"optional":optArgs},
             "text":{"mandatory":["t", "at"],"optional": optArgs + ["font-family", "font-size"]}}

# en este diciconario guardamos las apariciones de las funciones especiales
# por especiales llamamos a las que aparecen a lo sumo una vez.
specialFunctions = {"size" : 0}

# un argumento es una tupla (nombreArgumento, valor)
# argList es un diccionario 

# Funciones auxiliares
# por como se construye argList sabemos que args no tendra mas de un valor para la misma clave
def hasArg(argname, args, lineno, lexpos):
    if not(argname in args.keys()):
        raise Exception("ERROR: Argumento obligatorio no encontrado: " + str(argname) + ". Linea: " + str(lineno) + " Para la funcion en posicion (relativa a la linea): " + str(find_column(lexpos)))
        
def correctArgs(possibleArgs, args, lineno, lexpos):
    for k in args.keys():
        if k not in possibleArgs:
            raise Exception("ERROR: Argumento no válido: " + str(k) + ". Linea: " + str(lineno) + " Para la funcion en posicion (relativa a la linea): " + str(find_column(lexpos)))
        
def getOptionalArgs(args, isText):
    res = {}
    if "fill" in args.keys():
        res["fill"] = args["fill"]
    if "stroke" in args.keys():
        res["stroke"] = args["stroke"]
    if "stroke-width" in args.keys():
        res["stroke-width"] = args["stroke-width"]
    if "style" in args.keys():
        res["style"] = args["style"]
        
    if isText:
        if "font-family" in args.keys():
            res["font-family"] = args["font-family"]
        if "font-size" in args.keys():
            res["font-size"] = args["font-size"]
            
    return res

# Compute column. 
#     input is the input text string
#     token is a token instance
def find_column(posToken): # la sacamos de la documentacion
    last_cr = parserInput.rfind('\n',0,posToken)
    if last_cr < 0:
        last_cr = 0
    column = (posToken - last_cr) + 1
    return column

def p_error(subexpr):
    if subexpr:
        msg = "Error sintactico en linea " + str(subexpr.lineno) + " en la posición (relativa a la linea): " + str(find_column(subexpr.lexpos))
    else:
        msg="Error en el fin del archivo"
        
    raise Exception(msg)

# Producciones
# Producciones FPrima
def p_funciones_lambda(subexpressions):
    'fPrima : '
    subexpressions[0] = []

def p_funciones(subexpressions):
    'fPrima : f fPrima'
    rec = subexpressions[2]
    f = subexpressions[1]
    
    rec.insert(0,f)
    subexpressions[0] = rec

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
        raise Exception("El argumento " + str(k) +  " aparece mas de una vez. Linea: " + str(subexpressions.lineno(2)) + " Posicion (relativa a la linea) " + str(find_column(subexpressions.lexpos(2))))
    
    # agregamos el nuevo argumento
    subexpressions[1][k]=v
    subexpressions[0] = subexpressions[1]
  
# Producciones Arg

argsPerValue = {"number":{"rx", "ry", "radius", "stroke-width", "height", "width"},
                "string":{"fill", "stroke", "t", "font-family", "font-size", "style"},
                "point":{"upper_left", "from", "to", "center", "at"},
                "pointarray":{"points"}}

def p_arg_value(subexpressions):
    'arg : ARG EQUAL value '
    checkArgs = {}
    valor = ""
    if type(subexpressions[3]) is list:
        valor = "pointarray"
    elif type(subexpressions[3]) is tuple:
        valor = "point"
    elif subexpressions[3]["type"] == "string":
        valor = "string"
    elif subexpressions[3]["type"] == "number":
        valor = "number"
    
    checkArgs = argsPerValue[valor]
    
    if subexpressions[1] not in checkArgs:
        raise Exception("El argumento " + str(subexpressions[1]) +  " no acepta " + valor + ". Linea: " + str(subexpressions.lineno(1)) + " Posicion (relativa a la linea) " + str(find_column(subexpressions.lexpos(1))))
        
    if valor == "pointarray" or valor == "point":
        subexpressions[0] = (subexpressions[1], subexpressions[3])
    elif valor == "string" or valor == "number":
        subexpressions[0] = (subexpressions[1], subexpressions[3]["value"])

def p_value_number(subexpressions):
    'value : NUMBER'
    subexpressions[0] = subexpressions[1]
    
def p_value_string(subexpressions):
    'value : STRING'
    subexpressions[0] = subexpressions[1]
    
def p_value_point(subexpressions):
    'value : point'
    subexpressions[0] = subexpressions[1]
    
def p_value_pointarray(subexpressions):
    'value : pointarray'
    subexpressions[0] = subexpressions[1]  
def p_pointarray(subexpressions):
    'pointarray : LBRACKET pointlist RBRACKET'
    subexpressions[0] = subexpressions[2]

def p_pointlist_point(subexpressions):
    'pointlist : point'
    subexpressions[0] = [subexpressions[1]]

def p_pointlist(subexpressions):
    'pointlist : point COMMA pointlist'
    l = subexpressions[3]
    l.insert(0, subexpressions[1])
    subexpressions[0] = l

#Producciones de funciones

def p_f_func(subexpressions):
    'f : FUNC arglist'
    
    args = subexpressions[2]
    functionName = subexpressions[1]
    
    possibleArgs = arguments[functionName]["mandatory"] + arguments[functionName]["optional"]
    # nos fijamos que los argumentos sean validos
    correctArgs(possibleArgs, args, subexpressions.lineno(1), subexpressions.lexpos(1))      
    # nos fijamos que esten los obligatorios
    for arg in arguments[functionName]["mandatory"]:
        hasArg(arg, args, subexpressions.lineno(1), subexpressions.lexpos(1)) 
    
    # manejamos el caso de las funciones especiales que solo aparecen una vez
    # en este caso es solo size.
    if functionName in specialFunctions.keys():
        specialFunctions[functionName] += 1
        if specialFunctions[functionName] > 1:
            raise Exception("La funcion " + functionName + " solo puede aparecer a lo sumo una vez. Linea: "   + str(subexpressions.lineno(1)) + " Posicion (relativa a la linea) " + str(find_column(subexpressions.lexpos(1))))
        
    if functionName == "size":
        subexpressions[0] = Size(args["width"], args["height"], getOptionalArgs(args, False))
    elif functionName == "rectangle":
        subexpressions[0] = Rectangle((args["width"], args["height"]), args["upper_left"], getOptionalArgs(args, False))
    elif functionName ==  "line":
        subexpressions[0] = Line(args["from"], args["to"], getOptionalArgs(args, False))
    elif functionName == "circle":
        subexpressions[0] = Circle(args["center"], args["radius"], getOptionalArgs(args, False))
    elif functionName == "ellipse":
        subexpressions[0] = Ellipse(args["center"], args["rx"], args["ry"], getOptionalArgs(args, False))
    elif functionName == "polyline":
        subexpressions[0] = Polyline(args["points"], getOptionalArgs(args, False))
    elif functionName == "polygon":
        subexpressions[0] = Polygon(args["points"], getOptionalArgs(args, False))
    elif functionName == "text":
        subexpressions[0] = Text(args["t"], args["at"], getOptionalArgs(args, True))
    
def p_point(subexpressions):
    'point : LPAREN NUMBER COMMA NUMBER RPAREN'
    subexpressions[0] = (subexpressions[2]["value"], subexpressions[4]["value"])
                                                           
# Build the parser
parser = yacc.yacc(debug=True)
parserInput = ""

def parse(s):
    """Dado un string, me lo convierte a SVG."""
    global parserInput # asi la usamos para calcular la columna dentro de una linea a la hora de manejar errores
    parserInput = s
    global specialFunctions
    # reseteamos 
    for k,v in specialFunctions.items():
        specialFunctions[k] = 0
    reset() # reseteamos el objeto lexer - sino se superpone el conteo de lineas
    r = parser.parse(s)
    return buildSVG(r)

def buildSVG(ls):
    # Si todo fue exitoso ls debería ser una lista de expresiones.
    
    # 1) A partir del objeto size lo evaluamos para conseguir el tamaño del canvas y lo generamos con svgwriter
    
    #print("buildSVG: " + str(ls))
    
    s = None
    for f in ls: # iteramos nada mas para saber si hay o no un size. No nos ocupamos de rechazar aca!
        if type(f) is Size:
            s = f
    if s:
        # el nombre realmente no importa dado que nunca lo guardamos a disco
        dwg = svgwrite.Drawing('test.svg',size=s.evaluate(None)) # es nuestro lienzo para dibujar
    else:
        dwg = svgwrite.Drawing('test.svg')
    
    # 2) El drawing se lo pasamos a cada expresión de la lista con el método evaluar                         
    # iteramos por cada expression (que son funciones) y las evaluamos para que se agreguen al canvas (si es necesario)
    for f in ls:
        f.evaluate(dwg)
       
    # 3) a svgwriter le pedimos que genere el XML y lo devolvemos.                   
    return dwg.tostring()