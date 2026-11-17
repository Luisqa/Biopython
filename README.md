# 🧬 PyBioLearn: Python desde Cero Aplicado a la Bioinformática

**PyBioLearn** es una plataforma educativa interactiva diseñada para aprender programación en **Python desde cero absoluto**, aplicando cada concepto directamente a problemas, ejercicios, datasets y algoritmos de **Bioinformática y Genómica Computacional**.

La aplicación compagina la enseñanza de la sintaxis estándar de Python con:
- **Biopython Oficial**: Vinculado directamente con el manual `Tutorial-1.83.pdf` incluido en este repositorio.
- **NCBI Entrez E-utilities**: Búsqueda y descarga automatizada de secuencias y registros de GenBank y RefSeq.
- **UniProtKB**: Anotaciones funcionales de proteínas, ontologías y secuencias curadas.
- **EMBL-EBI OLS**: Navegación y búsqueda en Gene Ontology (GO), Disease Ontology (DOID) y Human Phenotype (HP).
- **Auto-Grader Biológico**: Editor interactivo con corrección automática inmediata de ejercicios basada en casos de prueba biológicos.

---

## 🚀 Cómo Iniciar la Aplicación

La aplicación cuenta con su propio entorno virtual preconfigurado. Para iniciarla, simplemente ejecuta:

```bash
./run_app.sh
```

O alternativamente mediante el comando directo:
```bash
./venv/bin/streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador web en `http://localhost:8501`.

---

## 📚 Estructura del Currículo Dual (10 Módulos)

Cada módulo combina **tres pilares pedagógicos**:
1. **🐍 Concepto Python**: Explicación clara y rigurosa de la sintaxis del lenguaje.
2. **🧬 Aplicación Bioinformática**: El motivo biológico por el que este concepto es indispensable en biología molecular y genómica.
3. **🧪 Retos Prácticos con Auto-Corrector**: Retos interactivos con pistas progresivas, evaluación automática inmediata contra casos de prueba reales y solución explicada.

| Módulo | Concepto Python | Aplicación Bioinformática | Retos Prácticos |
|---|---|---|---|
| **Módulo 1** | Variables, Tipos (`str`, `int`, `float`), Operadores | Secuencias de ADN/ARN, %GC, Transcripción y Peso molecular | Calculador %GC, Transcripción génica, Masa molecular |
| **Módulo 2** | Condicionales (`if/elif/else`), Bucles `for`, `range()` | Validación de datos crudos, Codones de inicio (`ATG`) y Sitios de restricción | Validador de ADN, Rastreo de `ATG`, Digestión con EcoRI |
| **Módulo 3** | Listas, Tuplas, Diccionarios (`dict`), Conjuntos (`set`) | El Código Genético Universal, Frecuencia de k-meros y Variantes | Traductor de codones, Conteo de k-meros, Mutaciones compartidas |
| **Módulo 4** | Funciones (`def`), Type Hints, Docstrings, Modularidad | Principio de Antiparalelismo, Hebra reversa complementaria y PCR | Reverso complementario, $T_m$ de Wallace, Filtro de calidad de primers |
| **Módulo 5** | Entrada/Salida (`with open`), Métodos de texto | Parsers manuales de FASTA, Escala Phred FASTQ y Ensamblaje ($N_{50}$) | Parser FASTA multi-línea, Decodificador Phred+33, Métrica $N_{50}$ |
| **Módulo 6** | Programación Orientada a Objetos (POO), Métodos mágicos | Clases de secuencias (`SecuenciaADN`), Detección de Transiciones/Transversiones | Clase `SecuenciaADN`, Clase `VarianteGenetica` |
| **Módulo 7** | Librería `pandas`, DataFrames, `math.log2` | Ventana Deslizante (Sliding Window), Islas CpG y Análisis de RNA-seq | Ventana deslizante de GC, Cálculo de Log2 Fold-Change |
| **Módulo 8** | Ecosistema **Biopython** (`Bio.Seq`, `Bio.SeqRecord`, `Bio.SeqIO`, `Bio.Align`) | Lectura masiva en flujo, Alineamiento por pares Needleman-Wunsch y Modelado 3D | Filtro masivo con SeqIO, Traducción genética, PairwiseAligner |
| **Módulo 9** | Consumo de APIs REST, Formato JSON defensivo | Conexión con **NCBI E-utilities**, **UniProtKB** y **EMBL-EBI OLS** | Extracción JSON UniProt, Filtro semántico de Gene Ontology |
| **Módulo 10** | **Proyecto Final Integrador**: Arquitectura de pipelines | Rastreo de marcos de lectura abiertos (ORFs) y Anotación automatizada | Algoritmo de ORF más largo, Pipeline completo de caracterización |

---

## 🛠️ Herramientas y Exploradores Integrados

Además del curso modular secuencial, la plataforma incluye:

1. **💻 Laboratorio Libre (Sandbox)**:
   - Editor de código interactivo para probar cualquier script de Python con `Bio`, `pandas`, `requests` o `matplotlib` en tiempo real.

2. **🌐 Explorador NCBI Entrez (E-utilities)**:
   - Búsqueda en bases de datos de nucleótidos y proteínas (`esearch`).
   - Descarga de archivos FASTA oficiales (`efetch`).
   - Caché local con secuencias humanas y de SARS-CoV-2 para funcionamiento offline garantizado.

3. **🔬 Explorador UniProtKB**:
   - Búsqueda de proteínas por ID (ej: `P01308` Insulina, `P68871` Hemoglobina beta, `P04637` p53).
   - Ficha técnica completa con longitud, masa molecular, función curada, localización subcelular, términos GO y secuencia primaria.

4. **🌳 Explorador EMBL-EBI OLS (Ontologías)**:
   - Búsqueda de términos biológicos y médicos en **Gene Ontology (GO)**, **Disease Ontology (DOID)** y **Human Phenotype (HP)**.
   - Definiciones formales, sinónimos y relaciones jerárquicas.

5. **📖 Visor del Tutorial Biopython v1.83**:
   - Índice interactivo referenciando los capítulos correspondientes del archivo `Tutorial-1.83.pdf` ubicado en la carpeta raíz.
   - Fragmentos de código extraídos directamente del tutorial listos para ejecutar con un solo clic.

---

## 📁 Estructura del Proyecto

```text
agente python/
├── app.py                      # Aplicación principal Streamlit
├── run_app.sh                  # Script de inicio rápido
├── Tutorial-1.83.pdf           # Manual oficial de Biopython
├── requirements.txt            # Dependencias del proyecto
├── progress.json               # Almacenamiento persistente del progreso del estudiante
├── data/                       # Archivos biológicos reales de ejemplo
│   ├── sample_dna.fasta        # Multi-FASTA (Insulina, Hemoglobina, Spike, GFP)
│   ├── sample_reads.fastq      # FASTQ con calidades Phred+33
│   ├── sample_record.gb        # Registro GenBank anotado completo (HBB)
│   └── expression_counts.tsv   # Matriz de conteos de expresión RNA-seq
├── modules/                    # Currículo de los 10 módulos educativos
│   ├── module_01_basics.py     # Módulo 1: Fundamentos y Secuencias
│   ├── module_02_control.py    # Módulo 2: Control de Flujo y Restricción
│   ├── module_03_structures.py # Módulo 3: Estructuras y Código Genético
│   ├── module_04_functions.py  # Módulo 4: Funciones y Primers
│   ├── module_05_files.py      # Módulo 5: I/O, FASTA, FASTQ y N50
│   ├── module_06_oop.py        # Módulo 6: Programación Orientada a Objetos
│   ├── module_07_data_viz.py   # Módulo 7: Pandas, Ventana Deslizante y RNA-seq
│   ├── module_08_biopython.py  # Módulo 8: Biopython a fondo
│   ├── module_09_databases.py  # Módulo 9: NCBI, UniProt y OLS
│   └── module_10_project.py    # Módulo 10: Pipeline Final Integrador
└── core/                       # Motores y clientes
    ├── runner.py               # Sandbox de ejecución y Auto-Grader con tests unitarios
    ├── progress.py             # Sistema de puntos, niveles y persistencia
    ├── ncbi_client.py          # Cliente NCBI Entrez E-utilities
    ├── uniprot_client.py       # Cliente UniProtKB REST API
    ├── ols_client.py           # Cliente EMBL-EBI OLS API
    └── tutorial_helper.py      # Puente con Tutorial-1.83.pdf
```

---

## 🏆 Sistema de Logros y Progresión

El estudiante acumula **10 puntos** por cada reto resuelto con éxito en el auto-grader:
- 🌱 **Principiante en Python Biológico** (0 - 29 pts)
- 🧬 **Explorador de Secuencias** (30 - 79 pts)
- 🔬 **Analista Bioinformático Junior** (80 - 149 pts)
- 💻 **Desarrollador de Pipelines Ómicos** (150 - 229 pts)
- 🚀 **Maestro en Python Bioinformático** (230+ pts)
