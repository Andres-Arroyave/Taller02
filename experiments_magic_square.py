"""
Taller 2 – Estructuras de Datos y Algoritmos (UPB)
Integrantes (IDs): 000528458, 000547528, 000558767
"""

"""
Evaluación experimental del algoritmo de generación de cuadrados mágicos
de tamaño impar (Algoritmo 2).

Se mide el tiempo promedio de construcción de un cuadrado mágico de orden n
utilizando el método Matrix.magic_square_odd(n), para varios valores de n.
"""

import csv
import time
from typing import Iterable, List, Tuple

from matrix import Matrix


def medir_tiempos(
    tamanos: Iterable[int], repeticiones: int = 5
) -> List[Tuple[int, float]]:
    """
    Mide el tiempo promedio (en segundos) de generación de cuadrados mágicos
    de orden n para cada n en `tamanos`.

    Para cada tamaño se ejecuta el algoritmo `repeticiones` veces y se calcula
    el promedio. No se incluyen operaciones de entrada/salida dentro de la
    ventana de medición.
    """
    resultados: List[Tuple[int, float]] = []

    for n in tamanos:
        # Pequeño "warm up" para estabilizar caches/JIT (si aplica)
        Matrix.magic_square_odd(n)

        tiempos: List[float] = []
        for _ in range(repeticiones):
            inicio = time.perf_counter()
            Matrix.magic_square_odd(n)
            fin = time.perf_counter()
            tiempos.append(fin - inicio)

        promedio = sum(tiempos) / len(tiempos)
        resultados.append((n, promedio))

    return resultados


def regresion_lineal(xs: List[float], ys: List[float]) -> Tuple[float, float, float]:
    """
    Ajuste lineal y = a*x + b y cálculo de R^2 usando solo la biblioteca estándar.
    """
    n = len(xs)
    if n == 0:
        raise ValueError("Se requieren al menos 1 par de datos para la regresión.")

    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_xx = sum(x * x for x in xs)
    sum_xy = sum(x * y for x, y in zip(xs, ys))

    denom = n * sum_xx - sum_x * sum_x
    if denom == 0:
        raise ValueError("Los datos no permiten calcular una regresión lineal (denominador cero).")

    a = (n * sum_xy - sum_x * sum_y) / denom
    b = (sum_y * sum_xx - sum_x * sum_xy) / denom

    # Cálculo de R^2
    mean_y = sum_y / n
    sst = sum((y - mean_y) ** 2 for y in ys)
    sse = sum((y - (a * x + b)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - sse / sst if sst > 0 else 1.0

    return a, b, r2


def main() -> None:
    # Valores de n impares crecientes para el experimento
    tamanos = [3, 5, 7, 9, 11, 15, 21, 25, 31, 41, 51]
    repeticiones = 5
    archivo_csv = "tiempos_cuadrados_magicos.csv"

    resultados = medir_tiempos(tamanos, repeticiones=repeticiones)

    # Guardar CSV para Excel/LibreOffice (datos tabulados y gráficas)
    with open(archivo_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "N=n^2", "tiempo_promedio_segundos"])
        for n, t in resultados:
            writer.writerow([n, n * n, f"{t:.6f}"])

    print(f"Datos guardados en: {archivo_csv}")
    print()
    print("n\tN=n^2\ttiempo_promedio_segundos")
    for n, t in resultados:
        print(f"{n}\t{n*n}\t{t:.6f}")

    # Ajuste lineal T(N) = a*N + b donde N = n^2 (número de elementos)
    xs = [float(n * n) for n, _ in resultados]
    ys = [t for _, t in resultados]

    a, b, r2 = regresion_lineal(xs, ys)
    print()
    print("Ajuste lineal T(N) = a*N + b, con N = n^2")
    print(f"a = {a:.6f}")
    print(f"b = {b:.6f}")
    print(f"R^2 = {r2:.6f}")


if __name__ == "__main__":
    main()

