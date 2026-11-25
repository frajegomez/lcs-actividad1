"""
Medición de tiempo de CPU y memoria máxima de una versión de la LCS.
Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos.

Cada medición se hace en un PROCESO HIJO independiente, por tres motivos:
  1) Aislamiento: la memoria de una medición no contamina la siguiente.
  2) Límite de tiempo: si la versión A tarda demasiado (es exponencial),
     el proceso padre lo detiene al superar el límite y lo anota.
  3) Las mediciones de tiempo y de memoria se hacen por separado, porque
     medir memoria con tracemalloc ralentiza el programa y falsearía el
     tiempo.

Qué medimos exactamente
-----------------------
  * Tiempo de CPU: time.process_time(), que cuenta solo el tiempo que la
    CPU dedica a NUESTRO proceso (no le afecta que el ordenador esté
    ocupado con otras cosas, a diferencia del tiempo de reloj). Repetimos
    varias veces y nos quedamos con la mediana, que es robusta frente a
    alguna ejecución anómala. Si el algoritmo es tan rápido que el reloj
    no llega a medirlo, lo ejecutamos varias veces seguidas y dividimos.
  * Memoria máxima: tracemalloc (biblioteca estándar) registra todas las
    reservas de memoria que hace Python y nos da el PICO alcanzado durante
    la ejecución del algoritmo. Mide la memoria que usa el algoritmo, sin
    contar lo que ocupa el propio intérprete de Python.
"""

import multiprocessing
import statistics
import time
import tracemalloc

from lcs import VERSIONES


# Tiempo mínimo que debe durar cada medición. En Windows el reloj de CPU
# solo avanza cada ~15,6 ms, así que una ejecución más corta mediría 0 s.
TIEMPO_MINIMO_S = 0.2


def _cronometrar(funcion, a, b):
    """Devolvemos (segundos por ejecución, resultado).

    Si una sola ejecución es demasiado rápida para el reloj, la repetimos
    1, 2, 4, 8... veces seguidas hasta superar TIEMPO_MINIMO_S, y dividimos
    el tiempo total entre el número de ejecuciones (igual que hace timeit).
    """
    veces = 1
    while True:
        inicio = time.process_time()
        for _ in range(veces):
            resultado = funcion(a, b)
        transcurrido = time.process_time() - inicio
        if transcurrido >= TIEMPO_MINIMO_S:
            return transcurrido / veces, resultado
        veces *= 2


def _medir_tiempo(nombre_version, a, b, repeticiones, cola):
    """(Proceso hijo) Ejecuta la versión varias veces y mide el tiempo de CPU."""
    funcion = VERSIONES[nombre_version]
    tiempos = []
    longitud = None
    for _ in range(repeticiones):
        segundos, resultado = _cronometrar(funcion, a, b)
        tiempos.append(segundos)
        longitud = len(resultado)
    cola.put((statistics.median(tiempos), longitud))


def _medir_memoria(nombre_version, a, b, cola):
    """(Proceso hijo) Ejecuta la versión una vez y mide el pico de memoria."""
    funcion = VERSIONES[nombre_version]
    tracemalloc.start()
    funcion(a, b)
    _, pico_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    cola.put(pico_bytes)


def _ejecutar_con_limite(objetivo, argumentos, limite_segundos):
    """Lanza `objetivo` en un proceso hijo. Devuelve su resultado o None si
    supera el límite de tiempo."""
    contexto = multiprocessing.get_context("spawn")  # funciona igual en Windows, Mac y Linux
    cola = contexto.Queue()
    proceso = contexto.Process(target=objetivo, args=(*argumentos, cola))
    proceso.start()
    proceso.join(limite_segundos)

    if proceso.is_alive():  # se pasó del límite: lo paramos
        proceso.terminate()
        proceso.join()
        return None
    return cola.get()


def medir(nombre_version, a, b, repeticiones=3, limite_segundos=60):
    """Mide una versión con una pareja de cadenas.

    Devuelve un diccionario con:
      tiempo_cpu_s   -> mediana del tiempo de CPU (segundos) o None
      memoria_kib    -> pico de memoria (KiB) o None
      longitud_lcs   -> longitud de la LCS encontrada o None
      estado         -> "ok" o "límite superado"
    """
    resultado_tiempo = _ejecutar_con_limite(
        _medir_tiempo, (nombre_version, a, b, repeticiones), limite_segundos
    )
    if resultado_tiempo is None:
        return {"tiempo_cpu_s": None, "memoria_kib": None,
                "longitud_lcs": None, "estado": "límite superado"}

    tiempo, longitud = resultado_tiempo
    pico_bytes = _ejecutar_con_limite(
        _medir_memoria, (nombre_version, a, b), limite_segundos * 3
    )
    memoria_kib = None if pico_bytes is None else pico_bytes / 1024
    return {"tiempo_cpu_s": tiempo, "memoria_kib": memoria_kib,
            "longitud_lcs": longitud, "estado": "ok"}
