"""
Módulo 8: El Ecosistema Biopython (Tutorial Oficial v1.83).
Temas: Bio.Seq, Bio.SeqRecord, Bio.SeqIO, Bio.Align (PairwiseAligner) y Estructuras 3D con Bio.PDB.
"""

from typing import Dict, Any, List

MODULE_INFO = {
    "id": 8,
    "title": "Módulo 8: El Ecosistema Biopython (Tutorial Oficial v1.83)",
    "summary": "Domina la librería estándar de bioinformática en Python: manipula objetos Seq, lee y filtra colecciones con SeqIO y realiza alineamientos con Bio.Align.",
    "biopython_ref": "Capítulos 3, 4, 5 y 6 del PDF Tutorial-1.83.pdf incluido en la carpeta",

    "theory_python": """
### 🐍 Biopython: La Biblioteca de Referencia

Biopython proporciona herramientas estándar de código abierto para biología computacional.

#### 1. El Objeto `Bio.Seq.Seq`
A diferencia de un string convencional, `Seq` entiende la semántica biológica:
```python
from Bio.Seq import Seq

adn = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")

# Transcripción a ARN
arn = adn.transcribe()

# Traducción a proteína usando la tabla estándar
proteina = adn.translate()                 # 'MAIVMGR*KGAR*'
proteina_hasta_stop = adn.translate(to_stop=True)  # 'MAIVMGR'
```

#### 2. Lectura Masiva y Filtrado con `Bio.SeqIO`
`SeqIO.parse()` devuelve un generador perezoso (iterator) que procesa archivos gigantes registro a registro sin colapsar la memoria RAM:
```python
from Bio import SeqIO
import io

fasta_texto = ">seq1\\nATGC\\n>seq2\\nGCGCGC\\n"
registros = list(SeqIO.parse(io.StringIO(fasta_texto), "fasta"))
print(f"Total registros leídos: {len(registros)}")
```

#### 3. Alineamiento Global y Local con `Bio.Align`
```python
from Bio.Align import PairwiseAligner

alineador = PairwiseAligner()
alineador.mode = "global"  # Algoritmo Needleman-Wunsch
puntuacion = alineador.score("ATCGTTAGC", "ATGTTGC")
```
""",

    "theory_bio": """
### 🧬 Aplicación Bioinformática: Biopython en el Laboratorio

#### 1. Del Manual Tutorial-1.83.pdf a la Práctica
En el documento `Tutorial-1.83.pdf` que acompaña este curso:
- **Capítulo 3**: Explica la transición del manejo de cadenas puras en Python a objetos biológicos tipados.
- **Capítulo 4**: Introduce `SeqRecord`, la estructura que unifica identificador, secuencia, taxonomía y anotaciones genómicas (coordenadas de exones, CDS, variantes).
- **Capítulo 5**: Detalla cómo transformar formatos de archivo en un solo comando:
  `SeqIO.convert("datos.gb", "genbank", "datos.fasta", "fasta")`.
- **Capítulo 6**: Implementa algoritmos de programación dinámica para alineamiento de secuencias homólogas.
- **Capítulo 11**: Explica la jerarquía **SMCRA** (*Structure*, *Model*, *Chain*, *Residue*, *Atom*) para diseccionar macromoléculas cristalográficas o predichas por AlphaFold en archivos `.pdb` y `.cif`.
""",

    "exercises": [
        {
            "id": "ex_08_01_seqio_filtering",
            "title": "Reto 8.1: Parseo y Filtrado de FASTA con Bio.SeqIO",
            "description": """
Crea una función llamada `filtrar_fasta_biopython(fasta_texto, min_len)` que utilice `Bio.SeqIO` y `io.StringIO` para leer un texto FASTA y retorne una lista con los identificadores (`record.id`) de aquellas secuencias cuya longitud sea mayor o igual a `min_len`.

**Requisitos**:
1. Utiliza `from Bio import SeqIO` e `import io`.
2. Lee los registros con `SeqIO.parse(io.StringIO(fasta_texto), "fasta")`.
3. Retorna la lista de IDs que cumplan `len(record) >= min_len`.
4. Si ninguna secuencia cumple el criterio o el texto está vacío, retornar `[]`.
""",
            "starter_code": """from Bio import SeqIO
import io

def filtrar_fasta_biopython(fasta_texto: str, min_len: int) -> list:
    # Tu código aquí:
    pass
""",
            "target_function": "filtrar_fasta_biopython",
            "test_cases": [
                {
                    "name": "Filtrado con umbral de 6 pb",
                    "args": (">seq1 Corta\nATGC\n>seq2 Larga\nATGCATGC\n>seq3 Exacta\nGCATGC\n", 6),
                    "expected": ["seq2", "seq3"]
                },
                {
                    "name": "Umbral muy alto (ninguna pasa)",
                    "args": (">seq1\nATGC\n", 50),
                    "expected": []
                },
                {
                    "name": "Texto FASTA vacío",
                    "args": ("", 10),
                    "expected": []
                }
            ],
            "hints": [
                "Usa `io.StringIO(fasta_texto)` para convertir el string en un flujo legible por SeqIO.",
                "Recorre cada `record` en `SeqIO.parse(stream, 'fasta')` y comprueba `len(record.seq) >= min_len`."
            ],
            "solution": """from Bio import SeqIO
import io

def filtrar_fasta_biopython(fasta_texto: str, min_len: int) -> list:
    ids_validos = []
    stream = io.StringIO(fasta_texto)
    for record in SeqIO.parse(stream, "fasta"):
        if len(record.seq) >= min_len:
            ids_validos.append(record.id)
    return ids_validos
"""
        },
        {
            "id": "ex_08_02_biopython_translation",
            "title": "Reto 8.2: Traducción con Bio.Seq y Parada Prematura",
            "description": """
Crea una función llamada `traducir_biopython(adn_str, to_stop=True)` que utilice la clase `Bio.Seq.Seq` para traducir una secuencia codificante de ADN a proteína.

**Requisitos**:
1. Instancia un objeto `Seq(adn_str.upper())`.
2. Traduce la secuencia llamando a `.translate(to_stop=to_stop)`.
3. Convierte el resultado a un string nativo de Python con `str(...)` antes de retornarlo.
4. Si `to_stop=True`, la traducción se detiene al alcanzar el primer codón de parada. Si es `False`, incluye el asterisco `*`.
""",
            "starter_code": """from Bio.Seq import Seq

def traducir_biopython(adn_str: str, to_stop: bool = True) -> str:
    # Tu código aquí:
    pass
""",
            "target_function": "traducir_biopython",
            "test_cases": [
                {
                    "name": "Traducción deteniéndose en codón de parada TAA (to_stop=True)",
                    "args": ("ATGGCCATTTAACCC", True),
                    "expected": "MAI"
                },
                {
                    "name": "Traducción completa con asterisco (to_stop=False)",
                    "args": ("ATGGCCATTTAACCC", False),
                    "expected": "MAI*P"
                }
            ],
            "hints": [
                "Crea el objeto: `seq_obj = Seq(adn_str.upper())`.",
                "Llama a `seq_obj.translate(to_stop=to_stop)`.",
                "Retorna `str(...)`."
            ],
            "solution": """from Bio.Seq import Seq

def traducir_biopython(adn_str: str, to_stop: bool = True) -> str:
    seq_obj = Seq(adn_str.upper())
    prot = seq_obj.translate(to_stop=to_stop)
    return str(prot)
"""
        },
        {
            "id": "ex_08_03_pairwise_aligner",
            "title": "Reto 8.3: Puntuación de Alineamiento con Bio.Align",
            "description": """
Crea una función llamada `puntuar_alineamiento_global(seq1, seq2)` que utilice `Bio.Align.PairwiseAligner` para calcular la puntuación óptima de alineamiento global (Needleman-Wunsch).

**Configuración requerida**:
1. Modo: `global`
2. `match_score = 1.0`
3. `mismatch_score = -1.0`
4. `open_gap_score = -2.0`
5. `extend_gap_score = -0.5`
6. Retornar la puntuación óptima como `float` redondeado a 2 decimales.
""",
            "starter_code": """from Bio.Align import PairwiseAligner

def puntuar_alineamiento_global(seq1: str, seq2: str) -> float:
    # Tu código aquí:
    pass
""",
            "target_function": "puntuar_alineamiento_global",
            "test_cases": [
                {
                    "name": "Secuencias idénticas (4 matches x 1.0 = 4.0)",
                    "args": ("ATGC", "ATGC"),
                    "expected": 4.0
                },
                {
                    "name": "Un mismatch (3 matches x 1.0 + 1 mismatch x -1.0 = 2.0)",
                    "args": ("ATGC", "ATTC"),
                    "expected": 2.0
                }
            ],
            "hints": [
                "Instancia `aligner = PairwiseAligner()`.",
                "Configura sus atributos `.mode`, `.match_score`, `.mismatch_score`, `.open_gap_score`, `.extend_gap_score`.",
                "Calcula el score con `aligner.score(seq1.upper(), seq2.upper())`."
            ],
            "solution": """from Bio.Align import PairwiseAligner

def puntuar_alineamiento_global(seq1: str, seq2: str) -> float:
    aligner = PairwiseAligner()
    aligner.mode = "global"
    aligner.match_score = 1.0
    aligner.mismatch_score = -1.0
    aligner.open_gap_score = -2.0
    aligner.extend_gap_score = -0.5
    score = aligner.score(seq1.upper(), seq2.upper())
    return round(float(score), 2)
"""
        }
    ]
}
