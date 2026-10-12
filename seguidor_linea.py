from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

# ---------- Configuración (cambiá los puertos si hace falta) ----------
motorIzquierda = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motorDerecha = Motor(Port.E, Direction.CLOCKWISE)
sensorIzq = ColorSensor(Port.C)
sensorDer = ColorSensor(Port.D)

skere = DriveBase(motorIzquierda, motorDerecha, 56, 96)
skere.use_gyro(True)

# Valores de luz reflejada (0-100). Medilos con calibrar() y cambialos.
NEGRO = 10
BLANCO = 90
OBJETIVO = (NEGRO + BLANCO) / 2  # el borde entre negro y blanco


# ---------- Calibración ----------
def calibrar(segundos=10):
    """Muestra la luz de los dos sensores. Pasalos por negro y por blanco
    y anotá los valores para NEGRO y BLANCO."""
    for _ in range(segundos * 4):
        print("Izq:", sensorIzq.reflection(), " Der:", sensorDer.reflection())
        wait(250)


# ---------- Seguidor de línea PD (un sensor, sigue el borde) ----------
def seguir_linea(sensor, distancia_mm, velocidad=150, kp=2.0, kd=10, lado=1):
    """Sigue el borde de la línea durante distancia_mm.
    lado = 1 o -1: cambialo si el robot se va de la línea en vez de seguirla
    (depende de qué borde de la línea sigas)."""
    skere.reset()
    error_anterior = 0
    while abs(skere.distance()) < distancia_mm:
        error = sensor.reflection() - OBJETIVO
        derivada = error - error_anterior
        giro = (kp * error + kd * derivada) * lado
        skere.drive(velocidad, giro)
        error_anterior = error
        wait(5)
    skere.stop()


# ---------- Seguir hasta un cruce (usa el otro sensor para frenar) ----------
def seguir_hasta_cruce(sensor, sensor_cruce, velocidad=150, kp=2.0, kd=10,
                       lado=1, maximo_mm=2000):
    """Sigue la línea con 'sensor' y frena cuando 'sensor_cruce' ve negro."""
    skere.reset()
    error_anterior = 0
    while sensor_cruce.reflection() > NEGRO + 10:
        if abs(skere.distance()) > maximo_mm:  # seguro por si no encuentra el cruce
            break
        error = sensor.reflection() - OBJETIVO
        derivada = error - error_anterior
        giro = (kp * error + kd * derivada) * lado
        skere.drive(velocidad, giro)
        error_anterior = error
        wait(5)
    skere.stop()


# ---------- Programa ----------
# Paso 1: descomentá esta línea, corré, y anotá NEGRO y BLANCO.
# calibrar()

# Paso 2: seguir la línea 500 mm con el sensor izquierdo.
seguir_linea(sensorIzq, 500)

# Ejemplo: seguir con el izquierdo hasta que el derecho vea una línea cruzada.
# seguir_hasta_cruce(sensorIzq, sensorDer)
