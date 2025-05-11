import matplotlib.pyplot as plt
from collections import deque
import time

MAX_DADES = 100

# ---------- Classe del controlador PID ----------
class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0.0
        self.last_error = 0.0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.last_error = error
        return output

# ---------- Funció principal ----------
def main() -> None:

    # Paràmetres del sistema
    Ca_normal = 9.5
    Ca_inicial = Ca_normal
    Ca_threshold = 8.5
    pas_temps = 1        # 0.1 hores = 6 minuts
    velocitat_baixada = 0.2  # mg/dL per hora
    pth_gain = 0.3         # efecte de la PTH sobre el calci
    absorcio_dietaria = 0.4    # increment de Ca2+ per cada àpat
    interval_apats = 6         # hores entre àpats

    # PID: ajust inicial
    # pid = PIDController(Kp=2.0, Ki=0.5, Kd=0.1)
    pid = PIDController(Kp=2.0, Ki=0.3, Kd=0.2)

    # Variables d’estat
    temps = deque([0.0]*MAX_DADES, maxlen=MAX_DADES)
    nivellsCa = deque([Ca_inicial]*MAX_DADES, maxlen=MAX_DADES)
    nivellsPTH = deque([0.0]*MAX_DADES, maxlen=MAX_DADES)

    Ca_actual = Ca_inicial
    temps_transcorregut = 0.0

    # Inicialització del gràfic
    plt.ion()
    fig, ax = plt.subplots()
    lineCa, = ax.plot(list(temps), list(nivellsCa), label='Ca2+ en sang', color='blue')
    linePTH, = ax.plot(list(temps), list(nivellsPTH), label='PTH en sang', color='magenta')
    ax.axhline(Ca_normal, color='green', linestyle='--', label='Nivell Normal')
    ax.axhline(Ca_threshold, color='red', linestyle='--', label='Llindar Hipocalcèmia')
    ax.set_xlabel('Temps (hores)')
    ax.set_ylabel('Ca2+ (mg/dL)')
    ax.set_title('Control de Ca2+ amb PID')
    #ax.set_ylim(7.5, 10.5)
    ax.legend()
    ax.grid(True)

    while True:
        # Baixada natural de Ca2+
        Ca_actual -= velocitat_baixada * pas_temps

        # Simulació d'una ingesta de calci (cada 6 hores)
        if int((temps_transcorregut - pas_temps) // interval_apats) != int(temps_transcorregut // interval_apats):
            Ca_actual += absorcio_dietaria

        # Error i resposta del PID
        error = Ca_normal - Ca_actual
        PTH_total = pid.update(error, pas_temps)
        PTH_total = max(0.0, PTH_total)  # Evita valors negatius
        nivellsPTH.append(PTH_total)

        # Efecte de la PTH sobre el calci
        Ca_actual += PTH_total * pth_gain * pas_temps

        # Actualització del temps i gràfic
        temps_transcorregut += pas_temps
        temps.append(temps_transcorregut)
        nivellsCa.append(Ca_actual)

        lineCa.set_xdata(temps)
        lineCa.set_ydata(nivellsCa)
        linePTH.set_xdata(temps)
        linePTH.set_ydata(nivellsPTH)
        ax.set_xlim(min(temps), max(temps))

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.01)

if __name__ == "__main__":
    main()
