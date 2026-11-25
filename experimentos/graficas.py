"""
Gráficas de los resultados (necesita matplotlib: pip install matplotlib).
Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos.

Se generan tres imágenes PNG en la carpeta resultados/:
  1) tiempo_cpu.png              -> tiempo de las tres versiones (escala log-log)
  2) memoria.png                 -> memoria de las tres versiones (escala log-log)
  3) version_a_exponencial.png   -> tiempo de la A con ejes normales (lineales)

¿Por qué escalas logarítmicas?
  * En log-log, una curva c·n^k aparece como una RECTA de pendiente k.
    Así se ve a simple vista que B y C son cuadráticas (pendiente ~2 en
    tiempo) y que la memoria de B es lineal (pendiente ~1) frente a la
    cuadrática de C (pendiente ~2).
  * La gráfica de la versión A, en cambio, usa ejes normales: así se ve
    directamente la "explosión" exponencial (la curva casi plana que de
    repente se dispara hacia arriba).
"""

import os

import matplotlib

matplotlib.use("Agg")  # dibuja en fichero, sin abrir ventanas
import matplotlib.pyplot as plt

ESTILO = {
    "A_recursiva": {"etiqueta": "A: recursiva directa", "color": "#d62728", "marcador": "o"},
    "B_hirschberg": {"etiqueta": "B: Hirschberg (DyC)", "color": "#1f77b4", "marcador": "s"},
    "C_dinamica": {"etiqueta": "C: programación dinámica", "color": "#2ca02c", "marcador": "^"},
}


def _serie(filas, version, campo):
    """Puntos (n, valor) de una versión, ignorando los que no se midieron.

    También se ignoran los valores 0: en Windows el reloj de CPU solo avanza
    cada ~15,6 ms, así que las ejecuciones más rápidas miden 0 s, y el
    logaritmo de 0 no existe (la escala log no puede dibujarlos)."""
    puntos = [(f["longitud"], f[campo]) for f in filas
              if f["version"] == version and f[campo] is not None and f[campo] > 0]
    return [p[0] for p in puntos], [p[1] for p in puntos]


def _grafica_comparativa(filas, campo, titulo, etiqueta_y, ruta):
    figura, eje = plt.subplots(figsize=(7, 4.5))
    for version, estilo in ESTILO.items():
        x, y = _serie(filas, version, campo)
        if x:
            eje.plot(x, y, marker=estilo["marcador"], color=estilo["color"], label=estilo["etiqueta"])
    eje.set_xscale("log")
    eje.set_yscale("log")
    eje.set_xlabel("Longitud de cada cadena, n (escala log)")
    eje.set_ylabel(etiqueta_y)
    eje.set_title(titulo)
    eje.grid(True, which="both", alpha=0.3)
    eje.legend()
    figura.tight_layout()
    figura.savefig(ruta, dpi=150)
    plt.close(figura)


def _grafica_version_a(filas, ruta):
    x, y = _serie(filas, "A_recursiva", "tiempo_cpu_s")
    if not x:
        return
    figura, eje = plt.subplots(figsize=(7, 4.5))
    estilo = ESTILO["A_recursiva"]
    eje.plot(x, y, marker=estilo["marcador"], color=estilo["color"], label=estilo["etiqueta"])
    # Añadimos B y C en las mismas longitudes cortas para comparar.
    for version in ("B_hirschberg", "C_dinamica"):
        xs, ys = _serie(filas, version, "tiempo_cpu_s")
        pares = [(n, t) for n, t in zip(xs, ys) if n <= max(x)]
        if pares:
            eje.plot(*zip(*pares), marker=ESTILO[version]["marcador"],
                     color=ESTILO[version]["color"], label=ESTILO[version]["etiqueta"])
    # Ejes lineales a propósito: B y C quedan pegadas a cero y la A se dispara.
    eje.set_ylim(bottom=0)
    eje.set_xlabel("Longitud de cada cadena, n")
    eje.set_ylabel("Tiempo de procesador (s)")
    eje.set_title("Cadenas cortas: el tiempo de la versión A se dispara (exponencial)")
    eje.grid(True, which="both", alpha=0.3)
    eje.legend()
    figura.tight_layout()
    figura.savefig(ruta, dpi=150)
    plt.close(figura)


def generar_graficas(filas, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    rutas = [
        os.path.join(carpeta, "tiempo_cpu.png"),
        os.path.join(carpeta, "memoria.png"),
        os.path.join(carpeta, "version_a_exponencial.png"),
    ]
    _grafica_comparativa(filas, "tiempo_cpu_s", "Tiempo de procesador según la longitud de la cadena",
                         "Tiempo de CPU (s, escala log)", rutas[0])
    _grafica_comparativa(filas, "memoria_kib", "Consumo máximo de memoria según la longitud de la cadena",
                         "Memoria máxima (KiB, escala log)", rutas[1])
    _grafica_version_a(filas, rutas[2])
    return rutas
