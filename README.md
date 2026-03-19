### Taller 2 – ADT Matriz y evaluación de algoritmos

**Asignatura**: Estructuras de Datos y Algoritmos  
**Tema**: ADT Matriz, operaciones básicas y evaluación analítica / experimental  
**Integrantes (IDs)**: 000528458, 000547528, 000558767  
**Concatenación usada para el hash**: `000528458000547528000558767`  
**SHA-256**: `c1abe9b66a84944396ffa21eef659b785a7baeb030a72c0c213daff1c328b1d9`  
**hashEquipo**: 2 (módulo 5 del hash anterior)  
**Algoritmo asignado**: **Algoritmo 2 – Generación de cuadrados mágicos (tamaño impar)**.

---

### Estructura del proyecto

- `**matrix.py`**: Implementación del **ADT Matriz** inmutable, incluyendo:
  - Constructor y representación interna.
  - Métodos `__eq__`, `__str__`, operaciones de **suma** y **producto** de matrices.
  - Constructores auxiliares: `from_flat`, `identity`.
  - Método estático `magic_square_odd` (Algoritmo 2 – cuadrados mágicos de tamaño impar).
  - Método de apoyo `is_magic_square` para validación en pruebas.
  - Al ejecutarlo como script (`python matrix.py`) imprime por consola ejemplos de cuadrados mágicos 3×3 y 5×5.
- `**test_matrix.py`**: Pruebas unitarias para:
  - `__eq__` (equals).
  - `add` (suma de matrices).
  - `multiply` (producto de matrices).
  - `magic_square_odd` (generación de cuadrados mágicos) e `is_magic_square`.
- `**experiments_magic_square.py`**:
  - Script de **evaluación experimental** del algoritmo de cuadrados mágicos.
  - Cálculo de tiempos promedio (formato fijo `.f` en segundos).
  - Escribe los datos en `**tiempos_cuadrados_magicos.csv`** para uso en Excel/LibreOffice.
  - Ajuste de curva lineal y cálculo de **R²**.

---

### 1. ADT Matriz (matrix.py)

#### 1.1. Representación e inmutabilidad

El ADT `Matrix` representa una matriz de tamaño m \times n de valores reales (tipo `float` en Python).

- El constructor recibe una secuencia de secuencias (`Sequence[Sequence[Number]]`).
- Se valida que:
  - Haya al menos **1 fila** y **1 columna**.
  - Todas las filas tengan la **misma longitud** (matriz rectangular).
- Los datos se normalizan a `float` y se almacenan como:

```python
Tuple[Tuple[Number, ...], ...]
```

es decir, una **tupla de tuplas**, lo cual:

- Evita que el usuario pueda modificar la estructura interna (inmutabilidad lógica).
- Garantiza que, una vez creada la matriz, su contenido no cambia.

Interfaz principal:

- **Propiedades**:
  - `rows: int` – número de filas m.
  - `cols: int` – número de columnas n.
- **Métodos**:
  - `shape() -> (int, int)` – retorna `(rows, cols)`.
  - `__getitem__(index: int)` – permite acceso tipo `matrix[i][j]`.

#### 1.2. Métodos heredados de Object

- `**__eq__(self, other)`**:
  - Si `other` no es instancia de `Matrix`, retorna `NotImplemented` (comportamiento estándar de Python).
  - Si sí lo es, compara las tuplas internas `self._data == other._data`.
  - Dado que los datos se almacenan como `float` exactos para nuestros casos (valores enteros y sumas/productos de enteros), la comparación exacta es adecuada para las pruebas requeridas.
- `**__str__(self)`**:
  - Retorna una representación legible de la matriz, por filas:
    - Cada fila se muestra como `[a b c ...]`.
    - Se usa el formato `"{x:g}"` para evitar notación científica innecesaria.

Ejemplo de salida:

```text
[1 2 3]
[4 5 6]
```

---

### 2. Algoritmo 2 – Generación de cuadrados mágicos (tamaño impar)

#### 2.1. Definición de cuadrado mágico

Una matriz cuadrada de orden n es un **cuadrado mágico** si:

- Está llena con los enteros del 1 al n^2 (en nuestro caso representados como `float`), **sin repetición**.
- La suma de cada fila, cada columna y de las dos diagonales principales es constante e igual a:

M = \frac{n (n^2 + 1)}{2}

#### 2.2. Método implementado: `Matrix.magic_square_odd(n)`

Se implementa el algoritmo clásico de **Siam** (también conocido como método de De la Loubère) para órdenes impares:

Precondiciones:

- `n` debe ser entero, **positivo** e **impar**.  
  - Si `n <= 0` o `n % 2 == 0`, se lanza `ValueError`.

Idea del algoritmo:

1. Crear una matriz local `magic` de tamaño n \times n inicializada en ceros.
2. Inicializar:
  - Posición inicial en la **fila 0** y **columna n//2** (centro de la primera fila).
  - Contador `num = 1` hasta `max_num = n*n`.
3. Mientras `num <= n^2`:
  - Asignar `magic[i][j] = num`.
  - Incrementar `num`.
  - Calcular la posición candidata:
    - `new_i = (i - 1) % n`  (una fila arriba).
    - `new_j = (j + 1) % n`  (una columna a la derecha).
  - Si la celda `(new_i, new_j)` está **ocupada** (`!= 0`):
    - Moverse **una fila hacia abajo** desde la posición actual: `i = (i + 1) % n` (la columna `j` no cambia).
  - En caso contrario:
    - Actualizar `i, j = new_i, new_j`.
4. Al final, envolver la matriz `magic` en un objeto `Matrix` inmutable.

Este método se corresponde con el algoritmo solicitado en el enunciado para cuadrados mágicos de **tamaño impar**.

#### 2.3. Método de validación: `Matrix.is_magic_square()`

Se implementa un método de apoyo, usado exclusivamente en pruebas, que verifica:

1. Que la matriz sea cuadrada: `rows == cols`.
2. Que todas las filas sumen el valor mágico teórico M.
3. Que todas las columnas sumen M.
4. Que las dos diagonales principales sumen M.

Si alguna de estas condiciones falla, retorna `False`; en caso contrario, `True`.

---

### 3. Evaluación analítica del algoritmo de cuadrados mágicos

#### 3.1. Modelo de costo adoptado

- Las llamadas a funciones que recorren estructuras (por ejemplo, el constructor de `Matrix`) se analizan según la cantidad de elementos que procesan.

También se consideran dos fases diferenciadas:

1. **Construcción del arreglo local `magic`** de tamaño n \times n.
2. **Bucle principal** que coloca los valores del 1 al n^2.
3. **Construcción del objeto `Matrix`** a partir de `magic`.

#### 3.2. Conteo aproximado de operaciones

1. **Inicialización de la matriz local `magic`**:
  - Se crea una lista de n filas, cada una con n columnas.
  - Número de asignaciones de cero: n^2.
  - Orden de complejidad: \Theta(n^2).
2. **Bucle principal** (`while num <= max_num`):
  - El bucle se ejecuta exactamente n^2 veces (una por cada valor de `num` desde 1 hasta n^2).
  - En cada iteración se realizan:
    - Una asignación a `magic[i][j]`.
    - Una suma y asignación para incrementar `num`.
    - Unas pocas operaciones aritméticas (`- 1`, `+ 1`, `% n`) para calcular `new_i`, `new_j`.
    - Una comparación y acceso a `magic[new_i][new_j]`.
    - Un conjunto constante de asignaciones para actualizar `i` y `j` (caso ocupado o libre).
  - Cada iteración cuesta una cantidad constante de operaciones c.
  - Por tanto, el bucle tiene un costo:

T_{\text{bucle}}(n) \approx c \cdot n^2

1. **Construcción del objeto `Matrix`**:
  - El constructor recorre nuevamente todos los elementos de `magic` para:
    - Verificar que las filas tienen la misma longitud.
    - Convertir cada valor a `float`.
    - Copiar los datos en una tupla de tuplas.
  - Esto implica otro recorrido completo de n^2 elementos:

T_{\text{constructor}}(n) = c' \cdot n^2

#### 3.3. Función tiempo y notación asintótica

Sumando los tres componentes:

T(n) = a \cdot n^2 + b \cdot n^2 + d \cdot n^2 + e
     = k \cdot n^2 + e

para algunas constantes positivas a, b, d, k, e.

Por tanto, la **función tilde** del tiempo requerido por el algoritmo es:

\tilde{T}(n) = \Theta(n^2)

En términos del tamaño total de la matriz N = n^2 (número total de elementos), se puede escribir:

N = n^2 \quad \Rightarrow \quad \tilde{T}(N) = \Theta(N)

es decir, el tiempo de ejecución crece **linealmente** con el número de posiciones que deben llenarse en el cuadrado mágico.

---

### 4. Evaluación experimental del algoritmo de cuadrados mágicos

#### 4.1. Metodología

Archivo: `experiments_magic_square.py`

Objetivo: obtener una aproximación experimental de la función de tiempo del algoritmo `Matrix.magic_square_odd(n)` y compararla con el análisis analítico anterior.

Pasos:

1. Se definen tamaños impares crecientes:
  ```python
   tamanos = [3, 5, 7, 9, 11, 15, 21, 25, 31, 41, 51]
  ```
2. Para cada tamaño `n`:
  - Se realiza un **“warm up”** llamando una vez a `Matrix.magic_square_odd(n)` (fuera de la medición) para estabilizar caches.
  - Se ejecuta el algoritmo `repeticiones` veces, con `repeticiones = 5`.
  - Se mide el tiempo de cada ejecución con `time.perf_counter()`.
  - Se calcula el **tiempo promedio**  \bar{T}(n)  de las 5 ejecuciones.
3. Los datos se **guardan** en el archivo `tiempos_cuadrados_magicos.csv` (columnas `n`, `N=n^2`, `tiempo_promedio_segundos`, formato de tiempo en decimal `.f`) y además se **imprimen** por consola.
4. Para el ajuste de curva:
  - Se toma N = n^2 como variable independiente.
  - Se ajusta un modelo lineal:

T(N) \approx a \cdot N + b

- Se implementa una función `regresion_lineal(xs, ys)` que calcula:
  - Coeficientes `a` y `b` mediante fórmulas de regresión lineal.
  - El coeficiente de determinación **R²**:

R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}

#### 2.2. Datos experimentales obtenidos

Ejecución en el entorno de desarrollo (Python 3, sin carga de trabajo adicional significativa):  
Salida del script `python experiments_magic_square.py`:


| n   | N = n^2 | Tiempo promedio (s) |
| --- | ------- | ------------------- |
| 3   | 9       | 0.000004            |
| 5   | 25      | 0.000007            |
| 7   | 49      | 0.000011            |
| 9   | 81      | 0.000016            |
| 11  | 121     | 0.000023            |
| 15  | 225     | 0.000040            |
| 21  | 441     | 0.000072            |
| 25  | 625     | 0.000099            |
| 31  | 961     | 0.000151            |
| 41  | 1681    | 0.000260            |
| 51  | 2601    | 0.000413            |


#### 4.3. Curva de mejor ajuste y R²

El propio script calcula el ajuste lineal T(N) = aN + b con N = n^2.  
Con los datos anteriores se obtuvo:

- **a** ≈ `1.5627e-07` (pendiente, segundos por elemento)  
- **b** ≈ `2.6959e-06` (ordenada en el origen)  
- **R²** ≈ `0.999649`

Interpretación:

- El valor de **R²** está muy cercano a 1, lo que indica que el modelo lineal en función de N = n^2 explica prácticamente toda la variabilidad observada en los tiempos medidos.
- Esto concuerda con la predicción analítica de que:

\tilde{T}(N) = \Theta(N), \quad \text{con } N = n^2

equivalente a:

\tilde{T}(n) = \Theta(n^2)

---

### 5. Pruebas unitarias

Archivo: `test_matrix.py`  
Framework: `unittest` de la biblioteca estándar de Python.

#### 5.1. Prueba de `equals` (`__eq`__)

- **Caso normal**:
  - Dos matrices con el mismo contenido, aunque una se cree con enteros y otra con `float`, deben ser iguales.
- **Caso diferente**:
  - Dos matrices con solo un elemento distinto deben resultar no iguales.

#### 5.2. Pruebas de suma

- **Caso normal**:
  - Suma de dos matrices 2 \times 2 con valores pequeños y resultado esperado especificado a mano.
- **Caso extremo**:
  - Intento de sumar matrices de dimensiones incompatibles (por ejemplo, 1 \times 2 con 2 \times 2); se espera `ValueError`.

#### 5.3. Pruebas de multiplicación

- **Caso normal**:
  - Multiplicación de matrices de tamaños 2 \times 3 y 3 \times 2, con resultado calculado manualmente.
- **Caso con identidad**:
  - Verificación de que A \cdot I = A e I \cdot A = A para una matriz identidad 3 \times 3.
- **Caso extremo**:
  - Dimensiones incompatibles (por ejemplo, 1 \times 2 por 1 \times 2); se espera `ValueError`.

#### 5.4. Pruebas del algoritmo de cuadrados mágicos

- **Caso extremo mínimo**:
  - `n = 1`: el cuadrado mágico es simplemente `[1]`.
  - Se verifica que `is_magic_square()` retorna `True`.
- **Caso conocido clásico**:
  - `n = 3`: se compara con el patrón estándar:
    ```text
    8 1 6
    3 5 7
    4 9 2
    ```
  - Se verifica igualdad elemento a elemento y que `is_magic_square()` es `True`.
- **Caso normal adicional**:
  - `n = 5`: se verifica que el resultado cumple `is_magic_square() == True`.
- **Casos inválidos**:
  - `n = 0`, `n = 2`, `n = -3`: en todos estos casos se espera `ValueError`.

