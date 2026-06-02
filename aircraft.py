from airport import *
import webbrowser
import matplotlib.pyplot as plt


class Aircraft:
    # id(str), origin(str), arrival (str), company(str), destination(str), departure(str)
    def __init__(self, id, origin="", arrival="", company="", destination="", departure=""):
        self.id = id
        self.origin = origin
        self.time = arrival
        self.company = company
        self.destination = destination
        self.departure = departure

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

# LoadDepartures: lee vuelos de salida desde archivo; parámetros (filename); devuelve lista o [] si error.
def LoadDepartures(filename):
    aircrafts = []

    try:
        F = open(filename, "r")
    except:
        print("File error")
        return []

    linea = F.readline()   # títulos
    linea = F.readline()   # primera línea real

    while linea != "":
        partes = linea.split()

        if len(partes) == 4:
            aircraft = partes[0]
            destination = partes[1]
            departure = partes[2]
            airline = partes[3]

            hora = int(departure.split(":")[0])
            min = int(departure.split(":")[1])

            if hora >= 0 and hora < 24 and min >= 0 and min < 60:
                airplane = Aircraft(aircraft, "", "", airline, destination, departure)
                aircrafts.append(airplane)

        linea = F.readline()

    F.close()
    return aircrafts

# MergeMovements: une llegadas y salidas con mismo id y horas compatibles; parámetros(arrivals, departures); devuelve lista o -1 si error.
def MergeMovements(arrivals, departures):
    if len(arrivals) == 0 or len(departures) == 0:
        print("Error: empty list")
        return -1

    result = []
    used = []

    i = 0
    while i < len(arrivals):
        arr = arrivals[i]

        j = 0
        found = False

        while j < len(departures):
            dep = departures[j]

            if arr.id == dep.id:

                arr_h = int(arr.time.split(":")[0])
                arr_m = int(arr.time.split(":")[1])
                dep_h = int(dep.departure.split(":")[0])
                dep_m = int(dep.departure.split(":")[1])

                if (arr_h < dep_h) or (arr_h == dep_h and arr_m < dep_m):
                    merged = Aircraft(arr.id, arr.origin,arr.time,arr.company, dep.destination,dep.departure)
                    result.append(merged)
                    used.append(j)
                    found = True
                    j = len(departures)

            j = j + 1

        if found == False:
            result.append(arr)

        i = i + 1

    k = 0
    while k < len(departures):
        if k not in used:
            dep = departures[k]
            night = Aircraft(dep.id, "", "", dep.company, dep.destination, dep.departure)
            result.append(night)
        k = k + 1

    return result

# NightAircraft: devuelve los aviones sin llegada (origin="" y arrival=""); si la lista está vacía devuelve -1.
def NightAircraft(aircrafts):
    if len(aircrafts) == 0:
        return -1

    night_list = []
    i = 0
    while i < len(aircrafts):
        avion = aircrafts[i]

        if avion.origin == "" and avion.time == "":
            night_list.append(avion)

        i = i + 1

    return night_list

# PlotArrivals: muestra número de vuelos por hora; parámetros(aircrafts); error si lista vacía.
def PlotArrivals(aircrafts):
    flights_hour = [0]*24
    i = 0

    while i < len(aircrafts):
        time_text = aircrafts[i].time

        if time_text != "":
            hour_text = time_text[0:2]
            hour = int(hour_text)
            if hour >= 0 and hour < 24:
                    flights_hour[hour] = flights_hour[hour] + 1
        i = i + 1

    ax.bar(range(24), flights_hour)
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

            linea = avion + " " + origen + " " + hora + " " + aerolinea
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


if __name__ == "__main__":
    airports = LoadAirports("Airports.txt")
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    arrivals = LoadArrivals("arrivals.txt")
    departures = LoadDepartures("departures.txt")

    aircrafts = MergeMovements(arrivals, departures)
    print("Movements merged:", len(aircrafts))

    night = NightAircraft(aircrafts)
    print("Night flights:", len(night))

    SaveFlights(arrivals, "arrivals_saved.txt")

    long = LongDistanceArrivals(arrivals)
    print("Long distance flights:", len(long))

    fig, ax = plt.subplots()
    PlotArrivals(arrivals)

    fig, ax = plt.subplots()
    PlotAirlines(arrivals)

    fig, ax = plt.subplots()
    PlotFlightsType(arrivals)

    plt.show()

    MapFlights(arrivals)

