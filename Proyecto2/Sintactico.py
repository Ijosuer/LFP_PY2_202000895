from prettytable import PrettyTable
import leer
class AnalizadorSintactico:

    def __init__(self,tokens : list):
        self.errores = []
        self.erroresNone = []
        self.tokens = tokens
        self.obj = leer.Lecturas()
        
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
            print('ENTRA')
        elif tmp.tipo == 'res_ADIOS':
            print('ENTRA')
        else:
            self.agregarError("res_RESULTADO | res_JORNADA | res_GOLES | res_TABLA | res_TEMPORADA | res_PARTIDOS | res_TOP | res_ADIOS",'-'+tmp.tipo+'-','1','1')

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
                self.agregarError("Cadena","EOF",'1','1')
                return
            elif token.tipo == "Cadena":
                equipo1 = token.lexema
                # Sacar otro token -- se espera res_VS
                token = self.sacarToken()
                if token is None:
                    self.agregarError("res_VS","EOF",'1','1')
                    return
                elif token.tipo == "res_VS":
                    # Sacar otro token -- se espera res_VS
                    token = self.sacarToken()
                    if token is None:
                        self.agregarError("Cadena","EOF",'1','1')
                        return
                    elif token.tipo == 'Cadena':
                        equipo2 = token.lexema
                    # Sacar otro token -- se espera res_temp
                        token = self.sacarToken()
                        token2 = self.observarToken()
                        if token is None:
                            self.agregarError("res_TEMPORADA","EOF",'1','1')
                        elif token.tipo == 'res_TEMPORADA':
                            # Sacar otro token -- se espera tk_years
                            token = self.sacarToken()
                            if token is None:
                                self.agregarError("tk_temporada","EOF",'1','1')
                                return
                            elif token.tipo == 'tk_temporada':
                                fecha = token.lexema
                                #YA TERMINO EL ANALISIS #
                                #LLAMO funcionalidad
                                print('CADENA CORRECTA PAPSSS')
                                self.obj.resultadoPartido(equipo1,equipo2,fecha)
                            else:
                                self.agregarError("tk_temporada",token.tipo,token.fila,token.columna)
                        elif token2.tipo == 'tk_temporada':
                                self.agregarError('res_TEMPORADA',token.tipo,1,token.columna)
                                fecha = token2.lexema
                                print('CADENA CORRECTA PAPSSS')
                                self.obj.resultadoPartido(equipo1,equipo2,fecha)
                        else:
                            self.agregarError("res_TEMPORADA",token2.tipo,token2.fila,token2.columna)
                    else:
                        self.agregarError("cadena",token.tipo,token.fila,token.columna)
                else:
                    self.agregarError("res_VS",token.tipo,token.fila,token.columna)
            else:
                self.agregarError("cadena",token.tipo,token.fila,token.columna)
        else:
            self.agregarError("res_RESULTADO",'EMPTY','1','1')

    def JORNADA(self):
        '''HTML de todos los partidos de una jornada y temporada'''
        #Produccion
            # <JORNADA> ::= res_jornada tk_num res_temp tk_temporada <JORNADA'>
            # <JORNADA'> ::= tk_flag tk_id
            #             | epsilon

        # Sacar token --- se espera res_jornada
        token = self.sacarToken()
        if token is None:
            self.agregarError('res_JORNADA','EOF','1','1')
            return
        elif token.tipo == 'res_JORNADA':
            # Sacar token --- se espera tk_num
            token = self.sacarToken()
            if token is None:
                self.agregarError('tk_num','EOF','1','1')
                return
            elif token.tipo == 'tk_num':
                # Sacar token --- se espera res_temp
                token = self.sacarToken()
                if token is None:
                    self.agregarError('res_TEMPORADA','EOF','1','1')
                    return
                elif token.tipo == 'res_TEMPORADA':
                    # Sacar token --- se espera tk_temporada
                    token = self.sacarToken()
                    if token is None:
                        self.agregarError('tk_temporada','EOF','1','1')
                        return
                    elif token.tipo == 'tk_temporada':
                        #debo mandar a llamar a JORNADA'
                        self.JORNADA_()
                    else:
                        self.agregarError('tk_temporada',token.tipo,token.fila,token.columna)
                else:
                    self.agregarError('res_TEMPORADA',token.tipo,token.fila,token.columna)
            else:
                self.agregarError('tk_num',token.tipo,token.fila,token.columna)
        else:
            self.agregarError('res_JORNADA',token.tipo,token.fila,token.columna)

    def JORNADA_(self):
        ''''''
        #Produccion:
            #<JORNADA'> ::= tk_flag tk_id
            #            | epsilon

        token = self.observarToken()
        if token is None:
            print('Se acepta paps')
            return
        if token.tipo == 'res_-f':
            token = self.sacarToken()
            token = self.sacarToken()
            if token is None:
                self.agregarError('ID','EOF','1','1')
                return
            elif token.tipo == 'ID':
                print('Se acepta y cambia nombre')
            else:
                self.agregarError('ID',token.tipo,token.fila,token.columna)
        else:
                self.agregarError('res_flag',token.tipo,token.fila,token.columna)

    def GOLES(self):
    #Produccion:
        #<GOLES> ::= res_goles <GOLES'> cadena res_temp tk_jornada

        token = self.sacarToken()
        if token is None:
            self.agregarError('res_GOLES','EOF','1','1')
            return
        elif token.tipo == 'res_GOLES':
            condicion = self.GOLES_()
            if condicion is None:
                self.agregarErrorNone('Condicion','EOF')
                return
            else:
                token = self.sacarToken()
                if token is None:
                    self.agregarErrorNone('Cadena','EOF')
                    return
                elif token.tipo == 'Cadena':
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('res_TEMPORADA','EOF')
                        return
                    elif token.tipo == 'res_TEMPORADA':
                        token = self.sacarToken()
                        if token is None:
                            self.agregarErrorNone('tk_temporada','EOF')
                        elif token.tipo == 'tk_temporada':
                            temporada = token.lexema
                            #llamar funcion
                            print('DE UÑAAAAA PERRI')
                        else:
                            self.agregarError('tk_temporada',token.tipo,token.fila,token.columna)
                    else:
                        self.agregarError('res_TEMPORADA',token.tipo,token.fila,token.columna)
                else:
                    self.agregarError('Cadena',token.tipo,token.fila,token.columna)
        else:
            self.agregarError('res_GOLES',token.tipo,token.fila,token.columna)

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
            return
        elif token.tipo == 'res_TABLA':
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('res_TEMPORADA','EOF')
            elif token.tipo == 'res_TEMPORADA':
                token = self.sacarToken()
                if token is None:
                    self.agregarErrorNone('tk_temporada','EOF')
                elif token.tipo == 'tk_temporada':
                    jornada = token.lexema
                    self.TABLA_()
                else:
                    self.agregarError('tk_temporada',token.tipo,token.fila,token.columna)
            else:
                self.agregarError('res_TEMPORADA',token.tipo,token.fila,token.columna)
        else:
            self.agregarError('res_TABLA',token.tipo,token.fila,token.columna)

    def TABLA_(self):
    #Produccion:
        # <TABLA'> ::= tk_flag tk_id
        #           |  epsilon
        token = self.observarToken()
        if token is None:
            print('Se acepta paps')
            return
        if token.tipo == 'res_-f':
            token = self.sacarToken()
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('ID','EOF')
                return
            elif token.tipo == 'ID':
                print('Se acepta y cambia nombre')
            else:
                self.agregarError('ID',token.tipo,token.fila,token.columna)
        else:
                self.agregarError('res_flag',token.tipo,token.fila,token.columna)


    def PARTIDOS(self):
        # Produccion:
            # res_partidos cadena res_temp tk_years <PARTIDOS'>
        token = self.sacarToken()
        if token is None:
            self.agregarErrorNone('res_PARTIDOS','EOF')
            return
        elif token.tipo == 'res_PARTIDOS':
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('Cadena','EOF')
                return
            elif token.tipo == 'Cadena':
                token = self.sacarToken()
                if token is None:
                    self.agregarErrorNone('res_TEMPORADA','EOF')
                    return
                elif token.tipo == 'res_TEMPORADA':
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('tk_temporada','EOF')
                        return
                    elif token.tipo == 'tk_temporada':
                        #Llamo a mi otra funcion
                        self.PARTIDOS_()
                    else:
                        self.agregarError('tk_temporada',token.tipo,token.fila,token.columna)
                else:
                        self.agregarError('res_TEMPORADA',token.tipo,token.fila,token.columna)
            else:
                self.agregarError('Cadena',token.tipo,token.fila,token.columna)
        else:
            self.agregarError('res_PARTIDOS',token.tipo,token.fila,token.columna)
#PENDIENTE DE COMPLETARRRRRR
    def PARTIDOS_(self):
        #Produccion:
        '''<PARTIDOS'> ::= res_flag tk_id
             |  res_ji tk_num
             |  res_jf tk_num
             |  epsilon'''
        token = self.observarToken()
        if token is None:
            print('Se acepta paps')
            return
        if token.tipo == 'res_-f':
            token = self.sacarToken()
            token = self.sacarToken()
            if token is None:
                self.agregarErrorNone('ID','EOF')
                return
            elif token.tipo == 'ID':
                token = self.observarToken()
                if token is None:
                    print('Se acepta y cambia nombre')
                    return
                elif token.tipo == 'res_-ji':
                    token = self.sacarToken()
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('tk_num','EOF')
                        return
                    elif token.tipo == 'tk_num':
                        token = self.sacarToken()
                        if token is None:
                            print('VINIERON 1 Y NOMBRE')
                            return
                        elif token.tipo == 'res_-jf':
                            token = self.sacarToken()
                            if token is None:
                                self.agregarErrorNone('tk_num','EOF')
                                return
                            elif token.tipo == 'tk_num':
                                print('VINIERON LAS 3')
                                return
                            else:
                                self.agregarError('tk_num',token.tipo,token.fila,token.columna)
                        else:
                            self.agregarError('res_jf',token.tipo,token.fila,token.columna)
                    else:
                        self.agregarError('tk_num',token.tipo,token.fila,token.columna)
                elif token.tipo == 'res_-jf':
                    token = self.sacarToken()
                    token = self.sacarToken()
                    if token is None:
                        self.agregarErrorNone('tk_num','EOF')
                    elif token == 'tk_num':
                        print('VINIERON LAS 3')
                        return
                else:
                    self.agregarError('res_ji | res_jf',token.tipo,token.fila,token.columna)
            else:
                self.agregarError('ID',token.tipo,token.fila,token.columna)
        elif token.tipo == 'res_ji':
            token = self.sacarToken()
            token = self.sacarToken()
            if token.tipo is None:
                self.agregarErrorNone('tk_num','EOF')
            elif token.tipo == 'tk_num':
                print('vino ji y numero chido then')
        else:
                self.agregarError('res_flag',token.tipo,token.fila,token.columna)
            

    def imprimirErrores(self):
        '''Imprime una tabla con los errores'''
        x = PrettyTable()
        x.field_names = ["Descripcion"]
        for error_ in self.errores:
            print(error_)            

    def imprimirErroresNone(self):
        '''Imprime una tabla con los errores'''
        x = PrettyTable()
        x.field_names = ["Descripcion"]
        for error_ in self.erroresNone:
            print(error_)            
