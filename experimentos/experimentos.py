"""
Experimentos: comparación empírica de las versiones A, B y C.
Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos.

Pasos:
  1) Generar parejas de cadenas aleatorias de longitud creciente
     (alfabeto ADN "ACGT", semilla fija -> siempre las mismas cadenas).
  2) Medir tiempo de CPU y memoria máxima de cada versión (ver medir.py).
  3) Guardar los resultados en CSV y en tablas Markdown.
  4) Dibujar las gráficas (ver graficas.py).

Diseño de los experimentos
--------------------------
  * Parejas CORTAS (6..22 símbolos): se ejecutan las TRES versiones. La A
    es exponencial y a partir de ~20 símbolos tarda segundos o minutos,
    así que lleva un límite de tiempo. Si una longitud supera el límite,
    las siguientes (más largas) ya no se intentan para la versión A.
  * Parejas LARGAS (250..4000 símbolos): solo B y C. Ejecutar la A aquí es
    imposible: con 1000 símbolos serían del orden de 2^2000 llamadas.
"""

import csv
import os
import random

from experimentos.medir import medir

ALFABETO = "ACGT"
SEMILLA = 12345

# Configuración normal y configuración rápida (para probar que todo funciona).
CONFIGURACIONES = {
    "completa": {
        "longitudes_cortas": [6, 9, 12, 15, 18, 20, 22],
        "longitudes_largas": [250, 500, 1000, 2000, 4000],
        "repeticiones": 3,
        "limite_segundos": 60,
    },
    "rapida": {
        "longitudes_cortas": [6, 9, 12, 15],
        "longitudes_largas": [250, 500, 1000],
        "repeticiones": 1,
        "limite_segundos": 10,
    },
}

CARPETA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(CARPETA_RAIZ, "datos")
CARPETA_RESULTADOS = os.path.join(CARPETA_RAIZ, "resultados")


def generar_parejas(longitudes):
    """Devuelve una lista de (longitud, cadena_a, cadena_b)."""
    generador = random.Random(SEMILLA)
    parejas = []
    for n in longitudes:
        a = "".join(generador.choice(ALFABETO) for _ in range(n))
        b = "".join(generador.choice(ALFABETO) for _ in range(n))
        parejas.append((n, a, b))
    return parejas


def guardar_parejas(parejas):
    """Guarda las cadenas usadas, para que los experimentos sean verificables."""
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    ruta = os.path.join(CARPETA_DATOS, "parejas.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as fichero:
        escritor = csv.writer(fichero)
        escritor.writerow(["longitud", "cadena_a", "cadena_b"])
        escritor.writerows(parejas)
    return ruta


def ejecutar(modo="completa"):
    """Lanza todos los experimentos y devuelve la lista de filas de resultados."""
    config = CONFIGURACIONES[modo]
    cortas = config["longitudes_cortas"]
    largas = config["longitudes_largas"]
    parejas = generar_parejas(cortas + largas)
    print(f"Parejas guardadas en {guardar_parejas(parejas)}")

    filas = []
    a_supero_limite = False  # cuando la A se pasa del límite, dejamos de probarla

    for n, a, b in parejas:
        for version in ("A_recursiva", "B_hirschberg", "C_dinamica"):
            if version == "A_recursiva" and n not in cortas:
                medida = {"tiempo_cpu_s": None, "memoria_kib": None,
                          "longitud_lcs": None, "estado": "no ejecutada (exponencial)"}
            elif version == "A_recursiva" and a_supero_limite:
                medida = {"tiempo_cpu_s": None, "memoria_kib": None,
                          "longitud_lcs": None, "estado": "omitida (límite ya superado)"}
            else:
                print(f"  n = {n:>5}  versión {version:<13} ...", end=" ", flush=True)
                medida = medir(version, a, b,
                               repeticiones=config["repeticiones"],
                               limite_segundos=config["limite_segundos"])
                if medida["estado"] == "ok":
                    print(f"{medida['tiempo_cpu_s']:.6f} s, "
                          f"{medida['memoria_kib']:.1f} KiB, LCS = {medida['longitud_lcs']}")
                else:
                    print(f"{medida['estado']} ({config['limite_segundos']} s)")
                    if version == "A_recursiva":
                        a_supero_limite = True

            filas.append({"longitud": n, "version": version, **medida})

    comprobar_longitudes(filas)
    return filas


def comprobar_longitudes(filas):
    """Validación extra: todas las versiones deben dar la misma longitud."""
    por_longitud = {}
    for fila in filas:
        if fila["longitud_lcs"] is not None:
            por_longitud.setdefault(fila["longitud"], set()).add(fila["longitud_lcs"])
    for n, valores in por_longitud.items():
        if len(valores) != 1:
            raise AssertionError(f"Las versiones no coinciden para n={n}: {valores}")
    print("Comprobado: todas las versiones dan la misma longitud de LCS.")


# ----------------------------------------------------------------------
# Guardado de resultados
# ----------------------------------------------------------------------

def guardar_csv(filas):
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    ruta = os.path.join(CARPETA_RESULTADOS, "resultados.csv")
    columnas = ["longitud", "version", "tiempo_cpu_s", "memoria_kib", "longitud_lcs", "estado"]
    with open(ruta, "w", newline="", encoding="utf-8") as fichero:
        escritor = csv.DictWriter(fichero, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)
    return ruta


def _formato(valor, decimales):
    return "—" if valor is None else f"{valor:.{decimales}f}"


def guardar_tablas_markdown(filas):
    """Escribe tablas listas para copiar en la memoria."""
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
    ruta = os.path.join(CARPETA_RESULTADOS, "tablas.md")
    longitudes = sorted({f["longitud"] for f in filas})
    dato = {(f["longitud"], f["version"]): f for f in filas}

    lineas = ["# Resultados de los experimentos", ""]

    # Tabla 1: tiempo de CPU
    lineas += ["## Tiempo de CPU (segundos, mediana)", "",
               "| n | A recursiva | B Hirschberg | C dinámica | B / C |",
               "|---:|---:|---:|---:|---:|"]
    for n in longitudes:
        ta = dato[(n, "A_recursiva")]["tiempo_cpu_s"]
        tb = dato[(n, "B_hirschberg")]["tiempo_cpu_s"]
        tc = dato[(n, "C_dinamica")]["tiempo_cpu_s"]
        texto_a = _formato(ta, 6) if ta is not None else dato[(n, "A_recursiva")]["estado"]
        cociente = _formato(tb / tc, 2) if tb and tc else "—"
        lineas.append(f"| {n} | {texto_a} | {_formato(tb, 6)} | {_formato(tc, 6)} | {cociente} |")

    # Tabla 2: memoria máxima
    lineas += ["", "## Memoria máxima (KiB, medida con tracemalloc)", "",
               "| n | A recursiva | B Hirschberg | C dinámica | C / B |",
               "|---:|---:|---:|---:|---:|"]
    for n in longitudes:
        ma = dato[(n, "A_recursiva")]["memoria_kib"]
        mb = dato[(n, "B_hirschberg")]["memoria_kib"]
        mc = dato[(n, "C_dinamica")]["memoria_kib"]
        cociente = _formato(mc / mb, 1) if mb and mc else "—"
        lineas.append(f"| {n} | {_formato(ma, 1)} | {_formato(mb, 1)} | {_formato(mc, 1)} | {cociente} |")

    # Tabla 3: comprobación de O(n^2). Si el tiempo es c·n^2, entonces
    # tiempo / n^2 debe mantenerse aproximadamente constante.
    lineas += ["", "## Comprobación de la complejidad cuadrática (B y C)", "",
               "Si el tiempo crece como n², el cociente tiempo / n² se mantiene casi constante.", "",
               "| n | B: tiempo/n² (µs) | C: tiempo/n² (µs) | C: memoria/n² (bytes) |",
               "|---:|---:|---:|---:|"]
    for n in longitudes:
        if n < 100:
            continue  # con cadenas tan cortas dominan los costes fijos
        tb = dato[(n, "B_hirschberg")]["tiempo_cpu_s"]
        tc = dato[(n, "C_dinamica")]["tiempo_cpu_s"]
        mc = dato[(n, "C_dinamica")]["memoria_kib"]
        lineas.append(
            f"| {n} | {_formato(tb and tb / n**2 * 1e6, 3)} | "
            f"{_formato(tc and tc / n**2 * 1e6, 3)} | {_formato(mc and mc * 1024 / n**2, 2)} |")

    with open(ruta, "w", encoding="utf-8") as fichero:
        fichero.write("\n".join(lineas) + "\n")
    return ruta


def leer_csv():
    """Leemos resultados/resultados.csv de una ejecución anterior.

    Sirve para volver a dibujar las gráficas o las tablas sin repetir las
    mediciones. Devuelve None si todavía no existe el fichero.
    """
    ruta = os.path.join(CARPETA_RESULTADOS, "resultados.csv")
    if not os.path.exists(ruta):
        return None
    filas = []
    with open(ruta, newline="", encoding="utf-8") as fichero:
        for fila in csv.DictReader(fichero):
            fila["longitud"] = int(fila["longitud"])
            for campo in ("tiempo_cpu_s", "memoria_kib"):
                fila[campo] = float(fila[campo]) if fila[campo] else None
            fila["longitud_lcs"] = int(fila["longitud_lcs"]) if fila["longitud_lcs"] else None
            filas.append(fila)
    return filas
