from airport import *
archivo= "Airports.txt"
filename="filename.txt"
code = "BIKF"
airport = Airport("ATES", 41.375833, -3.375833, True)
airports = LoadAirports(archivo)

RemoveAirport(airports,code)

AddAirport (airports, airport)

SaveSchengenAirports(airports, filename)

i = 0
while i < len(airports):
    PrintAirport (airports[i])
    i = i + 1
PlotAirports (airports)
MapAirports(airports)













