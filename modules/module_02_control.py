"""
Módulo 2: Control de Flujo, Filtros y Motivos de Restricción.
Temas: Condicionales (if/elif/else), Bucles (for/while), Operadores lógicos y Enzimas de Restricción.
"""

from typing import Dict, Any, List

MODULE_INFO = {
    "id": 2,
    "title": "Módulo 2: Control de Flujo, Filtros y Motivos de Restricción",
    "summary": "Domina la toma de decisiones con condicionales y la repetición con bucles para escanear secuencias, validar caracteres y simular digestiones enzimáticas.",
    "biopython_ref": "Capítulo 3 y 18 del Tutorial-1.83.pdf (Búsqueda de patrones y motivos en secuencias)",

    "theory_python": """
### 🐍 Control de Flujo en Python

#### 1. Condicionales: `if`, `elif`, `else`
Permiten bifurcar el flujo de ejecución según una condición lógica (evaluada a `True` o `False`):
```python
if len(secuencia) < 20:
    print("La secuencia es demasiado corta para ser un cebador (primer).")
elif len(secuencia) > 30:
    print("La secuencia es demasiado larga.")
else:
    print("Longitud óptima de cebador (entre 20 y 30 pb).")
```

#### 2. Operadores de Pertenencia y Lógicos
- `in` y `not in`: Comprueban si un elemento o subcadena está contenido en otra:
  `'N' in secuencia` devuelve `True` si hay bases ambiguas.
- `and`, `or`, `not`: Combinan expresiones booleanas.

#### 3. Bucles `for` y la función `range()`
Para iterar a lo largo de los elementos de una secuencia o por posiciones numéricas:
```python
# Iteración directa por caracteres
for base in "ATGC":
    print("Base:", base)

# Iteración por índices numéricos con range(inicio, fin, paso)
seq = "ATGCGATCG"
for i in range(0, len(seq), 3):
    triplete = seq[i:i+3]
    print(f"Codón en posición {i}: {triplete}")
```
""",

    "theory_bio": """
### 🧬 Aplicación Bioinformática: Motivos y Enzimas de Restricción

#### 1. Control de Calidad y Validación de Secuencias
Los datos de secuenciación (Sanger o Illumina) pueden contener errores o bases degeneradas (IUPAC):
- Una secuencia de ADN limpia solo debe contener **A**, **C**, **G**, **T**.
- Caracteres como **N** (cualquier base), números o espacios indican datos no limpios o ensamblajes con huecos.

#### 2. Codones de Inicio y Parada
En genética molecular, la maquinaria de traducción del ribosoma busca un codón de inicio:
- **Codón de inicio canónico**: `ATG` (codifica para Metionina en eucariotas y formil-metionina en bacterias).
- **Codones de parada**: `TAA` (ochre), `TAG` (amber), `TGA` (opal).

#### 3. Enzimas de Restricción (Endonucleasas)
Son proteínas bacterianas que cortan el ADN en secuencias palindrómicas específicas (sitios de reconocimiento).
Por ejemplo, **EcoRI** (aislada de *Escherichia coli*):
- Sitio de reconocimiento: `5'-G | A A T T C-3'`
- Corta dejando extremos cohesivos (sticky ends) entre la G y la primera A.
""",

    "exercises": [
        {
            "id": "ex_02_01_sequence_validation",
            "title": "Reto 2.1: Validador de Secuencias de ADN",
            "description": """
Crea una función llamada `validar_adn(secuencia)` que determine si una secuencia es estrictamente ADN válido.

**Requisitos**:
1. La función debe retornar `True` si y solo si todos los caracteres de la secuencia pertenecen al alfabeto `{A, C, G, T}` (en mayúsculas o minúsculas).
2. Si la secuencia contiene cualquier otro carácter (como `'N'`, `'U'`, espacios, números o símbolos), debe retornar `False`.
3. Si la secuencia está vacía, debe retornar `False` (una cadena vacía no es una molécula de ADN válida).
""",
            "starter_code": """def validar_adn(secuencia: str) -> bool:
    # 1. Si está vacía, retornar False
    # 2. Recorrer cada carácter de la secuencia
    # 3. Si algún carácter no es A, C, G o T, retornar False
    # 4. Si termina el bucle sin anomalías, retornar True
    # Tu código aquí:
    pass
""",
            "target_function": "validar_adn",
            "test_cases": [
                {
                    "name": "Secuencia válida normal",
                    "args": ("ATGCGATCGATC",),
                    "expected": True
                },
                {
                    "name": "Secuencia con minúsculas válidas",
                    "args": ("atgcgta",),
                    "expected": True
                },
                {
                    "name": "Secuencia con base ambigua IUPAC (N)",
                    "args": ("ATGCGNATC",),
                    "expected": False
                },
                {
                    "name": "Secuencia de ARN (con Uracilo)",
                    "args": ("AUGCGATC",),
                    "expected": False
                },
                {
                    "name": "Cadena con caracteres no alfabéticos o números",
                    "args": ("ATGC 123",),
                    "expected": False
                },
                {
                    "name": "Cadena vacía",
                    "args": ("",),
                    "expected": False
                }
            ],
            "hints": [
                "Comprueba primero si `not secuencia` para descartar cadenas vacías.",
                "Usa un conjunto o cadena de bases permitidas: `bases_validas = 'ACGT'`.",
                "Convierte la secuencia a mayúsculas con `.upper()` antes de iterar."
            ],
            "solution": """def validar_adn(secuencia: str) -> bool:
    if not secuencia:
        return False
    seq = secuencia.upper()
    bases_validas = {"A", "C", "G", "T"}
    for base in seq:
        if base not in bases_validas:
            return False
    return True
"""
        },
        {
            "id": "ex_02_02_start_codons",
            "title": "Reto 2.2: Rastreo de Codones de Inicio (ATG)",
            "description": """
Crea una función llamada `encontrar_codones_inicio(secuencia)` que busque todos los posibles codones de inicio `'ATG'` a lo largo de una secuencia de ADN.

**Requisitos**:
1. Debe buscar en cualquier posición (independientemente del marco de lectura por ahora).
2. Debe retornar una lista (`list`) con las posiciones numéricas enteras (índices 0-based) donde comienza cada `'ATG'`.
3. Debe ignorar diferencias de mayúsculas/minúsculas.
4. Si no se encuentra ningún `'ATG'`, debe retornar una lista vacía `[]`.
""",
            "starter_code": """def encontrar_codones_inicio(secuencia: str) -> list:
    # Tu código aquí:
    pass
""",
            "target_function": "encontrar_codones_inicio",
            "test_cases": [
                {
                    "name": "Un codón de inicio al principio",
                    "args": ("ATGCCCC",),
                    "expected": [0]
                },
                {
                    "name": "Dos codones en posiciones 0 y 6",
                    "args": ("ATGCCCATGTTT",),
                    "expected": [0, 6]
                },
                {
                    "name": "Secuencia en minúsculas con ATG solapado o continuo",
                    "args": ("ccatgatgcc",),
                    "expected": [2, 5]
                },
                {
                    "name": "Sin codones de inicio",
                    "args": ("CCCCGGGGTTTT",),
                    "expected": []
                }
            ],
            "hints": [
                "Recorre las posiciones con un bucle: `for i in range(len(seq) - 2):`.",
                "Extrae el triplete en cada paso con `triplete = seq[i:i+3]`.",
                "Si `triplete == 'ATG'`, añade `i` a tu lista de resultados con `.append(i)`."
            ],
            "solution": """def encontrar_codones_inicio(secuencia: str) -> list:
    seq = secuencia.upper()
    posiciones = []
    for i in range(len(seq) - 2):
        if seq[i:i+3] == "ATG":
            posiciones.append(i)
    return posiciones
"""
        },
        {
            "id": "ex_02_03_restriction_ecori",
            "title": "Reto 2.3: Digestión Enzimática con EcoRI",
            "description": """
La enzima de restricción **EcoRI** reconoce el motivo `GAATTC` y corta entre la primera `G` y la `A`:
`G | AATTC`.

Crea una función llamada `cortar_con_ecori(secuencia)` que simule la digestión de una molécula lineal de ADN.

**Requisitos**:
1. Convierte la secuencia a mayúsculas.
2. Si la secuencia contiene el sitio de corte `GAATTC`, divídela en los fragmentos resultantes teniendo en cuenta que la `G` queda en el extremo del fragmento izquierdo y `AATTC` en el fragmento derecho.
3. Si el sitio no aparece, retorna una lista con la secuencia completa como único elemento `[secuencia]`.
4. Ejemplo: Para `"CCCGAATTCAAA"`, el corte genera `["CCCG", "AATTCAAA"]`.
""",
            "starter_code": """def cortar_con_ecori(secuencia: str) -> list:
    # Truco: Si reemplazas 'GAATTC' por 'G|AATTC', luego puedes dividir con .split('|')
    # Tu código aquí:
    pass
""",
            "target_function": "cortar_con_ecori",
            "test_cases": [
                {
                    "name": "Un único sitio de corte",
                    "args": ("CCCGAATTCAAA",),
                    "expected": ["CCCG", "AATTCAAA"]
                },
                {
                    "name": "Dos sitios de corte en la misma molécula",
                    "args": ("TTGAATTCCCGAATTCGG",),
                    "expected": ["TTG", "AATTCCCG", "AATTCGG"]
                },
                {
                    "name": "Sin sitios de reconocimiento",
                    "args": ("ATCGATCGATCG",),
                    "expected": ["ATCGATCGATCG"]
                }
            ],
            "hints": [
                "Un truco elegante de Python consiste en usar `seq.replace('GAATTC', 'G|AATTC')`.",
                "Posteriormente aplica `.split('|')` para obtener la lista de fragmentos cortados."
            ],
            "solution": """def cortar_con_ecori(secuencia: str) -> list:
    seq = secuencia.upper()
    corte_simulado = seq.replace("GAATTC", "G|AATTC")
    return corte_simulado.split("|")
"""
        }
    ]
}
