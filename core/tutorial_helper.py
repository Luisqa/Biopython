"""
Guía interactiva y vinculación con el manual oficial 'Tutorial-1.83.pdf' de Biopython
ubicado en la raíz del proyecto.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional

PDF_PATH = Path(__file__).resolve().parent.parent / "Tutorial-1.83.pdf"

BIOPYTHON_CHAPTERS = {
    3: {
        "title": "Capítulo 3: Objetos de Secuencia (Bio.Seq)",
        "pages": "Págs. 14 - 28",
        "pdf_ref": "Capítulo 3 del PDF Tutorial-1.83.pdf",
        "summary": "Presenta el objeto central `Seq`, que actúa como una cadena de texto de Python pero con métodos biológicos integrados: `.complement()`, `.reverse_complement()`, `.transcribe()`, y `.translate()`.",
        "key_concepts": [
            "Creación de `Seq('AGTACACTG')`",
            "Indexación y rebanado (slicing) biológico",
            "Transcripción de ADN a ARN y retrotranscripción",
            "Traducción genética y tablas de codones (Standard vs Vertebrate Mitochondrial)",
            "Objetos mutables `MutableSeq`"
        ],
        "code_example": """from Bio.Seq import Seq

# 1. Crear una secuencia de ADN
dna = Seq("AGTACACTGGT")
print("Secuencia original:", dna)

# 2. Complemento y Reverso Complementario
print("Complemento:", dna.complement())
print("Reverso complementario:", dna.reverse_complement())

# 3. Transcripción y Traducción
rna = dna.transcribe()
print("ARN transcrito:", rna)

protein = rna.translate()
print("Proteína traducida:", protein)
"""
    },
    4: {
        "title": "Capítulo 4: Anotación de Secuencias (Bio.SeqRecord)",
        "pages": "Págs. 29 - 42",
        "pdf_ref": "Capítulo 4 del PDF Tutorial-1.83.pdf",
        "summary": "Estructura formal para encapsular una secuencia (`.seq`) junto con metadatos: identificador (`.id`), nombre (`.name`), descripción (`.description`), anotaciones libres (`.annotations`) y características posicionales (`.features` de tipo `SeqFeature`).",
        "key_concepts": [
            "Creación de registros `SeqRecord`",
            "Anotaciones de genes, organismos y fuentes",
            "Características de secuencia (`SeqFeature` y `FeatureLocation`)",
            "Formateo rápido a FASTA o GenBank con `.format('fasta')`"
        ],
        "code_example": """from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# Crear un registro completo con metadatos
record = SeqRecord(
    Seq("MKWVTFISLLFLFSSAYS"),
    id="SP001",
    name="SignalPeptide",
    description="Péptido señal sintético de prueba",
    annotations={"organism": "Homo sapiens"}
)

print(record.description)
print(record.format("fasta"))
"""
    },
    5: {
        "title": "Capítulo 5: Entrada y Salida de Secuencias (Bio.SeqIO)",
        "pages": "Págs. 43 - 75",
        "pdf_ref": "Capítulo 5 del PDF Tutorial-1.83.pdf",
        "summary": "El motor estándar de lectura y escritura de archivos biológicos. Soporta más de 20 formatos con una interfaz unificada: `SeqIO.parse()` para iterar, `SeqIO.read()` para un único registro y `SeqIO.write()` para exportar.",
        "key_concepts": [
            "Lectura perezosa (lazy generator) de archivos gigantes con `SeqIO.parse()`",
            "Lectura de archivos FASTA, FASTQ y GenBank",
            "Indexación en disco (`SeqIO.index()`) sin cargar todo en RAM",
            "Conversión automática de formatos (ej: GenBank a FASTA)"
        ],
        "code_example": """from Bio import SeqIO
import io

# Ejemplo de lectura de secuencias FASTA
fasta_data = \"\"\">seq1 Gen de prueba
ATGCGATCGATCGATCGTAG
>seq2 Otro gen
ATGAAACCCGGGTTTTAA
\"\"\"

for record in SeqIO.parse(io.StringIO(fasta_data), "fasta"):
    print(f"ID: {record.id} | Longitud: {len(record)} bp | GC%: {record.seq.count('G') + record.seq.count('C')}")
"""
    },
    6: {
        "title": "Capítulo 6: Alineamientos Múltiples (Bio.AlignIO y Bio.Align)",
        "pages": "Págs. 76 - 98",
        "pdf_ref": "Capítulo 6 del PDF Tutorial-1.83.pdf",
        "summary": "Manejo de alineamientos de secuencias de pares y múltiples (MSA). Lectura de formatos Clustal, Phylip, FASTA-alignment y cálculo de matrices de sustitución (BLOSUM62, PAM250).",
        "key_concepts": [
            "Alineador de pares `PairwiseAligner`",
            "Configuración de penalizaciones por gaps y matches",
            "Lectura y escritura con `AlignIO`",
            "Cálculo de secuencias consenso"
        ],
        "code_example": """from Bio.Align import PairwiseAligner

# Crear un alineador de secuencias de pares
aligner = PairwiseAligner()
aligner.mode = 'global'
aligner.match_score = 2
aligner.mismatch_score = -1
aligner.open_gap_score = -2
aligner.extend_gap_score = -0.5

seq1 = "ATCGTTAGC"
seq2 = "ATGTTGC"

score = aligner.score(seq1, seq2)
print("Puntuación del alineamiento:", score)
for alignment in aligner.align(seq1, seq2):
    print(alignment)
    break
"""
    },
    8: {
        "title": "Capítulo 8: Acceso a Entrez / NCBI (Bio.Entrez)",
        "pages": "Págs. 115 - 145",
        "pdf_ref": "Capítulo 8 del PDF Tutorial-1.83.pdf",
        "summary": "Conexión directa con los servidores de NCBI para automatizar búsquedas en PubMed, GenBank, Nucleotide y Protein mediante las herramientas E-utilities.",
        "key_concepts": [
            "Configuración de `Entrez.email` y `Entrez.api_key`",
            "`Entrez.esearch`: Búsquedas avanzadas por términos",
            "`Entrez.efetch`: Descarga masiva de registros en XML, FASTA o GenBank",
            "Integración fluida con `SeqIO`"
        ],
        "code_example": """from Bio import Entrez, SeqIO

# Siempre se debe especificar un correo de contacto
Entrez.email = "usuario@ejemplo.com"

# Buscar un gen en la base de datos de nucleótidos
# handle = Entrez.esearch(db="nucleotide", term="Homo sapiens HBB[Gene]", retmax=3)
# record = Entrez.read(handle)
# print("IDs encontrados:", record["IdList"])
"""
    },
    11: {
        "title": "Capítulo 11: Estructuras 3D Macromoleculares (Bio.PDB)",
        "pages": "Págs. 165 - 195",
        "pdf_ref": "Capítulo 11 del PDF Tutorial-1.83.pdf",
        "summary": "Exploración de la jerarquía estructural macromolecular SMCRA (Structure -> Model -> Chain -> Residue -> Atom) para archivos PDB y mmCIF.",
        "key_concepts": [
            "El modelo jerárquico SMCRA",
            "Lectura con `PDBParser` y `MMCIFParser`",
            "Iteración sobre cadenas de proteínas y aminoácidos",
            "Cálculo de distancias euclidianas entre átomos alfa-carbono (CA)"
        ],
        "code_example": """from Bio.PDB import PDBParser

# La jerarquía SMCRA permite acceder con precisión:
# structure = parser.get_structure("1A8O", "1A8O.pdb")
# for model in structure:
#     for chain in model:
#         for residue in chain:
#             if residue.has_id("CA"):
#                 ca_atom = residue["CA"]
#                 print(residue.resname, ca_atom.coord)
"""
    }
}


def get_available_chapters() -> List[int]:
    """Retorna los números de capítulo con guía integrada."""
    return sorted(list(BIOPYTHON_CHAPTERS.keys()))


def get_chapter_info(chapter_num: int) -> Optional[Dict[str, Any]]:
    """Retorna los datos y snippets de un capítulo del tutorial."""
    return BIOPYTHON_CHAPTERS.get(chapter_num)


def get_pdf_status() -> Dict[str, Any]:
    """Verifica la existencia del archivo PDF en la carpeta."""
    exists = PDF_PATH.exists()
    size_mb = round(PDF_PATH.stat().st_size / (1024 * 1024), 2) if exists else 0
    return {
        "exists": exists,
        "filename": PDF_PATH.name,
        "path": str(PDF_PATH),
        "size_mb": size_mb
    }
