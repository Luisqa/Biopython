"""
Módulo 6: Programación Orientada a Objetos (POO) en Bioinformática.
Temas: Clases, Métodos mágicos (__init__, __len__, __repr__), Propiedades (@property) y Modelado Biológico.
"""

from typing import Dict, Any, List

MODULE_INFO = {
    "id": 6,
    "title": "Módulo 6: Programación Orientada a Objetos (POO) en Bioinformática",
    "summary": "Diseña tus propias clases biológicas en Python (SecuenciaADN, VarianteGenetica) emulando la arquitectura subyacente de paquetes como Biopython.",
    "biopython_ref": "Capítulo 3 y 4 del Tutorial-1.83.pdf (Diseño de las clases Seq y SeqRecord)",

    "theory_python": """
### 🐍 Programación Orientada a Objetos en Python

La POO permite agrupar **estado** (datos y atributos) y **comportamiento** (métodos y funciones) dentro de una misma estructura llamada **Clase**.

#### 1. Definición de una Clase y el Constructor `__init__`
```python
class Gen:
    def __init__(self, simbolo: str, longitud_bp: int):
        self.simbolo = simbolo          # Atributo de instancia
        self.longitud_bp = longitud_bp  # Atributo de instancia

    def descripcion(self) -> str:
        return f"Gen {self.simbolo} de {self.longitud_bp} pares de bases."
```

#### 2. Métodos Mágicos (Dunder Methods)
Python permite que tus objetos se comporten como tipos nativos del lenguaje implementando métodos especiales:
- `__len__(self)`: Permite usar la función `len(objeto)`.
- `__repr__(self)`: Representación formal en string del objeto para depuración.
- `__getitem__(self, index)`: Permite indexación y rebanado (slicing) con corchetes `objeto[0:3]`.

#### 3. El Decorador `@property`
Convierte un método en un atributo de solo lectura que se calcula dinámicamente sin necesidad de llamarlo con paréntesis `()`:
```python
class Secuencia:
    def __init__(self, texto: str):
        self.texto = texto.upper()
        
    @property
    def gc_pct(self) -> float:
        total = len(self.texto)
        if total == 0:
            return 0.0
        return round(((self.texto.count('G') + self.texto.count('C')) / total) * 100, 2)
```
""",

    "theory_bio": """
### 🧬 Aplicación Bioinformática: Modelado de Objetos y Variantes

#### 1. La Arquitectura de Clases en Bioinformática
Librerías líderes como **Biopython** no tratan las secuencias como simples cadenas de texto primitivas (`str`), sino como objetos ricos:
- Un objeto `Seq` sabe cómo transcribirse, traducirse y complementarse sin necesidad de que el usuario recuerde los algoritmos subyacentes.
- Un objeto `SeqRecord` acopla la secuencia con su anotación de coordenadas, identificadores del NCBI y especie de origen.

#### 2. Transiciones vs. Transversiones en Genética de Poblaciones
Al clasificar sustituciones de nucleótidos simples (SNVs / SNPs):
- **Transición (Ti)**: Intercambio de una base de la misma familia química:
  - Purina por Purina: $\\text{A} \\longleftrightarrow \\text{G}$
  - Pirimidina por Pirimidina: $\\text{C} \\longleftrightarrow \\text{T}$
- **Transversión (Tv)**: Intercambio entre familias químicas distintas:
  - Purina por Pirimidina o viceversa: $\\text{A} \\longleftrightarrow \\text{C}$, $\\text{A} \\longleftrightarrow \\text{T}$, $\\text{G} \\longleftrightarrow \\text{C}$, $\\text{G} \\longleftrightarrow \\text{T}$.
- **Ratio Ti/Tv**: En genomas humanos el ratio natural es $\\approx 2.0 - 2.1$ en exomas debido a la desaminación espontánea de citosinas metiladas. Desviaciones de este ratio se usan en control de calidad de secuenciación clínica para detectar falsos positivos.
""",

    "exercises": [
        {
            "id": "ex_06_01_dna_class",
            "title": "Reto 6.1: Diseña la Clase SecuenciaADN",
            "description": """
Crea una clase llamada `SecuenciaADN` que represente una molécula de ADN con orientación a objetos.

**Requisitos**:
1. El método `__init__(self, id_seq: str, seq: str)` debe inicializar los atributos:
   - `self.id_seq = id_seq`
   - `self.seq = seq.upper()` (guardar siempre en mayúsculas)
2. El método mágico `__len__(self)` debe devolver la longitud de `self.seq` con `len()`.
3. El método `transcribir(self)` debe retornar una cadena con la secuencia transcrita a ARN (sustituyendo 'T' por 'U').
4. Debe tener una propiedad `@property def gc(self) -> float` que retorne el %GC como número decimal redondeado a 2 decimales (o `0.0` si está vacía).
""",
            "starter_code": """class SecuenciaADN:
    # Define aquí tu clase:
    pass
""",
            "target_function": "SecuenciaADN",
            "test_cases": [
                {
                    "name": "Instanciación y longitud",
                    "validator": lambda cls: len(cls("seq1", "ATGC")) == 4
                },
                {
                    "name": "Propiedad %GC calculada dinámicamente",
                    "validator": lambda cls: cls("seq1", "GCGC").gc == 100.0 and cls("seq2", "ATAT").gc == 0.0
                },
                {
                    "name": "Método transcribir a ARN",
                    "validator": lambda cls: cls("seq1", "atgc").transcribir() == "AUGC"
                }
            ],
            "hints": [
                "En `__init__`, asegúrate de asignar `self.seq = seq.upper()`.",
                "Implementa `def __len__(self): return len(self.seq)`.",
                "Decora el método de GC con `@property`."
            ],
            "solution": """class SecuenciaADN:
    def __init__(self, id_seq: str, seq: str):
        self.id_seq = id_seq
        self.seq = seq.upper()
        
    def __len__(self) -> int:
        return len(self.seq)
        
    def transcribir(self) -> str:
        return self.seq.replace("T", "U")
        
    @property
    def gc(self) -> float:
        if not self.seq:
            return 0.0
        g = self.seq.count("G")
        c = self.seq.count("C")
        return round(((g + c) / len(self.seq)) * 100.0, 2)
"""
        },
        {
            "id": "ex_06_02_variant_class",
            "title": "Reto 6.2: Clase VarianteGenetica y Detector de Transiciones",
            "description": """
Crea una clase llamada `VarianteGenetica` que modele una variante de nucleótido único (SNV).

**Requisitos**:
1. `__init__(self, cromo: str, pos: int, ref: str, alt: str)`:
   - Almacena `self.cromo = cromo`
   - `self.pos = pos`
   - `self.ref = ref.upper()`
   - `self.alt = alt.upper()`
2. Método `es_transicion(self) -> bool`:
   - Retorna `True` si el cambio de `ref` a `alt` es una **transición**:
     `A <-> G` (purina por purina) o `C <-> T` (pirimidina por pirimidina).
   - Retorna `False` si es una transversión o si alguno de los alelos no es una base única A, C, G, T.
""",
            "starter_code": """class VarianteGenetica:
    # Define aquí tu clase:
    pass
""",
            "target_function": "VarianteGenetica",
            "test_cases": [
                {
                    "name": "Transición purina A -> G",
                    "validator": lambda cls: cls("chr1", 1000, "A", "G").es_transicion() is True
                },
                {
                    "name": "Transición pirimidina C -> T",
                    "validator": lambda cls: cls("chr1", 1000, "C", "T").es_transicion() is True
                },
                {
                    "name": "Transversión A -> C",
                    "validator": lambda cls: cls("chr1", 1000, "A", "C").es_transicion() is False
                },
                {
                    "name": "Transversión T -> G",
                    "validator": lambda cls: cls("chr1", 1000, "T", "G").es_transicion() is False
                }
            ],
            "hints": [
                "Los pares de transición son: `('A', 'G'), ('G', 'A'), ('C', 'T'), ('T', 'C')`.",
                "Puedes comprobar si `(self.ref, self.alt) in transiciones`."
            ],
            "solution": """class VarianteGenetica:
    def __init__(self, cromo: str, pos: int, ref: str, alt: str):
        self.cromo = cromo
        self.pos = pos
        self.ref = ref.upper()
        self.alt = alt.upper()
        
    def es_transicion(self) -> bool:
        transiciones = {
            ("A", "G"), ("G", "A"),
            ("C", "T"), ("T", "C")
        }
        return (self.ref, self.alt) in transiciones
"""
        }
    ]
}
