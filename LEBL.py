from aircraft import *
from airport import *

class Gate:
    # Representa una puerta: name (str), occupied (TRUE/FALSE), aircraft_id (str).
    def __init__(self, name, occupied=False, aircraft_id=""):
        self.name = name
        self.occupied = occupied
        self.aircraft_id = aircraft_id

class BoardingArea:
    # Representa un área: name (str), type (Schengen/non schengen), lista de gates.
    def __init__(self, name, area_type):
        self.name = name
        self.type = area_type
        self.gates = []

class Terminal:
    # Representa un terminal: name (str), boarding_areas (list), airlines (list ICAO).
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []

class BarcelonaAP:
    # Representa el aeropuerto: code (str), lista de terminales.
    def __init__(self, code):
        self.code = code
        self.terminals = []

# Crea los gates de un área. Parámetros: area, init_gate, end_gate, prefix. Devuelve -1 si error.
def SetGates (area, init_gate, end_gate, prefix):

    if init_gate > end_gate:
        return -1

    area.gates = []

    while init_gate <= end_gate:
        gate_name = prefix + str(init_gate)
        gate = Gate(gate_name, occupied=False, aircraft_id="")
        area.gates.append(gate)
        init_gate = init_gate + 1

# Carga aerolíneas en un terminal desde archivo. Parámetros: terminal, t_name. Devuelve -1 si error.
def LoadAirlines (terminal, t_name):

    filename = t_name + "_Airlines.txt"

    try:
        F = open(filename, "r")
    except:
        return -1

    terminal.airlines = []

    line = F.readline()
    while line != "":
        line = line.strip()

        if line != "":
            parts = line.split("\t")
            if len(parts) == 2:
                icao = parts[1]
                terminal.airlines.append(icao)

        line = F.readline()

    F.close()

# Carga toda la estructura del aeropuerto. Parámetro: filename. Devuelve BarcelonaAP o -1 si error.
def LoadAirportStructure (filename):
    try:
        F = open(filename, "r")
    except:
        return -1

    line = F.readline().strip()
    parts = line.split()
    code = parts[0]
    num_terminals = int(parts[1])

    bcn = BarcelonaAP(code)
    i = 0
    while i < num_terminals:
        line = F.readline().strip()
        parts = line.split()

        t_name = parts[1]
        num_areas = int(parts[2])

        terminal = Terminal(t_name)

        i = i + 1
        j = 0
        while j < num_areas:
            line = F.readline().strip()
            parts = line.split()

            area_name = parts[1]
            area_type = parts[2].strip()

            if area_type == "Schengen":
                area_type = "schengen"
            elif area_type == "non-Schengen":
                area_type = "non-schengen"

            init_gate = int(parts[4])
            end_gate = int(parts[6])

            area = BoardingArea(area_name, area_type)

            prefix = t_name + area_name

            SetGates(area, init_gate, end_gate, prefix)

            terminal.boarding_areas.append(area)
            j = j + 1
        LoadAirlines(terminal, t_name)

        bcn.terminals.append(terminal)

    F.close()

    return bcn

# Devuelve lista con [gate_name, status, aircraft_id]. Parámetro: bcn.
def GateOccupancy(bcn):
    result = []
    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]
        j = 0
        while j < len(terminal.boarding_areas):
            area = terminal.boarding_areas[j]
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]
                if gate.occupied:
                    status = "Occupied"
                else:
                    status = "Free"
                result.append([gate.name, status, gate.aircraft_id])
                k = k + 1
            j = j + 1
        i = i + 1
    return result

# Comprueba si una aerolínea está en un terminal. Parámetros: terminal, name. Devuelve True/False.
def IsAirlineInTerminal(terminal, name):
    if name == "":
        return False
    i = 0
    encontrado = False
    while i < len(terminal.airlines) and not encontrado:
        if terminal.airlines[i] == name:
            encontrado = True
        else:
            i += 1
    return encontrado

# Busca el terminal donde opera una aerolínea. Parámetros: bcn, airline. Devuelve nombre o "".
def SearchTerminal(bcn, airline):
    airline = airline.strip()

    i = 0
    encontrado = False
    terminal_name = ""

    while i < len(bcn.terminals) and not encontrado:
        terminal = bcn.terminals[i]

        if IsAirlineInTerminal(terminal, airline):
            encontrado = True
            terminal_name = terminal.name
        else:
            i = i + 1

    return terminal_name

# Asigna la primera puerta libre correcta a un avión. Parámetros: bcn, aircraft. Devuelve gate o -1.
def AssignGate(bcn, aircraft):

    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        j = 0
        while j < len(terminal.boarding_areas):
            area = terminal.boarding_areas[j]

            k = 0
            while k < len(area.gates):
                gate = area.gates[k]

                if gate.aircraft_id == aircraft.id:
                    return gate.name

                k = k + 1
            j = j + 1
        i = i + 1

    t_name = SearchTerminal(bcn, aircraft.company)
    if t_name == "":
        print("ERROR: Airline", aircraft.company, "not found in any terminal")
        return -1

    es_Schengen = IsSchengenAirport(aircraft.origin)
    if es_Schengen:
        tipo = "schengen"
    else:
        tipo = "non-schengen"

    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        if terminal.name == t_name:

            j = 0
            while j < len(terminal.boarding_areas):
                area = terminal.boarding_areas[j]

                if area.type.strip().lower() == tipo:

                    k = 0
                    while k < len(area.gates):
                        gate = area.gates[k]

                        if not gate.occupied:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.id
                            print("Avión", aircraft.id, "asignado a la puerta", gate.name)
                            return gate.name

                        k = k + 1

                j = j + 1

            print("ERROR: No free gates in terminal", t_name, "for type", tipo)
            return -1

        i = i + 1

    print("ERROR: Terminal not found")
    return -1
# AssignNightGates: asigna puertas a aviones que solo tienen salida; parámetros(bcn, aircrafts); devuelve -1 si error.
def AssignNightGates(bcn, aircrafts):
    if len(aircrafts) == 0:
        print("Error: empty list")
        return -1

    i = 0
    while i < len(aircrafts):
        a = aircrafts[i]

        if a.origin == "" and a.time == "":
            AssignGate(bcn, a)
        else:
            print("Skipping aircraft", a.id, "(not night aircraft)")

        i = i + 1

# FreeGate: libera la puerta donde está un avión; parámetros(bcn, id); devuelve nombre de gate o -1 si no se encuentra.
def FreeGate(bcn, id):
    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        j = 0
        while j < len(terminal.boarding_areas):
            area = terminal.boarding_areas[j]

            k = 0
            while k < len(area.gates):
                gate = area.gates[k]

                if gate.aircraft_id == id:
                    gate.occupied = False
                    gate.aircraft_id = ""
                    return gate.name

                k = k + 1
            j = j + 1
        i = i + 1

    print("ERROR: aircraft not found")
    return -1

# AssignGatesAtTime: libera puertas de aviones ya salidos y asigna a los que aterrizan en esa hora; parámetros(bcn, aircrafts, time); devuelve número no asignados.
def AssignGatesAtTime(bcn, aircrafts, time):

    if len(aircrafts) == 0:
        return -1

    hora_inicio = int(time.split(":")[0])
    hora_fin = hora_inicio + 1

    # Liberar puertas de aviones ya despegados
    i = 0
    while i < len(aircrafts):

        aircraft = aircrafts[i]

        if aircraft.departure != "":

            dep_h = int(aircraft.departure.split(":")[0])

            # Si ya ha salido antes de esta hora
            if dep_h < hora_inicio:
                FreeGate(bcn, aircraft.id)

        i = i + 1

    # Asignar puertas a llegadas del periodo
    no_asignados = 0

    i = 0
    while i < len(aircrafts):

        aircraft = aircrafts[i]

        # Solo vuelos con llegada
        if aircraft.time != "":

            arr_h = int(aircraft.time.split(":")[0])

            # Si aterriza dentro de esta franja
            if arr_h >= hora_inicio and arr_h < hora_fin:

                gate = AssignGate(bcn, aircraft)

                if gate == -1:
                    no_asignados += 1

        i = i + 1

    return no_asignados

# PlotDayOccupancy, muestra ocupación diaria por terminal
def PlotDayOccupancy(bcn, aircrafts):

    if len(aircrafts) == 0:
        print("Error: empty aircraft list")
        return

    terminals = []
    i = 0
    while i < len(bcn.terminals):
        terminals.append(bcn.terminals[i].name)
        i += 1

    ocupacion_terminales = []
    i = 0
    while i < len(terminals):
        ocupacion_terminales.append([])
        i += 1
    no_asignados_hora = []
    horas = []

    h = 0
    while h < 24:

        horas.append(h)

        temp = BarcelonaAP(bcn.code)

        t = 0
        while t < len(bcn.terminals):
            term_real = bcn.terminals[t]
            term = Terminal(term_real.name)

            term.airlines = []
            a = 0
            while a < len(term_real.airlines):
                term.airlines.append(term_real.airlines[a])
                a += 1

            a = 0
            while a < len(term_real.boarding_areas):
                area_real = term_real.boarding_areas[a]
                area = BoardingArea(area_real.name, area_real.type)
                g = 0
                while g < len(area_real.gates):
                    gate_real = area_real.gates[g]
                    area.gates.append(Gate(gate_real.name))
                    g += 1

                term.boarding_areas.append(area)
                a += 1

            temp.terminals.append(term)
            t += 1

        night_list = NightAircraft(aircrafts)
        if night_list != -1:
            AssignNightGates(temp, night_list)

        sim = 0
        rejected_this_hour = 0

        while sim <= h:
            rejected = AssignGatesAtTime(temp, aircrafts, f"{sim:02d}:00")

            if sim == h:
                rejected_this_hour = rejected

            sim = sim + 1

        no_asignados_hora.append(rejected_this_hour)

        t = 0
        while t < len(temp.terminals):
            ocupadas = 0
            a = 0
            while a < len(temp.terminals[t].boarding_areas):
                g = 0
                while g < len(temp.terminals[t].boarding_areas[a].gates):
                    if temp.terminals[t].boarding_areas[a].gates[g].occupied:
                        ocupadas += 1
                    g += 1
                a += 1
            ocupacion_terminales[t].append(ocupadas)
            t += 1

        h += 1

    i = 0
    while i < len(terminals):
        ax.plot(horas, ocupacion_terminales[i], label=terminals[i])
        i += 1

    ax.plot(horas, no_asignados_hora, label="Not Assigned")

    ax.set_title("Gate Occupancy During the Day")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Assigned Gates")
    ax.set_xticks(range(24))
    ax.legend()


# TEST
if __name__ == "__main__":
    print("LOADAIRPORTSTRUCTURE")
    bcn = LoadAirportStructure("Terminals.txt")

    print("ASSIGNGATE")
    aircraft = Aircraft("VY1234","LEMD","12:30","VLG")
    gate = AssignGate(bcn, aircraft)
    print("Gate assigned:", gate)

    print("GATEOCCUPANCY")
    gates = GateOccupancy(bcn)
    for g in gates[:20]:
        print(g)

    print("ISAIRLINEINTERMINAL")
    t = bcn.terminals[0]
    if t.airlines:
        print("Airline", t.airlines[0], "in terminal", t.name, ":", IsAirlineInTerminal(t, t.airlines[0]))

    print("SEARCHTERMINAL")
    if bcn.terminals[0].airlines:
        airline = t.airlines[0]
        print("SearchTerminal for", airline, ":", SearchTerminal(bcn, airline))

    print("FREEGATE")
    f = FreeGate(bcn, aircraft.id)
    print("Freed gate:", f)

    print("ASSIGNNIGHTGATES")
    night = [Aircraft("NIGHT1", "", "", "VLG")]
    AssignNightGates(bcn, night)

    print("ASSIGNGATESATTIME")
    r = AssignGatesAtTime(bcn, [aircraft], "12:00")
    print("Not assigned:", r)

    print("PLOTDAYOCCUPANCY")
    fig, ax = plt.subplots()
    PlotDayOccupancy(bcn, [aircraft])
    plt.show()