"""
Módulo 4: Funciones, Modularidad y Diseño de Primers.
Temas: Definición de funciones (def), Parámetros, Type hints, Docstrings y Diseño de Oligonucleótidos.
"""

from typing import Dict, Any, List

MODULE_INFO = {
    "id": 4,
    "title": "Módulo 4: Funciones, Modularidad y Diseño de Primers",
    "summary": "Construye funciones bioinformáticas robustas y reutilizables para calcular el reverso complementario de ADN y validar cebadores de PCR.",
    "biopython_ref": "Capítulo 3 del Tutorial-1.83.pdf (Sección 3.3: Complemento y Reverso complementario)",

    "theory_python": """
### 🐍 Funciones y Modularidad en Python

Una función es un bloque de código reutilizable que realiza una tarea específica, recibe entradas (**argumentos**) y devuelve un resultado (**retorno**).

#### 1. Anatomía de una Función
```python
def calcular_longitud_media(secuencias: list[str]) -> float:
    \"\"\"Calcula la longitud promedio de una lista de secuencias.\"\"\"
    if not secuencias:
        return 0.0
    total = sum(len(s) for s in secuencias)
    return total / len(secuencias)
```
- `def`: Palabra reservada para definir funciones.
- **Type hints** (`secuencias: list[str] -> float`): Especifican los tipos esperados para mejorar la legibilidad y prevenir errores.
- **Docstring** (`\"\"\"...\"\"\"`): Documentación oficial de la función accesible mediante `help()`.
- `return`: Devuelve el valor calculado al invocador.

#### 2. Argumentos por Defecto (Default Parameters)
Permiten proporcionar valores predeterminados para parámetros opcionales:
```python
def filtrar_por_longitud(secuencias: list[str], min_len: int = 50) -> list[str]:
    return [s for s in secuencias if len(s) >= min_len]
```
""",

    "theory_bio": """
### 🧬 Aplicación Bioinformática: Reverso Complementario y PCR

#### 1. El Principio de Antiparalelismo y Reverso Complementario
El ADN en doble hélice es **antiparalelo** y **complementario**:
- Una hebra corre en sentido $5' \\to 3'$ y la hebra opuesta corre en sentido $3' \\to 5'$.
- Las reglas de apareamiento canónico de Watson-Crick establecen:
  - **A** se aparea con **T** (y viceversa).
  - **C** se aparea con **G** (y viceversa).
- Cuando sintetizamos o diseñamos un cebador para la hebra antisentido (Reverse Primer), debemos obtener el **reverso complementario**:
  1. Hallar la base complementaria de cada posición: `A->T, T->A, C->G, G->C`.
  2. Invertir el orden de la secuencia resultante para que siempre se lea en sentido convencional $5' \\to 3'$.

#### 2. Temperatura de Fusión ($T_m$) de un Primer de PCR
La temperatura de fusión es aquella en la que el 50% del oligonucleótido se encuentra en duplex (unido a su diana) y el 50% desnaturalizado.
- **Regla empírica de Wallace** (válida para oligos cortos de 14 a 25 nucleótidos):
  $$T_m = 2 \\times (\\text{A} + \\text{T}) + 4 \\times (\\text{G} + \\text{C}) \\quad [^\\circ\\text{C}]$$
""",

    "exercises": [
        {
            "id": "ex_04_01_reverse_complement",
            "title": "Reto 4.1: Función de Reverso Complementario",
            "description": """
Crea una función llamada `reverso_complementario(secuencia)` que reciba una cadena de ADN en sentido $5' \\to 3'$ y devuelva su hebra complementaria invertida, también en sentido $5' \\to 3'$.

**Requisitos**:
1. La función debe admitir secuencias en mayúsculas o minúsculas y devolver siempre el resultado en **letras mayúsculas**.
2. Aplica la complementariedad: `A <-> T`, `C <-> G`.
3. Invierte el orden de la cadena.
4. Si la secuencia está vacía, debe retornar `""`.
""",
            "starter_code": """def reverso_complementario(secuencia: str) -> str:
    # 1. Asegura mayúsculas
    # 2. Crea un diccionario o mapeo de complementariedad
    # 3. Invierte la cadena
    # Tu código aquí:
    pass
""",
            "target_function": "reverso_complementario",
            "test_cases": [
                {
                    "name": "Ejemplo clásico 5'-ATGC-3' -> 5'-GCAT-3'",
                    "args": ("ATGC",),
                    "expected": "GCAT"
                },
                {
                    "name": "Secuencia palindrómica de EcoRI (GAATTC)",
                    "args": ("GAATTC",),
                    "expected": "GAATTC"
                },
                {
                    "name": "Secuencia en minúsculas",
                    "args": ("aaaacccc",),
                    "expected": "GGGGTTTT"
                },
                {
                    "name": "Cadena vacía",
                    "args": ("",),
                    "expected": ""
                }
            ],
            "hints": [
                "Un diccionario de mapeo es muy útil: `comp = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}`.",
                "Para invertir una cadena en Python puedes usar rebanado (slicing) con paso negativo: `cadena[::-1]`."
            ],
            "solution": """def reverso_complementario(secuencia: str) -> str:
    tabla = str.maketrans("ACGTacgt", "TGCAtgca")
    complemento = secuencia.translate(tabla).upper()
    return complemento[::-1]
"""
        },
        {
            "id": "ex_04_02_tm_wallace",
            "title": "Reto 4.2: Calculador de Tm según Wallace",
            "description": """
Crea una función llamada `calcular_tm(primer)` que calcule la temperatura de fusión teórica de un oligonucleótido en grados Celsius ($^\\circ$C) usando la regla de Wallace:
$$T_m = 2 \\times (A + T) + 4 \\times (G + C)$$

**Requisitos**:
1. Debe ignorar si la secuencia viene en mayúsculas o minúsculas.
2. Si el primer está vacío, retornar `0.0`.
3. Retornar el resultado como número decimal `float`.
""",
            "starter_code": """def calcular_tm(primer: str) -> float:
    # Tu código aquí:
    pass
""",
            "target_function": "calcular_tm",
            "test_cases": [
                {
                    "name": "Primer con 2 (A+T) y 2 (G+C)",
                    "args": ("ATGC",),
                    "expected": 12.0
                },
                {
                    "name": "Primer típico de PCR de 20 nt (10 AT, 10 GC)",
                    "args": ("ATATATATATGCGCGCGCGC",),
                    "expected": 60.0
                },
                {
                    "name": "Secuencia vacía",
                    "args": ("",),
                    "expected": 0.0
                }
            ],
            "hints": [
                "Pasa el primer a mayúsculas con `.upper()`.",
                "Calcula `at = seq.count('A') + seq.count('T')` y `gc = seq.count('G') + seq.count('C')`.",
                "Retorna `float(2 * at + 4 * gc)`."
            ],
            "solution": """def calcular_tm(primer: str) -> float:
    seq = primer.upper()
    if not seq:
        return 0.0
    at = seq.count('A') + seq.count('T')
    gc = seq.count('G') + seq.count('C')
    return float(2 * at + 4 * gc)
"""
        },
        {
            "id": "ex_04_03_filter_primers",
            "title": "Reto 4.3: Filtro de Calidad de Primers para PCR",
            "description": """
Crea una función llamada `es_buen_primer(primer, min_len=18, max_len=25, min_gc=40.0, max_gc=60.0)` que evalúe si un cebador cumple los estándares básicos de calidad para una reacción en cadena de la polimerasa (PCR):

**Criterios**:
1. Longitud entre `min_len` y `max_len` (ambos inclusive).
2. Contenido de %GC entre `min_gc` y `max_gc` (ambos inclusive).
3. Debe retornar `True` si cumple ambos criterios y `False` si incumple alguno.
""",
            "starter_code": """def es_buen_primer(
    primer: str,
    min_len: int = 18,
    max_len: int = 25,
    min_gc: float = 40.0,
    max_gc: float = 60.0
) -> bool:
    # Tu código aquí:
    pass
""",
            "target_function": "es_buen_primer",
            "test_cases": [
                {
                    "name": "Primer ideal: 20 nt y 50% GC",
                    "args": ("ATGATGATGACCACCACCAC",),
                    "expected": True
                },
                {
                    "name": "Primer demasiado corto (10 nt)",
                    "args": ("ATGCGATCGG",),
                    "expected": False
                },
                {
                    "name": "Primer con GC excesivo (>60%)",
                    "args": ("GCGCGCGCGCGCGCGCGCGC",),
                    "expected": False
                }
            ],
            "hints": [
                "Calcula la longitud con `len(primer)`.",
                "Calcula el %GC con `((primer.upper().count('G') + primer.upper().count('C')) / len(primer)) * 100`.",
                "Comprueba si `min_len <= longitud <= max_len` y `min_gc <= gc <= max_gc`."
            ],
            "solution": """def es_buen_primer(
    primer: str,
    min_len: int = 18,
    max_len: int = 25,
    min_gc: float = 40.0,
    max_gc: float = 60.0
) -> bool:
    seq = primer.upper()
    n = len(seq)
    if not (min_len <= n <= max_len):
        return False
    gc_count = seq.count('G') + seq.count('C')
    gc_pct = (gc_count / n) * 100.0
    return min_gc <= gc_pct <= max_gc
"""
        }
    ]
}
