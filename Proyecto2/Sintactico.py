import time
from tkinter import N
import webbrowser
from prettytable import PrettyTable
import leer
import ok
import app
import Lexico
llamaErrores = []
class AnalizadorSintactico:

    def __init__(self,tokens : list):
        self.errores = []
        self.erroresNone = []
        self.tokens = tokens
        self.obj = leer.Lecturas()
        self.mensaje = ''
        self.tokenAux = ''
    
    def llama(self):
        llamaErrores = self.errores
        return llamaErrores
    def agregarError(self,esperado,obtenido,fila,columna):
        self.errores.append(
            '''>>ERROR SINTÁCTICO: se obtuvo {} se esperaba {} en: [{},{}]'''.format(obtenido,esperado,fila,columna)
        )
    
    def agregarErrorNone(self,esperado,obtenido):
        self.erroresNone.append(
            '''>>ERROR SINTÁCTICO: se obtuvo {} se esperaba {}'''.format(obtenido,esperado)
        )
    
    def sacarToken(self):
        ''' Saca el primer token y lo quita de la lista'''
        try:
            return self.tokens.pop(0)
        except:
            return None

    def observarToken(self):
        ''' Saca el primer token y lo mete de nuevo en de la lista'''
        try:
            return self.tokens[0]
        except:
            return None

    def analizar(self):
        self.S()

    def S(self):
        self.INICIO()

    def INICIO(self):
        # Observar el primer elemento para
        # decidir a donde ir
        tmp = self.observarToken()
        if tmp is None:
            self.agregarError("res_RESULTADO | res_JORNADA | res_GOLES | res_TABLA  res_PARTIDOS | res_TOP | res_ADIOS",'EMPTY','1','1')
        elif tmp.tipo == 'res_RESULTADO':
            self.RESULTADO()
        elif tmp.tipo == 'res_JORNADA':
            self.JORNADA()
        elif tmp.tipo == 'res_GOLES':
            self.GOLES()
        elif tmp.tipo == 'res_TABLA':
            self.TABLA()
        elif tmp.tipo == 'res_PARTIDOS':
            self.PARTIDOS()
        elif tmp.tipo == 'res_TOP':
            self.TOP()
        elif tmp.tipo == 'res_ADIOS':
            print('ENTRA')
        else:
            self.agregarError("res_RESULTADO | res_JORNADA | res_GOLES | res_TABLA | res_TEMPORADA | res_PARTIDOS | res_TOP | res_ADIOS",'-'+tmp.tipo+'-','1','1')
            mensaje = self.errores[0]
            ok.mensaje = mensaje
  
    def RESULTADO(self):
        '''Resultado de un partido  '''
    # Produccion
        # <RESULTADO> ::= res_resultado cadena res_vs cadena res_temp tk_years

    # Sacar token --- se espera res_resultado
        token = self.sacarToken()
        if token.tipo == 'res_RESULTADO':
            # Sacar otro token -- se espera cadena
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone("Cadena","EOF")
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == "Cadena":
                equipo1 = token.lexema
                # Sacar otro token -- se espera res_VS
                token = self.sacarToken()
                if token is None:
                    self.agregarErrorNone("res_VS","EOF")
                    mensaje = self.erroresNone[0]
                    ok.mensaje = mensaje
                    return
                elif token.tipo == "res_VS":
                    # Sacar otro token -- se espera res_VS
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone("Cadena","EOF")
                        mensaje = self.erroresNone[0]
                        ok.mensaje = mensaje
                        return
                    elif token.tipo == 'Cadena':
                        equipo2 = token.lexema
                    # Sacar otro token -- se espera res_temp
                        token = self.sacarToken()
                        token2 = self.observarToken()
                        if token is None:
                            self.agregarErrorNone("res_TEMPORADA","EOF")
                            mensaje = self.erroresNone[0]
                            ok.mensaje = mensaje
                            return
                        elif token.tipo == 'res_TEMPORADA':
                            # Sacar otro token -- se espera tk_years
                            token = self.sacarToken()
                            if token is None:
                                self.agregarErrorNone("tk_temporada","EOF")
                                mensaje = self.erroresNone[0]
                                ok.mensaje = mensaje
                                return
                            elif token.tipo == 'tk_temporada':
                                fecha = token.lexema
                                #YA TERMINO EL ANALISIS #
                                #LLAMO funcionalidad
                                print('CADENA CORRECTA PAPSSS')
                                self.obj.resultadoPartido(equipo1,equipo2,fecha)
                            else:
                                self.agregarError("tk_temporada",token.tipo,token.fila,token.columna)
                                mensaje = self.errores[0]
                                ok.mensaje = mensaje
                        elif token.tipo == 'tk_temporada':
                            self.agregarError('res_TEMPORADA',token.tipo,1,token.columna)
                            fecha = token.lexema
                            self.obj.resultadoPartido(equipo1,equipo2,fecha)
                        elif token2.tipo == 'tk_temporada':
                            self.agregarError('res_TEMPORADA',token.tipo,1,token.columna)
                            fecha = token2.lexema
                            self.obj.resultadoPartido(equipo1,equipo2,fecha)
                        else:
                            self.agregarError("res_TEMPORADA",token2.tipo,token2.fila,token2.columna)
                            mensaje = self.errores[0]
                            ok.mensaje = mensaje
                    else:
                        self.agregarError("cadena",token.tipo,token.fila,token.columna)
                        mensaje = self.errores[0]
                        ok.mensaje = mensaje
                else:
                    self.agregarError("res_VS",token.tipo,token.fila,token.columna)
                    mensaje = self.errores[0]
                    ok.mensaje = mensaje
            else:
                self.agregarError("cadena",token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        else:
            self.agregarError("res_RESULTADO",'EMPTY','1','1')
            mensaje = self.errores[0]
            ok.mensaje = mensaje

    def JORNADA(self):
        '''HTML de todos los partidos de una jornada y temporada'''
        #Produccion
            # <JORNADA> ::= res_jornada tk_num res_temp tk_temporada <JORNADA'>
            # <JORNADA'> ::= tk_flag tk_id
            #             | epsilon

        # Sacar token --- se espera res_jornada
        token = self.sacarToken()
        if token is None:
            self.agregarErrorNone('res_JORNADA','EOF')
            mensaje = self.erroresNone[0]
            ok.mensaje = mensaje
            return
        elif token.tipo == 'res_JORNADA':
            # Sacar token --- se espera tk_num
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('tk_num','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == 'tk_num':
                # Sacar token --- se espera res_temp
                num = token.lexema
                token = self.sacarToken()
                if token is None:
                    self.agregarErrorNone('res_TEMPORADA','EOF')
                    mensaje = self.erroresNone[0]
                    ok.mensaje = mensaje
                    return
                elif token.tipo == 'res_TEMPORADA':
                    # Sacar token --- se espera tk_temporada
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('tk_temporada','EOF')
                        mensaje = self.erroresNone[0]
                        ok.mensaje = mensaje
                        return
                    elif token.tipo == 'tk_temporada':
                        #debo mandar a llamar a JORNADA'
                        fecha = token.lexema
                        self.JORNADA_(num,fecha)
                    else:
                        self.agregarError('tk_temporada',token.tipo,token.fila,token.columna)
                        mensaje = self.errores[0]
                        ok.mensaje = mensaje
                else:
                    self.agregarError('res_TEMPORADA',token.tipo,token.fila,token.columna)
                    mensaje = self.errores[0]
                    ok.mensaje = mensaje
            else:
                self.agregarError('tk_num',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        else:
            self.agregarError('res_JORNADA',token.tipo,token.fila,token.columna)
            mensaje = self.errores[0]
            ok.mensaje = mensaje

    def JORNADA_(self,num,fecha):
        ''''''
        #Produccion:
            #<JORNADA'> ::= tk_flag tk_id
            #            | epsilon

        token = self.observarToken()
        if token is None:
            self.obj.resultadoJornada(num,fecha,'jornada')
            return
        if token.tipo == 'res_-f':
            token = self.sacarToken()
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('ID','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == 'ID':
                id = token.lexema
                self.obj.resultadoJornada(num,fecha,id)
                return
            else:
                self.agregarError('ID',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        else:
            self.agregarError('res_flag',token.tipo,token.fila,token.columna)
            mensaje = self.errores[0]
            ok.mensaje = mensaje

    def GOLES(self):
    #Produccion:
        #<GOLES> ::= res_goles <GOLES'> cadena res_temp tk_jornada

        token = self.sacarToken()
        if token is None:
            self.agregarErrorNone('res_GOLES','EOF')
            mensaje = self.erroresNone[0]
            ok.mensaje = mensaje
            return
        elif token.tipo == 'res_GOLES':
            condicion = self.GOLES_()
            if condicion is None:
                self.agregarErrorNone('Condicion','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            else:
                token = self.sacarToken()
                if token is None:
                    self.agregarErrorNone('Cadena','EOF')
                    mensaje = self.erroresNone[0]
                    ok.mensaje = mensaje
                    return
                elif token.tipo == 'Cadena':
                    team = token.lexema
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('res_TEMPORADA','EOF')
                        mensaje = self.erroresNone[0]
                        ok.mensaje = mensaje
                        return
                    elif token.tipo == 'res_TEMPORADA':
                        token = self.sacarToken()
                        if token is None:
                            self.agregarErrorNone('tk_temporada','EOF')
                            mensaje = self.erroresNone[0]
                            ok.mensaje = mensaje
                            return
                        elif token.tipo == 'tk_temporada':
                            temporada = token.lexema
                            #llamar funcion
                            self.obj.totalGoles(condicion,team,temporada)
                        else:
                            self.agregarError('tk_temporada',token.tipo,token.fila,token.columna)
                            mensaje = self.errores[0]
                            ok.mensaje = mensaje
                    else:
                        self.agregarError('res_TEMPORADA',token.tipo,token.fila,token.columna)
                        mensaje = self.errores[0]
                        ok.mensaje = mensaje
                else:
                    self.agregarError('Cadena',token.tipo,token.fila,token.columna)
                    mensaje = self.errores[0]
                    ok.mensaje = mensaje
        else:
            self.agregarError('res_GOLES',token.tipo,token.fila,token.columna)
            mensaje = self.errores[0]
            ok.mensaje = mensaje

    def GOLES_(self):
        #<GOLES'> ::= res_local |  res_visitante |  res_total
        token = self.sacarToken()
        if token is None:
            return
        if token.tipo == 'res_LOCAL':
            condicion = token.lexema
            return condicion
        elif token.tipo == 'res_VISITANTE':
            condicion = token.lexema
            return condicion
        elif token.tipo == 'res_TOTAL':
            condicion = token.lexema
            return condicion
        else:
            self.agregarError('res_local |  res_visitante |  res_total',token.tipo,token.fila,token.columna)

    def TABLA(self):
        #Produccion:
        #   <TABLA> ::= res_TABLA res_temp tk_years <TABLA TEMPORADA'>    
        token = self.sacarToken()
        if token is None:
            self.agregarErrorNone('res_TABLA','EOF')
            mensaje = self.erroresNone[0]
            ok.mensaje = mensaje
            return
        elif token.tipo == 'res_TABLA':
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('res_TEMPORADA','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == 'res_TEMPORADA':
                token = self.sacarToken()
                if token is None:
                    self.agregarErrorNone('tk_temporada','EOF')
                    mensaje = self.erroresNone[0]
                    ok.mensaje = mensaje
                    return
                elif token.tipo == 'tk_temporada':
                    jornada = token.lexema
                    self.TABLA_(jornada)
                else:
                    self.agregarError('tk_temporada',token.tipo,token.fila,token.columna)
                    mensaje = self.errores[0]
                    ok.mensaje = mensaje
            else:
                self.agregarError('res_TEMPORADA',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        else:
            self.agregarError('res_TABLA',token.tipo,token.fila,token.columna)
            mensaje = self.errores[0]
            ok.mensaje = mensaje

    def TABLA_(self,jornada):
    #Produccion:
        # <TABLA'> ::= tk_flag tk_id
        #           |  epsilon
        token = self.observarToken()
        if token is None:
            self.obj.tablaGeneral(jornada,'temporada')
            return
        if token.tipo == 'res_-f':
            token = self.sacarToken()
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('ID','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == 'ID':
                Id = token.lexema
                self.obj.tablaGeneral(jornada,Id)
            else:
                self.agregarError('ID',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        else:
                self.agregarError('res_flag',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje


    def PARTIDOS(self):
        # Produccion:
            # res_partidos cadena res_temp tk_years <PARTIDOS'>
        token = self.sacarToken()
        if token is None:
            self.agregarErrorNone('res_PARTIDOS','EOF')
            mensaje = self.erroresNone[0]
            ok.mensaje = mensaje
            return
        elif token.tipo == 'res_PARTIDOS':
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('Cadena','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == 'Cadena':
                equipo = token.lexema
                token = self.sacarToken()
                if token is None:
                    self.agregarErrorNone('res_TEMPORADA','EOF')
                    mensaje = self.erroresNone[0]
                    ok.mensaje = mensaje
                    return
                elif token.tipo == 'res_TEMPORADA':
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('tk_temporada','EOF')
                        mensaje = self.erroresNone[0]
                        ok.mensaje = mensaje
                        return
                    elif token.tipo == 'tk_temporada':
                        tempo = token.lexema
                        #Llamo a mi otra funcion
                        self.PARTIDOS_(equipo,tempo)
                    else:
                        self.agregarError('tk_temporada',token.tipo,token.fila,token.columna)
                        mensaje = self.errores[0]
                        ok.mensaje = mensaje
                else:
                        self.agregarError('res_TEMPORADA',token.tipo,token.fila,token.columna)
                        mensaje = self.errores[0]
                        ok.mensaje = mensaje
            else:
                self.agregarError('Cadena',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        else:
            self.agregarError('res_PARTIDOS',token.tipo,token.fila,token.columna)
            mensaje = self.errores[0]

#PENDIENTE DE COMPLETARRRRRR
    def PARTIDOS_(self,equipo,tempo):
        #Produccion:
        '''<PARTIDOS'> ::= res_flag tk_id
             |  res_ji tk_num
             |  res_jf tk_num
             |  epsilon'''
        token = self.observarToken()
        if token is None:
            self.obj.temporadaEquipo('partidos',equipo,tempo,'','')
            return
        if token.tipo == 'res_-f':
            token = self.sacarToken()
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('ID','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == 'ID':
                name = token.lexema
                token = self.observarToken()
                if token is None:
                    self.obj.temporadaEquipo(name,equipo,tempo,'','')
                    return
                elif token.tipo == 'res_-ji':
                    token = self.sacarToken()
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('tk_num','EOF')
                        mensaje = self.erroresNone[0]
                        ok.mensaje = mensaje
                        return
                    elif token.tipo == 'tk_num':
                        num1 = token.lexema
                        token = self.sacarToken()
                        if token is None:
                            self.obj.temporadaEquipo(name,equipo,tempo,num1,'')
                            return
                        elif token.tipo == 'res_-jf':
                            token = self.sacarToken()
                            if token is None:
                                self.agregarErrorNone('tk_num','EOF')
                                mensaje = self.erroresNone[0]
                                ok.mensaje = mensaje
                                return
                            elif token.tipo == 'tk_num':
                                num2 = token.lexema
                                self.obj.temporadaEquipo(name,equipo,tempo,num1,num2)
                                return
                            else:
                                self.agregarError('tk_num',token.tipo,token.fila,token.columna)
                                mensaje = self.errores[0]
                                ok.mensaje = mensaje
                        else:
                            self.agregarError('res_jf',token.tipo,token.fila,token.columna)
                            mensaje = self.errores[0]
                            ok.mensaje = mensaje
                    else:
                        self.agregarError('tk_num',token.tipo,token.fila,token.columna)
                        mensaje = self.errores[0]
                        ok.mensaje = mensaje
                elif token.tipo == 'res_-jf':
                    token = self.sacarToken()
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('tk_num','EOF')
                        mensaje = self.erroresNone[0]
                        ok.mensaje = mensaje
                        return
                    elif token.tipo == 'tk_num':
                        num2 = token.lexema
                        self.obj.temporadaEquipo(name,equipo,tempo,'',num2)
                        print('Vino nombre y jf ')
                        
                else:
                    self.agregarError('res_-ji | res_-jf',token.tipo,token.fila,token.columna)
                    mensaje = self.errores[0]
                    ok.mensaje = mensaje
            else:
                self.agregarError('ID',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        elif token.tipo == 'res_-ji':
            token = self.sacarToken()
            token = self.sacarToken()
            if token.tipo is None:
                self.agregarErrorNone('tk_num','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == 'tk_num':
                num1 = token.lexema
                token = self.sacarToken()
                if token is None:
                    self.obj.temporadaEquipo('partidos',equipo,tempo,num1,'')
                elif token.tipo == 'res_-jf':
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('tk_num','EOF')
                        mensaje=self.erroresNone[0]
                        ok.mensaje = mensaje
                        return
                    elif token.tipo == 'tk_num':
                        num2 = token.lexema
                        self.obj.temporadaEquipo('partidos',equipo,tempo,num1,num2)
                    else:
                        self.agregarError('tk_num',token.tipo,token.fila,token.columna)
                        mensaje = self.errores[0]
                        ok.mensaje = mensaje
                else:
                    self.agregarError('res_-ji',token.tipo,token.fila,token.columna)
                    mensaje = self.errores[0]
                    ok.mensaje = mensaje
            else:
                self.agregarError('res_-ji',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        else:
                self.agregarError('res_flag',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
                
    def TOP(self):
        # res_top res_sup res_temp tk_years <TOP'>
#       |  res_top res_inf res_temp tk_years <TOP'>      
        token = self.sacarToken()
        if token is None:
            self.agregarErrorNone('res_TOP','EOF')
            mensaje = self.erroresNone[0]
            ok.mensaje = mensaje
            return
        elif token.tipo == 'res_TOP':
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('res_SUPERIOR | res_INFERIOR','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == 'res_SUPERIOR' or token.tipo == 'res_INFERIOR':
                condicion = token.lexema
                token = self.sacarToken()
                if token is None:
                    self.agregarErrorNone('res_TEMPORADA','EOF')
                    mensaje = self.erroresNone[0]
                    ok.mensaje = mensaje
                    return
                elif token.tipo == 'res_TEMPORADA':
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('tk_temporada','EOF')
                        mensaje = self.erroresNone[0]
                        ok.mensaje = mensaje
                    elif token.tipo == 'tk_temporada':
                        fecha = token.lexema
                        self.TOP_(fecha,condicion)
                    else:
                        self.agregarError('tk_temporada','EOF')
                        mensaje = self.errores[0]
                        ok.mensaje = mensaje
                        return
                else:
                    self.agregarError('res_TEMPORADA',token.tipo,token.fila,token.columna)
                    mensaje = self.errores[0]
                    ok.mensaje = mensaje
            else:
                self.agregarError('res_SUPERIOR | res_INFERIOR',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        else:
            self.agregarError('res_TOP',token.tipo,token.fila,token.columna)
            mensaje = self.errores[0]
            ok.mensaje = mensaje


    def TOP_(self,fecha,condicion):
        num = '5'
        token = self.observarToken()
        if token is None:
            self.obj.Top(num,fecha,condicion)
            return
        if token.tipo == 'res_-n':
            token = self.sacarToken()
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('ID','EOF')
                mensaje = self.erroresNone[0]
                ok.mensaje = mensaje
                return
            elif token.tipo == 'tk_num':
                num = token.lexema
                self.obj.Top(num,fecha,condicion)
                return
            else:
                self.agregarError('tk_num',token.tipo,token.fila,token.columna)
                mensaje = self.errores[0]
                ok.mensaje = mensaje
        else:
            self.agregarError('res_-n',token.tipo,token.fila,token.columna)
            mensaje = self.errores[0]
            ok.mensaje = mensaje

    def imprimirErrores(self):
        '''Imprime una tabla con los errores'''
        x = PrettyTable()
        x.field_names = ["Descripcion"]
        for error_ in self.errores:
            x.add_row([error_])
            print(x)            

    def imprimirErroresNone(self):
        '''Imprime una tabla con los errores'''
        x = PrettyTable()
        x.field_names = ["Descripcion"]
        for error_ in self.erroresNone:
            x.add_row([error_])
        print(x)            

    def crearT(self):
        texto = ''
        f = open('./ReporteErroresSintacticos.html','w')
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
        for error in self.errores:
            texto +='''
        <!-- ASI SE CREA UNA FILA -->
        <tr>
            <td class="text-center">'''+error.esperado+'''</td>
            <td class="text-center">'''+error.obtenido+'''</td>
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

        webbrowser.open_new_tab('ReporteErroresSintacticos.html')
