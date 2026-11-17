"""
Módulo 9: Consulta Programática a Bases de Datos (NCBI, UniProt y EMBL-EBI OLS).
Temas: Integración de APIs REST, NCBI E-utilities, UniProtKB y Ontologías Biomédicas (OLS).
"""

from typing import Dict, Any, List

MODULE_INFO = {
    "id": 9,
    "title": "Módulo 9: Consulta Programática a Bases de Datos (NCBI, UniProt y EMBL-EBI OLS)",
    "summary": "Aprende a conectar tus scripts de Python con las mayores bases de datos públicas: NCBI Entrez, UniProtKB y las ontologías de EMBL-EBI (Gene Ontology).",
    "biopython_ref": "Capítulos 8 y 9 del Tutorial-1.83.pdf (Acceso a Entrez, Swiss-Prot y ExPASy)",

    "theory_python": """
### 🐍 Consumo de APIs REST y Estructuras JSON en Python

La mayor parte de los repositorios biomédicos modernos exponen **APIs REST** que devuelven respuestas en formato **JSON** (JavaScript Object Notation), el cual en Python se traduce de forma natural en **diccionarios y listas anidadas**.

#### 1. Realizar Peticiones HTTP con `requests`
```python
import requests

url = "https://rest.uniprot.org/uniprotkb/P01308.json"
response = requests.get(url, timeout=10)

if response.status_code == 200:
    datos = response.json()  # Se convierte en un diccionario de Python
    print("ID de acceso:", datos.get("primaryAccession"))
```

#### 2. Navegación Segura de Diccionarios Anidados
Para evitar excepciones `KeyError` cuando algún campo es opcional en la base de datos:
```python
# Uso encadenado del método .get(clave, valor_por_defecto)
organismo = datos.get("organism", {}).get("scientificName", "Desconocido")
```

#### 3. Políticas de Uso Responsable y Rate Limiting
- **NCBI**: Sin clave de API se permite un máximo de **3 peticiones/segundo**. Con `NCBI_API_KEY` el límite se amplía a **10 peticiones/segundo**.
- **EMBL-EBI**: Máximo **5 peticiones/segundo**.
- Siempre se recomienda introducir pequeñas pausas con `time.sleep(0.35)` o usar los clientes dedicados creados en este curso.
""",

    "theory_bio": """
### 🧬 Aplicación Bioinformática: El Trío de Bases de Datos

#### 1. NCBI (National Center for Biotechnology Information)
- Alberga GenBank, RefSeq, PubMed, dbSNP y BLAST.
- A través de sus herramientas **E-utilities** (`esearch`, `efetch`, `elink`), permite automatizar la recuperación de genomas completos, transcritos y secuencias codificantes (CDS).

#### 2. UniProt (Universal Protein Resource)
- El repositorio central de secuencias y anotaciones funcionales de proteínas.
- La sección **Swiss-Prot** (revisada manualmente) contiene anotaciones curadas por biólogos expertos sobre función catalítica, sitios de unión a fármacos, modificaciones postraduccionales (PTMs) y variantes patogénicas.

#### 3. EMBL-EBI OLS (Ontology Lookup Service)
- Punto de acceso centralizado a más de 250 ontologías biomédicas controladas:
  - **Gene Ontology (GO)**: Describe funciones moleculares (*Molecular Function*), procesos biológicos (*Biological Process*) y componentes celulares (*Cellular Component*).
  - **Disease Ontology (DOID)**: Clasificación jerárquica de patologías humanas.
  - **Human Phenotype Ontology (HPO)**: Anomalías fenotípicas clínicas.
""",

    "exercises": [
        {
            "id": "ex_09_01_parse_uniprot_json",
            "title": "Reto 9.1: Extracción Segura de Metadatos de UniProt",
            "description": """
Crea una función llamada `extraer_metadatos_uniprot(datos_json)` que procese un diccionario devuelto por la API de UniProt y extraiga un resumen estructurado.

**Requisitos**:
1. Debe retornar un diccionario con exactamente las siguientes 4 claves:
   - `'accession'`: cadena con el accession principal (`primaryAccession`).
   - `'organism'`: nombre científico del organismo (`organism -> scientificName`).
   - `'length'`: número entero con la longitud de la secuencia (`sequence -> length`).
   - `'gene'`: nombre del primer gen (`genes[0] -> geneName -> value`), o `'N/A'` si no tiene genes.
2. Usa navegación defensiva con `.get(...)` para que nunca falle con `KeyError`.
""",
            "starter_code": """def extraer_metadatos_uniprot(datos_json: dict) -> dict:
    # Tu código aquí:
    pass
""",
            "target_function": "extraer_metadatos_uniprot",
            "test_cases": [
                {
                    "name": "Estructura típica de UniProtKB (ejemplo Insulina P01308)",
                    "args": ({
                        "primaryAccession": "P01308",
                        "organism": {"scientificName": "Homo sapiens"},
                        "sequence": {"length": 110},
                        "genes": [{"geneName": {"value": "INS"}}]
                    },),
                    "expected": {
                        "accession": "P01308",
                        "organism": "Homo sapiens",
                        "length": 110,
                        "gene": "INS"
                    }
                },
                {
                    "name": "Entrada sin genes definidos",
                    "args": ({
                        "primaryAccession": "P99999",
                        "organism": {"scientificName": "Escherichia coli"},
                        "sequence": {"length": 350},
                        "genes": []
                    },),
                    "expected": {
                        "accession": "P99999",
                        "organism": "Escherichia coli",
                        "length": 350,
                        "gene": "N/A"
                    }
                }
            ],
            "hints": [
                "Extrae el gen comprobando si la lista `genes` contiene al menos un elemento:",
                "`genes_list = datos_json.get('genes', [])`",
                "`gene_name = genes_list[0].get('geneName', {}).get('value', 'N/A') if genes_list else 'N/A'`"
            ],
            "solution": """def extraer_metadatos_uniprot(datos_json: dict) -> dict:
    acc = datos_json.get("primaryAccession", "")
    org = datos_json.get("organism", {}).get("scientificName", "Desconocido")
    length = datos_json.get("sequence", {}).get("length", 0)
    
    genes_list = datos_json.get("genes", [])
    gene_name = "N/A"
    if genes_list and isinstance(genes_list, list):
        first_gene = genes_list[0]
        gene_name = first_gene.get("geneName", {}).get("value", "N/A")
        
    return {
        "accession": acc,
        "organism": org,
        "length": length,
        "gene": gene_name
    }
"""
        },
        {
            "id": "ex_09_02_filter_go_terms",
            "title": "Reto 9.2: Clasificador de Términos de Gene Ontology",
            "description": """
Crea una función llamada `filtrar_terminos_go(terminos_go, tipo_deseado)` que reciba una lista de diccionarios de términos ontológicos y retorne una lista únicamente con los identificadores OBO (`'id'`) de aquellos términos cuyo tipo (`'type'`) coincida exactamente con `tipo_deseado`.

Cada elemento de la lista tiene la estructura:
`{'id': 'GO:0005179', 'name': 'hormone activity', 'type': 'Molecular Function'}`

**Requisitos**:
1. Retorna la lista de strings de IDs coincidentes.
2. Si no hay coincidencias o la lista está vacía, retornar `[]`.
""",
            "starter_code": """def filtrar_terminos_go(terminos_go: list, tipo_deseado: str) -> list:
    # Tu código aquí:
    pass
""",
            "target_function": "filtrar_terminos_go",
            "test_cases": [
                {
                    "name": "Filtrar por 'Biological Process'",
                    "args": ([
                        {"id": "GO:0005179", "name": "hormone activity", "type": "Molecular Function"},
                        {"id": "GO:0006006", "name": "glucose metabolic process", "type": "Biological Process"},
                        {"id": "GO:0008283", "name": "cell proliferation", "type": "Biological Process"}
                    ], "Biological Process"),
                    "expected": ["GO:0006006", "GO:0008283"]
                },
                {
                    "name": "Filtrar por tipo sin coincidencias",
                    "args": ([
                        {"id": "GO:0005179", "name": "hormone activity", "type": "Molecular Function"}
                    ], "Cellular Component"),
                    "expected": []
                }
            ],
            "hints": [
                "Usa una comprensión de lista:",
                "`[t['id'] for t in terminos_go if t.get('type') == tipo_deseado]`"
            ],
            "solution": """def filtrar_terminos_go(terminos_go: list, tipo_deseado: str) -> list:
    return [t["id"] for t in terminos_go if t.get("type") == tipo_deseado]
"""
        }
    ]
}
