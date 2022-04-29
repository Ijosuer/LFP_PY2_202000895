import time
import webbrowser
from Token import Token
from Error import Error
from prettytable import PrettyTable
import Sintactico
RESERVADAS = ['RESULTADO','VS','TEMPORADA','JORNADA','-f','-n','-ji','-jf','GOLES','TABLA','LOCAL','VISITANTE','TOTAL','PARTIDOS','TOP','SUPERIOR','INFERIOR','ADIOS']
class AnalizadorLexico:
    def __init__(self) -> None:
        self.listaTokens  = []
        self.listaTokens2  = []
        self.listaErrores = []
        self.listaErrores2 = []
        self.linea = 1
        self.columna = 1
        self.buffer = ''
        self.estado = 0
        self.i = 0

    def agregar_token(self,caracter,linea,columna,token):
        self.listaTokens.append(Token(caracter,linea,columna,token))
        self.listaTokens2.append(Token(caracter,linea,columna,token))
        self.buffer = ''
        


    def agregar_error(self,caracter,linea,columna):
        self.listaErrores.append(Error('Caracter ' + caracter + ' no reconocido en el lenguaje.', linea, columna))
        self.listaErrores2.append(Error('Caracter ' + caracter + ' no reconocido en el lenguaje.', linea, columna))

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
        elif caracter == '[' or caracter ==']':
            self.columna +=1
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
            if self.buffer in RESERVADAS:
                self.agregar_token(self.buffer,self.linea,self.columna-len(self.buffer),'res_'+self.buffer)    
                self.estado = 0
                self.i -= 1

            else:
                self.agregar_token(self.buffer,self.linea,self.columna-len(self.buffer),'ID')
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
                self.agregar_token(self.buffer,self.linea,self.columna-len(self.buffer),'tk_year')
                self.estado = 0
                self.i -= 1
            if len(self.buffer) == 11:
                self.agregar_token(self.buffer,self.linea,self.columna-len(self.buffer),'tk_temporada')
                self.estado = 0
                self.i -= 1
            elif len(self.buffer) <= 2 and len(self.buffer) >0:
                self.agregar_token(self.buffer,self.linea,self.columna-len(self.buffer),'tk_num')
                self.estado = 0
                self.i -= 1
            else:
                self.agregar_error(self.buffer,self.linea,self.columna-len(self.buffer))

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
        '''Estado 4 - cadenas'''
        self.agregar_token(self.buffer,self.linea,self.columna-len(self.buffer),'Cadena')
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
        # x = PrettyTable()
        text = 'LEXEMA - FILA - COL - TIPO\n'
        # x.field_names = ["Lexema","linea","columna","tipo"]
        for token in self.listaTokens:
            
            # x.add_row([token.lexema, token.fila, token.columna,token.tipo])
            text+=(token.lexema)
            text+=' ['
            text+=(str(token.fila))
            text+=' '
            text+=(str(token.columna))
            text+='] '
            text+=(token.tipo)
            text+='\n'
        return text

    def imprimirErrores(self):
        '''Imprime una tabla con los errores'''
        x = PrettyTable()
        x.field_names = ["DEscripcion","linea","columna"]
        for error_ in self.listaErrores:
            x.add_row([error_.descripcion, error_.fila, error_.columna])
        print(x)  

    def limpiarTokens(self):
        print(len(self.listaTokens),len(self.listaTokens2))
        self.listaTokens = []
        self.listaTokens2 = []
        self.columna = 1
        print(len(self.listaTokens),len(self.listaTokens2))

    def limpiarErrores(self):
        print(len(self.listaErrores),len(self.listaErrores))
        self.listaErrores = []
        self.listaErrores2 = []
        self.columna = 1
        print(len(self.listaErrores),len(self.listaErrores2))

    def crearTTokens(self):
        texto = ''
        f = open('./ReporteTokens.html','w')
        texto += '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Reporte Tokens</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
            rel="stylesheet"
            integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We"
            crossorigin="anonymous"
            />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
        </head>
        <body style="background-color: rgb(243, 240, 235);">
        <div class="container">
        <br>
        <h2 class="text-center" style="font-weight: bold; color: rgb(36, 36, 179);">Tabla de Tokens</h2>
        <br>
        <h6 style="font-weight:600 ;">A continuacion se presentan tabla de tokens encontrados en el lenguaje:</h6>
        <table class="table table-hover">
            <thead class="thead-dark">
        <tr>
        <th class="text-center">LEXEMA</th>
        <th class="text-center">FILA</th>
        <th class="text-center">COLUMNA</th>
        <th class="text-center">TIPO</th>
        </tr>
        </thead>
        <tbody>'''
        for token in self.listaTokens2:
            texto +='''
        <tr>
            <td class="text-center">'''+token.lexema+'''</td>
            <td class="text-center">'''+str(token.fila)+'''</td>
            <td class="text-center">'''+str(token.columna)+'''</td>
            <td class="text-center">'''+token.tipo+'''</td>
        </tr>   '''
        texto +='''
        </tbody>
        </table>
        <br>
                    
        </body>
        <hr>
        <footer>
            <h5 style="text-align: right; font-weight: bolder;">Josue Gramajo - 202000895</h5>
            <h6 style="text-align: right; font-weight: bold;">Reporte generado:'''+time.ctime()+'''</h6>
        </footer>
        </html>
        '''
        mensaje = texto 
        f.write(mensaje)
        f.close()

        webbrowser.open_new_tab('ReporteTokens.html')

    def crearTErrores(self):
        texto = ''
        f = open('./ReporteErrores.html','w')
        texto += '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Reporte Errores</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css"
            rel="stylesheet"
            integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We"
            crossorigin="anonymous"
            />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
        </head>
        <body style="background-color: rgb(243, 240, 235);">
        <div class="container">
        <br>
        <h2 class="text-center" style="font-weight: bold; color: rgb(36, 36, 179);">Tabla de Errores</h2>
        <br>
        <h6 style="font-weight:600 ;">A continuacion se presentan tabla de errores lexicos encontrados en el lenguaje:</h6>
        <table class="table table-hover">
            <thead class="thead-dark">
        <tr>
        <th class="text-center">Descripcion</th>
        <th class="text-center">fila</th>
        <th class="text-center">COLUMNA</th>
        </tr>
        </thead>
        <tbody>'''
        for error in self.listaErrores2:
            texto +='''
        <!-- ASI SE CREA UNA FILA -->
        <tr>
            <td class="text-center">'''+error.descripcion+'''</td>
            <td class="text-center">'''+str(error.fila)+'''</td>
            <td class="text-center">'''+str(error.columna)+'''</td>
        </tr>   '''
        texto +='''
        </tbody>
        </table>             
        </body>
        <hr>
        <footer>
            <h5 style="text-align: right; font-weight: bolder;">Josue Gramajo - 202000895</h5>
            <h6 style="text-align: right; font-weight: bold;">Reporte generado:'''+time.ctime()+'''</h6>
        </footer>
        </html>
        '''
        mensaje = texto 
        f.write(mensaje)
        f.close()

        webbrowser.open_new_tab('ReporteErrores.html')
    '''
obj = AnalizadorLexico()
obj.analizar('RESULTADO "Barcelona" VS "Levante" fa!@ <2019-2020>')
res = obj.imprimirTokens()

print(res)
sint = Sintactico.AnalizadorSintactico(obj.listaTokens)
sint.analizar()
# sint.imprimirErrores()
# sint.imprimirErroresNone()
'''
