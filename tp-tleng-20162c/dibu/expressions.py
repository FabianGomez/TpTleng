import svgwrite

# Clase abstracta
class Expression(object):
    def evaluate(self, dwg=None):
        # Aca se implementa cada tipo de expresion.
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()
# las funciones nada mas son representadas por clases
# los argumentos de listas no

class Size(Expression):
    def __init__(self, width, height, optional):
        self.width = width
        self.height = height
        self.optional = optional

    def __str__(self):
        cadena = "Size: width=" + str(self.width) + " height=" + str(self.height) + " optionals=" + str(self.optional)
        return cadena  

    def evaluate(self, dwg=None):
        return (self.width, self.height)
    

class Rectangle(Expression):
    def __init__(self, size, upper_left, optional):
        self.size = size
        self.upper_left = upper_left
        self.optional = optional
            
    def evaluate(self, dwg):
        opt = self.optional
        dwg.add(dwg.rect(insert=self.upper_left, size=self.size, rx=None, ry=None, fill=opt.get("fill", ""), stroke=opt.get("stroke", ""), stroke_width=opt.get("stroke-width", 1)))        

    def __str__(self):
        cadena = "Rectangle: size=" + str(self.size) + " upper_left=" + str(self.upper_left) + " optional=" + str(self.optional)
        return cadena  
    
class Line(Expression):
    # from es keyword
    def __init__(self, froM, to, optional):
        self.froM = froM
        self.to = to
        self.optional = optional

    def evaluate(self,dwg):
        opt = self.optional
        dwg.add(dwg.line(start=self.froM, end=self.to, fill=opt.get("fill", ""), stroke=opt.get("stroke", ""), stroke_width=opt.get("stroke-width", 1)))
        
    def __str__(self):
        cadena = "Line: from=" + str(self.froM) + " to=" + str(self.to) + " optional=" + str(self.optional)
        return cadena  
    
class Circle(Expression):

    def __init__(self, center, radius, optional):
        self.center = center
        self.radius = radius
        self.optional = optional

    def evaluate(self,dwg):
        opt = self.optional
        dwg.add(dwg.circle(center=self.center, r=self.radius, fill=opt.get("fill", ""), stroke=opt.get("stroke", ""), stroke_width=opt.get("stroke-width", 1)))
        
    def __str__(self):
        cadena = "Circle: center=" + str(self.center) + " radius=" + str(self.radius) + " optional=" + str(self.optional)
        return cadena  


class Ellipse(Expression):

    def __init__(self, center, rx, ry, optional):
        self.center = center
        self.rx = rx
        self.ry = ry
        self.optional = optional
        
    def evaluate(self, dwg):
        opt = self.optional
        dwg.add(dwg.ellipse(self.center, (self.rx,self.ry), fill=opt.get("fill", ""), stroke=opt.get("stroke", ""), stroke_width=opt.get("stroke-width", 1)))
        
    def __str__(self):
        cadena = "Ellipse: center=" + str(self.center) + " rx=" + str(self.rx) +  " ry=" + str(self.ry) + " optional=" + str(self.optional)
        return cadena 
    
class Polyline(Expression):
    def __init__(self, points, optional):
        self.points = points
        self.optional = optional
        
    def evaluate(self, dwg):
        opt = self.optional
        dwg.add(dwg.polyline(points=self.points, fill=opt.get("fill", ""), stroke=opt.get("stroke", ""), stroke_width=opt.get("stroke-width", 1)))
        
    def __str__(self):
        cadena = "Polyline: points=" + str(self.points) + " optional=" + str(self.optional)
        return cadena 
    
class Polygon(Expression):
    def __init__(self, points, optional):
        self.points = points
        self.optional = optional
    
    def evaluate(self, dwg):
        opt = self.optional
        dwg.add(dwg.polygon(points=self.points, fill=opt.get("fill", ""), stroke=opt.get("stroke", ""), stroke_width=opt.get("stroke-width", 1)))
    def __str__(self):
        cadena = "Polygon: points=" + str(self.points) + " optional=" + str(self.optional)
        return cadena 
    
class Text(Expression):
    def __init__(self, t, at, optional):
        self.t = t
        sefl.at = at
        self.optional = optional
    def evaluate(self, dwg):
        opt = self.optional
        dwg.add(dwg.text(self.t, [self.at[0]], [self.at[1]], fill=opt.get("fill", ""), stroke=opt.get("stroke", ""), stroke_width=opt.get("stroke-width", 1)))
        
    def __str__(self):
        cadena = "Text: t=" + str(self.t) + "at=" + str(self.at) + " optional=" + str(self.optional)
        return cadena 
    
class Point(Expression):

    def __init__(self, x, y):
        self.x = x
        sefl.y = y
        
    def evaluate(self, dwg=None):
        return (x,y)
    
    def __str__(self):
        return str((self.x, self.y))

  