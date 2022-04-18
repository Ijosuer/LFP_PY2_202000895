import csv
import time
import webbrowser
class Bot:
    def __init__(self,fecha,tempo,jornada,eq1,eq2,gol1,gol2):
        self.fecha = fecha
        self.tempo = tempo
        self.jornada = jornada
        self.eq1 = eq1
        self.eq2 = eq2
        self.gol1 = gol1
        self.gol2 = gol2

class Lecturas:
    def __init__(self):
        self.data = []
    def lectura(self):
        with open('Proyecto2/archivo1.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            mycsv = []
            for row in reader:
                mycsv.append(row)
        return mycsv

    def resultadoPartido(self):
        '''Retorna equipos y goles'''
        reader = self.lectura()
        equipos = []
        equipo1 = 'Español'
        equipo2= 'AD Almería'
        equipos.append(equipo1)
        equipos.append(equipo2)
        ans = 'El resultado fue: '
        for row in reader:
            if row['Equipo1'] in equipos:
                ans += (row['Equipo1'])+ ' '
                ans+=(row['Goles1'])+' - '
            if row['Equipo2'] in equipos:
                ans+=(row['Equipo2'])+' '
                ans+=(row['Goles2'])
        print(ans)
    def resultadoJornada(self):
        '''Retorna HMTL de jornada y temporada con todos los datos'''
        reader = self.lectura()
        numero = '2'
        temporada = '1981-1982'
        listaData = []
        for row in reader:
            if row['Jornada'] == numero and row['Temporada'] == temporada:
                self.data.append(Bot(row['Fecha'],row['Temporada'],row['Jornada'],row['Equipo1'],row['Equipo2'],row['Goles1'],row['Goles2']))
       

        texto = ''
        f = open('Proyecto2/archivos/jornada.html','w')
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
        mensaje = texto 
        f.write(mensaje)
        f.close()
        webbrowser.open_new_tab('Proyecto2/archivos/jornada.html')
    def totalGoles():
        pass
    def tablaGeneral():
        pass
    def temporadaEquipo():
        pass
    def Top():
        pass
obj = Lecturas()
obj.resultadoJornada()