"""
Módulo 7: Análisis de Datos Bioinformáticos con Pandas y Visualización.
Temas: DataFrames con Pandas, Perfiles con Ventana Deslizante (Sliding Window) y RNA-seq.
"""

import math
from typing import Dict, Any, List

MODULE_INFO = {
    "id": 7,
    "title": "Módulo 7: Análisis de Datos Bioinformáticos con Pandas y Visualización",
    "summary": "Aprende a analizar tablas ómicas con Pandas, calcula perfiles de GC a lo largo de cromosomas con ventanas deslizantes y analiza cambios de expresión génica.",
    "biopython_ref": "Capítulo 17 del Tutorial-1.83.pdf (Visualización de datos genómicos y diagramas)",

    "theory_python": """
### 🐍 Análisis de Datos con Pandas en Python

`pandas` es el estándar de facto para la manipulación y análisis de datos estructurados en tablas (**DataFrames**).

#### 1. Crear y Leer DataFrames
```python
import pandas as pd

# Lectura directa de archivos tabulares (TSV o CSV)
df = pd.read_csv("datos_expresion.tsv", sep="\\t")

# Ver las primeras filas y columnas
print(df.head())
print(df.columns)
```

#### 2. Filtrado y Nuevas Columnas
```python
# Crear una nueva columna calculada
df["Total_Reads"] = df["Muestra_1"] + df["Muestra_2"]

# Filtrar filas según condiciones lógicas
genes_altos = df[df["Total_Reads"] > 1000]
```

#### 3. Matemáticas con `math` o `numpy`
En análisis de expresión es estándar trabajar en escala logarítmica binaria ($log_2$):
```python
import math
lfc = math.log2(tratado / control)
```
""",

    "theory_bio": """
### 🧬 Aplicación Bioinformática: Ventana Deslizante y RNA-seq

#### 1. Perfil de GC por Ventana Deslizante (Sliding Window)
El contenido de GC no es uniforme a lo largo de un cromosoma:
- **Islas CpG**: Regiones de 200 a 2000 pb con alta densidad de GC localizadas cerca de los promotores de genes de mantenimiento (housekeeping).
- **Algoritmo de ventana deslizante**: Se define un tamaño de ventana $W$ (ej: 100 pb) y un desplazamiento o paso $S$ (ej: 50 pb). Se extrae la subcadena `seq[i : i+W]`, se calcula su %GC y se avanza `i += S`.

#### 2. Log2 Fold-Change en Secuenciación de ARN (RNA-seq)
Mide la magnitud del cambio en la abundancia de transcritos entre una condición experimental y un control:
$$\\log_2(\\text{Fold-Change}) = \\log_2\\left(\\frac{\\text{Expresión Tratado} + 1}{\\text{Expresión Control} + 1}\\right)$$
- El sumando $+1$ es un **pseudoconteo** (pseudocount) imprescindible para evitar divisiones por cero o logaritmos de cero.
- $\\log_2FC = +1 \\implies$ El gen se expresa al doble (inducido / sobreexpresado).
- $\\log_2FC = -1 \\implies$ El gen se expresa a la mitad (reprimido / subexpresado).
""",

    "exercises": [
        {
            "id": "ex_07_01_sliding_window_gc",
            "title": "Reto 7.1: Perfil de GC con Ventana Deslizante",
            "description": """
Crea una función llamada `ventana_deslizante_gc(secuencia, ventana, paso)` que calcule el %GC a lo largo de la secuencia mediante ventanas contiguas.

**Requisitos**:
1. Recorre la secuencia desde `i = 0` mientras `i + ventana <= len(secuencia)`.
2. En cada paso, extrae el fragmento de longitud `ventana`.
3. Calcula el %GC del fragmento y redondéalo a 2 decimales.
4. Añade a una lista de resultados una tupla `(posicion_inicio, gc_pct)` donde `posicion_inicio` es el índice `i`.
5. Avanza `i` sumándole `paso`.
6. Si la secuencia es más corta que `ventana`, retornar una lista vacía `[]`.
""",
            "starter_code": """def ventana_deslizante_gc(secuencia: str, ventana: int, paso: int) -> list:
    # Tu código aquí:
    pass
""",
            "target_function": "ventana_deslizante_gc",
            "test_cases": [
                {
                    "name": "Secuencia de 8 pb con ventana=4 y paso=2",
                    "args": ("GCGCATAT", 4, 2),
                    "expected": [(0, 100.0), (2, 50.0), (4, 0.0)]
                },
                {
                    "name": "Secuencia más corta que la ventana",
                    "args": ("ATG", 10, 2),
                    "expected": []
                }
            ],
            "hints": [
                "Usa un bucle `while i + ventana <= len(seq):` o `range(0, len(seq) - ventana + 1, paso)`.",
                "En cada ventana, calcula `gc = ((frag.count('G') + frag.count('C')) / ventana) * 100`."
            ],
            "solution": """def ventana_deslizante_gc(secuencia: str, ventana: int, paso: int) -> list:
    seq = secuencia.upper()
    resultados = []
    if len(seq) < ventana or ventana <= 0 or paso <= 0:
        return resultados
    for i in range(0, len(seq) - ventana + 1, paso):
        fragmento = seq[i:i+ventana]
        g = fragmento.count("G")
        c = fragmento.count("C")
        gc_pct = round(((g + c) / ventana) * 100.0, 2)
        resultados.append((i, gc_pct))
    return resultados
"""
        },
        {
            "id": "ex_07_02_log2_fold_change",
            "title": "Reto 7.2: Cálculo de Log2 Fold-Change con Pseudoconteo",
            "description": """
Crea una función llamada `calcular_log2_fc(control, tratado)` que calcule el cambio relativo en escala logarítmica base 2:
$$\\log_2\\left(\\frac{\\text{tratado} + 1.0}{\\text{control} + 1.0}\\right)$$

**Requisitos**:
1. Suma `1.0` tanto a `control` como a `tratado`.
2. Calcula el logaritmo en base 2 con `math.log2(...)`.
3. Retorna el resultado redondeado a 2 decimales.
""",
            "starter_code": """import math

def calcular_log2_fc(control: float, tratado: float) -> float:
    # Tu código aquí:
    pass
""",
            "target_function": "calcular_log2_fc",
            "test_cases": [
                {
                    "name": "Duplicación exacta de la expresión (ej: 99 control, 199 tratado -> ratio 2 -> LFC 1.0)",
                    "args": (99.0, 199.0),
                    "expected": 1.0,
                    "tolerance": 0.05
                },
                {
                    "name": "Misma expresión (sin cambios -> LFC 0.0)",
                    "args": (50.0, 50.0),
                    "expected": 0.0,
                    "tolerance": 0.05
                },
                {
                    "name": "Represión a la mitad (ej: 199 control, 99 tratado -> LFC -1.0)",
                    "args": (199.0, 99.0),
                    "expected": -1.0,
                    "tolerance": 0.05
                }
            ],
            "hints": [
                "Usa `math.log2((tratado + 1.0) / (control + 1.0))`.",
                "Aplica `round(..., 2)` al valor resultante."
            ],
            "solution": """import math

def calcular_log2_fc(control: float, tratado: float) -> float:
    ratio = (tratado + 1.0) / (control + 1.0)
    return round(math.log2(ratio), 2)
"""
        }
    ]
}
