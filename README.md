# Actividad 1 · Subsecuencia común más larga (LCS)

_Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos._

Tres algoritmos para calcular la LCS de dos cadenas, y experimentos que
comparan su tiempo de CPU y su memoria máxima.

| Versión | Técnica | Tiempo | Memoria | Fichero |
|---|---|---|---|---|
| A | Recursiva directa, sin memorización | O(2^(m+n)) | O(m+n) (pila) | `lcs/version_a_recursiva.py` |
| B | Divide y conquista de Hirschberg | O(m·n) | O(m+n) | `lcs/version_b_hirschberg.py` |
| C | Programación dinámica tabular | O(m·n) | O(m·n) | `lcs/version_c_dinamica.py` |

Lenguaje: Python 3.10 o superior. Los algoritmos y los tests solo usan la
biblioteca estándar; **no se usa ninguna librería de LCS**. `matplotlib`
solo hace falta para dibujar las gráficas.

## Cómo ejecutarlo (un único comando)

```bash
pip install -r requirements.txt     # una sola vez: instala matplotlib
python run.py                       # tests + experimentos + tablas + gráficas
```

En Linux o Mac también vale `make`, que hace las dos cosas de una vez.
En algunos sistemas el comando es `python3` en lugar de `python`.

Otras opciones:

| Comando | Qué hace |
|---|---|
| `python run.py --rapido` | Experimentos reducidos (unos 10 s), para comprobar que todo funciona |
| `python run.py --tests` | Solo los tests |
| `python run.py --graficas` | Vuelve a dibujar tablas y gráficas con los datos ya medidos, sin repetir los experimentos |
| `python run.py --ejemplo` | LCS de una pareja de cadenas de muestra (29 y 28 símbolos) |
| `python -m unittest discover -s tests -v` | Tests con detalle |

La ejecución completa tarda unos minutos, sobre todo por la versión A con
cadenas de 20 símbolos o más y por las cadenas de 4 000 símbolos.

## Estructura

```
lcs/                        Las tres versiones del algoritmo
  version_a_recursiva.py
  version_b_hirschberg.py
  version_c_dinamica.py
  __init__.py               es_subsecuencia() y el diccionario VERSIONES
tests/test_lcs.py           Juego de tests (unittest)
experimentos/
  medir.py                  Mide tiempo de CPU y memoria en un proceso aparte
  experimentos.py           Genera las cadenas, lanza las mediciones, guarda CSV y tablas
  graficas.py               Dibuja las gráficas
run.py                      Punto de entrada único
datos/parejas.csv           (generado) cadenas usadas en los experimentos
resultados/                 (generado) resultados.csv, tablas.md y gráficas PNG
```

## Tests

Como puede haber varias LCS distintas igual de largas, los tests no comparan
cadenas, sino que comprueban que el resultado **es subsecuencia común** de
ambas entradas y que su **longitud** es la correcta:

* Casos conocidos (cadenas vacías, iguales, sin nada en común, ejemplos
  clásicos y el ejemplo del Tema 3, cuya LCS mide 20).
* Validación cruzada de A, B y C con 200 parejas aleatorias cortas.
* Validación cruzada de B y C con cadenas largas (hasta 1 000 símbolos) y
  con alfabetos binario y de 26 letras.

Además, los experimentos comprueban de nuevo que todas las versiones dan la
misma longitud en cada pareja medida.

## Metodología de los experimentos

* **Cadenas:** aleatorias sobre el alfabeto ADN `ACGT`, con semilla fija
  (12345), así que cada ejecución usa exactamente las mismas cadenas.
  Se guardan en `datos/parejas.csv`.
* **Longitudes:**
  * Cortas, 6, 9, 12, 15, 18, 20 y 22: se miden A, B y C.
  * Largas, 250, 500, 1 000, 2 000 y 4 000: solo B y C.
* **Versión A:** tiene un límite de 60 s por medición. Si una longitud lo
  supera, las más largas ya no se intentan y la tabla lo indica. No se
  ejecuta con cadenas largas porque es exponencial: con n = 1 000 haría del
  orden de 2^2000 llamadas.
* **Tiempo de CPU:** `time.process_time()`, mediana de 3 repeticiones.
  Si una ejecución dura menos de 0,2 s, se repite 1, 2, 4, 8... veces
  seguidas hasta superar 0,2 s y se divide el total entre el número de
  ejecuciones. Así se pueden medir también los casos muy rápidos, aunque
  el reloj de Windows solo avance cada ~15,6 ms.
* **Memoria máxima:** pico de `tracemalloc` durante una ejecución aparte
  (medir memoria ralentiza, así que no se mezcla con la medida de tiempo).
  Mide la memoria que reserva el algoritmo, sin contar el intérprete.
* **Aislamiento:** cada medición corre en un proceso hijo nuevo, para que
  unas no influyan en otras y para poder cortar la versión A por tiempo.

### Nota para interpretar la memoria

En Python cada número entero es un objeto. Los enteros de −5 a 256 están
precreados y se comparten, pero los mayores ocupan 28 bytes cada uno. Por eso,
cuando la LCS supera 256 caracteres, la memoria por celda sube un poco. La
tendencia (lineal en B, cuadrática en C) no cambia.

## Resultados

Tras `python run.py`:

* `resultados/tablas.md`: tablas de tiempo, memoria y cociente tiempo/n².
* `resultados/resultados.csv`: datos en bruto.
* `resultados/tiempo_cpu.png`, `resultados/memoria.png`,
  `resultados/version_a_exponencial.png`: gráficas.

Los tiempos absolutos dependen del ordenador. Lo que debe mantenerse es la
forma de las curvas y los cocientes entre versiones.
