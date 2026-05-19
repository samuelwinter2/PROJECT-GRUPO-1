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
            area_type = parts[2]
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

    t_name = SearchTerminal(bcn, aircraft.company)
    if t_name == "":
        print("ERROR: Airline not found in any terminal")
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
                    print("ERROR: No free gates in terminal", t_name, "for type", tipo)
                    return -1
                j = j + 1
        i = i + 1
    print("ERROR: Terminal not found")
    return -1

# TEST
if __name__ == "__main__":
    bcn = LoadAirportStructure("Terminals.txt")

    aircraft = Aircraft("VY1234","LEMD","12:30","VLG")

    gate = AssignGate(bcn, aircraft)
    print("Gate assigned:", gate)

    gates = GateOccupancy(bcn)
    for g in gates[:20]:
        print(g)

    t = bcn.terminals[0]
    if t.airlines:
        print("Airline", t.airlines[0], "in terminal",t.name,":", IsAirlineInTerminal(t, t.airlines[0]))

    if bcn.terminals[0].airlines:
        airline = t.airlines[0]
        print("SearchTerminal for", airline, ":", SearchTerminal(bcn, airline))
