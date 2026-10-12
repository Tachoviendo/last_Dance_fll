from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
reloj = StopWatch()

# ---------- Configuración ----------
motorIzquierda = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motorDerecha = Motor(Port.E, Direction.CLOCKWISE)
sensorIzq = ColorSensor(Port.C)
sensorDer = ColorSensor(Port.D)

skere = DriveBase(motorIzquierda, motorDerecha, 56, 96)
skere.use_gyro(True)

# Velocidades generales (mm/s, mm/s², grados/s, grados/s²).
# Aceleración suave = arranca y frena sin patinar, aunque vaya rápido.
VEL_RECTA = 350
ACEL_RECTA = 600
VEL_GIRO = 250
ACEL_GIRO = 800
skere.settings(VEL_RECTA, ACEL_RECTA, VEL_GIRO, ACEL_GIRO)

# Valores de luz reflejada: medilos con calibrar() del otro archivo.
NEGRO = 10
BLANCO = 90
UMBRAL = (NEGRO + BLANCO) / 2

# Si al seguir la línea el robot gira para el lado contrario, cambiá -1 por 1.
SENTIDO = -1

# ---------- Medidas a ajustar en la mesa (mm y grados) ----------
DISTANCIA_BARRERA_1 = 200  # desde la línea de arranque hasta pasar la barrera 1
DISTANCIA_CURVA = 350      # cuánto seguir la curva: frenar ANTES de la barrera 2
ANGULO_BARRERA_2 = 90      # rumbo para quedar perpendicular a la barrera 2
DISTANCIA_BARRERA_2 = 250  # recto para pasar la barrera 2

# Velocidad al pasar barreras: subila de a 50 mientras no se rompa nada.
VEL_BARRERA = 200


# ---------- 1. Alinear contra la línea de arranque ----------
def alinear_en_linea(velocidad=150):
    """Retrocede un poco y avanza: cada rueda frena cuando SU sensor ve negro."""
    skere.straight(-25)
    izq_listo = False
    der_listo = False
    motorIzquierda.run(velocidad)
    motorDerecha.run(velocidad)
    while not (izq_listo and der_listo):
        if not izq_listo and sensorIzq.reflection() < UMBRAL:
            motorIzquierda.hold()
            izq_listo = True
        if not der_listo and sensorDer.reflection() < UMBRAL:
            motorDerecha.hold()
            der_listo = True
        wait(2)
    skere.reset()  # desde acá: rumbo 0 = recto como quedó alineado


# ---------- Movimientos ----------
def recto(distancia_mm, velocidad=VEL_RECTA, frenar=True):
    """frenar=False encadena con el movimiento siguiente sin detenerse."""
    skere.settings(straight_speed=velocidad)
    skere.straight(distancia_mm, then=Stop.HOLD if frenar else Stop.NONE)
    skere.settings(straight_speed=VEL_RECTA)


def girar_a_rumbo(rumbo):
    """Gira hasta un rumbo ABSOLUTO (medido desde la alineación inicial)."""
    skere.turn(rumbo - skere.angle())


def seguir_linea_dos_sensores(distancia_mm, vel_max=250, vel_min=100,
                              kp=1.5, kd=8):
    """La línea va ENTRE los dos sensores.
    Va rápido cuando está centrado y frena solo en las correcciones."""
    inicio = skere.distance()
    error_anterior = 0
    while abs(skere.distance() - inicio) < distancia_mm:
        error = sensorIzq.reflection() - sensorDer.reflection()
        derivada = error - error_anterior
        giro = (kp * error + kd * derivada) * SENTIDO
        # Cuanto más grande el error, más despacio (curvas cerradas)
        velocidad = max(vel_min, vel_max - abs(error) * 2)
        skere.drive(velocidad, giro)
        error_anterior = error
        wait(2)
    skere.stop()


# ---------- Programa ----------
reloj.reset()

alinear_en_linea()

# Barrera 1: sin frenar al final, sigue directo a la curva
recto(DISTANCIA_BARRERA_1, velocidad=VEL_BARRERA, frenar=False)

# Curva: seguir la línea, pero frenar antes de la barrera 2
seguir_linea_dos_sensores(DISTANCIA_CURVA)

# Barrera 2: ponerse perpendicular y pasarla
girar_a_rumbo(ANGULO_BARRERA_2)
recto(DISTANCIA_BARRERA_2, velocidad=VEL_BARRERA)

print("Rumbo final:", skere.angle())
print("Tiempo total:", reloj.time() / 1000, "s")
