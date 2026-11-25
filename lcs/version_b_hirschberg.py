"""
Versión B: LCS con divide y conquista (algoritmo de Hirschberg, 1975).
Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos.

Problema que resuelve
---------------------
La versión C necesita la tabla completa (memoria O(m·n)) para poder
reconstruir la subsecuencia. Con m = n = 10 000 serían 100 millones de
celdas. Hirschberg obtiene la MISMA respuesta usando solo memoria lineal
O(m + n), manteniendo el tiempo en O(m · n).

Dos ingredientes
----------------
1) Calcular solo la ÚLTIMA FILA de la tabla de programación dinámica.
   Para rellenar una fila solo hace falta la anterior, así que basta con
   dos filas: memoria O(n). Con eso sabemos la LONGITUD de la LCS de
   a con cada prefijo de b, pero no la subsecuencia.

2) Divide y conquista. Partimos a por la mitad: a = a_izq + a_der.
   La LCS de (a, b) se puede partir también en dos trozos, uno que viene
   de (a_izq, b[:k]) y otro de (a_der, b[k:]) para algún punto de corte k.
   Para encontrar el mejor k:
     * izq[j] = LCS(a_izq, b[:j])         -> última fila hacia delante
     * der[j] = LCS(a_der, b[j:])         -> última fila hacia atrás
     * k = el j que maximiza izq[j] + der[j]
   Después resolvemos recursivamente las dos mitades y concatenamos.

     DIVIDIR:    partir a por la mitad y hallar el corte k en b.
     CONQUISTAR: resolver (a_izq, b[:k]) y (a_der, b[k:]) por separado.
     COMBINAR:   concatenar las dos subsecuencias.

Complejidad
-----------
  * Tiempo: el primer nivel recorre m·n celdas, el segundo m·n/2, el
    tercero m·n/4... La suma es  m·n · (1 + 1/2 + 1/4 + ...) = 2·m·n,
    es decir O(m · n). Hace ~el doble de trabajo que la versión C.
  * Memoria: O(m + n). Solo guardamos dos filas a la vez y la pila de
    recursión tiene profundidad O(log m).

Implementación: trabajamos con índices (rangos [i_ini, i_fin) de a y
[j_ini, j_fin) de b) en vez de recortar cadenas, para no crear copias y
mantener de verdad la memoria lineal.
"""


def ultima_fila_hacia_delante(a, i_ini, i_fin, b, j_ini, j_fin):
    """Devolvemos fila[k] = longitud LCS(a[i_ini:i_fin], b[j_ini:j_ini+k]).

    Calculamos la última fila de la tabla de la versión C guardando
    solo dos filas (anterior y actual). Longitud: (j_fin-j_ini) + 1.
    """
    n = j_fin - j_ini
    anterior = [0] * (n + 1)
    for i in range(i_ini, i_fin):
        actual = [0] * (n + 1)
        for k in range(1, n + 1):
            if a[i] == b[j_ini + k - 1]:
                actual[k] = anterior[k - 1] + 1
            else:
                actual[k] = max(anterior[k], actual[k - 1])
        anterior = actual
    return anterior


def ultima_fila_hacia_atras(a, i_ini, i_fin, b, j_ini, j_fin):
    """Devolvemos fila[k] = longitud LCS(a[i_ini:i_fin], b[j_ini+k:j_fin]).

    Igual que la anterior, pero recorremos ambas cadenas desde el
    final (equivale a calcular la LCS de las cadenas invertidas). Así
    fila[k] mide la LCS con el SUFIJO de b que empieza en j_ini + k.
    """
    n = j_fin - j_ini
    anterior = [0] * (n + 1)
    for i in range(i_fin - 1, i_ini - 1, -1):
        actual = [0] * (n + 1)
        for k in range(n - 1, -1, -1):
            if a[i] == b[j_ini + k]:
                actual[k] = anterior[k + 1] + 1
            else:
                actual[k] = max(anterior[k], actual[k + 1])
        anterior = actual
    return anterior


def lcs_hirschberg(a: str, b: str) -> str:
    """Devolvemos la subsecuencia más larga común de a y b (Versión B)."""
    resultado = []  # vamos añadiendo los caracteres de la LCS en orden
    _hirschberg(a, 0, len(a), b, 0, len(b), resultado)
    return "".join(resultado)


def _hirschberg(a, i_ini, i_fin, b, j_ini, j_fin, resultado):
    """Añadimos a `resultado` la LCS de a[i_ini:i_fin] y b[j_ini:j_fin]."""
    m = i_fin - i_ini
    n = j_fin - j_ini

    # --- Casos base ---------------------------------------------------
    # Alguna parte vacía, nada en común.
    if m == 0 or n == 0:
        return
    # a con un único carácter, está en la LCS si aparece en el trozo de b.
    if m == 1:
        if a[i_ini] in b[j_ini:j_fin]:
            resultado.append(a[i_ini])
        return

    # --- Dividir ------------------------------------------------------
    i_mitad = i_ini + m // 2
    izq = ultima_fila_hacia_delante(a, i_ini, i_mitad, b, j_ini, j_fin)
    der = ultima_fila_hacia_atras(a, i_mitad, i_fin, b, j_ini, j_fin)

    # Buscamos el corte k de b que maximiza LCS(izq) + LCS(der).
    mejor_k = 0
    mejor_valor = -1
    for k in range(n + 1):
        valor = izq[k] + der[k]
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_k = k
    j_corte = j_ini + mejor_k

    # Liberamos las filas antes de bajar en la recursión,
    # así la memoria sigue siendo lineal.
    del izq, der

    # --- Conquistar y combinar ---------------------------------------
    # Primero la mitad izquierda y luego la derecha, así los caracteres
    # quedan en orden (combinar = concatenar).
    _hirschberg(a, i_ini, i_mitad, b, j_ini, j_corte, resultado)
    _hirschberg(a, i_mitad, i_fin, b, j_corte, j_fin, resultado)
