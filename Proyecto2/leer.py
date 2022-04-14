import csv
listaFechas = []
listaTempo = []
listaJornada = []
listaEquipo1 = []
listaEquipo2 = []
listaGoles1 = []
listaGoles2 = []
with open('Proyecto2/archivo.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        listaFechas.append(row['Fecha'])
        listaTempo.append(row['Temporada'])
        listaJornada.append(row['Jornada'])
        listaEquipo1.append(row['Equipo1'])
        listaEquipo2.append(row['Equipo2'])
        listaGoles1.append(row['Goles1'])
        listaGoles2.append(row['Goles2'])
# print(listaFechas)
# print(listaTempo)
# print(listaJornada)
# print(listaEquipo1)
# print(listaEquipo2)
# print(listaGoles1)
# print(listaGoles2)