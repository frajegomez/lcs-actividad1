"""
Juego de tests de las tres versiones de la LCS.
Autoría: Gómez, para la asignatura Diseño avanzado de algoritmos.

Se ejecutan con:   python -m unittest discover -s tests -v
(o automáticamente con `python run.py`).

Como puede haber varias LCS distintas con la misma longitud, no comparamos
las cadenas devueltas, sino que comprobamos dos cosas:
  1) que el resultado ES una subsecuencia común de ambas cadenas, y
  2) que su LONGITUD es la correcta (la misma en todas las versiones).
"""

import os
import random
import sys
import unittest

# Permite importar el paquete `lcs` al lanzar los tests desde cualquier carpeta.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lcs import es_subsecuencia, lcs_dinamica, lcs_hirschberg, lcs_recursiva


def cadena_aleatoria(generador, longitud, alfabeto="ACGT"):
    return "".join(generador.choice(alfabeto) for _ in range(longitud))


class CasosConocidos(unittest.TestCase):
    """Ejemplos pequeños cuya respuesta sabemos de antemano."""

    # (cadena a, cadena b, longitud de la LCS esperada)
    CASOS = [
        ("", "", 0),
        ("", "ABC", 0),
        ("ABC", "", 0),
        ("A", "A", 1),
        ("A", "B", 0),
        ("ABC", "ABC", 3),
        ("ABC", "DEF", 0),
        ("ABCBDAB", "BDCABA", 4),      # ejemplo clásico (BCBA, BDAB...)
        ("AGGTAB", "GXTXAYB", 4),      # GTAB
        ("XMJYAUZ", "MZJAWXU", 4),     # MJAU
        ("AAAA", "AA", 2),
    ]

    def comprobar(self, funcion):
        for a, b, esperada in self.CASOS:
            with self.subTest(funcion=funcion.__name__, a=a, b=b):
                resultado = funcion(a, b)
                self.assertEqual(len(resultado), esperada)
                self.assertTrue(es_subsecuencia(resultado, a))
                self.assertTrue(es_subsecuencia(resultado, b))

    def test_version_a(self):
        self.comprobar(lcs_recursiva)

    def test_version_b(self):
        self.comprobar(lcs_hirschberg)

    def test_version_c(self):
        self.comprobar(lcs_dinamica)

    def test_ejemplo_del_tema_3(self):
        """Entrenamiento 3 del Tema 3: la LCS tiene 20 caracteres."""
        a = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
        b = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
        for funcion in (lcs_hirschberg, lcs_dinamica):
            with self.subTest(funcion=funcion.__name__):
                resultado = funcion(a, b)
                self.assertEqual(len(resultado), 20)
                self.assertTrue(es_subsecuencia(resultado, a))
                self.assertTrue(es_subsecuencia(resultado, b))


class ValidacionCruzada(unittest.TestCase):
    """Comparamos las versiones entre sí con muchas cadenas aleatorias."""

    def test_las_tres_coinciden_en_cadenas_cortas(self):
        generador = random.Random(2024)  # semilla fija: tests reproducibles
        for _ in range(200):
            a = cadena_aleatoria(generador, generador.randint(0, 9))
            b = cadena_aleatoria(generador, generador.randint(0, 9))
            longitudes = {
                len(lcs_recursiva(a, b)),
                len(lcs_hirschberg(a, b)),
                len(lcs_dinamica(a, b)),
            }
            self.assertEqual(len(longitudes), 1, f"Discrepancia con a={a}, b={b}")

    def test_b_y_c_coinciden_en_cadenas_largas(self):
        generador = random.Random(7)
        for longitud_a, longitud_b in [(50, 80), (200, 200), (300, 150), (1000, 1000)]:
            a = cadena_aleatoria(generador, longitud_a)
            b = cadena_aleatoria(generador, longitud_b)
            with self.subTest(longitudes=(longitud_a, longitud_b)):
                r_b = lcs_hirschberg(a, b)
                r_c = lcs_dinamica(a, b)
                self.assertEqual(len(r_b), len(r_c))
                for resultado in (r_b, r_c):
                    self.assertTrue(es_subsecuencia(resultado, a))
                    self.assertTrue(es_subsecuencia(resultado, b))

    def test_otros_alfabetos(self):
        """Alfabeto binario (muchas coincidencias) y amplio (pocas)."""
        generador = random.Random(99)
        for alfabeto in ("01", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            for _ in range(20):
                a = cadena_aleatoria(generador, generador.randint(0, 60), alfabeto)
                b = cadena_aleatoria(generador, generador.randint(0, 60), alfabeto)
                with self.subTest(alfabeto=alfabeto, a=a, b=b):
                    self.assertEqual(len(lcs_hirschberg(a, b)), len(lcs_dinamica(a, b)))


class FuncionAuxiliar(unittest.TestCase):
    def test_es_subsecuencia(self):
        self.assertTrue(es_subsecuencia("", "ABC"))
        self.assertTrue(es_subsecuencia("AC", "ABC"))
        self.assertFalse(es_subsecuencia("CA", "ABC"))
        self.assertFalse(es_subsecuencia("ABCD", "ABC"))


if __name__ == "__main__":
    unittest.main()
