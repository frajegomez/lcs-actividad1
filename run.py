"""
Punto de arranque único del proyecto.
Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos.

    python run.py            -> pruebas + experimentos completos + tablas + gráficas
    python run.py --rapido   -> lo mismo con menos datos (dura segundos)
    python run.py --tests    -> únicamente las pruebas
    python run.py --ejemplo  -> obtiene la LCS de una pareja de muestra con las 3 versiones
    python run.py --graficas -> vuelve a dibujar tablas y gráficas con los datos ya medidos
"""

import argparse
import sys
import time
import unittest

from lcs import VERSIONES


def ejecutar_tests():
    print("=" * 60)
    print("1) PRUEBAS")
    print("=" * 60)
    suite = unittest.defaultTestLoader.discover("tests")
    resultado = unittest.TextTestRunner(verbosity=1).run(suite)
    return resultado.wasSuccessful()


def ejemplo():
    a = "ATCAGTCATTAAACTATAAACCACTTGAA"
    b = "CCACAACGATGTCGTTTATAGCGCGCGG"
    print(f"a = {a}\nb = {b}\n")
    for nombre, funcion in VERSIONES.items():
        if nombre == "A_recursiva":
            print(f"{nombre:<13}: (se salta, con 29 x 28 símbolos se demoraría en exceso)")
            continue
        lcs = funcion(a, b)
        print(f"{nombre:<13}: {lcs}  (tamaño {len(lcs)})")


def ejecutar_experimentos(modo):
    # Lo importamos aquí para que las pruebas funcionen aunque no esté matplotlib.
    from experimentos.experimentos import (CARPETA_RESULTADOS, ejecutar,
                                           guardar_csv, guardar_tablas_markdown)
    print("=" * 60)
    print(f"2) EXPERIMENTOS (modo {modo})")
    print("=" * 60)
    inicio = time.time()
    filas = ejecutar(modo)
    print(f"\nDatos medidos en: {guardar_csv(filas)}")
    print(f"Tablas en:        {guardar_tablas_markdown(filas)}")

    try:
        from experimentos.graficas import generar_graficas
    except ImportError:
        print("\nATENCIÓN: matplotlib no está instalado, no se crean gráficas.")
        print("          Puedes instalarlo con:  pip install -r requirements.txt")
    else:
        for ruta in generar_graficas(filas, CARPETA_RESULTADOS):
            print(f"Gráfica:          {ruta}")
    print(f"\nDuración total de los experimentos: {time.time() - inicio:.0f} s")


def redibujar():
    """Rehacemos tablas y gráficas desde resultados.csv, sin volver a medir."""
    from experimentos.experimentos import (CARPETA_RESULTADOS, guardar_tablas_markdown,
                                           leer_csv)
    from experimentos.graficas import generar_graficas
    filas = leer_csv()
    if filas is None:
        print("No hay datos medidos todavía: ejecuta primero  python run.py")
        return 1
    print(f"Tablas en:        {guardar_tablas_markdown(filas)}")
    for ruta in generar_graficas(filas, CARPETA_RESULTADOS):
        print(f"Gráfica:          {ruta}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="LCS: versiones A, B y C y sus experimentos")
    parser.add_argument("--rapido", action="store_true", help="experimentos abreviados")
    parser.add_argument("--tests", action="store_true", help="lanzar solo las pruebas")
    parser.add_argument("--ejemplo", action="store_true", help="pareja de cadenas de muestra")
    parser.add_argument("--graficas", action="store_true",
                        help="redibujar tablas y gráficas sin volver a medir")
    args = parser.parse_args()

    if args.ejemplo:
        ejemplo()
        return 0
    if args.graficas:
        return redibujar()

    if not ejecutar_tests():
        print("\nAlgunas pruebas fallan: no se ponen en marcha los experimentos.")
        return 1
    if args.tests:
        return 0

    ejecutar_experimentos("rapida" if args.rapido else "completa")
    return 0


if __name__ == "__main__":  # imprescindible para multiprocessing en Windows y Mac
    sys.exit(main())
