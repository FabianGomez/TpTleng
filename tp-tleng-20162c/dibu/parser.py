#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import ply.yacc as yacc
import collections

import svgwrite
from .expressions import *

from .lexer import tokens
from .lexer import reset


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

def p_arg_fill(subexpressions):
    'arg : FILL EQUAL STRING'
    subexpressions[0] = ("fill", subexpressions[3]["value"])
    
def p_arg_stroke(subexpressions):
    'arg : STROKE EQUAL STRING'
    subexpressions[0] = ("stroke", subexpressions[3]["value"])
    
def p_arg_strwidth(subexpressions):
    'arg : STRWIDTH EQUAL NUMBER'
    subexpressions[0] = ("stroke-width", subexpressions[3]["value"])
    
def p_arg_height(subexpressions):
    'arg : HEIGHT EQUAL NUMBER'
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
    subexpressions[0] = subexpressions[2]

def p_pointlist_point(subexpressions):
    'pointlist : point'
    subexpressions[0] = [subexpressions[1]]

def p_pointlist(subexpressions):
    'pointlist : point COMMA pointlist'
    l = subexpressions[3]
    l.insert(0, subexpressions[1])
    subexpressions[0] = l
    
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

def p_arg_size(subexpressions):
    'arg : SIZE EQUAL point'
    subexpressions[0] = ("size", subexpressions[3])

def p_arg_style(subexpressions):
    'arg : STYLE EQUAL STRING'
    subexpressions[0] = ("style", subexpressions[3]["value"])

def p_f_size(subexpressions):
    'f : SIZE arglist' 
    args = subexpressions[2]
    
    possibleArgs = ["width", "height", "fill", "stroke", "stroke-width", "style"]
    correctArgs(possibleArgs, args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("width", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("height", args, subexpressions.lineno(1), subexpressions.lexpos(1))  

    subexpressions[0] = Size(args["width"], args["height"], getOptionalArgs(args, False)) 

    
def p_f_rectangle(subexpressions):
    'f : RECTANGLE arglist' 
    args = subexpressions[2]
    possibleArgs = ["size", "upper_left", "fill", "stroke", "stroke-width", "style"]
    correctArgs(possibleArgs, args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("size", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("upper_left", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    
    subexpressions[0] = Rectangle(args["size"], args["upper_left"], getOptionalArgs(args, False)) 

def p_f_line(subexpressions):
    'f : LINE arglist' 
    args = subexpressions[2]
    possibleArgs = ["from", "to", "fill", "stroke", "stroke-width", "style"]
    correctArgs(possibleArgs, args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("from", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("to", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    
    subexpressions[0] = Line(args["from"], args["to"], getOptionalArgs(args, False)) 

def p_f_circle(subexpressions):
    'f : CIRCLE arglist' 
    args = subexpressions[2]
    
    possibleArgs = ["center", "radius", "fill", "stroke", "stroke-width", "style"]
    correctArgs(possibleArgs, args, subexpressions.lineno(1), subexpressions.lexpos(1))
    hasArg("center", args, subexpressions.lineno(1), subexpressions.lexpos(1))
    hasArg("radius", args, subexpressions.lineno(1), subexpressions.lexpos(1))
    
    subexpressions[0] = Circle(args["center"], args["radius"], getOptionalArgs(args, False)) 
    
def p_f_ellipse(subexpressions):
    'f : ELLIPSE arglist' 
    args = subexpressions[2]
    possibleArgs = ["center", "rx", "ry", "fill", "stroke", "stroke-width", "style"]
    correctArgs(possibleArgs, args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("center", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("rx", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("ry", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    
    subexpressions[0] = Ellipse(args["center"], args["rx"], args["ry"], getOptionalArgs(args, False))

def p_f_polyline(subexpressions):
    'f : POLYLINE arglist' 
    args = subexpressions[2]
    possibleArgs = ["points", "fill", "stroke", "stroke-width", "style"]
    correctArgs(possibleArgs, args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("points", args, subexpressions.lineno(1), subexpressions.lexpos(1))  

    subexpressions[0] = Polyline(args["points"], getOptionalArgs(args, False))
    
def p_f_polygon(subexpressions):
    'f : POLYGON arglist' 
    args = subexpressions[2]
    possibleArgs = ["points", "fill", "stroke", "stroke-width", "style"]
    correctArgs(possibleArgs, args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("points", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    
    subexpressions[0] = Polygon(args["points"], getOptionalArgs(args, False))

def p_f_text(subexpressions):
    'f : TEXT arglist' 
    args = subexpressions[2]
    possibleArgs = ["t", "at", "font-family", "font-size", "fill", "stroke", "stroke-width", "style"]
    correctArgs(possibleArgs, args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("t", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    hasArg("at", args, subexpressions.lineno(1), subexpressions.lexpos(1))  
    
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
    reset() # reseteamos el objeto lexer - sino se superpone el conteo de lineas
    r = parser.parse(s)
    return buildSVG(r)

def buildSVG(ls):
    # Si todo fue exitoso ls debería ser una lista de expresiones.
    # 1) Revisamos que solo exista una expresion Size
    
    c = 0
    s = None
    for f in ls:
        if isinstance(f, Size):
            c = c+1
            s = f

    if c > 1:
        # para este error no hay una linea en donde lanzar el error.
        raise Exception("ERROR: Debe haber a lo sumo una funcion size definida.")
                  
    # 2) A partir del objeto size lo evaluamos para conseguir el tamaño del canvas y lo generamos con svgwriter
    
    if s:
        # el nombre realmente no importa dado que nunca lo guardamos a disco
        dwg = svgwrite.Drawing('test.svg',size=s.evaluate(None)) # es nuestro lienzo para dibujar
    else:
        dwg = svgwrite.Drawing('test.svg')
    
    # 3) El drawing se lo pasamos a cada expresión de la lista con el método evaluar                         
    # iteramos por cada expression (que son funciones) y las evaluamos para que se agreguen al canvas (si es necesario)
    for f in ls:
        f.evaluate(dwg)
       
    # 4) a svgwriter le pedimos que genere el XML y lo devolvemos.                   
    return dwg.tostring()