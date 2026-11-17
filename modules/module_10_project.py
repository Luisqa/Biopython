"""
Módulo 10: Proyecto Final Integrador - Pipeline de Anotación y Análisis Ómico.
Temas: Integración completa de algoritmos bioinformáticos, búsqueda de ORFs y generación de pipelines.
"""

from typing import Dict, Any, List

MODULE_INFO = {
    "id": 10,
    "title": "Módulo 10: Proyecto Final Integrador - Pipeline de Anotación",
    "summary": "Integra todo lo aprendido en un pipeline automatizado completo: desde la validación de secuencias crudas y búsqueda de ORFs hasta la traducción y reporte de calidad.",
    "biopython_ref": "Capítulo 18 del Tutorial-1.83.pdf (Cookbook y pipelines avanzados)",

    "theory_python": """
### 🐍 Construcción de Pipelines y Flujos de Trabajo en Python

Un **pipeline bioinformático** es una secuencia encadenada de etapas computacionales donde la salida procesada de una fase sirve como entrada para la siguiente.

#### Buenas Prácticas en el Diseño de Pipelines:
1. **Funciones Modulares y Especializadas**: Cada función debe resolver una única tarea (Principio de Responsabilidad Única).
2. **Estructuras de Retorno Estandarizadas**: Usar diccionarios, tuplas con nombre o clases para transportar resultados entre etapas.
3. **Manejo Defensivo de Errores**: Validar los datos de entrada antes de ejecutar etapas costosas (como traducciones o llamadas de red).
4. **Reproducibilidad y Logs**: Registrar parámetros, versiones y métricas de calidad en cada paso.
""",

    "theory_bio": r"""
### 🧬 Aplicación Bioinformática: Búsqueda de Marcos de Lectura Abiertos (ORFs)

#### 1. ¿Qué es un Marco de Lectura Abierto (ORF)?
Un **Open Reading Frame (ORF)** es una porción contigua de una secuencia de nucleótidos que:
1. Comienza con un **codón de inicio** (típicamente `ATG`).
2. Continúa con una serie de codones de 3 nucleótidos consecutivos sin interrupciones.
3. Finaliza con un **codón de parada** en fase (`TAA`, `TAG` o `TGA`).
- En ADN bicatenario existen **6 marcos de lectura posibles**: 3 en la hebra directa ($+1, +2, +3$) y 3 en la hebra reversa complementaria ($-1, -2, -3$).
- En bacterias y virus, los ORFs mayores a 100 codones ($\ge 300$ pb) tienen una probabilidad altísima de codificar proteínas funcionales reales.
""",

    "exercises": [
        {
            "id": "ex_10_01_longest_orf",
            "title": "Reto 10.1: Rastreador del ORF Más Largo (Hebra Directa)",
            "description": """
Crea una función llamada `encontrar_orf_mas_largo(secuencia_adn)` que busque todos los ORFs válidos en los 3 marcos de lectura hacia adelante (frames 0, 1 y 2) y devuelva la secuencia de nucleótidos del **ORF más largo** (incluyendo el codón de inicio `ATG` y el codón de parada).

**Reglas de un ORF**:
- Inicia estrictamente con `ATG`.
- Los codones avanzan de 3 en 3 nucleótidos en el mismo marco.
- Termina en el primer codón de parada en fase (`TAA`, `TAG` o `TGA`).
- Si hay varios ORFs, retorna el que tenga mayor longitud en nucleótidos.
- Si no se encuentra ningún ORF cerrado completo, retornar una cadena vacía `""`.
""",
            "starter_code": """def encontrar_orf_mas_largo(secuencia_adn: str) -> str:
    # Tu código aquí:
    pass
""",
            "target_function": "encontrar_orf_mas_largo",
            "test_cases": [
                {
                    "name": "Secuencia con un único ORF de 12 pb (ATGAAACCCTAA)",
                    "args": ("CCATGAAACCCTAAGG",),
                    "expected": "ATGAAACCCTAA"
                },
                {
                    "name": "Dos ORFs: uno corto (9 pb) y uno largo (15 pb)",
                    "args": ("ATGTTTTAACCCATGAAAGGGCCCTGA",),
                    "expected": "ATGAAAGGGCCCTGA"
                },
                {
                    "name": "Sin codón de parada en fase",
                    "args": ("ATGAAACCCGGG",),
                    "expected": ""
                },
                {
                    "name": "Secuencia vacía",
                    "args": ("",),
                    "expected": ""
                }
            ],
            "hints": [
                "Para cada marco `frame` en `[0, 1, 2]`:",
                "Recorre en pasos de 3: `for i in range(frame, len(seq) - 2, 3):`.",
                "Si encuentras `'ATG'` y no estabas dentro de un ORF, marca el inicio. Luego continúa buscando codones de parada `{'TAA', 'TAG', 'TGA'}`.",
                "Cuando encuentres un codón de parada, extrae `seq[inicio : fin+3]` y compáralo con el más largo registrado."
            ],
            "solution": """def encontrar_orf_mas_largo(secuencia_adn: str) -> str:
    seq = secuencia_adn.upper()
    paradas = {"TAA", "TAG", "TGA"}
    mejor_orf = ""
    
    for frame in range(3):
        i = frame
        while i < len(seq) - 2:
            codon = seq[i:i+3]
            if codon == "ATG":
                # Encontrado codón de inicio, buscar la parada en este marco
                inicio = i
                j = i + 3
                while j < len(seq) - 2:
                    c_stop = seq[j:j+3]
                    if c_stop in paradas:
                        orf = seq[inicio:j+3]
                        if len(orf) > len(mejor_orf):
                            mejor_orf = orf
                        break
                    j += 3
                # Continuar buscando después de este inicio
                i += 3
            else:
                i += 3
                
    return mejor_orf
"""
        },
        {
            "id": "ex_10_02_full_pipeline",
            "title": "Reto 10.2: Pipeline Completo de Anotación de Secuencia",
            "description": """
Crea una función integradora llamada `pipeline_anotacion(secuencia_adn)` que ejecute el pipeline completo de análisis.

**Flujo del Pipeline**:
1. Estandariza la secuencia a mayúsculas.
2. Si la secuencia está vacía o contiene caracteres distintos de `A, C, G, T`, retorna:
   `{"valida": False, "error": "Secuencia no válida o vacía"}`
3. Si es válida:
   - Calcula la longitud total de la molécula (`"longitud"`: `int`).
   - Calcula el %GC de la molécula (`"gc_pct"`: `float` a 2 decimales).
   - Localiza el ORF más largo con la lógica del ejercicio 10.1 (`"orf_adn"`: `str`).
   - Si se encontró un ORF, tradúcelo a proteína (sin incluir el asterisco de parada) usando `Bio.Seq.Seq(orf).translate(to_stop=True)` o tu propio diccionario genético (`"proteina"`: `str`). Si no hubo ORF, `"proteina"` debe ser `""`.
   - Retorna el diccionario con las claves:
     `{"valida": True, "longitud": ..., "gc_pct": ..., "orf_adn": ..., "proteina": ...}`
""",
            "starter_code": """from Bio.Seq import Seq

def pipeline_anotacion(secuencia_adn: str) -> dict:
    # Tu código aquí:
    pass
""",
            "target_function": "pipeline_anotacion",
            "test_cases": [
                {
                    "name": "Secuencia válida con ORF funcional",
                    "args": ("CCATGAAACCCTAAGG",),
                    "expected": {
                        "valida": True,
                        "longitud": 16,
                        "gc_pct": 50.0,
                        "orf_adn": "ATGAAACCCTAA",
                        "proteina": "MKP"
                    }
                },
                {
                    "name": "Secuencia con bases no válidas",
                    "args": ("ATGNNNTAA",),
                    "expected": {
                        "valida": False,
                        "error": "Secuencia no válida o vacía"
                    }
                }
            ],
            "hints": [
                "Valida primero con `set(seq) <= {'A', 'C', 'G', 'T'}` y `len(seq) > 0`.",
                "Reutiliza la lógica de ORF para obtener el fragmento codificante.",
                "Traduce con `str(Seq(orf_adn).translate(to_stop=True))`."
            ],
            "solution": """from Bio.Seq import Seq

def pipeline_anotacion(secuencia_adn: str) -> dict:
    seq = secuencia_adn.strip().upper()
    if not seq or not set(seq).issubset({"A", "C", "G", "T"}):
        return {"valida": False, "error": "Secuencia no válida o vacía"}
        
    n = len(seq)
    g = seq.count("G")
    c = seq.count("C")
    gc_pct = round(((g + c) / n) * 100.0, 2)
    
    # Búsqueda de ORF más largo
    paradas = {"TAA", "TAG", "TGA"}
    mejor_orf = ""
    for frame in range(3):
        i = frame
        while i < n - 2:
            if seq[i:i+3] == "ATG":
                inicio = i
                j = i + 3
                while j < n - 2:
                    if seq[j:j+3] in paradas:
                        orf = seq[inicio:j+3]
                        if len(orf) > len(mejor_orf):
                            mejor_orf = orf
                        break
                    j += 3
                i += 3
            else:
                i += 3
                
    proteina = ""
    if mejor_orf:
        proteina = str(Seq(mejor_orf).translate(to_stop=True))
        
    return {
        "valida": True,
        "longitud": n,
        "gc_pct": gc_pct,
        "orf_adn": mejor_orf,
        "proteina": proteina
    }
"""
        }
    ]
}
