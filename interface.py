from tkinter import *
import airport
import aircraft
from LEBL import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



airports = []
aircrafts = []


# Actualiza la listbox de aeropuertos con los datos de airports
def refresh_list():
    listbox_airports.delete(0, END)  # Borra toda la listbox
    i = 0
    while i < len(airports):
        a = airports[i]
        listbox_airports.insert(END,f"{a.ICAO} ({a.latitude:.4f}, {a.longitude:.4f}) - Schengen: {a.Schengen}")
        # Inserta una línea en la listbox
        i = i + 1

# Actualiza la listbox de aerolíneas según aircrafts
def refresh_airlines_list():
    listbox_airlines.delete(0, END)  # Borra todas las aerolíneas mostradas en la listbox.
    companies = []
    i = 0
    while i < len(aircrafts):
        if aircrafts[i].company not in companies:
            companies.append(aircrafts[i].company)
        i = i + 1

    j = 0
    while j < len(companies):        # Inserta cada compañía en la listbox
        listbox_airlines.insert(END, companies[j])
        j = j + 1


def load_airports():
    from tkinter import filedialog
    global airports
    filename = filedialog.askopenfilename()
    if filename:
        airports = LoadAirports(filename)
        refresh_list()


def add_airport():
    try:
        code = entry_code.get()
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
        a = Airport(code, lat, lon)
        SetSchengen(a)
        AddAirport(airports, a)
        refresh_list()
    except:
        print("Error")


def remove_airport():
    sel = listbox_airports.curselection()  # Línea seleccionada en la listbox
    if sel:
        i = sel[0]                          # Primera línea seleccionada
        RemoveAirport(airports, airports[i].ICAO)
        refresh_list()


def set_schengen():
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1
    refresh_list()


def save_schengen():
    from tkinter import filedialog
    filename = filedialog.asksaveasfilename()
    if filename:
        SaveSchengenAirports(airports, filename)


def plot_airports():
    fig.clf()
    ax = fig.add_subplot(111)
    airport.ax = ax
    PlotAirports(airports)
    canvas.draw()


def map_airports():
    MapAirports(airports)


def load_arrivals():
    from tkinter import filedialog
    global aircrafts
    filename = filedialog.askopenfilename()
    if filename:
        aircrafts = LoadArrivals(filename)

        listbox_arrivals.delete(0, END)  # Borra la listbox de vuelos

        i = 0
        while i < len(aircrafts):# Inserta cada vuelo en la listbox
            a = aircrafts[i]
            listbox_arrivals.insert(END, f"{a.id} | {a.origin} → {a.time} | {a.company}")
            i = i + 1

        refresh_airlines_list() # Actualiza aerolíneas


def save_flights():
    from tkinter import filedialog
    filename = filedialog.asksaveasfilename()
    if filename:
        SaveFlights(aircrafts, filename)


def plot_arrivals():
    fig.clf()
    ax = fig.add_subplot(111)
    aircraft.ax = ax
    PlotArrivals(aircrafts)
    canvas.draw()


# Plot de aerolíneas con filtro según selección en listbox_airlines
def plot_airlines():
    fig.clf()
    ax = fig.add_subplot(111)
    aircraft.ax = ax

    selected = [] # Lista de compañías seleccionadas
    sel = listbox_airlines.curselection()  # Líneas seleccionadas en la listbox

    i = 0
    while i < len(sel):
        selected.append(listbox_airlines.get(sel[i]))  # Obtiene el texto de cada selección
        i = i + 1
    if len(selected) == 0: # Si no hay selección escoge todas las aerolíneas
        PlotAirlines(aircrafts)
    else:
        filtro = []  # Filtra vuelos por compañía
        j = 0
        while j < len(aircrafts):
            k = 0
            encontrado = False
            while k < len(selected) and not encontrado:
                if aircrafts[j].company == selected[k]:
                    encontrado = True
                k = k + 1
            if encontrado:
                filtro.append(aircrafts[j])
            j = j + 1
        PlotAirlines(filtro)
    canvas.draw()



def plot_flight_types():
    fig.clf()
    ax = fig.add_subplot(111)
    aircraft.ax = ax
    PlotFlightsType(aircrafts)
    canvas.draw()


def map_flights():
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1
    MapFlights(aircrafts)


def map_long_flights():
    long = LongDistanceArrivals(aircrafts)
    MapFlights(long)


def load_LEBL():
    global bcn
    from tkinter import filedialog

    filename = filedialog.askopenfilename(title="Select LEBL structure file")
    if not filename:
        return

    bcn = LoadAirportStructure(filename)
    if bcn == -1:
        print("Error loading airport structure.")
    else:
        print("LEBL structure loaded:", bcn.code, "Terminals:", len(bcn.terminals))


# Asigna una puerta al vuelo seleccionado en la listbox de llegadas
def assign_gate():
    global bcn

    sel = listbox_arrivals.curselection()  # Línea seleccionada en la listbox
    if not sel:
        print("Select a flight.")
        return

    aircraft_sel = aircrafts[sel[0]] # Vuelo seleccionado
    gate = AssignGate(bcn, aircraft_sel) # Asigna puerta
    print("Gate assigned:", gate)


# Variable global para controlar qué terminal estamos mostrando (empieza en la T1)
terminal_actual = 1

def show_gate_occupancy():
    global bcn
    global terminal_actual

    fig.clf()
    ax = fig.add_subplot(111)

    nombre_buscado = "T" + f"{terminal_actual}"
    encontrado = False

    i = 0
    while i < len(bcn.terminals):
        t = bcn.terminals[i]
        if t.name == nombre_buscado:
            terminal_a_dibujar = t
            encontrado = True
        i = i + 1

    if encontrado == False:
        print("Terminal no encontrada:", nombre_buscado)
        return
    # transform=ax.transAxes hace que las X y Y del plot vayan de 0 a 1
    # de abajo arriba y de izquierda a derecha, independientemente del tamaño real del gráfico.
    ax.text(0.2, 1, f"ESTADO DE PUERTAS - {bcn.code} ({terminal_a_dibujar.name})", transform=ax.transAxes, fontsize=11, fontweight="bold")

    ax.text(0.2, 0, "(Pulsa el botón otra vez para cambiar de Terminal)", transform=ax.transAxes, fontsize=9, color="black", style="italic")

    start_x = 2 # Inicio del dibujo
    num_areas = len(terminal_a_dibujar.boarding_areas)
    end_x = start_x + (num_areas * 4) # Final del dibujo

    ax.plot([start_x - 1, end_x], [25, 25], color='blue', linewidth=6)  # Barra superior
    ax.text(start_x - 0.5, 26, terminal_a_dibujar.name,color='blue', fontweight='bold', fontsize=12)
    # Nombre terminal

    i = 0
    while i < len(terminal_a_dibujar.boarding_areas): # Recorre áreas
        area = terminal_a_dibujar.boarding_areas[i]
        x = start_x + (i * 4) + 1 # Posición X del área

        ax.plot([x, x], [25, 1], color='blue', linewidth=4)  # Línea vertical del área
        ax.text(x - 0.5, 1, area.name, fontweight='bold', fontsize=10)  # Nombre del área

        num_puertas = len(area.gates) # Número de puertas del área

        if num_puertas > 0:
            separacion = 23.0 / num_puertas # Distancia entre puertas
        else:
            separacion = 1.0

        if "Area B" in area.name:
            tamaño_cuadrado = 0.15 # Cuadrado pequeño para Area B
        else:
            tamaño_cuadrado = 0.45 # Cuadrado grande para otras áreas

        j = 0
        while j < len(area.gates): # Recorre puertas
            gate = area.gates[j]
            y = 24.5 - (j * separacion) # Posición Y de la puerta

            if j % 2 == 0: # Alterna izquierda/derecha
                gx_end = x + 0.5
                rect_x = gx_end
                text_x = x + 1
            else:
                gx_end = x - 0.5
                rect_x = gx_end - tamaño_cuadrado
                text_x = x - 2

            ax.plot([x, gx_end], [y, y], color='blue', linewidth=1)  # Línea horizontal

            if gate.occupied:
                color_puerta = 'red' # Ocupado rojo
            else:
                color_puerta = 'green' # Libre verde

            import matplotlib.patches as patches
            rectangulo = patches.Rectangle((rect_x, y - (tamaño_cuadrado / 2)),tamaño_cuadrado,tamaño_cuadrado,facecolor=color_puerta,edgecolor='black',linewidth=0.5)
            ax.add_patch(rectangulo) # Dibuja el cuadrado

            if gate.occupied:
                ax.text(text_x, y - 0.1, gate.aircraft_id,
                        color='red', fontsize=7, fontweight='bold')  # Muestra avión
            else:
                ax.text(text_x, y - 0.1, gate.name,
                        color='black', fontsize=7, fontweight='bold')  # Muestra nombre puerta

            j = j + 1

        i = i + 1

    ax.set_xlim(0, end_x + 1) # Límites X
    ax.set_ylim(0, 26) # Límites Y
    ax.set_axis_off() # Oculta ejes

    canvas.draw()

    if terminal_actual == 1: # Alterna terminal
        terminal_actual = 2
    else:
        terminal_actual = 1


window = Tk()
window.geometry("1920x1080")
window.title("Proyecto Informatica")
window.configure(bg="whitesmoke")

for i in range(16):
    window.rowconfigure(i, weight=1)
for j in range(6):
    window.columnconfigure(j, weight=1)

Label(window, text="AIRPORTS AND FLIGHTS", font=("Segoe UI", 28), bg="whitesmoke", fg="black").grid(row=0, column=0, columnspan=6, pady=30, sticky=N+S+E+W)

Label(window, text="AIRPORTS", font=("Segoe UI", 16), bg="whitesmoke", fg="black").grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
listbox_airports = Listbox(window, font=("Consolas", 10), bg="white", fg="black", borderwidth=0, highlightthickness=0)
listbox_airports.grid(row=2, column=0, columnspan=2, rowspan=5, padx=5, pady=10, sticky=N+S+E+W)

Button(window, text="LOAD AIRPORTS", bg="aliceblue", fg="black", font=("Segoe UI", 8), command=load_airports).grid(row=7, column=0, padx=30, pady=5, sticky=N+S+E+W)
Button(window, text="SAVE SCHENGEN", bg="aliceblue", fg="black", font=("Segoe UI", 8), command=save_schengen).grid(row=7, column=1, padx=30, pady=5, sticky=N+S+E+W)
Button(window, text="SET SCHENGEN", bg="lightsteelblue", fg="black", font=("Segoe UI", 8), command=set_schengen).grid(row=8, column=0, padx=30, pady=5, sticky=N+S+E+W)
Button(window, text="REMOVE AIRPORT", bg="mistyrose", fg="black", font=("Segoe UI", 8), command=remove_airport).grid(row=8, column=1, padx=30, pady=5, sticky=N+S+E+W)

Label(window, text="ADD AIRPORT", font=("Segoe UI", 12), bg="whitesmoke", fg="black").grid(row=9, column=0, columnspan=2, pady=(20,0), sticky=N+S+E+W)
Label(window, text="ICAO CODE", bg="whitesmoke", fg="black").grid(row=10, column=0, padx=10, sticky=N+S+E+W)
entry_code = Entry(window, borderwidth=0); entry_code.grid(row=10, column=1, padx=10, sticky=N+S+E+W)
Label(window, text="LATITUDE", bg="whitesmoke", fg="black").grid(row=11, column=0, padx=10, sticky=N+S+E+W)
entry_lat = Entry(window, borderwidth=0); entry_lat.grid(row=11, column=1, padx=10, sticky=N+S+E+W)
Label(window, text="LONGITUDE", bg="whitesmoke", fg="black").grid(row=12, column=0, padx=10, sticky=N+S+E+W)
entry_lon = Entry(window, borderwidth=0); entry_lon.grid(row=12, column=1, padx=10, sticky=N+S+E+W)
Button(window, text="ADD", bg="lightgray", fg="black", font=("Segoe UI", 10), command=add_airport).grid(row=13, column=0, columnspan=2, padx=60, pady=15, sticky=N+S+E+W)

Label(window, text="FLIGHTS", font=("Segoe UI", 16), bg="whitesmoke", fg="black").grid(row=1, column=2, columnspan=2, sticky=N+S+E+W)
listbox_arrivals = Listbox(window, font=("Consolas", 8), bg="white", fg="black", borderwidth=0, highlightthickness=0)
listbox_arrivals.grid(row=2, column=2, columnspan=2, rowspan=5, padx=5, pady=10, sticky=N+S+E+W)

Label(window, text="SELECT PLOT AIRLINES", font=("Segoe UI", 10), bg="whitesmoke", fg="black").grid(row=10, column=4, columnspan=2, sticky=N+S+E+W)

listbox_airlines = Listbox(window, selectmode="multiple", font=("Consolas", 8), bg="white", fg="black", height=12)
listbox_airlines.grid(row=11, column=4, rowspan=5, columnspan=2, padx=10, pady=10, sticky=N+S+E+W)



Button(window, text="LOAD ARRIVALS", bg="aliceblue", fg="black", font=("Segoe UI", 8), command=load_arrivals).grid(row=7, column=2, columnspan=2, padx=30, pady=5, sticky=N+S+E+W)
Button(window, text="SAVE FLIGHTS", bg="aliceblue", fg="black", font=("Segoe UI", 8), command=save_flights).grid(row=8, column=2, columnspan=2, padx=30, pady=5, sticky=N+S+E+W)


Label(window, text="PLOTS AND MAPS", font=("Segoe UI", 14), bg="whitesmoke", fg="black").grid(row=9, column=2, columnspan=2, pady=(15,0), sticky=N+S+E+W)
Button(window, text="PLOT ARRIVALS", bg="lightcyan", fg="black", font=("Segoe UI", 8), command=plot_arrivals).grid(row=10, column=2, columnspan=2, padx=30, pady=2, sticky=N+S+E+W)
Button(window, text="PLOT AIRLINES", bg="lightcyan", fg="black", font=("Segoe UI", 8), command=plot_airlines).grid(row=11, column=2, columnspan=2, padx=30, pady=2, sticky=N+S+E+W)

Button(window, text="PLOT FLIGHT TYPES", bg="lightcyan", fg="black", font=("Segoe UI", 8), command=plot_flight_types).grid(row=12, column=2, columnspan=2, padx=30, pady=2, sticky=N+S+E+W)
Button(window, text="PLOT AIRPORTS", bg="lightcyan", fg="black", font=("Segoe UI", 8), command=plot_airports).grid(row=13, column=2, columnspan=2, padx=30, pady=2, sticky=N+S+E+W)

Button(window, text="AIRPORTS MAP", bg="aquamarine", fg="black", font=("Segoe UI", 8), command=map_airports).grid(row=14, column=2, columnspan=2, padx=30, pady=2, sticky=N+S+E+W)
Button(window, text="FLIGHTS MAP", bg="aquamarine", fg="black", font=("Segoe UI", 8), command=map_flights).grid(row=15, column=2, columnspan=2, padx=30, pady=2, sticky=N+S+E+W)
Button(window, text="LONG FLIGHTS MAP", bg="aquamarine", fg="black", font=("Segoe UI", 8), command=map_long_flights).grid(row=16, column=2, columnspan=2, padx=30, pady=2, sticky=N+S+E+W)

Label(window, text="LEBL GATES", font=("Segoe UI", 16), bg="whitesmoke", fg="black").grid(row=1, column=4, columnspan=2, sticky=N+S+E+W)
Button(window, text="LOAD LEBL STRUCTURE", bg="khaki", command=load_LEBL).grid(row=2, column=4, columnspan=2, sticky=N+S+E+W)
Button(window, text="ASSIGN GATE", bg="lightgreen", command=assign_gate).grid(row=3, column=4, columnspan=2, sticky=N+S+E+W)
Button(window, text="SHOW GATE OCCUPANCY", bg="lightgreen", command=show_gate_occupancy).grid(row=4, column=4, columnspan=2, sticky=N+S+E+W)


fig = Figure(figsize=(8, 6), dpi=100, facecolor="white")
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=1, column=10, rowspan=14, columnspan=2, padx=5, pady=2, sticky=N+S+E+W)

window.mainloop()