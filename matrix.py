from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

"""
Taller 2 – Estructuras de Datos y Algoritmos (UPB)
Integrantes (IDs): 000528458, 000547528, 000558767
"""

Number = float


class Matrix:
    """
    ADT Matriz inmutable de tamaño m x n de números reales.

    Internamente almacena los datos como una tupla de tuplas para garantizar
    inmutabilidad desde el punto de vista del usuario. La clase es "frozen":
    no se pueden añadir ni modificar atributos después de la construcción.
    """

    __slots__ = ("_rows", "_cols", "_data")

    def __init__(self, data: Sequence[Sequence[Number]]) -> None:
        if not data or not data[0]:
            raise ValueError("La matriz debe tener al menos 1 fila y 1 columna.")

        rows = len(data)
        cols = len(data[0])

        normalized: List[Tuple[Number, ...]] = []
        for row in data:
            if len(row) != cols:
                raise ValueError("Todas las filas deben tener la misma longitud.")
            normalized.append(tuple(float(x) for x in row))

        self._rows = rows
        self._cols = cols
        self._data = tuple(normalized)

    def __setattr__(self, name: str, value: object) -> None:
        """Bloquea la asignación de atributos después de la construcción (inmutabilidad fuerte)."""
        try:
            getattr(self, "_data")
        except AttributeError:
            object.__setattr__(self, name, value)
            return
        raise AttributeError("Matrix is immutable")

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def shape(self) -> Tuple[int, int]:
        return self._rows, self._cols

    def __getitem__(self, index: int) -> Tuple[Number, ...]:
        return self._data[index]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self._data == other._data

    def __str__(self) -> str:
        # Representación legible de la matriz
        filas = []
        for row in self._data:
            # Formato compacto, evitando notación científica cuando es posible
            fila = " ".join(f"{x:g}" for x in row)
            filas.append("[" + fila + "]")
        return "\n".join(filas)

    def __repr__(self) -> str:
        return f"Matrix({self._rows}x{self._cols})"

    # ------------------------------------------------------------------
    # Operaciones básicas
    # ------------------------------------------------------------------
    def add(self, other: "Matrix") -> "Matrix":
        """Suma de matrices."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Las matrices deben tener las mismas dimensiones para sumarse.")

        result: List[List[Number]] = []
        for i in range(self.rows):
            row: List[Number] = []
            for j in range(self.cols):
                row.append(self._data[i][j] + other._data[i][j])
            result.append(row)
        return Matrix(result)

    def multiply(self, other: "Matrix") -> "Matrix":
        """Producto de matrices (multiplicación matricial estándar)."""
        if self.cols != other.rows:
            raise ValueError(
                "Dimensiones incompatibles para multiplicación: "
                f"{self.rows}x{self.cols} * {other.rows}x{other.cols}"
            )

        # Algoritmo clásico O(m * n * p)
        result: List[List[Number]] = [[0.0 for _ in range(other.cols)] for _ in range(self.rows)]

        for i in range(self.rows):
            for k in range(self.cols):
                aik = self._data[i][k]
                if aik == 0:
                    continue
                for j in range(other.cols):
                    result[i][j] += aik * other._data[k][j]

        return Matrix(result)

    # ------------------------------------------------------------------
    # Constructores auxiliares
    # ------------------------------------------------------------------
    @staticmethod
    def from_flat(values: Sequence[Number], rows: int, cols: int) -> "Matrix":
        if rows <= 0 or cols <= 0:
            raise ValueError("Las dimensiones deben ser positivas.")
        expected = rows * cols
        if len(values) != expected:
            raise ValueError(f"Se esperaban {expected} valores, se recibieron {len(values)}.")

        it = iter(values)
        data: List[List[Number]] = []
        for _ in range(rows):
            data.append([float(next(it)) for _ in range(cols)])
        return Matrix(data)

    @staticmethod
    def identity(n: int) -> "Matrix":
        if n <= 0:
            raise ValueError("El tamaño debe ser positivo.")
        data: List[List[Number]] = []
        for i in range(n):
            row: List[Number] = []
            for j in range(n):
                row.append(1.0 if i == j else 0.0)
            data.append(row)
        return Matrix(data)

    @staticmethod
    def zeros(rows: int, cols: int) -> "Matrix":
        """Crea una matriz de ceros de tamaño rows x cols."""
        if rows <= 0 or cols <= 0:
            raise ValueError("Las dimensiones deben ser positivas.")
        data: List[List[Number]] = [[0.0 for _ in range(cols)] for _ in range(rows)]
        return Matrix(data)

    # ------------------------------------------------------------------
    # Algoritmo 2: generación de cuadrados mágicos (tamaño impar)
    # ------------------------------------------------------------------
    @staticmethod
    def magic_square_odd(n: int) -> "Matrix":
        """
        Genera un cuadrado mágico de tamaño n impar usando el algoritmo de
        Siam (método clásico para órdenes impares).

        El algoritmo recorre exactamente n^2 posiciones, por lo que su
        complejidad temporal es O(n^2).
        """
        if n <= 0 or n % 2 == 0:
            raise ValueError("El tamaño n debe ser un entero positivo impar.")

        # Matriz interna mutable solo durante la construcción
        magic: List[List[Number]] = [[0.0 for _ in range(n)] for _ in range(n)]

        i = 0
        j = n // 2
        num = 1
        max_num = n * n

        while num <= max_num:
            magic[i][j] = float(num)
            num += 1

            # Movimiento "hacia arriba y a la derecha"
            new_i = (i - 1) % n
            new_j = (j + 1) % n

            if magic[new_i][new_j] != 0.0:
                # Celda ocupada: moverse una fila hacia abajo desde la posición actual
                i = (i + 1) % n
                # j se mantiene
            else:
                i, j = new_i, new_j

        return Matrix(magic)

    # ------------------------------------------------------------------
    # Métodos de apoyo para validación de cuadrados mágicos
    # ------------------------------------------------------------------
    def is_magic_square(self) -> bool:
        """
        Verifica si la matriz actual es un cuadrado mágico.
        Solo se utiliza en pruebas y validaciones.
        """
        if self.rows != self.cols:
            return False

        n = self.rows
        # Suma mágica teórica para un cuadrado de orden n
        target = n * (n * n + 1) / 2.0

        # Filas
        for i in range(n):
            if sum(self._data[i][j] for j in range(n)) != target:
                return False

        # Columnas
        for j in range(n):
            if sum(self._data[i][j] for i in range(n)) != target:
                return False

        # Diagonales
        if sum(self._data[i][i] for i in range(n)) != target:
            return False
        if sum(self._data[i][n - 1 - i] for i in range(n)) != target:
            return False

        return True


if __name__ == "__main__":
    # Ejemplo simple: imprimir un cuadrado mágico de tamaño impar 3x3
    m3 = Matrix.magic_square_odd(3)
    print("Cuadrado mágico 3x3:")
    print(m3)

    # Otro ejemplo: cuadrado mágico 5x5
    m5 = Matrix.magic_square_odd(5)
    print("\nCuadrado mágico 5x5:")
    print(m5)
