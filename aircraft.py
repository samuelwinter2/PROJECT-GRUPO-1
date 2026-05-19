from airport import *
ax = None

class Aircraft:
    # Aircraft: id(str), origin(str), time(str), company(str); representa un vuelo de llegada.
    def __init__(self, id, origin, time, company):
        self.id = id
        self.company = company
        self.origin = origin
        self.time = time


# LoadArrivals: lee vuelos desde archivo; parámetros (filename); devuelve lista o [] si File error.
def LoadArrivals(filename):
    aircrafts = []

    try:
        F = open(filename, 'r')
    except:
        print("File error")
        return []

    i = 1
    linea = F.readline()   # primera línea (títulos)

    linea = F.readline()   # primera línea real
    while linea != "":
        partes = linea.split(" ")

        if len(partes) == 4:
            aircraft = partes[0]
            origin = partes[1]
            arrival = partes[2]
            airline = partes[3]

            hora = int(arrival.split(":")[0])
            min = int(arrival.split(":")[1])

            if hora >= 0 and hora < 24 and min >= 0 and min < 60:
                airplane = Aircraft(aircraft, origin, arrival, airline)
                aircrafts.append(airplane)

        linea = F.readline()
        i = i + 1

    F.close()
    return aircrafts


# PlotArrivals: muestra número de vuelos por hora; parámetros(aircrafts); error si lista vacía.
def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:
        print("Error: la lista está vacía")
        return

    flights_hour = [0] * 24
    i = 0
    while i < len(aircrafts):
        hour_text = aircrafts[i].time
        hour = int(hour_text.split(":")[0])
        flights_hour[hour] = flights_hour[hour] + 1
        i = i + 1

    day_hour = range(24)
    ax.bar(day_hour, flights_hour)
    ax.set_title("Número de aviones que aterrizan por hora")
    ax.set_xlabel("Hora del día")
    ax.set_ylabel("Número de vuelos")


# SaveFlights: guarda vuelos en archivo; parámetros(aircrafts, filename); error si lista vacía.
def SaveFlights(aircrafts, filename):
    if len(aircrafts) == 0:
        print("Error: la lista está vacía")
        return

    try:
        f = open(filename, 'w')
        f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
        i = 0
        while i < len(aircrafts):
            avion = aircrafts[i].id
            origen = aircrafts[i].origin
            hora = aircrafts[i].time
            aerolinea = aircrafts[i].company

            if avion == "":
                avion = "-"
            if origen == "":
                origen = "-"
            if hora == "":
                hora = "0"
            if aerolinea == "":
                aerolinea = "-"

            linea = avion + " " + origen + " " + hora + " " + aerolinea + "\n"
            f.write(linea)
            i = i + 1

        f.close()
    except:
        print("File error")
        return


# PlotAirlines: muestra números de vuelos por aerolínea; parámetros(aircrafts); error si lista vacía.
def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        print("Error: la lista está vacía")
        return

    airlines = []
    num_flights = []
    i = 0

    while i < len(aircrafts):
        aerolinea = aircrafts[i].company
        encontrado = False
        j = 0

        while j < len(airlines) and not encontrado:
            if airlines[j] == aerolinea:
                encontrado = True
                num_flights[j] = num_flights[j] + 1
            j = j + 1

        if not encontrado:
            airlines.append(aerolinea)
            num_flights.append(1)

        i = i + 1

    ax.bar(airlines, num_flights)
    ax.set_title("Número de vuelos por aerolínea")
    ax.set_xlabel("Aerolínea")
    ax.set_ylabel("Número de vuelos")
    ax.tick_params(axis='x', rotation=90, labelsize=6)


# PlotFlightsType: muestra vuelos Schengen vs No-Schengen; parámetros(aircrafts); error si vacía.
def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        print("Error: la lista está vacía")
        return

    schengen = 0
    no_schengen = 0

    i = 0
    while i < len(aircrafts):
        code = aircrafts[i].origin
        if IsSchengenAirport(code):
            schengen = schengen + 1
        else:
            no_schengen = no_schengen + 1
        i = i + 1

    x = [0]
    y1 = [schengen]
    y2 = [no_schengen]

    ax.bar(x, y1, color='blue', label='Schengen')
    ax.bar(x, y2, bottom=y1, color='red', label='No Schengen')

    ax.set_ylabel("Número de vuelos")
    ax.set_title("Vuelos por tipo de origen (Schengen / No Schengen)")
    ax.legend()


import webbrowser

# MapFlights: dibuja rutas en Google Earth; parámetros(aircrafts); usa colores según Schengen.
def MapFlights(aircrafts):
    airports = LoadAirports("Airports.txt")
    F = open("flights.kml", "w")
    F.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
    F.write("<Document>\n")

    lebl = False
    i = 0
    while i < len(airports) and lebl == False:
        if airports[i].ICAO == "LEBL":
            lebl = airports[i]
        i = i + 1

    i = 0
    while i < len(aircrafts):
        airports = LoadAirports("Airports.txt")
        k = 0
        while k < len(airports):
            SetSchengen(airports[k])
            k = k + 1

        origin_code = aircrafts[i].origin
        origin_airport = False

        j = 0
        while j < len(airports) and origin_airport == False:
            if airports[j].ICAO == origin_code:
                origin_airport = airports[j]
            j = j + 1

        if origin_airport != False:

            if origin_airport.Schengen:
                color = "ffff0000"  # rojo
            else:
                color = "ff0000ff"  # azul

            F.write(f"""
            <Placemark>
                <Style>
                    <LineStyle>
                        <color>{color}</color>
                        <width>3</width>
                    </LineStyle>
                </Style>
                <LineString>
                    <coordinates>
                        {origin_airport.longitude},{origin_airport.latitude}
                        {lebl.longitude},{lebl.latitude}
                    </coordinates>
                </LineString>
            </Placemark>
            """)

        i = i + 1

    F.write("</Document>\n")
    F.write("</kml>\n")
    F.close()

    webbrowser.open("flights.kml")


# LongDistanceArrivals: devuelve vuelos con origen a >2000 km; parámetros(aircrafts).
def LongDistanceArrivals(aircrafts):
    from math import radians, sin, cos, sqrt, atan2

    airports = LoadAirports("Airports.txt")

    if len(aircrafts) == 0:
        return []

    lebl = airports[0]
    i = 0
    while i < len(airports):
        if airports[i].ICAO == "LEBL":
            lebl = airports[i]
        i = i + 1

    result = []

    i = 0
    while i < len(aircrafts):

        origin_code = aircrafts[i].origin

        origin_airport = airports[0]
        encontrado = False
        j = 0
        while j < len(airports) and not encontrado:
            if airports[j].ICAO == origin_code:
                origin_airport = airports[j]
                encontrado = True
            j = j + 1

        if encontrado:

            R = 6371  # radio de la Tierra en km

            lat1 = radians(origin_airport.latitude)
            lon1 = radians(origin_airport.longitude)
            lat2 = radians(lebl.latitude)
            lon2 = radians(lebl.longitude)

            dlat = lat2 - lat1
            dlon = lon2 - lon1

            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distancia = R * c

            if distancia > 2000:
                result.append(aircrafts[i])

        i = i + 1

    return result


# TEST
if __name__ == "__main__":
    airports = LoadAirports("Airports.txt")
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    aircrafts = LoadArrivals("arrivals.txt")
    PlotArrivals(aircrafts)
    PlotAirlines(aircrafts)
    PlotFlightsType(aircrafts)
    SaveFlights(aircrafts, "arrivals_saved.txt")

    long = LongDistanceArrivals(aircrafts)
    i = 0
    while i < len(long):
        print(long[i].id, long[i].origin)
        i += 1

    MapFlights(aircrafts)
