"""
Módulo 1: Fundamentos de Python y Secuencias Biológicas.
Temas: Variables, Tipos de datos, Operaciones matemáticas y Cadenas de ADN/ARN.
"""

from typing import Dict, Any, List

MODULE_INFO = {
    "id": 1,
    "title": "Módulo 1: Fundamentos de Python y Secuencias Biológicas",
    "summary": "Aprende los conceptos básicos de programación (variables, números, cadenas y operaciones) aplicados al análisis inmediato de secuencias de ADN y ARN.",
    "biopython_ref": "Capítulo 3 del Tutorial-1.83.pdf (Introducción a cadenas y objetos Seq)",
    
    "theory_python": """
### 🐍 Conceptos Fundamentales de Python

En Python, un programa manipula **datos** almacenados en **variables**.

#### 1. Variables y Asignación
Una variable es un nombre que apunta a un valor en memoria. Se asigna con el operador `=`:
```python
longitud = 1500           # int (entero)
peso_molecular = 330.25   # float (número decimal)
nombre_gen = "TP53"       # str (cadena de texto)
es_codificante = True     # bool (booleano: True o False)
```

#### 2. Cadenas de Texto (`str`)
Las secuencias biológicas se representan naturalmente como cadenas de texto entre comillas simples `'` o dobles `"`:
- **Longitud**: `len(secuencia)` devuelve el número de caracteres.
- **Conteo**: `secuencia.count('A')` cuenta cuántas veces aparece una letra.
- **Mayúsculas / Minúsculas**: `secuencia.upper()` y `secuencia.lower()`.
- **Reemplazo**: `secuencia.replace('T', 'U')` sustituye subcadenas.
- **Concatenación**: Unir cadenas con el operador `+`: `"ATG" + "CCC" -> "ATGCCC"`.

#### 3. Operaciones Matemáticas
- Suma `+`, Resta `-`, Multiplicación `*`, División decimal `/`, División entera `//`, Módulo (resto) `%`.
- Redondeo: `round(valor, decimales)` (ej: `round(3.14159, 2)` devuelve `3.14`).
""",

    "theory_bio": """
### 🧬 Aplicación Bioinformática: El Lenguaje del ADN

El ácido desoxirribonucleico (ADN) es un polímero compuesto por cuatro bases nitrogenadas:
- **Adenina (A)**
- **Citosina (C)**
- **Guanina (G)**
- **Timina (T)**

#### 1. Contenido de GC (%GC)
El porcentaje de bases Guanina y Citosina en una secuencia es una de las métricas más universales en bioinformática:
$$\\%GC = \\frac{\\text{Conteo}(G) + \\text{Conteo}(C)}{\\text{Longitud Total}} \\times 100$$
- **Importancia biológica**:
  - Los pares **G-C** forman 3 puentes de hidrógeno, mientras que **A-T** forman 2.
  - Mayor %GC implica mayor estabilidad térmica y mayor temperatura de desnaturalización ($T_m$).
  - En bacterias, el %GC varía del 25% al 75% y se utiliza en taxonomía y genómica comparativa para detectar transferencia horizontal de genes (islas genómicas).

#### 2. Transcripción: De ADN a ARN
Durante la transcripción génica, la ARN polimerasa sintetiza ARN mensajero reemplazando la base **Timina (T)** por **Uracilo (U)**.
""",

    "exercises": [
        {
            "id": "ex_01_01_gc_content",
            "title": "Reto 1.1: Calculador de Contenido GC (%GC)",
            "description": """
Crea una función llamada `calcular_gc(secuencia)` que reciba una cadena de ADN (puede venir en mayúsculas o minúsculas) y retorne el porcentaje de bases **G** y **C** (número decimal `float`) redondeado a 2 decimales.

**Requisitos**:
1. La función debe ignorar si la secuencia viene en mayúsculas o minúsculas (por ejemplo, `'gcat'` debe funcionar igual que `'GCAT'`).
2. Si la secuencia está vacía (longitud 0), la función debe retornar `0.0`.
3. Debe retornar el resultado como un porcentaje entre 0.0 y 100.0 redondeado con `round(resultado, 2)`.
""",
            "starter_code": """def calcular_gc(secuencia: str) -> float:
    # 1. Asegúrate de pasar la secuencia a mayúsculas
    # 2. Si la longitud es 0, retorna 0.0
    # 3. Cuenta las bases 'G' y 'C'
    # 4. Calcula el porcentaje y redondéalo a 2 decimales
    # Tu código aquí:
    pass
""",
            "target_function": "calcular_gc",
            "test_cases": [
                {
                    "name": "Secuencia balanceada (50% GC)",
                    "args": ("GCAT",),
                    "expected": 50.0
                },
                {
                    "name": "Secuencia rica en GC (75% GC)",
                    "args": ("GCGC",),
                    "expected": 100.0
                },
                {
                    "name": "Secuencia en minúsculas (gcatgcat)",
                    "args": ("gcatgcat",),
                    "expected": 50.0
                },
                {
                    "name": "Fragmento de insulina humana (73.33% GC)",
                    "args": ("ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCC",),
                    "expected": 73.33,
                    "tolerance": 0.05
                },
                {
                    "name": "Secuencia vacía (debe retornar 0.0)",
                    "args": ("",),
                    "expected": 0.0
                }
            ],
            "hints": [
                "Usa `secuencia = secuencia.upper()` para estandarizar a mayúsculas.",
                "Recuerda que `len(secuencia)` te da el número total de nucleótidos.",
                "Fórmula: `((g_count + c_count) / total) * 100` y usa `round(..., 2)`."
            ],
            "solution": """def calcular_gc(secuencia: str) -> float:
    seq = secuencia.upper()
    total = len(seq)
    if total == 0:
        return 0.0
    g = seq.count('G')
    c = seq.count('C')
    gc_pct = ((g + c) / total) * 100
    return round(gc_pct, 2)
"""
        },
        {
            "id": "ex_01_02_transcription",
            "title": "Reto 1.2: Simulador de Transcripción Génica",
            "description": """
Crea una función llamada `transcribir_adn(adn_seq)` que reciba una cadena de ADN codificante y retorne su correspondiente transcrito de ARN mensajero (reemplazando cada `T` por `U`).

**Requisitos**:
1. El resultado siempre debe estar en letras mayúsculas.
2. Si la entrada contiene minúsculas, conviértelas a mayúsculas antes de transcribir.
3. Ejemplo: `'atgc'` -> `'AUGC'`.
""",
            "starter_code": """def transcribir_adn(adn_seq: str) -> str:
    # Tu código aquí:
    pass
""",
            "target_function": "transcribir_adn",
            "test_cases": [
                {
                    "name": "Codón de inicio simple",
                    "args": ("ATG",),
                    "expected": "AUG"
                },
                {
                    "name": "Secuencia en minúsculas",
                    "args": ("atgctacta",),
                    "expected": "AUGCUACUA"
                },
                {
                    "name": "Sin timinas",
                    "args": ("GGGCCC",),
                    "expected": "GGGCCC"
                },
                {
                    "name": "Cadena vacía",
                    "args": ("",),
                    "expected": ""
                }
            ],
            "hints": [
                "Usa el método `.upper()` para convertir el texto a mayúsculas.",
                "El método `.replace('T', 'U')` te permite sustituir todas las apariciones de 'T' por 'U'."
            ],
            "solution": """def transcribir_adn(adn_seq: str) -> str:
    return adn_seq.upper().replace('T', 'U')
"""
        },
        {
            "id": "ex_01_03_molecular_weight",
            "title": "Reto 1.3: Peso Molecular de Oligonucleótidos",
            "description": """
Crea una función llamada `peso_molecular_adn(secuencia)` que calcule el peso molecular aproximado en Daltons (g/mol) de una hebra simple de ADN lineal.

Usa los siguientes pesos promedio por nucleótido monomérico monofosfato:
- **A**: 313.21 Da
- **T**: 304.20 Da
- **C**: 289.18 Da
- **G**: 329.21 Da

**Requisitos**:
1. Debe aceptar mayúsculas y minúsculas.
2. Si la secuencia está vacía, retornar `0.0`.
3. Retornar el valor redondeado a 2 decimales.
""",
            "starter_code": """def peso_molecular_adn(secuencia: str) -> float:
    # Tu código aquí:
    pass
""",
            "target_function": "peso_molecular_adn",
            "test_cases": [
                {
                    "name": "Oligo simple ATGC",
                    "args": ("ATGC",),
                    "expected": 1235.8,
                    "tolerance": 0.05
                },
                {
                    "name": "Poli-A de 10 nucleótidos",
                    "args": ("AAAAAAAAAA",),
                    "expected": 3132.1,
                    "tolerance": 0.1
                },
                {
                    "name": "Secuencia vacía",
                    "args": ("",),
                    "expected": 0.0
                }
            ],
            "hints": [
                "Cuenta individualmente cada base con `seq.count('A')`, etc.",
                "Multiplica la cantidad de cada base por su respectivo peso molecular y súmalos.",
                "Aplica `round(total, 2)`."
            ],
            "solution": """def peso_molecular_adn(secuencia: str) -> float:
    seq = secuencia.upper()
    if not seq:
        return 0.0
    peso_a = seq.count('A') * 313.21
    peso_t = seq.count('T') * 304.20
    peso_c = seq.count('C') * 289.18
    peso_g = seq.count('G') * 329.21
    return round(peso_a + peso_t + peso_c + peso_g, 2)
"""
        }
    ]
}
