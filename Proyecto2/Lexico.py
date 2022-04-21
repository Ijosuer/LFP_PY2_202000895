from Token import Token
from Error import Error
from prettytable import PrettyTable

class AnalizadorLexico:
    
    def __init__(self) -> None:
        self.listaTokens  = []
        self.listaErrores = []
        self.linea = 1
        self.columna = 0
        self.buffer = ''
        self.estado = 0
        self.i = 0
        self.flag_comillas = False

    def agregar_token(self,caracter,linea,columna,token):
        self.listaTokens.append(Token(caracter,linea,columna,token))
        self.buffer = ''


    def agregar_error(self,caracter,linea,columna):
        self.listaErrores.append(Error('Caracter ' + caracter + ' no reconocido en el lenguaje.', linea, columna))

    def s0(self,caracter : str):
        '''Estado S0'''
        if caracter.isalpha():
            self.estado = 1
            self.buffer += caracter
            self.columna += 1
        elif caracter.isdigit():
            self.estado = 2
            self.buffer += caracter
            self.columna += 1
        elif caracter == '\"':
            self.estado = 3
            self.buffer += caracter
            self.columna += 1
        elif (caracter.isalpha() or (ord(caracter)>= 48 and ord(caracter)<= 57)):
            self.estado = 4 
            self.buffer += caracter
            self.columna += 1   
        elif caracter == '<':
            self.buffer += caracter
            self.estado = 2
            self.columna += 1   
        elif caracter == '>':
            self.buffer += caracter
            self.estado = 2
            self.columna += 1   
        elif caracter == '-':
            self.buffer += caracter
            self.estado = 1
            self.columna += 1   
        elif caracter== '\n':
            self.linea += 1
            self.columna = 0
        elif caracter in ['\t',' ']:
            self.columna += 1
        elif caracter == '$':
            print('Se terminó el análisis')
        else:
            self.agregar_error(caracter,self.linea,self.columna)

    def s1(self,caracter : str):
        '''Estado S1'''
        if caracter.isalpha():
            self.estado = 1
            self.buffer += caracter
            self.columna += 1
        elif caracter.isdigit():
            self.estado = 1
            self.buffer += caracter
            self.columna += 1          
        else: 
            if self.buffer in ['RESULTADO','VS','TEMPORADA','JORNADA','-f','GOLES','TABLA','TEMPORADA','PARTIDOS','TOP','SUPERIOR','INFERIOR','ADIOS']:
                self.agregar_token(self.buffer,self.linea,self.columna,'reservada_'+self.buffer)    
                self.estado = 0
                self.i -= 1

            else:
                self.agregar_token(self.buffer,self.linea,self.columna,'ID')
                self.estado = 0
                self.i -= 1

    def s2(self,caracter : str):
        '''Estado S2'''
        if caracter =='<':
            self.estado = 2
            self.buffer += caracter
            self.columna += 1
        elif caracter =='-':
            self.estado = 2
            self.buffer += caracter
            self.columna += 1
        elif caracter.isdigit():
            self.estado = 2
            self.buffer += caracter
            self.columna += 1
        elif caracter =='>':
            self.estado = 2
            self.buffer += caracter
            self.columna += 1
        else:
            if len(self.buffer) == 6:
                self.agregar_token(self.buffer,self.linea,self.columna,'year')
                self.estado = 0
                self.i -= 1
            if len(self.buffer) == 11:
                self.agregar_token(self.buffer,self.linea,self.columna,'jornadas')
                self.estado = 0
                self.i -= 1
            elif len(self.buffer) <= 2 and len(self.buffer) >0:
                self.agregar_token(self.buffer,self.linea,self.columna,'numero_gol')
                self.estado = 0
                self.i -= 1
            else:
                self.agregar_error(self.buffer,self.linea,self.columna)

    def s3(self,caracter):
        '''Estado 3 - cadenas'''
        if caracter == '"':
            self.estado = 4
            self.buffer += caracter
            self.columna += 1
        else:
            self.buffer += caracter
            self.columna += 1
    def s4(self,caracter : str):
        '''Estado 3 - cadenas'''
        if caracter.isalpha():
            self.estado = 4
            self.buffer += caracter
            self.columna += 1
        elif caracter in ['+','!','*','@','-',':',';','#','%','^','&','?',',','.','|']:
            self.estado = 4
            self.buffer += caracter
            self.columna += 1
        elif caracter.isdigit():
            self.estado = 4
            self.buffer += caracter
            self.columna += 1
        else:
            self.agregar_token(self.buffer,self.linea,self.columna,'Cadena X')
            self.estado = 0
            self.i -= 1

    def analizar(self, cadena):
        cadena = cadena + '$'
        self.listaErrores = []
        self.listaTokens = []
        self.i = 0
        while self.i < len(cadena):
            if self.estado == 0:
                self.s0(cadena[self.i])
            elif self.estado == 1:
                self.s1(cadena[self.i])
            elif self.estado == 2:
                self.s2(cadena[self.i])
            elif self.estado == 3:
                self.s3(cadena[self.i])
            elif self.estado == 4:
                self.s4(cadena[self.i])
            self.i += 1    

    def imprimirTokens(self):
        '''Imprime una tabla con los tokens'''
        x = PrettyTable()
        x.field_names = ["Lexema","linea","columna","tipo"]
        for token in self.listaTokens:
            x.add_row([token.lexema, token.fila, token.columna,token.tipo])
        print(x)

    def imprimirErrores(self):
        '''Imprime una tabla con los errores'''
        x = PrettyTable()
        x.field_names = ["DEscripcion","linea","columna"]
        for error_ in self.listaErrores:
            x.add_row([error_.descripcion, error_.fila, error_.columna])
        print(x)  

obj = AnalizadorLexico()
obj.analizar('<1234-1234>"a fd" 2 JORNADAS')
obj.imprimirTokens()
obj.imprimirErrores()