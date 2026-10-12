# Robot FLL — temporada BIOGLOW 2026-27

Contexto del proyecto para quien trabaje en este repo (personas o Claude Code).

## Equipo y competencia
- FIRST LEGO League Challenge, temporada **BIOGLOW** (2026-27), Founders Edition con **LEGO SPIKE Prime**.
- Programamos en **Pybricks** (MicroPython), no con el firmware oficial de LEGO.
- Notas de diseño del robot: documento "Robot FLL BIOGLOW — notas de diseño" (Claude Docs).

## Robot
- Box robot con hub SPIKE Prime, ruedas de **56 mm**, ball caster.
- Distancia entre ruedas (axle track): **96 mm** (12 espacios LEGO, centro a centro). Pendiente: calibrar con 10 vueltas.
- Puertos:
  - Motor izquierdo: **A** (`Direction.COUNTERCLOCKWISE`)
  - Motor derecho: **E** (`Direction.CLOCKWISE`)
  - Sensor de color izquierdo: **C**
  - Sensor de color derecho: **D**
  - Motores de accesorios: por definir.
- `DriveBase` se llama `skere`. Usa `use_gyro(True)`.
- Valores de luz: `NEGRO = 10`, `BLANCO = 90` (pendiente: calibrar en la mesa real).
- Seguimiento con dos sensores: `SENTIDO = -1` (con 1 giraba para el lado contrario).

## Lo que ya funciona
- `barrera_y_curva.py`: alinear en la línea de arranque → pasar barrera 1 recto → seguir la curva con dos sensores (la línea va entre los sensores) → girar a rumbo absoluto → pasar barrera 2 perpendicular.
  - Medidas actuales: barrera 1 = 200 mm, curva = 350 mm, rumbo barrera 2 = 90°, barrera 2 = 250 mm.
  - Importante: la línea llega en diagonal a la barrera 2. No hay que seguirla hasta el final, sino frenar antes, girar a rumbo absoluto y pasar recto, o se rompe la misión.
- `seguidor_linea.py`: seguidor PD de borde con un sensor + `calibrar()` + `seguir_hasta_cruce()`.

## Próximo paso: framework propio sobre Pybricks
Estructura acordada (Pybricks Code y pybricksdev empaquetan los imports solos):

```
robot.py       → configuración: puertos, DriveBase, NEGRO/BLANCO, velocidades, voltaje mínimo
movimientos.py → recto, girar_a_rumbo, alinear_en_linea, alinear_en_pared,
                 seguir_linea (1 y 2 sensores), seguir_hasta_cruce, accesorios
salidaN.py     → una salida por archivo, solo usa movimientos.py
main.py        → menú en el hub (elegir salida con botones, pasa sola a la siguiente),
                 chequeo de batería, cronómetro
```

Requisitos del framework:
1. Velocidad y aceleración centralizadas, con rampas suaves; velocidades rápidas para trasladarse y lentas para misiones delicadas. Pybricks por defecto limita a ~40% del máximo y acelera brusco.
2. Giros y rectas con giroscopio usando **rumbos absolutos** (desde la alineación inicial).
3. Alineación contra líneas y paredes para resetear el error acumulado.
4. Encadenar movimientos sin frenar (`then=Stop.NONE`) cuando no hace falta precisión.
5. Accesorios: mover a posiciones exactas, resetear posición al inicio de cada salida.
6. Batería: no pedir velocidades cerca del máximo del motor (dejar ~20-30% de margen); calibrar con la batería a nivel intermedio, no recién cargada; definir `VOLTAJE_MINIMO` según datos de pruebas; `main.py` muestra el voltaje y avisa con un beep si está bajo.
7. Cronometrar cada salida (el partido dura 2:30).

## Convenciones
- Comentarios y nombres en español.
- Nombres de archivo simples, sin espacios ni tildes.
- Toda medida que se ajusta en la mesa va como constante en MAYÚSCULAS al principio del archivo.

## Referencias
- OFDL Robotics Lab (Taiwán): https://github.com/ofdl-robotics-tw — seguidor PD, utilidades de Pybricks.
- MonongahelaCryptidCooperative/FLL: framework propio (`MCCDriveBase`) sobre Pybricks.
- GO-Robot-FLL/Pybricks-for-spike-prime: VS Code + pybricksdev.
- Pybricks: menú en el hub (pybricks/support#1064).
