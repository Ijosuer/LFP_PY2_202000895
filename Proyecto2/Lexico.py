from prettytable import PrettyTable
from Error import Error
from Token import Token

class Scanner:
    def __init__(self):
        self.buffer = ''
        self.fila = 1
        self.columna = 1
        self.estado = 0
        self.listaTokens = []
        self.listaErrores = []
        self.i = 0

    def agregar_Token(self,caracter,fila,columna,token):
        self.listaTokens.append(Token(caracter,fila,columna,token))
        self.buffer = ''

    def agregar_Error(self,caracter,fila,columna):
        self.listaErrores.append(Error('Caracter \'' + caracter + '\' error de tipo Numero',fila,columna))#pendiente
    
    def s0(self,caracter):
        '''Estado 0'''
    #pendiente todos los estados

    def analizar(self,cadena):
        '''Realiza los cambios de estados'''
        cadena += '$'
        self.i = 0
    
    def imprimirTokens(self):
        x = PrettyTable()
        x.field_names = ["Lexema","fila","Columna","Tipo"]
        for token in self.listaTokens:
            x.add_row([token.lexema,token.fila,token.columna,token.tipo])
        print(x)
    
    def imprimirTokens(self):
        x = PrettyTable()
        x.field_names = ["Lexema","fila","Columna","Tipo"]
        for token in self.listaTokens:
            x.add_row([token.lexema,token.fila,token.columna,token.tipo])
        print(x)
