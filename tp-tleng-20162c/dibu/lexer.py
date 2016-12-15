#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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
'NEWLINE','NUMBER', 'STRING','LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET','COMMA', 'EQUAL',
#inicios de funciones
    'FUNC',
#parametros
    'ARG'
    ]

def t_NUMBER(token):
    #primera parte es para floats  y la segunda para integers
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
    r'"(.*?)"'
    #r'\"([^\\\n]|(\\.))*\"'
    string_type = "string"
    #removemos las comillas obligatorias
    string_value = token.value[1:-1]
    token.value = {"value": string_value, "type": string_type}
    return token

t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_EQUAL            = r'='
t_COMMA            = r','

def t_FUNC(token):
    r'text|size|rectangle|line|circle|ellipse|polyline|polygon'
    return token

def t_ARG(token):
    r'height|width|upper_left|from|center|radius|rx|ry|to|at|t|font-family|font-size|fill|stroke-width|stroke|style|points'
    return token

def t_NEWLINE(token):
    r"\n"
    token.lexer.lineno += 1
    
t_ignore = " \t"

# EOF handling rule
def t_eof(t):
    return None

def t_error(token):
    
    message = "Error Lexer."
    message += "\nToken desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)

# Build the lexer
lexer = lex.lex()

# entre distintos casos de tests es necesario resetear el parser
# sino se usa el mismo objeto lexer para todos los parseos
# eso introduce errores como tener mal el numero de lineas
def reset():
    global lexer
    lexer = lex.lex()
    
def apply(string):
    u"""Aplica el análisis léxico al string dado."""
    lex.input(string)

    return list(lexer)
