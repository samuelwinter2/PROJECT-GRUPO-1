#El usario debe introducir en dos cuadros de texto dos horas entre le 0 y el 23 y cuando pulse un boton el programa debe indicar el numero de vuelos que tienen prevista su salida del aeorpuerto en el perido de primera a la segunda hora
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import airport
import aircraft
from LEBL import *
import LEBL
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import winsound
import tkintermapview

airports = []
aircrafts = []
departures = []
bcn = -1

# Actualiza la listbox de aeropuertos con los datos de airports
def refresh_list():
    listbox_airports.delete(0, END)  # Borra toda la listbox
    i = 0
    while i < len(airports):
        a = airports[i]
        if a.Schengen:
            sch = "✔"
        else:
            sch = "✖"

        listbox_airports.insert(END, f"{a.ICAO}  ({a.latitude:.2f}, {a.longitude:.2f})  [{sch}]")

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
    global airports
    filename = filedialog.askopenfilename()
    if not filename:
        return
    try:
        airports = airport.LoadAirports(filename)
        if len(airports) == 0:
            messagebox.showwarning("Warning", "The file is empty or contains no valid airports.")
            print("Warning: empty or invalid file.")
        refresh_list()
    except:
        messagebox.showwarning("Warning", "Could not load the airports file.")
        print("Warning: error loading airports.")

def add_airport():
    try:
        code = entry_code.get().strip()
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
        a = airport.Airport(code, lat, lon)
        airport.SetSchengen(a)
        airport.AddAirport(airports, a)
        refresh_list()
    except:
        messagebox.showwarning("Warning", "Invalid data. Check ICAO, latitude and longitude.")
        print("Warning: invalid data when adding airport.")

def remove_airport():
    sel = listbox_airports.curselection()  # Línea seleccionada en la listbox
    if not sel:
        messagebox.showwarning("Warning", "Select an airport to remove.")
        print("Warning: no airport selected.")
        return
    i = sel[0]                          # Primera línea seleccionada
    RemoveAirport(airports, airports[i].ICAO)
    refresh_list()


def set_schengen():
    if len(airports) == 0:
        messagebox.showwarning("Warning", "No airports loaded.")
        print("Warning: airport list is empty.")
        return
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1
    refresh_list()


def save_schengen():
    if len(airports) == 0:
        messagebox.showwarning("Warning", "No airports loaded.")
        print("Warning: airport list is empty.")
        return
    filename = filedialog.asksaveasfilename()
    if not filename:
        return
    try:
        airport.SaveSchengenAirports(airports, filename)
    except:
        messagebox.showwarning("Warning", "Could not save the file.")
        print("Warning: error saving file.")


def plot_airports():
    if len(airports) == 0:
        messagebox.showwarning("Warning", "No airports loaded.")
        print("Warning: airport list is empty.")
        return

    notebook.select(1)
    fig.clf()
    ax = fig.add_subplot(111)
    airport.ax = ax
    PlotAirports(airports)
    canvas.draw()

def map_airports():
    if len(airports) == 0:
        messagebox.showwarning("Warning", "No airports loaded.")
        print("Warning: airport list is empty.")
        return

    notebook.select(0)
    map_widget.delete_all_marker()
    map_widget.delete_all_path()
    i = 0
    while i < len(airports):
        airport.SetSchengen(airports[i])
        a = airports[i]
        color_a = "blue" if a.Schengen else "red"
        map_widget.set_marker(a.latitude, a.longitude, text=a.ICAO, marker_color_circle=color_a)
        i = i + 1
    if len(airports) > 0:
        map_widget.set_position(airports[0].latitude, airports[0].longitude)
        map_widget.set_zoom(4)

def map_flights():
    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "No arrivals loaded.")
        print("Warning: flight list is empty.")
        return
    if len(airports) == 0:
        messagebox.showwarning("Warning", "No airports loaded.")
        print("Warning: airport list is empty.")
        return
    notebook.select(0)
    map_widget.delete_all_marker()
    map_widget.delete_all_path()
    i = 0
    while i < len(aircrafts):
        flight = aircrafts[i]
        j = 0
        encontrado = False
        lat = 0
        lon = 0
        while j < len(airports) and not encontrado:
            if airports[j].ICAO == flight.origin:
                encontrado = True
                if airports[j].Schengen:
                    color_vuelo = "blue"
                else:
                    color_vuelo = "red"
                lat = airports[j].latitude
                lon = airports[j].longitude
            j = j + 1
        if encontrado:
            map_widget.set_path([(lat, lon), (41.2974, 2.0833)], color=color_vuelo, width=2)
        i = i + 1
    map_widget.set_position(41.2974, 2.0833)
    map_widget.set_zoom(4)

def map_long_flights():
    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "No arrivals loaded.")
        print("Warning: flight list is empty.")
        return
    if len(airports) == 0:
        messagebox.showwarning("Warning", "No airports loaded.")
        print("Warning: airport list is empty.")
        return
    notebook.select(0)
    map_widget.delete_all_marker()
    map_widget.delete_all_path()
    long_flights = aircraft.LongDistanceArrivals(aircrafts)
    i = 0
    while i < len(long_flights):
        flight = long_flights[i]
        j = 0
        encontrado = False
        lat = 0
        lon = 0
        while j < len(airports) and not encontrado:
            if airports[j].ICAO == flight.origin:
                encontrado = True
                if airports[j].Schengen:
                    color_vuelo = "blue"
                else:
                    color_vuelo = "red"
                lat = airports[j].latitude
                lon = airports[j].longitude
            j = j + 1
        if encontrado:
            map_widget.set_path([(lat, lon), (41.2974, 2.0833)], color=color_vuelo, width=2)
        i = i + 1
    map_widget.set_position(41.2974, 2.0833)
    map_widget.set_zoom(3)

def load_arrivals():
    global aircrafts
    filename = filedialog.askopenfilename()
    if not filename:
        return
    try:
        aircrafts = aircraft.LoadArrivals(filename)
    except:
        messagebox.showwarning("Warning", "Could not load the arrivals file.")
        print("Warning: error loading arrivals.")
        return

    listbox_arrivals.delete(0, END) # Borra la listbox de vuelos

    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "The arrivals file is empty.")
        print("Warning: empty arrivals file.")
        return

    i = 0
    while i < len(aircrafts):  # Inserta cada vuelo en la listbox
        a = aircrafts[i]
        listbox_arrivals.insert(END, f"{a.id} | {a.origin} → {a.time} | {a.company}")
        i = i + 1

    refresh_airlines_list()  # Actualiza aerolíneas

def save_flights():
    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "No arrivals loaded.")
        print("Warning: flight list is empty.")
        return
    filename = filedialog.asksaveasfilename()
    if not filename:
        return

    try:
        aircraft.SaveFlights(aircrafts, filename)
    except:
        messagebox.showwarning("Warning", "Could not save the flights file.")
        print("Warning: error saving flights.")

def plot_arrivals():
    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "No arrivals loaded.")
        print("Warning: flight list is empty.")
        return
    notebook.select(1)
    fig.clf()
    ax = fig.add_subplot(111)
    aircraft.ax = ax
    PlotArrivals(aircrafts)
    canvas.draw()

def plot_airlines():
    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "No arrivals loaded.")
        print("Warning: flight list is empty.")
        return
    notebook.select(1)
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
    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "No arrivals loaded.")
        print("Warning: flight list is empty.")
        return
    notebook.select(1)
    fig.clf()
    ax = fig.add_subplot(111)
    aircraft.ax = ax
    PlotFlightsType(aircrafts)
    canvas.draw()

def load_LEBL():
    global bcn

    filename = filedialog.askopenfilename(title="Select LEBL structure file")
    if not filename:
        return
    try:
        bcn = LoadAirportStructure(filename)
    except:
        messagebox.showwarning("Warning", "Could not load LEBL structure.")
        print("Warning: error loading LEBL.")
        return

    if bcn == -1:
        messagebox.showwarning("Warning", "The LEBL file is empty or invalid.")
        print("Warning: invalid LEBL file.")
    else:
        print("LEBL structure loaded:", bcn.code, "Terminals:", len(bcn.terminals))

def assign_gate():
    global bcn

    if bcn == -1:
        messagebox.showwarning("Warning", "Load LEBL before assigning gates.")
        print("Warning: LEBL not loaded.")
        return

    sel = listbox_merged.curselection()
    if not sel:
        messagebox.showwarning("Warning", "Select a flight.")
        print("Warning: no flight selected.")
        return

    aircraft_sel = aircrafts[sel[0]]
    gate = AssignGate(bcn, aircraft_sel)

    print("Gate assigned:", gate)

def assign_all_gates():
    global bcn
    if bcn == -1:
        messagebox.showwarning("Warning", "Load LEBL before assigning gates.")
        print("Warning: LEBL not loaded.")
        return
    if bcn == -1:
        print("Load LEBL first.")
        return

    i = 0
    not_assigned = 0
    while i < len(aircrafts):
        gate = AssignGate(bcn, aircrafts[i])
        if gate == -1:
            not_assigned += 1
        i = i + 1

    print("Finished assigning all gates. Not assigned:", not_assigned)

def unassign_gate():
    global bcn
    if bcn == -1:
        messagebox.showwarning("Warning", "Load LEBL before freeing gates.")
        print("Warning: LEBL not loaded.")
        return

    sel = listbox_merged.curselection()
    if not sel:
        messagebox.showwarning("Warning", "Select a flight.")
        print("Warning: no flight selected.")
        return

    aircraft_sel = aircrafts[sel[0]]
    gate = FreeGate(bcn, aircraft_sel.id)

    if gate == -1:
        print("This aircraft was not assigned to any gate.")
    else:
        print("Gate", gate, "freed from aircraft", aircraft_sel.id)

def unassign_all_gates():
    if bcn == -1:
        messagebox.showwarning("Warning", "Load LEBL before freeing gates.")
        print("Warning: LEBL not loaded.")
        return
    t = 0
    while t < len(bcn.terminals):
        a = 0
        while a < len(bcn.terminals[t].boarding_areas):
            g = 0
            while g < len(bcn.terminals[t].boarding_areas[a].gates):
                gate = bcn.terminals[t].boarding_areas[a].gates[g]
                gate.occupied = False
                gate.aircraft_id = ""
                g = g + 1
            a = a + 1
        t = t + 1
    print("All gates freed")

def assign_gate_text():
    global bcn
    if bcn == -1:
        messagebox.showwarning("Warning", "Load LEBL before assigning gates.")
        print("Warning: LEBL not loaded.")
        return

    sel = listbox_merged.curselection()
    if not sel:
        messagebox.showwarning("Warning", "Select a flight.")
        print("Warning: no flight selected.")
        return

    aircraft_sel = aircrafts[sel[0]]
    gate_name = entry_gate.get().strip()
    if gate_name == "":
        messagebox.showwarning("Warning", "Enter a gate.")
        print("Warning: empty gate name.")
        return

    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                if gate.name == gate_name:
                    if gate.occupied:
                        print("Gate already occupied.")
                        return
                    gate.occupied = True
                    gate.aircraft_id = aircraft_sel.id
                    print("Assigned", aircraft_sel.id, "to gate", gate_name)
                    return

    print("Gate not found:", gate_name)
    messagebox.showwarning("Warning", "Gate not found")
# Variable global para controlar qué terminal estamos mostrando (empieza en la T1)
terminal_actual = 1

def show_gate_occupancy():
    global bcn
    global terminal_actual
    if bcn == -1:
        messagebox.showwarning("Warning", "Load LEBL before showing occupancy.")
        print("Warning: LEBL not loaded.")
        return
    notebook.select(1)
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
    ax.text(0.2, 1, f"ESTADO DE PUERTAS - {bcn.code} ({terminal_a_dibujar.name})",transform=ax.transAxes, fontsize=11, fontweight="bold", color="black")

    ax.text(0.2, 0, "(Pulsa el botón otra vez para cambiar de Terminal)",transform=ax.transAxes, fontsize=9, color="black", style="italic")

    start_x = 2 # Inicio del dibujo
    num_areas = len(terminal_a_dibujar.boarding_areas)
    end_x = start_x + (num_areas * 7) # Final del dibujo

    ax.plot([start_x - 1, end_x], [25, 25], color='blue', linewidth=6)  # Barra superior
    ax.text(start_x - 0.5, 26, terminal_a_dibujar.name,color='blue', fontweight='bold', fontsize=12)

    i = 0
    while i < len(terminal_a_dibujar.boarding_areas): # Recorre áreas
        area = terminal_a_dibujar.boarding_areas[i]
        x = start_x + (i * 7) + 1 # Posición X del área

        ax.plot([x, x], [25, 1], color='blue', linewidth=4)  # Línea vertical del área
        ax.text(x - 0.5, 1, area.name, fontweight='bold', fontsize=10, color="black")

        num_puertas = len(area.gates) # Número de puertas del área

        if num_puertas > 0:
            separacion = 23.0 / num_puertas # Disancia entre puertas
        else:
            separacion = 1.0

        if "Area B" in area.name:
            ancho_rectangulo = 1.4
            alto_rectangulo = 0.46
            tamano_letra = 5.0
        else:
            ancho_rectangulo = 2.4
            alto_rectangulo = 0.58
            tamano_letra = 7.0

        j = 0
        while j < len(area.gates): # Recorre puertas
            gate = area.gates[j]
            y = 24.3 - (j * separacion)

            if j % 2 == 0: # Alterna izquierda/derecha
                gx_end = x + 0.9
                rect_x = gx_end
            else:
                gx_end = x - 0.9
                rect_x = gx_end - ancho_rectangulo

            text_x = rect_x + (ancho_rectangulo / 2)

            ax.plot([x, gx_end], [y, y], color='blue', linewidth=1)

            if gate.occupied:
                color_puerta = 'red'
            else:
                color_puerta = 'green'

            import matplotlib.patches as patches
            rectangulo = patches.Rectangle((rect_x, y - (alto_rectangulo / 2)),ancho_rectangulo,alto_rectangulo,facecolor=color_puerta,edgecolor='black',linewidth=0.5 )
            ax.add_patch(rectangulo)

            if gate.occupied:
                ax.text(text_x, y - 0.02, gate.aircraft_id, color='black', fontsize=tamano_letra, fontweight='bold', ha='center', va='center')
            else:
                ax.text(text_x, y - 0.02, gate.name,color='black', fontsize=tamano_letra, fontweight='bold',ha='center', va='center')

            j = j + 1

        i = i + 1

    ax.set_xlim(0, end_x + 1)
    ax.set_ylim(0, 26)
    ax.set_axis_off()

    canvas.draw()

    if terminal_actual == 1: # Alterna terminal
        terminal_actual = 2
    else:
        terminal_actual = 1

def show_gate_occupancy_hour():
    global bcn, aircrafts
    if bcn == -1:
        messagebox.showwarning("Warning", "Load LEBL before showing occupancy.")
        print("Warning: LEBL not loaded.")
        return

    hour = entry_hour.get()
    if hour == "":
        messagebox.showwarning("Warning", "Enter an hour.")
        print("Warning: empty hour.")
        return

    try:
        hour_int = int(hour)
        if hour_int < 0 or hour_int > 23:
            messagebox.showwarning("Warning", "Hour must be between 0 and 23.")
            print("Warning: hour out of range.")
            return
    except:
        messagebox.showwarning("Warning", "Enter a valid hour.")
        print("Warning: invalid hour.")
        return

    t = 0
    while t < len(bcn.terminals):
        a = 0
        while a < len(bcn.terminals[t].boarding_areas):
            g = 0
            while g < len(bcn.terminals[t].boarding_areas[a].gates):
                gate = bcn.terminals[t].boarding_areas[a].gates[g]
                gate.aircraft_id = ""
                gate.occupied = False
                g += 1
            a += 1
        t += 1

    night_list = NightAircraft(aircrafts)
    if night_list != -1:
        AssignNightGates(bcn, night_list)

    h = 0
    while h <= hour_int:
        AssignGatesAtTime(bcn, aircrafts, f"{h:02d}:00")
        h += 1

    show_gate_occupancy()


def load_departures():
    global departures
    filename = filedialog.askopenfilename()
    if not filename:
        return
    try:
        departures = aircraft.LoadDepartures(filename)
    except:
        messagebox.showwarning("Warning", "Could not load the departures file.")
        print("Warning: error loading departures.")
        return

    listbox_departures.delete(0, END)

    if len(departures) == 0:
        messagebox.showwarning("Warning", "The departures file is empty.")
        print("Warning: empty departures file.")
        return

    i = 0
    while i < len(departures):
        d = departures[i]
        listbox_departures.insert(END, f"{d.id} | {d.destination} {d.departure} | {d.company}")
        i = i + 1


def merge_movements():
    global aircrafts
    global departures

    if len(aircrafts) == 0 or len(departures) == 0:
        messagebox.showwarning("Warning", "Load arrivals and departures before merging.")
        print("Warning: missing arrivals or departures.")
        return

    aircrafts = MergeMovements(aircrafts, departures)

    listbox_merged.delete(0, END)

    i = 0
    while i < len(aircrafts):
        a = aircrafts[i]
        listbox_merged.insert(END, f"{a.id} | {a.origin} | ARR:{a.time} | {a.company} | DEP:{a.departure}")
        i = i + 1

    print("Movements merged:", len(aircrafts))


def plot_day_occupancy():
    notebook.select(1)
    global bcn, aricrafts
    if bcn == -1:
        messagebox.showwarning("Warning", "Load LEBL before showing daily occupancy.")
        print("Warning: LEBL not loaded.")
        return
    fig.clf()
    ax = fig.add_subplot(111)
    LEBL.ax = ax
    PlotDayOccupancy(bcn, aircrafts)
    canvas.draw()

def assign_night_aircraft():
    global bcn, aircrafts

    if bcn == -1:
        messagebox.showwarning("Warning", "Load LEBL before assigning night aircraft.")
        print("Warning: LEBL not loaded.")
        return

    night_list = NightAircraft(aircrafts)
    if night_list == -1:
        messagebox.showwarning("Warning", "No night aircraft found.")
        print("Warning: no night aircraft.")
        return

    AssignNightGates(bcn, night_list)

def search_flights(event=None):
    text = entry_search.get().lower()

    listbox_merged.delete(0, END)

    i = 0
    while i < len(aircrafts):
        a = aircrafts[i]
        line = f"{a.id} {a.origin} {a.time} {a.company} {a.departure}".lower()
        if text in line:
            listbox_merged.insert(END, f"{a.id} | {a.origin} | ARR:{a.time} | {a.company} | DEP:{a.departure}")

        i = i + 1

# BACKGROUND MUSIC (WINSOUND)

def play_selected_music():

    sel = listbox_music.curselection()
    if not sel:
        messagebox.showwarning("Warning", "Select a sound first.")
        print("Warning: no sound selected.")
        return

    sound_name = listbox_music.get(sel[0])

    sound_files = {
        "Cafe": "Sonidos/Cafe.wav",
        "Crab Rave": "Sonidos/CrabRave.wav",
        "Guitar": "Sonidos/Guitar.wav",
        "Jazz": "Sonidos/Jazz.wav",
        "Lounge": "Sonidos/Lounge.wav",
        "Piano": "Sonidos/Piano.wav",
    }

    filename = sound_files[sound_name]

    try:

        winsound.PlaySound(
            filename,
            winsound.SND_FILENAME
            | winsound.SND_ASYNC
            | winsound.SND_LOOP
        )

        print("Playing:", sound_name)


    except Exception as e:
        messagebox.showwarning("Warning", "Error playing sound. Check file path or WAV format.")
        print("Warning: error playing sound:", e)
        print("Warning: check file path or WAV format.")


def stop_music():

    winsound.PlaySound(None, winsound.SND_PURGE)

    print("Music stopped")


def aplicar_hover_automatico(ventana):
    colores_hover = {
        "#C2B69D": "#D8CFC0",
        "#BAC5C6": "#D0D9DA",
        "#4A5D6B": "#5C7485",
        "#A64B42": "#BD5A50",
        "#D4E2D7": "#E4F0E7",
        "#B9CDCE": "#CFE1E2",
        "#8C6D53": "#A18268"
    }

    def activar_color(boton, color_normal, color_hover):
        boton.bind("<Enter>", lambda e: boton.configure(bg=color_hover))
        boton.bind("<Leave>", lambda e: boton.configure(bg=color_normal))
    for widget in ventana.winfo_children():

        if widget.winfo_class() == 'Button':

            color_original = str(widget.cget('bg')).upper()
            if color_original in colores_hover:
                color_claro = colores_hover[color_original]
                activar_color(widget, color_original, color_claro)


window = Tk()
window.geometry("1920x1080")
window.title("Proyecto Informatica - Airport Manager")
window.configure(bg="#E6E2D3")

for i in range(16):
    window.rowconfigure(i, weight=1)

window.columnconfigure(0, weight=4)
window.columnconfigure(1, weight=4)
window.columnconfigure(2, weight=4)
window.columnconfigure(3, weight=4)
window.columnconfigure(4, weight=4)
window.columnconfigure(5, weight=4)
window.columnconfigure(6, weight=2)
window.columnconfigure(7, weight=2)
window.columnconfigure(8, weight=12)

Label(window, text="AIRPORT MANAGER", font=("Segoe UI", 26, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=0, column=3, columnspan=5, pady=(20, 15), sticky=N+S+E+W)

Label(window, text="AIRPORTS", font=("Segoe UI", 14, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=1, column=0, columnspan=2, sticky=W, padx=15)

listbox_airports = Listbox(window, font=("Consolas", 10), bg="#FAF8F5", fg="#2A2421", bd=1, relief="solid", width=55)
listbox_airports.grid(row=2, column=0, columnspan=2, rowspan=5, padx=15, pady=5, sticky=N+S+E+W)

Button(window, text="LOAD AIRPORTS", bg="#C2B69D", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=load_airports).grid(row=7, column=0, padx=(15, 5), pady=3, sticky=N+S+E+W)
Button(window, text="SAVE SCHENGEN", bg="#BAC5C6", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=save_schengen).grid(row=7, column=1, padx=(5, 15), pady=3, sticky=N+S+E+W)
Button(window, text="SET SCHENGEN", bg="#4A5D6B", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=set_schengen).grid(row=8, column=0, padx=(15, 5), pady=3, sticky=N+S+E+W)
Button(window, text="REMOVE AIRPORT", bg="#A64B42", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=remove_airport).grid(row=8, column=1, padx=(5, 15), pady=3, sticky=N+S+E+W)

Label(window, text="ADD NEW AIRPORT", font=("Segoe UI", 11, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=9, column=0, columnspan=2, pady=(15, 5), padx=15, sticky=W)
Label(window, text="ICAO CODE", bg="#E6E2D3", fg="#2A2421", font=("Segoe UI", 9)).grid(row=10, column=0, padx=15, sticky=W)
entry_code = Entry(window, bd=1, relief="solid")
entry_code.grid(row=10, column=1, padx=15, sticky=E+W)
Label(window, text="LATITUDE", bg="#E6E2D3", fg="#2A2421", font=("Segoe UI", 9)).grid(row=11, column=0, padx=15, sticky=W)
entry_lat = Entry(window, bd=1, relief="solid")
entry_lat.grid(row=11, column=1, padx=15, sticky=E+W)
Label(window, text="LONGITUDE", bg="#E6E2D3", fg="#2A2421", font=("Segoe UI", 9)).grid(row=12, column=0, padx=15, sticky=W)
entry_lon = Entry(window, bd=1, relief="solid")
entry_lon.grid(row=12, column=1, padx=15, sticky=E+W)
Button(window, text="ADD AIRPORT", bg="#C2B69D", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=add_airport).grid(row=13, column=0, columnspan=2, padx=15, pady=10, sticky=E+W)

Label(window, text="ARRIVALS", font=("Segoe UI", 14, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=1, column=2, columnspan=2, sticky=W, padx=10)
listbox_arrivals = Listbox(window, font=("Consolas", 10), bg="#FAF8F5", fg="#2A2421", bd=1, relief="solid", width=48)
listbox_arrivals.grid(row=2, column=2, columnspan=2, rowspan=5, padx=10, pady=5, sticky=N+S+E+W)

Label(window, text="DEPARTURES", font=("Segoe UI", 14, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=1, column=4, columnspan=2, sticky=W, padx=10)
listbox_departures = Listbox(window, font=("Consolas", 10), bg="#FAF8F5", fg="#2A2421", bd=1, relief="solid", width=48)
listbox_departures.grid(row=2, column=4, columnspan=2, rowspan=5, padx=10, pady=5, sticky=N+S+E+W)

Button(window, text="LOAD ARRIVALS", bg="#C2B69D", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=load_arrivals).grid(row=7, column=2, columnspan=2, padx=10, pady=3, sticky=N+S+E+W)
Button(window, text="LOAD DEPARTURES", bg="#C2B69D", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=load_departures).grid(row=7, column=4, columnspan=2, padx=10, pady=3, sticky=N+S+E+W)
Button(window, text="SAVE FLIGHTS", bg="#BAC5C6", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=save_flights).grid(row=8, column=2, columnspan=2, padx=10, pady=3, sticky=N+S+E+W)

Label(window, text="MAPS & FLIGHT VISUALIZATIONS", font=("Segoe UI", 11, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=9, column=2, columnspan=4, pady=(15, 5), padx=10, sticky=W)
Button(window, text="PLOT ARRIVALS", bg="#D4E2D7", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=plot_arrivals).grid(row=10, column=2, columnspan=2, padx=10, pady=3, sticky=N+S+E+W)
Button(window, text="AIRPORTS MAP", bg="#B9CDCE", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=map_airports).grid(row=10, column=4, columnspan=2, padx=10, pady=3, sticky=N+S+E+W)
Button(window, text="PLOT FLIGHT TYPES", bg="#D4E2D7", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=plot_flight_types).grid(row=11, column=2, columnspan=2, padx=10, pady=3, sticky=N+S+E+W)
Button(window, text="FLIGHTS MAP", bg="#B9CDCE", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=map_flights).grid(row=11, column=4, columnspan=2, padx=10, pady=3, sticky=N+S+E+W)
Button(window, text="PLOT AIRPORTS", bg="#D4E2D7", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=plot_airports).grid(row=12, column=2, columnspan=2, padx=10, pady=3, sticky=N+S+E+W)
Button(window, text="LONG FLIGHTS MAP", bg="#B9CDCE", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=map_long_flights).grid(row=12, column=4, columnspan=2, padx=10, pady=3, sticky=N+S+E+W)

Label(window, text="SELECT AIRLINES", font=("Segoe UI", 10, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=13, column=2, columnspan=2, padx=10, pady=(10, 2), sticky=W)
listbox_airlines = Listbox(window, selectmode="multiple", font=("Consolas", 10), bg="#FAF8F5", fg="#2A2421", bd=1, relief="solid", width=35)
listbox_airlines.grid(row=14, column=2, columnspan=2, padx=10, pady=2, sticky=N+S+E+W)
Button(window, text="PLOT SELECTED AIRLINES", bg="#D4E2D7", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=plot_airlines).grid(row=15, column=2, columnspan=2, padx=10, pady=5, sticky=N+S+E+W)

Label(window, text="LEBL GATES", font=("Segoe UI", 14, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=1, column=6, columnspan=2, sticky=W, padx=15)

Button(window, text="LOAD LEBL STRUCTURE", bg="#C2B69D", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=load_LEBL).grid(row=2, column=6, columnspan=2, padx=15, pady=4, sticky=N+S+E+W)

Button(window, text="MERGE MOVEMENTS", bg="#C2B69D", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", width=18, command=merge_movements).grid(row=3, column=6, padx=(15,5), pady=4, sticky=N+S+E+W)
Button(window, text="ASSIGN NIGHT", bg="#8C6D53", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", width=18, command=assign_night_aircraft).grid(row=3, column=7, padx=(5,15), pady=4, sticky=N+S+E+W)

Button(window, text="ASSIGN GATE", bg="#8C6D53", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", width=18, command=assign_gate).grid(row=4, column=6, padx=(15, 5), pady=4, sticky=N+S+E+W)
Button(window, text="ASSIGN ALL", bg="#8C6D53", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", width=18, command=assign_all_gates).grid(row=4, column=7, padx=(5, 15), pady=4, sticky=N+S+E+W)

Button(window, text="UNASSIGN", bg="#A64B42", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", width=18, command=unassign_gate).grid(row=5, column=6, padx=(15, 5), pady=4, sticky=N+S+E+W)
Button(window, text="UNASSIGN ALL", bg="#A64B42", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", width=18, command=unassign_all_gates).grid(row=5, column=7, padx=(5, 15), pady=4, sticky=N+S+E+W)

Label(window, text="GATE NAME:", bg="#E6E2D3", fg="#2A2421", font=("Segoe UI", 9, "bold")).grid(row=6, column=6, padx=(15, 5), sticky=E)
entry_gate = Entry(window, bd=1, relief="solid", font=("Consolas", 10), width=8)
entry_gate.grid(row=6, column=7, padx=(5, 15), sticky=W)

Button(window, text="ASSIGN GATE TEXT", bg="#4A5D6B", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=assign_gate_text).grid(row=7, column=6, columnspan=2, padx=15, pady=4, sticky=N+S+E+W)
Button(window, text="PLOT DAY OCCUPANCY", bg="#D4E2D7", fg="#2A2421", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=plot_day_occupancy).grid(row=8, column=6, columnspan=2, padx=15, pady=4, sticky=N+S+E+W)
Button(window, text="SHOW GATE OCCUPANCY", bg="#8C6D53", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=show_gate_occupancy).grid(row=9, column=6, columnspan=2, padx=15, pady=(10, 5), sticky=N+S+E+W)

Label(window, text="HOUR(00-23):", bg="#E6E2D3", fg="#2A2421", font=("Segoe UI", 9, "bold")).grid(row=10, column=6, padx=(15, 5), sticky=E)
entry_hour = Entry(window, bd=1, relief="solid", font=("Consolas", 10), width=8)
entry_hour.grid(row=10, column=7, padx=(5, 15), sticky=W)

Button(window, text="ASSIGN AND SHOW OCCUPANCY AT HOUR", bg="#4A5D6B", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=show_gate_occupancy_hour).grid(row=11, column=6, columnspan=2, padx=15, pady=5, sticky=N+S+E+W)
Label(window, text="MERGED MOVEMENTS", font=("Segoe UI", 14, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=12, column=6, columnspan=2, sticky=W, padx=15)
listbox_merged = Listbox(window, font=("Consolas", 10), bg="#FAF8F5", fg="#2A2421", bd=1, relief="solid", width=48)
listbox_merged.grid(row=14, column=6, columnspan=2, rowspan=2, padx=15, pady=5, sticky=N+S+E+W)
Label(window, text="SEARCH:", bg="#E6E2D3", fg="#2A2421", font=("Segoe UI", 9, "bold")).grid(row=13, column=6, padx=(15, 5), sticky=E)
entry_search = Entry(window, bd=1, relief="solid", font=("Consolas", 10), width=8)
entry_search.grid(row=13, column=7,columnspan=1, padx=(5, 15), sticky=W)
entry_search.bind("<KeyRelease>", search_flights)

Label(window, text="BACKGROUND MUSIC", font=("Segoe UI", 11, "bold"), bg="#E6E2D3", fg="#1B2A4A").grid(row=13, column=4, columnspan=2, padx=15, pady=(10, 5), sticky=W)
listbox_music = Listbox(window, font=("Consolas", 10), height=6, bg="#FAF8F5", relief="solid")
listbox_music.grid(row=14, column=4, columnspan=2, padx=15, pady=5, sticky=N+S+E+W)
musics = ["Cafe", "Crab Rave", "Guitar", "Jazz", "Lounge", "Piano"]

i = 0
while i < len(musics):
    listbox_music.insert(END, musics[i])
    i += 1

Button(window, text="PLAY MUSIC", bg="#4A5D6B", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=play_selected_music).grid(row=15, column=4, padx=(15, 5), pady=5, sticky=N+S+E+W)
Button(window, text="STOP MUSIC", bg="#A64B42", fg="white", font=("Segoe UI", 9, "bold"), bd=1, relief="groove", command=stop_music).grid(row=15, column=5, padx=(5, 15), pady=5, sticky=N+S+E+W)



notebook = ttk.Notebook(window)
notebook.grid(row=1, column=8, rowspan=15, columnspan=2, padx=(15, 20), pady=10, sticky=N+S+E+W)


pestana_mapa = Frame(notebook)
pestana_graficos = Frame(notebook)

notebook.add(pestana_mapa, text="Map")
notebook.add(pestana_graficos, text="Plots and gate occupancy")

map_widget = tkintermapview.TkinterMapView(pestana_mapa, width=800, height=600, corner_radius=0)
map_widget.pack(fill="both", expand=True)
map_widget.set_position(41.2974, 2.0833)
map_widget.set_zoom(4)

fig = Figure(figsize=(8, 6), dpi=100, facecolor="white")
canvas = FigureCanvasTkAgg(fig, master=pestana_graficos)
canvas.get_tk_widget().pack(fill="both", expand=True)

aplicar_hover_automatico(window)


def on_closing():
    stop_music()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()