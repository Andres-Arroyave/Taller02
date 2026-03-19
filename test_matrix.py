import unittest

"""
Taller 2 – Estructuras de Datos y Algoritmos (UPB)
Integrantes (IDs): 000528458, 000547528, 000558767
"""

from matrix import Matrix


class TestMatrixEquals(unittest.TestCase):
    def test_equals_same_content(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1.0, 2.0], [3.0, 4.0]])
        self.assertEqual(a, b)

    def test_not_equals_different_content(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2], [3, 5]])
        self.assertNotEqual(a, b)


class TestMatrixAddition(unittest.TestCase):
    def test_addition_basic(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        c = a.add(b)

        expected = Matrix([[6, 8], [10, 12]])
        self.assertEqual(c, expected)

    def test_addition_dimension_mismatch(self) -> None:
        a = Matrix([[1, 2]])
        b = Matrix([[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            a.add(b)


class TestMatrixMultiplication(unittest.TestCase):
    def test_multiplication_basic(self) -> None:
        a = Matrix([[1, 2, 3], [4, 5, 6]])
        b = Matrix([[7, 8], [9, 10], [11, 12]])
        c = a.multiply(b)

        expected = Matrix([[58, 64], [139, 154]])
        self.assertEqual(c, expected)

    def test_multiplication_with_identity(self) -> None:
        ident = Matrix.identity(3)
        a = Matrix([[2, -1, 0], [0, 3, 5], [4, 4, 1]])
        self.assertEqual(a.multiply(ident), a)
        self.assertEqual(ident.multiply(a), a)

    def test_multiplication_dimension_mismatch(self) -> None:
        a = Matrix([[1, 2]])
        b = Matrix([[1, 2]])
        with self.assertRaises(ValueError):
            a.multiply(b)


class TestMagicSquare(unittest.TestCase):
    def test_magic_square_order_1(self) -> None:
        m = Matrix.magic_square_odd(1)
        self.assertTrue(m.is_magic_square())
        self.assertEqual(m.shape(), (1, 1))
        self.assertEqual(m[0][0], 1.0)

    def test_magic_square_order_3(self) -> None:
        m = Matrix.magic_square_odd(3)
        self.assertTrue(m.is_magic_square())

        # Patrón clásico conocido para n = 3
        expected = Matrix([[8, 1, 6], [3, 5, 7], [4, 9, 2]])
        self.assertEqual(m, expected)

    def test_magic_square_order_5_is_magic(self) -> None:
        m = Matrix.magic_square_odd(5)
        self.assertTrue(m.is_magic_square())

    def test_magic_square_invalid_n(self) -> None:
        with self.assertRaises(ValueError):
            Matrix.magic_square_odd(0)
        with self.assertRaises(ValueError):
            Matrix.magic_square_odd(2)
        with self.assertRaises(ValueError):
            Matrix.magic_square_odd(-3)


if __name__ == "__main__":
    unittest.main()

