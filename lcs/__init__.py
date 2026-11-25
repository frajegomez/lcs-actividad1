"""Paquete con las tres versiones del cálculo de la LCS.
Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos.

    A -> lcs_recursiva   (recursiva directa, sin memorización)
    B -> lcs_hirschberg  (divide y conquista de Hirschberg)
    C -> lcs_dinamica    (programación dinámica tabular)

Todas reciben dos cadenas y devuelven UNA subsecuencia común más larga.
Puede haber varias LCS distintas de la misma longitud, así que dos
versiones pueden devolver cadenas diferentes pero igual de largas.
"""

from .version_a_recursiva import lcs_recursiva
from .version_b_hirschberg import lcs_hirschberg
from .version_c_dinamica import lcs_dinamica


def es_subsecuencia(sub: str, cadena: str) -> bool:
    """True si `sub` se obtiene de `cadena` borrando algunos caracteres."""
    posicion = 0
    for caracter in cadena:
        if posicion < len(sub) and sub[posicion] == caracter:
            posicion += 1
    return posicion == len(sub)


# Nombre legible de cada versión -> función. Lo usan los tests y los experimentos.
VERSIONES = {
    "A_recursiva": lcs_recursiva,
    "B_hirschberg": lcs_hirschberg,
    "C_dinamica": lcs_dinamica,
}
