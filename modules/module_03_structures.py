"""
Módulo 3: Estructuras de Datos y el Código Genético.
Temas: Listas, Tuplas, Diccionarios, Conjuntos (sets) y Conteo de k-meros.
"""

from typing import Dict, Any, List

MODULE_INFO = {
    "id": 3,
    "title": "Módulo 3: Estructuras de Datos y el Código Genético",
    "summary": "Mapea el código genético universal usando diccionarios, cuenta frecuencias de k-meros y compara repertorios de variantes mediante conjuntos.",
    "biopython_ref": "Capítulo 3 del Tutorial-1.83.pdf (Sección 3.8: Tablas de traducción genética)",

    "theory_python": """
### 🐍 Estructuras de Datos Fundamentales en Python

#### 1. Listas (`list`)
Colecciones ordenadas y mutables de elementos:
```python
genes = ["BRCA1", "TP53", "EGFR"]
genes.append("KRAS")       # Añade al final
genes.sort()               # Ordena alfabéticamente
primer_gen = genes[0]      # Indexación 0-based
```

#### 2. Diccionarios (`dict`)
Colecciones de pares **clave: valor** con búsqueda ultra rápida $O(1)$:
```python
codigo_genetico = {
    "ATG": "M",  # Metionina
    "TTT": "F",  # Fenilalanina
    "TAA": "*",  # Stop
}
aa = codigo_genetico.get("ATG", "?")  # Retorna 'M'
```

#### 3. Conjuntos (`set`)
Colecciones desordenadas de elementos **únicos** (sin duplicados). Soportan operaciones de teoría de conjuntos:
```python
mutaciones_paciente_A = {"p.V600E", "p.T790M", "p.R175H"}
mutaciones_paciente_B = {"p.V600E", "p.G12D"}

# Intersección (mutaciones compartidas)
comunes = mutaciones_paciente_A & mutaciones_paciente_B  # {'p.V600E'}

# Unión (todas las mutaciones observadas)
todas = mutaciones_paciente_A | mutaciones_paciente_B
```

#### 4. Comprensión de Listas (List Comprehension)
Sintaxis concisa y rápida para transformar listas:
```python
longitudes = [len(seq) for seq in ["ATGC", "A", "GCTAGCTA"]]  # [4, 1, 8]
```
""",

    "theory_bio": """
### 🧬 Aplicación Bioinformática: Traducción y k-meros

#### 1. El Código Genético Estándar
La información genética se organiza en tripletes de nucleótidos denominados **codones**.
- Existen $4^3 = 64$ combinaciones posibles de codones.
- 61 codones especifican alguno de los 20 aminoácidos estándar.
- 3 codones (`TAA`, `TAG`, `TGA`) son señales de terminación (**stop codons**, representados frecuentemente con `*`).
- El código es **degenerado** o redundante: varios codones sinónimos codifican para el mismo aminoácido (por ejemplo, `GCT`, `GCC`, `GCA` y `GCG` codifican todos para Alanina).

#### 2. Conteo de k-meros ($k$-mers)
Un **k-mero** es una subcadena contigua de longitud $k$ contenida en una secuencia biológica:
- Para una secuencia de longitud $L$, existen $L - k + 1$ k-meros posibles.
- **Aplicaciones cruciales**:
  - Ensamblaje de novo de genomas (Grafos de De Bruijn).
  - Clasificación taxonómica metagenómica ultra rápida (ej: Kraken).
  - Estimación del tamaño del genoma y nivel de heterocigosidad.
""",

    "exercises": [
        {
            "id": "ex_03_01_translate_codon",
            "title": "Reto 3.1: Diccionario del Código Genético",
            "description": """
Crea una función llamada `traducir_codon(triplete)` que reciba un triplete de ADN de 3 letras (en mayúsculas o minúsculas) y retorne el aminoácido en formato de código de 1 letra (ej: `'M'` para Metionina, `'*'` para parada).

**Requisitos**:
1. Si el triplete no es válido, tiene longitud distinta de 3 o contiene caracteres desconocidos, retornar `'?'`.
2. Debe contemplar los siguientes codones esenciales:
   - `ATG` -> `'M'`
   - `TAA`, `TAG`, `TGA` -> `'*'`
   - `TTT`, `TTC` -> `'F'`
   - `TTA`, `TTG`, `CTT`, `CTC`, `CTA`, `CTG` -> `'L'`
   - `GCT`, `GCC`, `GCA`, `GCG` -> `'A'`
   - `TGT`, `TGC` -> `'C'`
   - `GAT`, `GAC` -> `'D'`
   - `GAA`, `GAG` -> `'E'`
   - `GGT`, `GGC`, `GGA`, `GGG` -> `'G'`
""",
            "starter_code": """TABLA_GENETICA = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
    'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
}

def traducir_codon(triplete: str) -> str:
    # Tu código aquí:
    pass
""",
            "target_function": "traducir_codon",
            "test_cases": [
                {
                    "name": "Metionina canónica (inicio)",
                    "args": ("ATG",),
                    "expected": "M"
                },
                {
                    "name": "Codón de parada TAA",
                    "args": ("TAA",),
                    "expected": "*"
                },
                {
                    "name": "Codón en minúsculas (gct -> Alanina)",
                    "args": ("gct",),
                    "expected": "A"
                },
                {
                    "name": "Triplete con caracteres inválidos",
                    "args": ("NNN",),
                    "expected": "?"
                },
                {
                    "name": "Longitud incorrecta",
                    "args": ("AT",),
                    "expected": "?"
                }
            ],
            "hints": [
                "Limpia el triplete con `.upper().strip()`.",
                "Usa el método `.get(triplete, '?')` del diccionario `TABLA_GENETICA`."
            ],
            "solution": """TABLA_GENETICA = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
    'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
}

def traducir_codon(triplete: str) -> str:
    if len(triplete) != 3:
        return '?'
    return TABLA_GENETICA.get(triplete.upper(), '?')
"""
        },
        {
            "id": "ex_03_02_kmer_counter",
            "title": "Reto 3.2: Frecuencia de k-meros",
            "description": """
Crea una función llamada `contar_kmeros(secuencia, k)` que reciba una secuencia de ADN y un número entero positivo `k` correspondiente a la longitud de los k-meros.

**Requisitos**:
1. La función debe retornar un diccionario (`dict`) donde las claves sean los k-meros (en mayúsculas) y los valores sean el recuento de apariciones (números enteros).
2. Si la longitud de la secuencia es menor que `k`, retornar un diccionario vacío `{}`.
3. Ejemplo: Para `"ACAC"`, con `k=2`, los 2-meros son `"AC"` (aparece 2 veces) y `"CA"` (aparece 1 vez) -> `{"AC": 2, "CA": 1}`.
""",
            "starter_code": """def contar_kmeros(secuencia: str, k: int) -> dict:
    # Tu código aquí:
    pass
""",
            "target_function": "contar_kmeros",
            "test_cases": [
                {
                    "name": "Secuencia periódica simple con k=2",
                    "args": ("ACAC", 2),
                    "expected": {"AC": 2, "CA": 1}
                },
                {
                    "name": "Conteo de 3-meros (trinucleótidos)",
                    "args": ("ATGATGATG", 3),
                    "expected": {"ATG": 3, "TGA": 2, "GAT": 2}
                },
                {
                    "name": "Secuencia más corta que k",
                    "args": ("AT", 4),
                    "expected": {}
                }
            ],
            "hints": [
                "Usa un bucle `for i in range(len(seq) - k + 1):`.",
                "En cada iteración, el k-mero es `seq[i:i+k]`.",
                "Incrementa el valor en el diccionario con `conteo[kmero] = conteo.get(kmero, 0) + 1`."
            ],
            "solution": """def contar_kmeros(secuencia: str, k: int) -> dict:
    seq = secuencia.upper()
    conteos = {}
    if len(seq) < k or k <= 0:
        return conteos
    for i in range(len(seq) - k + 1):
        kmero = seq[i:i+k]
        conteos[kmero] = conteos.get(kmero, 0) + 1
    return conteos
"""
        },
        {
            "id": "ex_03_03_shared_mutations",
            "title": "Reto 3.3: Mutaciones Compartidas con Conjuntos (Sets)",
            "description": """
Crea una función llamada `mutaciones_comunes(muestra_a, muestra_b)` que reciba dos listas de cadenas representando variantes genéticas (ej: `["BRAF_V600E", "KRAS_G12D"]`) y retorne un conjunto (`set`) con las mutaciones presentes simultáneamente en ambas muestras.

**Requisitos**:
1. Debe retornar un objeto de tipo `set`.
2. Si no comparten ninguna mutación, debe retornar un conjunto vacío `set()`.
""",
            "starter_code": """def mutaciones_comunes(muestra_a: list, muestra_b: list) -> set:
    # Tu código aquí:
    pass
""",
            "target_function": "mutaciones_comunes",
            "test_cases": [
                {
                    "name": "Una mutación compartida",
                    "args": (["BRAF_V600E", "KRAS_G12D"], ["BRAF_V600E", "EGFR_T790M"]),
                    "expected": {"BRAF_V600E"}
                },
                {
                    "name": "Muestras disjuntas (ninguna coincidencia)",
                    "args": (["TP53_R175H"], ["BRCA1_185delAG"]),
                    "expected": set()
                },
                {
                    "name": "Todas compartidas con orden distinto",
                    "args": (["VAR1", "VAR2"], ["VAR2", "VAR1"]),
                    "expected": {"VAR1", "VAR2"}
                }
            ],
            "hints": [
                "Convierte cada lista a un conjunto usando la función constructora `set(lista)`.",
                "Utiliza el operador de intersección `&` entre los dos conjuntos."
            ],
            "solution": """def mutaciones_comunes(muestra_a: list, muestra_b: list) -> set:
    return set(muestra_a) & set(muestra_b)
"""
        }
    ]
}
