from tkinter import *
from airport import *
airports = []

def refresh_list():
    listbox.delete(0, END)
    for a in airports:
        listbox.insert(END, f"{a.ICAO} ({a.latitude:.4f}, {a.longitude:.4f}) - Schengen: {a.Schengen}")

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
    sel = listbox.curselection()
    if sel:
        i = sel[0]
        RemoveAirport(airports, airports[i].ICAO)
        refresh_list()

def set_schengen():
    for a in airports:
        SetSchengen(a)
    refresh_list()

def save_schengen():
    from tkinter import filedialog
    filename = filedialog.asksaveasfilename()
    if filename:
        SaveSchengenAirports(airports, filename)

def plot_airports():
    PlotAirports(airports)

def map_airports():
    MapAirports(airports)

window = Tk()
window.geometry("800x500")
window.title("Airports")

for i in range(7):
    window.rowconfigure(i, weight=1)
for j in range(5):
    window.columnconfigure(j, weight=1)

Label(window, text="Airport Project", font=("Arial", 25)).grid(row=0, column=1, columnspan=3, sticky=N+S+E+W)

listbox = Listbox(window)
listbox.grid(row=1, column=1, columnspan=3, rowspan=3, padx=10, pady=10, sticky=N+S+E+W)

Button(window, text="Load", bg="lightgreen", command=load_airports).grid(row=1, column=0, padx=5, pady=5, sticky=N+S+E+W)
Button(window, text="Save\nSchengen", bg="lightgreen", command=save_schengen).grid(row=2, column=0, padx=5, pady=5, sticky=N+S+E+W)

Button(window, text="Set\nSchengen", bg="lightgreen", command=set_schengen).grid(row=1, column=4, padx=5, pady=5, sticky=N+S+E+W)
Button(window, text="Remove Airport", bg="lightgrey", command=remove_airport).grid(row=2, column=4, padx=5, pady=5, sticky=N+S+E+W)
Button(window, text="Plot", bg="cyan", command=plot_airports).grid(row=3, column=4, padx=5, pady=5, sticky=N+S+E+W)
Button(window, text="Map", bg="cyan", command=map_airports).grid(row=4, column=4, padx=5, pady=5, sticky=N+S+E+W)

Label(window, text="ICAO", font=("Arial", 16)).grid(row=4, column=1, sticky=E)
entry_code = Entry(window)
entry_code.grid(row=4, column=2, sticky=N+S+E+W)

Label(window, text="Latitude", font=("Arial", 16)).grid(row=5, column=1, sticky=E)
entry_lat = Entry(window)
entry_lat.grid(row=5, column=2, sticky=N+S+E+W)

Label(window, text="Longitude", font=("Arial", 16)).grid(row=6, column=1, sticky=E)
entry_lon = Entry(window)
entry_lon.grid(row=6, column=2, sticky=N+S+E+W)

Button(window, text="Add", bg="grey", command=add_airport).grid(row=4, column=3, rowspan=3, padx=5, pady=5, sticky=N+S+E+W)

window.mainloop()