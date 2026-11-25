"""
Versión A: LCS recursiva directa, SIN memorización.
Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos.

Idea (definición recursiva del problema)
----------------------------------------
Sean a y b dos cadenas. Miramos sus primeros caracteres a[i] y b[j]:

  * Si alguna cadena se ha acabado, la LCS es la cadena vacía.
  * Si a[i] == b[j], ese carácter forma parte de una LCS, así que lo
    tomamos y seguimos con el resto de ambas cadenas (i+1, j+1).
  * Si son distintos, al menos uno de los dos sobra. Probamos las dos
    opciones (quitar a[i] o quitar b[j]) y nos quedamos con la mejor.

Complejidad
-----------
En el peor caso (caracteres distintos) cada llamada genera DOS llamadas
nuevas y el problema solo se reduce en 1:

    T(m, n) = T(m-1, n) + T(m, n-1) + O(1)   =>   O(2^(m+n))

El problema es que los MISMOS subproblemas (i, j) se recalculan una y otra
vez, porque no guardamos nada. Precisamente eso es lo que arreglan la
programación dinámica (versión C) y Hirschberg (versión B).

Memoria: la profundidad máxima de la recursión es m + n, así que la pila
ocupa O(m + n). Además cada nivel construye cadenas parciales.

Por su coste exponencial, esta versión solo se usa con cadenas cortas
(unas 20 letras) y con un límite de tiempo en los experimentos.
"""

import sys


def lcs_recursiva(a: str, b: str) -> str:
    """Devolvemos la subsecuencia más larga común de a y b (Versión A)."""
    # Recursión hasta profundidad len(a) + len(b).
    # Nos aseguramos de que Python no corte antes de tiempo.
    profundidad_necesitamos = len(a) + len(b) + 100
    if sys.getrecursionlimit() < profundidad_necesitamos:
        sys.setrecursionlimit(profundidad_necesitamos)

    return _lcs_desde(a, b, 0, 0)


def _lcs_desde(a: str, b: str, i: int, j: int) -> str:
    """LCS de los sufijos a[i:] y b[j:].

    Usamos índices en lugar de recortar las cadenas (a[1:]) para no crear
    copias en cada llamada; así el código mide el coste del algoritmo y no
    el de copiar cadenas.
    """
    # Caso base: una de las dos cadenas ya no tiene caracteres.
    if i == len(a) or j == len(b):
        return ""

    # Caso 1: caracteres coinciden, forman parte de la LCS.
    if a[i] == b[j]:
        return a[i] + _lcs_desde(a, b, i + 1, j + 1)

    # Caso 2: no coinciden, descartamos uno u otro.
    sin_caracter_de_a = _lcs_desde(a, b, i + 1, j)
    sin_caracter_de_b = _lcs_desde(a, b, i, j + 1)

    # Nos quedamos con la más larga (si hay empate, la primera).
    if len(sin_caracter_de_a) >= len(sin_caracter_de_b):
        return sin_caracter_de_a
    return sin_caracter_de_b
