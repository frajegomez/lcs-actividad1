# Resultados de los experimentos

## Tiempo de CPU (segundos, mediana)

| n | A recursiva | B Hirschberg | C dinámica | B / C |
|---:|---:|---:|---:|---:|
| 6 | 0.000011 | 0.000013 | 0.000007 | 1.87 |
| 9 | 0.000198 | 0.000029 | 0.000014 | 2.00 |
| 12 | 0.002808 | 0.000046 | 0.000024 | 1.92 |
| 15 | 0.140625 | 0.000065 | 0.000034 | 1.89 |
| 18 | 1.203125 | 0.000092 | 0.000050 | 1.85 |
| 20 | 16.500000 | 0.000107 | 0.000057 | 1.87 |
| 22 | límite superado | 0.000122 | 0.000072 | 1.68 |
| 250 | no ejecutada (exponencial) | 0.012695 | 0.007812 | 1.62 |
| 500 | no ejecutada (exponencial) | 0.050781 | 0.035156 | 1.44 |
| 1000 | no ejecutada (exponencial) | 0.203125 | 0.148438 | 1.37 |
| 2000 | no ejecutada (exponencial) | 0.843750 | 0.609375 | 1.38 |
| 4000 | no ejecutada (exponencial) | 3.453125 | 2.500000 | 1.38 |

## Memoria máxima (KiB, medida con tracemalloc)

| n | A recursiva | B Hirschberg | C dinámica | C / B |
|---:|---:|---:|---:|---:|
| 6 | 0.1 | 0.2 | 0.6 | 3.0 |
| 9 | 0.3 | 0.3 | 1.1 | 4.2 |
| 12 | 0.4 | 0.3 | 1.8 | 5.2 |
| 15 | 0.6 | 0.4 | 2.5 | 5.9 |
| 18 | 0.8 | 0.5 | 3.3 | 6.9 |
| 20 | 0.9 | 0.5 | 4.0 | 7.5 |
| 22 | — | 0.6 | 4.7 | 8.1 |
| 250 | — | 5.9 | 509.0 | 86.0 |
| 500 | — | 11.8 | 2155.5 | 183.0 |
| 1000 | — | 55.6 | 11708.6 | 210.5 |
| 2000 | — | 141.6 | 54653.4 | 386.0 |
| 4000 | — | 299.9 | 234400.1 | 781.5 |

## Comprobación de la complejidad cuadrática (B y C)

Si el tiempo crece como n², el cociente tiempo / n² se mantiene casi constante.

| n | B: tiempo/n² (µs) | C: tiempo/n² (µs) | C: memoria/n² (bytes) |
|---:|---:|---:|---:|
| 250 | 0.203 | 0.125 | 8.34 |
| 500 | 0.203 | 0.141 | 8.83 |
| 1000 | 0.203 | 0.148 | 11.99 |
| 2000 | 0.211 | 0.152 | 13.99 |
| 4000 | 0.216 | 0.156 | 15.00 |
