# Simulacions de sistemes de control per a la regulació del calci

Aquest repositori conté dues simulacions senzilles implementades en Python com a part d'un projecte de l'assignatura _Modelització i Control de Sistemes Biomèdics_.

L'objectiu és explorar com es podria controlar artificialment la concentració de calci en sang en un pacient amb hipocalcèmia secundària a hipoparatiroïdisme, mitjançant l'administració simulada de PTH.

**Aquestes simulacions no tenen valor clínic ni científic real.** El model és conceptual i s'ha creat amb propòsits educatius.

## Models implementats

- **Control en llaç obert** (`controladorObert.py`):  
  Simulació bàsica on el sistema injecta una dosi fixa de PTH (bolus) cada cop que el nivell de calci baixa per sota d'un llindar.

- **Control en llaç tancat amb PID** (`controladorPID.py`):  
  S'implementa un controlador PID per regular de manera contínua la quantitat de PTH administrada, segons l'error entre el nivell de calci actual i el desitjat. Els paràmetres `Kp`, `Ki` i `Kd` s'han ajustat manualment.

## Requisits

- Python 3.8+
- Matplotlib
