#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import ply.yacc as yacc
import collections

import svgwrite
from expressions import *

from lexer import tokens


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

def p_error(subexpr):
    raise Exception("Syntax error.")

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
        raise SemanticException("El argumento " + str(k) +  " aparece mas de una vez")
    
    # agregamos el nuevo argumento
    subexpressions[1][k]=v
    subexpressions[0] = subexpressions[1]

# Producciones Arg
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

def p_arg_size(subexpressions):
    'arg : SIZE EQUAL point'
    subexpressions[0] = ("size", subexpressions[3])

def p_f_size(subexpressions):
    'f : SIZE arglist' 
    args = subexpressions[2]
    
    hasArg("width", args)
    hasArg("height", args)    

    subexpressions[0] = Size(args["width"], args["height"], getOptionalArgs(args, False)) 

    
def p_f_rectangle(subexpressions):
    'f : RECTANGLE arglist' 
    args = subexpressions[2]
    
    #hasArg("width", args)
    #hasArg("height", args)
    hasArg("size", args)
    hasArg("upper_left", args)
    
    subexpressions[0] = Rectangle(args["size"], args["upper_left"], getOptionalArgs(args, False)) 

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
    subexpressions[0] = (subexpressions[2]["value"], subexpressions[4]["value"])
                                                           
# Build the parser
parser = yacc.yacc(debug=True)

def parse(str):
    """Dado un string, me lo convierte a SVG."""
    return parser.parse(str)

def buildSVG(ls):
    # Si todo fue exitoso ls debería ser una lista de expresiones.
    # 1) Revisamos que solo exista una expresion Size
    
    c = 0
    s = None
    for f in ls:
        if isinstance(f, Size):
            c = c+1
            s = f
   
    if c > 1 or c < 1:
        pass #tirar error
                         
    # 2) A partir del objeto size lo evaluamos para conseguir el tamaño del canvas y lo generamos con svgwriter
    
    # el nombre realmente no importa dado que nunca lo guardamos a disco
    dwg = svgwrite.Drawing('test.svg', size=s.evaluate(None)) # es nuestro lienzo para dibujar
    
    # 3) El drawing se lo pasamos a cada expresión de la lista con el método evaluar                         
    # iteramos por cada expression (que son funciones) y las evaluamos para que se agreguen al canvas (si es necesario)
    for f in ls:
        f.evaluate(dwg)
                         
    # 4) a svgwriter le pedimos que genere el XML y lo devolvemos.                   
    return dwg.tostring()