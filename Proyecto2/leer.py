import csv
import time
import webbrowser
import ok
class Bot:
    def __init__(self,fecha,tempo,jornada,eq1,eq2,g1,g2):
        self.fecha = fecha
        self.tempo = tempo
        self.jornada = jornada
        self.eq1 = eq1
        self.eq2 = eq2
        self.gol1 = g1
        self.gol2 = g2

class Bot2:
    def __init__(self,tempo,jornada,eq1,eq2,g1,g2):
        self.tempo = tempo
        self.jornada = jornada
        self.eq1 = eq1
        self.eq2 = eq2
        self.g1 = g1
        self.g2 = g2

class Puntos:
    def __init__(self,name,puntos):
        self.name = name
        self.puntos = puntos

class Lecturas:
    def __init__(self):
        self.mensaje = ''
        self.data = []
        self.teams = {}

    def lectura(self):
        with open('Proyecto2/archivo.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            mycsv = []
            for row in reader:
                mycsv.append(row)
        return mycsv

    def resultadoPartido(self,equipo1,equipo2,fecha):
        '''Retorna equipos y goles'''
        reader = self.lectura()
        # equipo1 = 'Español'
        # equipo2= 'AD Almería'
        equipo1=equipo1.replace('"','')
        equipo2=equipo2.replace('"','')
        characters = "<>"
        fecha = ''.join( x for x in fecha if x not in characters)
        ans = 'El resultado fue: '
        for row in reader:
            if row['Equipo1'] == equipo1 and row['Equipo2'] == equipo2 and row['Temporada'] == fecha:
                ans += (row['Equipo1'])+ ' '
                ans+=(row['Goles1'])+' - '
                ans+=(row['Equipo2'])+' '
                ans+=(row['Goles2'])
        if ans =='El resultado fue: ':
            print('>>Revisar nombres y fechas por favor ')
            ok.mensaje = '>>Revisar nombres y fechas por favor '
        else:
            # txt.config(state='normal')
            # txt.insert('end',ans,("LEFT",))
            self.mensaje = (ans)
            # obje.mensaje.append(ans)          
            print(ans)
            ok.mensaje = ans
            return

    def resultadoJornada(self,jornada,fecha,rutaa):
        '''Retorna HMTL de jornada y temporada con todos los datos'''
        reader = self.lectura()
        characters = "<>"
        fecha = ''.join( x for x in fecha if x not in characters)
        for row in reader:
            if row['Jornada'] == jornada and row['Temporada'] == fecha:
                self.data.append(Bot(row['Fecha'],row['Temporada'],row['Jornada'],row['Equipo1'],row['Equipo2'],row['Goles1'],row['Goles2']))
       
        if rutaa == 'jornada':
            ruta = 'Proyecto2/archivos/jornada.html'
        else:
            ruta = 'Proyecto2/archivos/'+rutaa+'.html'

        texto = ''
        f = open(ruta,'w')
        texto += '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Reporte Jornada</title>
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
        <h2 class="text-center" style="font-weight: bold; color: rgb(36, 36, 179);">Datos JORNADA</h2>
        <br>
        <h6 style="font-weight:600 ;">A continuacion se presentan todos los datos recopilados en la jornada seleccionada:</h6>
        <table class="table table-hover">
            <thead class="thead-dark">
        <tr>
        <th class="text-center">FECHA</th>
        <th class="text-center">TEMPORADA</th>
        <th class="text-center">JORNADA</th>
        <th class="text-center">Equipo1</th>
        <th class="text-center">Equipo2</th>
        <th class="text-center">Goles1</th>
        <th class="text-center">Goles2</th>
        </tr>
        </thead>
        <tbody>'''
        for i in self.data:
            texto +='''
        <tr>
            <td class="text-center">'''+i.fecha+'''</td>
            <td class="text-center">'''+i.tempo+'''</td>
            <td class="text-center">'''+i.jornada+'''</td>
            <td class="text-center">'''+i.eq1+'''</td>
            <td class="text-center">'''+i.eq2+'''</td>
            <td class="text-center">'''+i.gol1+'''</td>
            <td class="text-center">'''+i.gol2+'''</td>
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
        ok.mensaje = 'Archivo generado de resultados jornada '+jornada+' Temporada '+fecha
        mensaje = texto 
        f.write(mensaje)
        f.close()
        webbrowser.open_new_tab(ruta)
        return
    
    def totalGoles(self,condicion,team,fechas):
        goles = ''
        realgoles = 0
        reader = self.lectura()
        team = team.replace('"','')
        characters = "<>"
        fechas = ''.join( x for x in fechas if x not in characters)
        print(condicion,fechas,team)
        if condicion =='LOCAL':
            for row in reader:
                if row['Temporada'] == fechas and row['Equipo1'] == team:
                    goles = (row['Goles1'])
                    realgoles += int(goles)
        elif condicion == 'VISITANTE':
            for row in reader:
                if row['Temporada'] == fechas and row['Equipo2'] == team:
                    goles = (row['Goles2'])
                    realgoles += int(goles)
        elif condicion == 'TOTAL':
            for row in reader:
                if row['Temporada'] == fechas:
                    if row['Equipo1'] == team:
                        goles = (row['Goles1'])
                        realgoles += int(goles)
                    elif row['Equipo2'] == team:
                        goles = (row['Goles2'])
                        realgoles += int(goles)
        # print(realgoles)
        ok.mensaje = 'Los goles anotados por el equipo '+ team+' en '+condicion+' en la temporada '+fechas+' fueron '+str(realgoles)+''
    
    def tablaGeneral(self,fecha,rutaa):
        gol1=gol2 = ''
        reader = self.lectura()
        characters = "<>"
        fecha = ''.join( x for x in fecha if x not in characters)
        for row in reader:
            if row['Temporada'] == fecha:
                team1 = row['Equipo1']
                team2 = row['Equipo2']
                if row['Equipo1'] in self.teams and row['Equipo2'] in self.teams:
                    continue
                else:
                    self.teams[team1]=0
                    self.teams[team2]=0
        for row in reader:
            if row['Temporada'] == fecha:
                team1 = row['Equipo1']
                team2 = row['Equipo2']
                if row['Equipo1'] in self.teams and row['Equipo2'] in self.teams:
                    gol1 = row['Goles1']
                    gol2 = row['Goles2']
                    if gol1 > gol2:
                        self.teams[team1] +=3
                    elif gol1 < gol2:
                        self.teams[team2] +=3
                    else:
                        self.teams[team1] +=1
                        self.teams[team2] +=1
                else:
                    continue
        if rutaa == 'temporada':
            ruta = 'Proyecto2/archivos/temporada.html'
        else:
            ruta = 'Proyecto2/archivos/'+rutaa+'.html'

        points = sorted(self.teams.items(),key=lambda x:x[1],reverse=True)
        for i in points:
            self.data.append(Puntos(i[0],i[1]))
        texto = ''
        f = open(ruta,'w')
        texto += '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Tabla de Puntos</title>
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
        <h2 class="text-center" style="font-weight: bold; color: rgb(36, 36, 179);">Tabla de puntos</h2>
        <br>
        <h6 style="font-weight:600 ;">A continuacion se presenta la clasificacion por puntos de la jornada:'''+fecha+'''</h6>
        <table class="table table-hover">
            <thead class="thead-dark">
        <tr>
        <th class="text-center">Equipo</th>
        <th class="text-center">Puntos</th>
        </tr>
        </thead>
        <tbody>'''
        for i in self.data:
            texto +='''
        <tr>
            <td class="text-center">'''+i.name+'''</td>
            <td class="text-center">'''+str(i.puntos)+'''</td>
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
        ok.mensaje = 'Archivo generado de clasificación de temporada '+str(fecha)+''
        print(ok.mensaje)
        mensaje = texto 
        f.write(mensaje)
        f.close()
        webbrowser.open_new_tab(ruta)
        return
    
    def temporadaEquipo(self,ruta,equipo,fecha,num1,num2):
        reader = self.lectura()
        equipo = equipo.replace('"','')
        characters = "<>"
        fecha = ''.join( x for x in fecha if x not in characters)
        goles1 = ''
        goles2 = ''
        equipo1 = ''
        equipo2 = ''
        jornada = ''
        for row in reader:
            if num2 == '' and num1 != '':
                if row['Temporada'] == fecha and row['Jornada']== num1:
                    if row['Equipo1'] == equipo :
                        equipo1 = row['Equipo1']
                        goles1 = row['Goles1']
                        equipo2 = row['Equipo2']
                        goles2 = row['Goles2']
                        self.data.append(Bot2(fecha,num1,equipo1,equipo2,goles1,goles2))
                    elif row['Equipo2'] == equipo :
                        equipo1 = row['Equipo1']
                        goles1 = row['Goles1']
                        equipo2 = row['Equipo2']
                        goles2 = row['Goles2']
                        self.data.append(Bot2(fecha,num1,equipo1,equipo2,goles1,goles2))
            elif num2 != '' and num1 == '':
                if row['Temporada'] == fecha and row['Jornada'] == num2:
                    if row['Equipo1'] == equipo:
                        equipo1 = row['Equipo1']
                        goles1 = row['Goles1']
                        equipo2 = row['Equipo2']
                        goles2 = row['Goles2']
                        self.data.append(Bot2(fecha,num2,equipo1,equipo2,goles1,goles2))
                    elif row['Equipo1'] == equipo:
                        equipo1 = row['Equipo1']
                        goles1 = row['Goles1']
                        equipo2 = row['Equipo2']
                        goles2 = row['Goles2']
                        self.data.append(Bot2(fecha,num2,equipo1,equipo2,goles1,goles2))
            
            elif num1 !='' and num2 !='':
                if row['Temporada'] == fecha: 
                    if row['Jornada']>= num1 and row['Jornada']<= num2:
                        if row['Equipo1'] == equipo:
                            equipo1 = row['Equipo1']
                            goles1 = row['Goles1']
                            equipo2 = row['Equipo2']
                            goles2 = row['Goles2']
                            jornada = row['Jornada']
                            self.data.append(Bot2(fecha,jornada,equipo1,equipo2,goles1,goles2))
                        elif row['Equipo2'] == equipo:
                            equipo1 = row['Equipo1']
                            goles1 = row['Goles1']
                            equipo2 = row['Equipo2']
                            goles2 = row['Goles2']
                            jornada = row['Jornada']
                            self.data.append(Bot2(fecha,jornada,equipo1,equipo2,goles1,goles2))
            else:
                if row['Temporada'] == fecha: 
                        if row['Equipo1'] == equipo:
                            equipo1 = row['Equipo1']
                            goles1 = row['Goles1']
                            equipo2 = row['Equipo2']
                            goles2 = row['Goles2']
                            jornada = row['Jornada']
                            self.data.append(Bot2(fecha,jornada,equipo1,equipo2,goles1,goles2))
                        elif row['Equipo2'] == equipo:
                            equipo1 = row['Equipo1']
                            goles1 = row['Goles1']
                            equipo2 = row['Equipo2']
                            goles2 = row['Goles2']
                            jornada = row['Jornada']
                            self.data.append(Bot2(fecha,jornada,equipo1,equipo2,goles1,goles2))

        if ruta != 'partidos':
            name = ruta
        else:
            name = ruta

        texto = ''
        f = open(name,'w')
        texto += '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <title>Tabla de Puntos</title>
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
        <h2 class="text-center" style="font-weight: bold; color: rgb(36, 36, 179);">Tabla de puntos</h2>
        <br>
        <h6 style="font-weight:600 ;">A continuacion se presenta la clasificacion por puntos de la jornada:'''+fecha+'''</h6>
        <table class="table table-hover">
            <thead class="thead-dark">
        <tr>
        <th class="text-center">Temporada</th>
        <th class="text-center">Jornada</th>
        <th class="text-center">Equipo 1</th>
        <th class="text-center">Equipo 2</th>
        <th class="text-center">Goles 1</th>
        <th class="text-center">Goles 2</th>
        </tr>
        </thead>
        <tbody>'''
        for i in self.data:
            texto +='''
        <tr>
            <td class="text-center">'''+i.tempo+'''</td>
            <td class="text-center">'''+i.jornada+'''</td>
            <td class="text-center">'''+i.eq1+'''</td>
            <td class="text-center">'''+i.eq2+'''</td>
            <td class="text-center">'''+i.g1+'''</td>
            <td class="text-center">'''+i.g2+'''</td>
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
        ok.mensaje = 'Archivo generado de los resultados de temporada '+str(fecha)+' del '+equipo+''
        print(ok.mensaje)
        mensaje = texto 
        f.write(mensaje)
        f.close()
        webbrowser.open_new_tab(ruta)
        return


    def Top(self,num,fecha,condicion):
        gol1=gol2 = ''
        reader = self.lectura()
        characters = "<>"
        fecha = ''.join( x for x in fecha if x not in characters)
        for row in reader:
            if row['Temporada'] == fecha:
                team1 = row['Equipo1']
                team2 = row['Equipo2']
                if row['Equipo1'] in self.teams and row['Equipo2'] in self.teams:
                    continue
                else:
                    self.teams[team1]=0
                    self.teams[team2]=0
        for row in reader:
            if row['Temporada'] == fecha:
                team1 = row['Equipo1']
                team2 = row['Equipo2']
                if row['Equipo1'] in self.teams and row['Equipo2'] in self.teams:
                    gol1 = row['Goles1']
                    gol2 = row['Goles2']
                    if gol1 > gol2:
                        self.teams[team1] +=3
                    elif gol1 < gol2:
                        self.teams[team2] +=3
                    else:
                        self.teams[team1] +=1
                        self.teams[team2] +=1
                else:
                    continue
        points = sorted(self.teams.items(),key=lambda x:x[1],reverse=True)
        for i in points:
            self.data.append(i[0])
        points_down = sorted(self.teams.items(),key=lambda x:x[1])
        data2 = []
        for i in points_down:
            data2.append(i[0])
        if condicion == 'SUPERIOR':
            if num == '5':
                ok.mensaje = """El top superior de la temporada """+fecha+""" fue:\n
                \t\t1. """+self.data[0]+"""
                \t\t2. """+self.data[1]+"""
                \t\t3. """+self.data[2]+"""
                \t\t4. """+self.data[3]+"""
                \t\t5. """+self.data[4]+"""
                            """ 
                print(ok.mensaje)
                return
            else:
                ok.mensaje = """ El top superior de la temporada """+fecha+""" fue:\n """ 
                text = ''
                numero = int(num)
                for j in range(numero):
                    text+=''+str((j+1))+'. '+self.data[j]+'\n '
                ok.mensaje+=text
                print(ok.mensaje)

        elif condicion =='INFERIOR':
            if num == '5':
                ok.mensaje = """El top superior de la temporada """+fecha+""" fue:\n
                \t\t1. """+data2[0]+"""
                \t\t2. """+data2[1]+"""
                \t\t3. """+data2[2]+"""
                \t\t4. """+data2[3]+"""
                \t\t5. """+data2[4]+"""
                            """ 
                return
            else:
                ok.mensaje = """ El top inferior de la temporada """+fecha+""" fue:\n """ 
                text = ''
                numero = int(num)
                for j in range(numero):
                    text+=''+str((j+1))+'. '+data2[j]+'\n '
                ok.mensaje+=text

# obj = Lecturas()
# obj.temporadaEquipo('okkk','Real Madrid','1979-1980','','2')