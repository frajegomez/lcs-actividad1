"""
Versión C: LCS con programación dinámica tabular (de abajo a arriba).
Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos.

Idea
----
Es la misma recurrencia que la versión A, pero cada subproblema se
resuelve UNA sola vez y se guarda en una tabla L de (m+1) x (n+1):

    L[i][j] = longitud de la LCS de a[:i] y b[:j]   (prefijos)

    L[i][j] = 0                              si i == 0 o j == 0
    L[i][j] = L[i-1][j-1] + 1                si a[i-1] == b[j-1]
    L[i][j] = max(L[i-1][j], L[i][j-1])      en otro caso

La tabla se rellena de arriba a abajo y de izquierda a derecha, de modo
que cuando calculamos una celda, las tres que necesita ya están hechas.
La celda L[m][n] contiene la longitud de la LCS.

Para obtener la propia subsecuencia (no solo su longitud) recorremos la
tabla hacia atrás desde L[m][n] ("reconstrucción" o backtracking).

Complejidad
-----------
  * Tiempo:  O(m · n)  -> una operación constante por celda.
  * Memoria: O(m · n)  -> guardamos la tabla completa, que hace falta
                          para reconstruir la subsecuencia.

Esta memoria cuadrática es justo lo que mejora Hirschberg (versión B).
"""


def construir_tabla(a: str, b: str) -> list[list[int]]:
    """Construimos la tabla L de longitudes descrita arriba."""
    m, n = len(a), len(b)

    # Fila 0 y columna 0 a cero, LCS con cadena vacía.
    L = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                # Coinciden, alargamos la LCS anterior.
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                # No coinciden, lo mejor de descartar uno u otro.
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L


def lcs_dinamica(a: str, b: str) -> str:
    """Devolvemos la subsecuencia más larga común de a y b (Versión C)."""
    L = construir_tabla(a, b)

    # Reconstrucción desde la esquina L[m][n] hacia atrás.
    i, j = len(a), len(b)
    caracteres_al_reves = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            # Carácter de la LCS, vamos en diagonal.
            caracteres_al_reves.append(a[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            # Viene de arriba, descartamos a[i-1].
            i -= 1
        else:
            # Viene de la izquierda, descartamos b[j-1].
            j -= 1

    # Recogidos del final al principio, damos la vuelta.
    return "".join(reversed(caracteres_al_reves))
