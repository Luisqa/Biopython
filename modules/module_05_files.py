"""
Módulo 5: Entrada/Salida de Archivos y Formatos Bioinformáticos.
Temas: Manejo de archivos (with open), Parseo de FASTA manual, FASTQ Phred scores y Métrica N50.
"""

from typing import Dict, Any, List

MODULE_INFO = {
    "id": 5,
    "title": "Módulo 5: Entrada/Salida de Archivos y Formatos Bioinformáticos",
    "summary": "Construye tu propio parser manual para archivos FASTA, descifra las puntuaciones de calidad Phred de archivos FASTQ y calcula el N50 de un ensamblaje.",
    "biopython_ref": "Capítulo 5 del Tutorial-1.83.pdf (Sección 5.1: Lectura de archivos con SeqIO)",

    "theory_python": """
### 🐍 Manejo de Archivos en Python

#### 1. La Sentencia `with open(...)`
La forma canónica y segura de abrir archivos en Python garantiza que el archivo se cierre automáticamente incluso si ocurre una excepción:
```python
with open("datos.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        linea_limpia = linea.strip()  # Elimina saltos de línea \n
        print(linea_limpia)
```

#### 2. Lectura y Escritura
- Modos: `'r'` (lectura), `'w'` (escritura destructiva), `'a'` (añadir al final).
- Métodos útiles:
  - `archivo.read()`: Lee todo el contenido como un único string.
  - `archivo.readlines()`: Lee todas las líneas en una lista.
  - `cadena.startswith(">")`: Comprueba si la línea inicia con un carácter específico (clave para cabeceras FASTA).
  - `ord(caracter)`: Devuelve el código numérico ASCII/Unicode de un carácter (ej: `ord('!') -> 33`, `ord('I') -> 73`).
""",

    "theory_bio": """
### 🧬 Aplicación Bioinformática: Estándares FASTA, FASTQ y Métrica N50

#### 1. Formato FASTA
El formato de secuencia más extendido de la historia:
```text
>NM_000518.5 Homo sapiens hemoglobin subunit beta (HBB)
ACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACCATGGTGCATC
TGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAG
```
- Línea de encabezado: Comienza obligatoriamente con `>` seguido del ID y descripción opcional.
- Líneas siguientes: La secuencia de nucleótidos o aminoácidos, que con frecuencia está dividida en múltiples líneas de 60 a 80 caracteres. Un buen parser debe **concatenar** estas líneas en una única cadena contigua.

#### 2. Formato FASTQ y Escala Phred (Q-score)
Estándar para lecturas de secuenciación de segunda generación (Illumina):
Cada lectura consta de exactamente 4 líneas:
1. `@ID_LECTURA` (Cabecera)
2. `Secuencia de bases` (ej: `ATGC...`)
3. `+` (Separador)
4. `Cadena de caracteres ASCII` que codifican la calidad Phred ($Q$).
- **Fórmula de codificación Phred+33**:
  $$Q = \\text{ord}(\\text{caracter}) - 33$$
  - `Q = 10` $\\implies$ Probabilidad de error $P = 10^{-1} = 10\\%$ (Precisión 90%)
  - `Q = 20` $\\implies$ Probabilidad de error $P = 10^{-2} = 1\\%$ (Precisión 99%)
  - `Q = 30` $\\implies$ Probabilidad de error $P = 10^{-3} = 0.1\\%$ (Precisión 99.9%, estándar de calidad clínica)

#### 3. La Métrica de Ensamblaje $N_{50}$
Es una medida estadística fundamental de la continuidad de un ensamblaje genómico:
- Se ordenan todos los cóntigos o secuencias de mayor a menor longitud.
- El $N_{50}$ es la longitud del cóntigo más pequeño dentro del conjunto de cóntigos más grandes cuya suma acumulada representa al menos el **50% del tamaño total del ensamblaje**.
""",

    "exercises": [
        {
            "id": "ex_05_01_fasta_parser",
            "title": "Reto 5.1: Parser de FASTA Multi-línea desde Cero",
            "description": """
Crea una función llamada `parsear_fasta(texto_fasta)` que reciba un string con contenido en formato FASTA (pudiendo tener una o varias secuencias, y secuencias divididas en múltiples líneas) y devuelva un diccionario `{id_secuencia: secuencia_completa}`.

**Requisitos**:
1. El identificador debe ser la primera palabra inmediatamente después del `>` (sin incluir el `>` y sin la descripción posterior).
2. La secuencia debe estar en letras mayúsculas y sin espacios ni saltos de línea.
3. Si el texto está vacío o no contiene secuencias válidas, retornar `{}`.
""",
            "starter_code": """def parsear_fasta(texto_fasta: str) -> dict:
    # Tu código aquí:
    pass
""",
            "target_function": "parsear_fasta",
            "test_cases": [
                {
                    "name": "FASTA simple de un registro",
                    "args": (">seq1 Gen de prueba\nATGC\nGGCC\n",),
                    "expected": {"seq1": "ATGCGGCC"}
                },
                {
                    "name": "Multi-FASTA de dos registros con saltos múltiples",
                    "args": (">idA Primera\nAAA\nTTT\n>idB Segunda\nCCC\nGGG\n",),
                    "expected": {"idA": "AAATTT", "idB": "CCCGGG"}
                },
                {
                    "name": "Texto vacío",
                    "args": ("",),
                    "expected": {}
                }
            ],
            "hints": [
                "Divide el texto en líneas usando `.splitlines()`.",
                "Mantén variables `current_id = None` y `current_seq = []`.",
                "Cuando encuentres una línea que empiece con `>`: guarda la secuencia acumulada anterior y extrae el nuevo ID con `linea[1:].split()[0]`."
            ],
            "solution": """def parsear_fasta(texto_fasta: str) -> dict:
    resultado = {}
    current_id = None
    current_seq_parts = []
    
    for line in texto_fasta.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if current_id is not None:
                resultado[current_id] = "".join(current_seq_parts).upper()
            header_parts = line[1:].strip().split()
            current_id = header_parts[0] if header_parts else ""
            current_seq_parts = []
        else:
            current_seq_parts.append(line)
            
    if current_id is not None:
        resultado[current_id] = "".join(current_seq_parts).upper()
        
    return resultado
"""
        },
        {
            "id": "ex_05_02_phred_scores",
            "title": "Reto 5.2: Decodificador de Calidad Phred+33",
            "description": """
Crea una función llamada `decodificar_phred(cadena_ascii)` que reciba la 4ª línea de una lectura FASTQ (la cadena de caracteres ASCII de calidad) y retorne una lista de números enteros con las puntuaciones de calidad $Q = \\text{ord}(c) - 33$.

**Requisitos**:
1. Por cada carácter `c`, calcula su valor Phred restando 33 a su código ordinal con `ord(c) - 33`.
2. Retorna la lista resultante de enteros.
3. Si la cadena está vacía, retorna `[]`.
""",
            "starter_code": """def decodificar_phred(cadena_ascii: str) -> list:
    # Tu código aquí:
    pass
""",
            "target_function": "decodificar_phred",
            "test_cases": [
                {
                    "name": "Caracteres estándar: '!' es 0, 'I' es 40",
                    "args": ("!I",),
                    "expected": [0, 40]
                },
                {
                    "name": "Lectura típica de alta calidad 'IIII'",
                    "args": ("IIII",),
                    "expected": [40, 40, 40, 40]
                },
                {
                    "name": "Lectura mixta '?@AB'",
                    "args": ("?@AB",),
                    "expected": [30, 31, 32, 33]
                },
                {
                    "name": "Cadena vacía",
                    "args": ("",),
                    "expected": []
                }
            ],
            "hints": [
                "Usa una comprensión de lista: `[ord(c) - 33 for c in cadena_ascii]`."
            ],
            "solution": """def decodificar_phred(cadena_ascii: str) -> list:
    return [ord(c) - 33 for c in cadena_ascii]
"""
        },
        {
            "id": "ex_05_03_n50_metric",
            "title": "Reto 5.3: Cálculo del N50 de un Ensamblaje",
            "description": """
Crea una función llamada `calcular_n50(longitudes)` que reciba una lista de números enteros representando las longitudes de los cóntigos de un ensamblaje y devuelva el valor del estadístico $N_{50}$ (entero `int`).

**Algoritmo**:
1. Si la lista está vacía, retornar `0`.
2. Calcula la suma total de todas las longitudes ($L_{total}$).
3. El umbral del 50% es $L_{total} / 2$.
4. Ordena las longitudes en orden **descendente** (de mayor a menor).
5. Acumula las longitudes sumándolas una a una. En cuanto la suma acumulada sea mayor o igual que el umbral del 50%, la longitud del cóntigo actual es el $N_{50}$.
""",
            "starter_code": """def calcular_n50(longitudes: list) -> int:
    # Tu código aquí:
    pass
""",
            "target_function": "calcular_n50",
            "test_cases": [
                {
                    "name": "Ejemplo clásico [2, 3, 4, 5, 6, 10] (Suma=30, 50%=15 -> N50=6)",
                    "args": ([2, 3, 4, 5, 6, 10],),
                    "expected": 6
                },
                {
                    "name": "Un único cóntigo [1000]",
                    "args": ([1000],),
                    "expected": 1000
                },
                {
                    "name": "Lista vacía",
                    "args": ([],),
                    "expected": 0
                }
            ],
            "hints": [
                "Ordena de mayor a menor con `sorted(longitudes, reverse=True)`.",
                "Calcula `mitad = sum(longitudes) / 2`.",
                "Recorre la lista ordenada acumulando `acumulado += lon`. Cuando `acumulado >= mitad`, retorna `lon`."
            ],
            "solution": """def calcular_n50(longitudes: list) -> int:
    if not longitudes:
        return 0
    total = sum(longitudes)
    mitad = total / 2.0
    ordenados = sorted(longitudes, reverse=True)
    acumulado = 0
    for lon in ordenados:
        acumulado += lon
        if acumulado >= mitad:
            return lon
    return ordenados[-1]
"""
        }
    ]
}
