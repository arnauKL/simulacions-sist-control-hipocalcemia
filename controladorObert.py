import matplotlib.pyplot as plt
from collections import deque
import numpy as np
import time

MAX_DADES = 100

def main() -> None:

    #plt.style.use('dark_background')

    # 1. Paràmetres fisiològics
    Ca_normal = 9.5            # mg/dL, nivell normal de calci total
    Ca_inicial = Ca_normal     # punt de partida
    Ca_threshold = 8.5         # mg/dL, llindar d'hipocalcèmia
    #pas_temps = 0.5            # cada pas és 0.5 hores (30 minuts)
    pas_temps = 1            # cada pas és 1 hora

    # Constants model (m les he inventades, podríem experimentar amb diferents valors x diferents pacients)
    # aquestes constants mantenten un nivel norlmal sense necessitar bolus
    pth_gain = 0.2             # efecte de la PTH sobre el Ca2+
    absorcio_dietaria = 0.4    # increment de Ca2+ per cada àpat
    interval_apats = 6         # hores entre àpats

    # 2. Inicialització de variables
    temps = deque([0.0]*MAX_DADES, maxlen=MAX_DADES)                # Vector amb instants de temps
    nivells_Ca = deque([Ca_inicial]*MAX_DADES, maxlen=MAX_DADES)    # Vector amb dades de calci
    nivells_PTH = deque([0.0]*MAX_DADES, maxlen=MAX_DADES)

    temps_transcorregut = 0.0
    Ca_actual = Ca_inicial

    # Iniciam plot
    plt.ion()
    fig, ax = plt.subplots()
    lineCa, = ax.plot(list(temps), list(nivells_Ca), label='Nivell de Ca2+ en sang', color='blue')
    linePTH, = ax.plot(list(temps), list(nivells_PTH), label='Nivell de PTH en sang', color='magenta')
    ax.axhline(Ca_normal, color='green', linestyle='--', label='Nivell Normal')
    ax.axhline(Ca_threshold, color='red', linestyle='--', label='Llindar Hipocalcèmia')
    ax.set_xlabel('Temps (hores)')
    ax.set_ylabel('Nivell de Ca2+ (mg/dL)')
    ax.set_title('Simulació de Control de la Hipocalcèmia en un pacient sa')
    ax.legend()
    ax.grid(True)
    #ax.set_ylim(7.5, 10.5)

    while True:
        # Simulació de la caiguda natural del Ca2+
        # Aquesta caiguda varia durant el dia (per exemple, activitat renal, hormones, etc.)
        velocitat_baixada = 0.15 + 0.07 * np.sin(temps_transcorregut / 2 * np.pi / 24)
        Ca_actual -= velocitat_baixada * pas_temps

        # Simulació d'una ingesta de calci (cada 6 hores)
        if int((temps_transcorregut - pas_temps) // interval_apats) != int(temps_transcorregut // interval_apats):
            Ca_actual += absorcio_dietaria

        nivells_Ca.append(Ca_actual)
        # Producció de PTH proporcional al dèficit de Ca2+
        produccio_PTH = max(0.0, Ca_normal - Ca_actual) # En un pacient normal
        #produccio_PTH = 0.0                             # En el nostre pacient

        # Administració bolus
        if Ca_actual < Ca_threshold:
            print(f"Bolus de PTH a temps {temps_transcorregut}")
            PTH_exogena = 3.0
        else:
            PTH_exogena = 0.0

        # suma amb la producció endògena
        PTH_total = produccio_PTH + PTH_exogena
        nivells_PTH.append(PTH_total)
        
        # Efecte de la PTH: augment de Ca2+
        Ca_actual += PTH_total * pth_gain * pas_temps

        # gràfic
        temps_transcorregut += pas_temps
        temps.append(temps_transcorregut)

        linePTH.set_ydata(nivells_PTH)
        linePTH.set_xdata(temps)
        lineCa.set_ydata(nivells_Ca)
        lineCa.set_xdata(temps)
        ax.set_xlim(min(temps), max(temps))

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.01)

if __name__ == "__main__":
    main()
