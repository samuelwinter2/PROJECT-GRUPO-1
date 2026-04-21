import matplotlib.pyplot as plt

class Airport:
    def __init__(self, ICAO, latitude, longitude, Schengen=False):
        self.ICAO = ICAO
        self.latitude = latitude
        self.longitude = longitude
        self.Schengen = Schengen

schengen =['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH','BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES','LS']

def IsSchengenAirport (code):
    i = 0
    encontrado=False
    while i < len(schengen) and not encontrado:
        if code[:2] == schengen[i]:
            encontrado = True
        else:
            i = i + 1
    if encontrado:
        return True
    else:
        return False

def SetSchengen(airport):
    airport.Schengen = IsSchengenAirport(airport.ICAO)

def PrintAirport (airport):
    print("ICAO:", airport.ICAO)
    print("Schengen:", airport.Schengen)
    print("Latitude:", airport.latitude)
    print("Longitude:", airport.longitude)


def LoadAirports(filename):
    airports = []

    try:
        F = open(filename, 'r')
        lineas = F.readlines()
        F.close()
        i = 1 #para no contar los titulos
        while i<len(lineas):
            linea = lineas[i]
            partes = linea.split()
            code = partes[0]
            lat = partes[1]
            lon = partes[2]
            #latitud
            if lat[0] == "N":
                signo_lat = 1
            else:
                signo_lat = -1
            grados = int(lat[1:3])
            minutos = int(lat[3:5])
            segundos = int(lat[5:7])
            lat = signo_lat * (grados + minutos / 60 + segundos / 3600)

            # longitud
            if lon[0] == 'E':
                signo_lon = 1
            else:
                signo_lon = -1
            grados = int(lon[1:4])
            minutos = int(lon[4:6])
            segundos = int(lon[6:8])
            lon = signo_lon * (grados + minutos / 60 + segundos / 3600)

            airport = Airport(code, lat, lon)
            airports.append(airport)
            i = i + 1

    except:
        return []

    return airports

def SaveSchengenAirports (airports, filename):
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1

    cuenta = 0
    i = 0
    while i < len(airports):
        if airports[i].Schengen:
            cuenta = cuenta + 1
        i = i + 1
    if cuenta == 0:
        print("No hay aeropuertos Schengen para guardar.")

    try:
            F = open(filename, 'w')
            F.write("ICAO Latitude Longitude")
            i = 0
            while i < len(airports):
                airport = airports[i]
                if airport.Schengen:
                    if airport.latitude >= 0:
                        lat_signo = 'N'
                        lat_dec = airport.latitude
                    else:
                        lat_signo = 'S'
                        lat_dec = -airport.latitude
                    lat_ent = int(lat_dec)
                    lat_min = int((lat_dec - lat_ent) * 60)
                    lat_seg = int(((lat_dec - lat_ent) * 60 - lat_min) * 60)

                    # añadir ceros a minutos
                    if lat_min < 10:
                        lat_min_str = "0" + str(lat_min)
                    else:
                        lat_min_str = str(lat_min)

                    # añadir ceros a segundos
                    if lat_seg < 10:
                        lat_seg_str = "0" + str(lat_seg)
                    else:
                        lat_seg_str = str(lat_seg)

                    # grados
                    if lat_ent < 10:
                        lat_ent_str = "0" + str(lat_ent)
                    else:
                        lat_ent_str = str(lat_ent)

                    lat_str = lat_signo + lat_ent_str + lat_min_str + lat_seg_str

                    if airport.longitude >= 0:
                        lon_signo = 'E'
                        lon_dec = airport.longitude
                    else:
                        lon_signo = 'W'
                        lon_dec = -airport.longitude

                    lon_ent = int(lon_dec)
                    lon_min = int((lon_dec - lon_ent) * 60)
                    lon_seg = int((((lon_dec - lon_ent) * 60) - lon_min) * 60)

                    # grados (longitud 3 dígitos)
                    if lon_ent < 10:
                        lon_ent_str = "00" + str(lon_ent)
                    elif lon_ent < 100:
                        lon_ent_str = "0" + str(lon_ent)
                    else:
                        lon_ent_str = str(lon_ent)

                    # minutos
                    if lon_min < 10:
                        lon_min_str = "0" + str(lon_min)
                    else:
                        lon_min_str = str(lon_min)

                    # segundos
                    if lon_seg < 10:
                        lon_seg_str = "0" + str(lon_seg)
                    else:
                        lon_seg_str = str(lon_seg)

                    lon_str = lon_signo + lon_ent_str + lon_min_str + lon_seg_str

                    linea = "\n" + airport.ICAO + " " + lat_str + " " + lon_str
                    F.write(linea)

                i = i + 1

            F.close()
    except:
        return -1 # error

def AddAirport (airports, airport):
    i = 0
    encontrado = False
    while i < len(airports) and not encontrado:
        if airports[i].ICAO == airport.ICAO:
            encontrado=True
        else:
            i = i + 1
    if not encontrado:
        airports.append(airport)

def RemoveAirport (airports, code):
    i = 0
    encontrado = False
    while i < len(airports) and not encontrado:
        if airports[i].ICAO == code:
            encontrado=True
        else:
            i = i + 1
    if encontrado:
        n = len(airports) - 1
        while i < n:
            airports[i] = airports[i + 1]
            i = i + 1
        airports[:] = airports[:n] #modifica la longitud de la lista
    else:
        return -1  #error

def PlotAirports (airports):
    schengen = 0
    no_schengen = 0
    i = 0
    while i < len(airports):
        if airports[i].Schengen:
            schengen = schengen + 1
        else:
            no_schengen = no_schengen + 1
        i = i + 1
    x = [0]
    y1 = [schengen]
    y2 = [no_schengen]

    plt.bar(x, y1, color='blue', label='Schengen')
    plt.bar(x, y2, bottom=y1, color='red', label='No Schengen')

    plt.ylabel("Número de aeropuertos")
    plt.title("Aeropuertos Schengen vs No Schengen")
    plt.legend()
    plt.show()

import webbrowser

def MapAirports(airports):
    F = open("airports.kml", "w")
    F.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    F.write("<Document>\n")
    F.write("<name>Airports</name>\n")

    i = 0
    while i < len(airports):
        if airports[i].Schengen:
            color = "http://maps.google.com/mapfiles/kml/paddle/blu-circle.png"
        else:
            color = "http://maps.google.com/mapfiles/kml/paddle/red-circle.png"

        F.write(f"""
<Placemark>
    <name>{airports[i].ICAO}</name>
    <Style>
        <IconStyle>
            <Icon>
                <href>{color}</href>
            </Icon>
        </IconStyle>
    </Style>
    <Point>
        <coordinates>{airports[i].longitude},{airports[i].latitude}</coordinates>
    </Point>
</Placemark>
""")

        i = i + 1

    F.write("</Document>\n")
    F.write("</kml>")
    F.close()
    webbrowser.open("airports.kml")