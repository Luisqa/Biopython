"""
Motor de ejecución de código y auto-calificador pedagógico (Auto-Grader)
para los ejercicios interactivos de PyBioLearn.
Incluye traducción didáctica de errores en español y eliminación de trazas internas.
"""

import sys
import io
import re
import traceback
import math
from typing import Dict, Any, List, Optional, Callable


def _is_biological_sequence(text: str) -> bool:
    """Detecta si un identificador parece ser una secuencia de ADN, ARN o péptido."""
    cleaned = text.strip().upper()
    if len(cleaned) < 4:
        return False
    # Nucleótidos (ADN/ARN con degeneraciones IUPAC comunes)
    dna_chars = set("ACGTUNRYKMSWBDHV")
    dna_ratio = sum(1 for c in cleaned if c in dna_chars) / len(cleaned)
    if dna_ratio >= 0.8:
        return True
    # Aminoácidos
    aa_chars = set("ACDEFGHIKLMNPQRSTVWY")
    aa_ratio = sum(1 for c in cleaned if c in aa_chars) / len(cleaned)
    return len(cleaned) >= 8 and aa_ratio >= 0.85


def format_pedagogical_error(exc: Exception, user_code: str) -> str:
    """
    Traduce y formatea excepciones de Python a un formato didáctico en español,
    eliminando trazas internas del framework (como runner.py) y ofreciendo
    diagnóstico y soluciones contextuales para estudiantes de bioinformática.
    """
    exc_type = type(exc).__name__
    exc_msg = str(exc)
    code_lines = user_code.splitlines()

    lineno = None
    offset = None
    error_line_text = ""

    if isinstance(exc, (SyntaxError, IndentationError)):
        lineno = exc.lineno
        offset = exc.offset
        if exc.text:
            error_line_text = exc.text.rstrip()
    else:
        # Extraer únicamente los frames que corresponden al código del estudiante (<string>)
        tb = exc.__traceback__
        user_frames = [f for f in traceback.extract_tb(tb) if f.filename == "<string>"]
        if user_frames:
            last_frame = user_frames[-1]
            lineno = last_frame.lineno

    if not error_line_text and lineno and 1 <= lineno <= len(code_lines):
        error_line_text = code_lines[lineno - 1]

    # Construir indicador de línea con puntero visual
    line_snippet = ""
    if error_line_text:
        line_clean = error_line_text.rstrip()
        line_snippet = f"```python\nLínea {lineno}: {line_clean}\n"
        if offset and offset > 0:
            pointer = " " * (len(f"Línea {lineno}: ") + offset - 1) + "^"
            line_snippet += f"{pointer}\n"
        line_snippet += "```\n"

    # Encabezado limpio sin rutas internas
    header = f"### 🛑 Error en la Línea {lineno} de tu código\n" if lineno else "### 🛑 Error al ejecutar tu código\n"

    # Traducción pedagógica y diagnóstico
    title = f"**❌ {exc_type}:** `{exc_msg}`"
    explanation = "Ocurrió un error durante la ejecución de esta instrucción."
    solution = "Revisa la sintaxis y los valores en la línea indicada."

    if exc_type == "NameError":
        m = re.search(r"name '([^']+)' is not defined", exc_msg)
        var_name = m.group(1) if m else ""

        if var_name and _is_biological_sequence(var_name):
            title = "**❌ Error de Nombre (NameError): Secuencia sin comillas**"
            short_var = var_name[:35] + ("..." if len(var_name) > 35 else "")
            explanation = (
                f"Has escrito la secuencia biológica `{short_var}` directamente sin comillas. "
                "Python asume que es el nombre de una variable, y al no haberla definido antes con un signo `=`, "
                "arroja este error porque no sabe qué significa."
            )
            solution = (
                "En Python, todas las secuencias de ADN, ARN o proteínas deben ser cadenas de texto (**strings**) "
                "encerradas entre comillas simples (`'...'`) o dobles (`\"...\"`).\n\n"
                f"**✅ Solución:** Rodea la secuencia con comillas:\n```python\nsecuencia = \"{var_name}\"\n```"
            )
        elif var_name in ["Seq", "SeqIO", "Align", "pairwise2"]:
            title = f"**❌ Error de Nombre (NameError): Clase de Biopython `{var_name}` no importada**"
            explanation = f"Intentas utilizar `{var_name}`, pero aún no has importado la clase o función de Biopython."
            imports = {
                "Seq": "from Bio.Seq import Seq",
                "SeqIO": "from Bio import SeqIO",
                "Align": "from Bio import Align",
                "pairwise2": "from Bio import pairwise2"
            }
            solution = f"**✅ Añade esta importación al inicio de tu código:**\n```python\n{imports.get(var_name, f'import {var_name}')}\n```"
        elif var_name in ["pd", "pandas", "np", "numpy", "plt", "math", "re"]:
            title = f"**❌ Error de Nombre (NameError): Librería `{var_name}` no importada**"
            explanation = f"Intentas utilizar `{var_name}` antes de importarlo."
            lib_imports = {
                "pd": "import pandas as pd",
                "pandas": "import pandas as pd",
                "np": "import numpy as np",
                "numpy": "import numpy as np",
                "plt": "import matplotlib.pyplot as plt",
                "math": "import math",
                "re": "import re"
            }
            solution = f"**✅ Añade esta importación al inicio:**\n```python\n{lib_imports.get(var_name, f'import {var_name}')}\n```"
        else:
            title = f"**❌ Error de Nombre (NameError): `{var_name}` no está definido**"
            explanation = f"Python no encuentra ninguna variable o función llamada `{var_name}`."
            solution = (
                f"1. Comprueba si hay alguna falta tipográfica en `{var_name}` (Python distingue mayúsculas de minúsculas).\n"
                f"2. Asegúrate de haber definido o asignado la variable antes de usarla (ejemplo: `{var_name} = ...`)."
            )

    elif exc_type == "SyntaxError":
        if "was never closed" in exc_msg or "unexpected EOF" in exc_msg:
            title = "**❌ Error de Sintaxis (SyntaxError): Paréntesis o comillas sin cerrar**"
            explanation = "Has abierto un paréntesis `(`, corchete `[`, llave `{` o comilla que nunca se cerró antes del final."
            solution = "Revisa la línea señalada y las anteriores para asegurar que todos los paréntesis y comillas estén cerrados."
        elif error_line_text and (error_line_text.strip().startswith("then ") or error_line_text.strip() == "then"):
            clean_cmd = error_line_text.strip()[5:].strip() if error_line_text.strip().startswith("then ") else ""
            title = "**❌ Error de Sintaxis (SyntaxError): La palabra 'then' no existe en Python**"
            explanation = (
                "En Python **no se utiliza la palabra 'then'** (a diferencia de otros lenguajes o pseudocódigo). "
                "Para definir las instrucciones que se ejecutan dentro de un `if`, simplemente coloca dos puntos `:` "
                "al final de la condición e indenta la siguiente línea con **4 espacios**."
            )
            solution = (
                f"Elimina la palabra `then` y sangra la línea con 4 espacios:\n\n"
                f"**❌ Incorrecto:**\n```python\n{error_line_text.strip()}\n```\n"
                f"**✅ Correcto (sin 'then' y con 4 espacios):**\n```python\n    {clean_cmd}\n```"
            )
        elif error_line_text and error_line_text.strip().startswith(("def ", "if ", "elif ", "else", "for ", "while ", "class ")) and not error_line_text.strip().endswith(":"):
            title = "**❌ Error de Sintaxis (SyntaxError): Falta el signo de dos puntos `:`**"
            explanation = "En Python, las instrucciones que inician un bloque (`def`, `if`, `for`, `while`, etc.) deben terminar obligatoriamente con dos puntos `:`."
            solution = f"**✅ Añade `:` al final de la línea:**\n```python\n{error_line_text.strip()}:\n```"
        elif error_line_text and " = " in error_line_text and ("if " in error_line_text or "elif " in error_line_text) and "==" not in error_line_text and "<=" not in error_line_text and ">=" not in error_line_text and "!=" not in error_line_text:
            title = "**❌ Error de Sintaxis (SyntaxError): Asignación `=` en lugar de comparación `==`**"
            explanation = "Utilizaste un solo signo igual `=` dentro de una condición. En Python, `=` asigna variables y `==` compara igualdad."
            solution = "Cambia `=` por `==` en la condición de tu `if`."
        else:
            title = "**❌ Error de Sintaxis (SyntaxError): Código no válido**"
            explanation = f"Python no pudo interpretar esta línea: `{exc_msg}`."
            solution = "Revisa la puntuación, operadores, paréntesis y comillas en esa línea."

    elif exc_type == "IndentationError":
        stripped_err_line = error_line_text.strip() if error_line_text else ""
        if stripped_err_line.startswith("then ") or stripped_err_line == "then":
            clean_cmd = stripped_err_line[5:].strip() if stripped_err_line.startswith("then ") else ""
            title = "**❌ Error de Indentación y Sintaxis: La palabra 'then' no existe en Python**"
            explanation = (
                "En Python **no se utiliza la palabra 'then'** (a diferencia de otros lenguajes o pseudocódigo). "
                "Para definir el cuerpo de una condición `if`, simplemente coloca dos puntos `:` al final de la condición "
                "y en la siguiente línea deja **4 espacios de sangría**."
            )
            solution = (
                f"Elimina la palabra `then` y sangra la línea con 4 espacios:\n\n"
                f"**❌ Incorrecto:**\n```python\n{error_line_text.strip()}\n```\n"
                f"**✅ Correcto (sin 'then' y con 4 espacios):**\n```python\n    {clean_cmd}\n```"
            )
        elif "expected an indented block" in exc_msg:
            prev_line_text = ""
            if lineno and lineno >= 2 and lineno - 2 < len(code_lines):
                prev_line_text = code_lines[lineno - 2].strip()

            title = "**❌ Error de Sangría (IndentationError): Falta el bloque de 4 espacios**"
            explanation = (
                f"La línea anterior (`{prev_line_text}`) termina en dos puntos `:`, por lo que Python exige que "
                "la siguiente instrucción pertenezca a ese bloque y lleve obligatoriamente **4 espacios de sangría**."
            )
            solution = (
                "Añade 4 espacios de sangría al inicio de esta línea:\n\n"
                f"**✅ Ejemplo correcto:**\n```python\n{prev_line_text}\n    {stripped_err_line}\n```"
            )
        else:
            title = "**❌ Error de Sangría / Indentación (IndentationError)**"
            explanation = "En Python, los bloques de código se definen obligatoriamente mediante espacios de sangría (indentación)."
            solution = (
                "1. Tras una línea que termina en dos puntos `:`, la siguiente línea debe llevar 4 espacios de sangría.\n"
                "2. No mezcles tabulaciones con espacios.\n"
                "3. Todas las instrucciones del mismo bloque deben estar alineadas con la misma sangría."
            )

    elif exc_type == "TypeError":
        if "can only concatenate str" in exc_msg or "unsupported operand type(s) for +" in exc_msg:
            title = "**❌ Error de Tipos (TypeError): Operación incompatible entre texto y número**"
            explanation = "Intentaste sumar o unir directamente una cadena de texto (`str`) con un número (`int` o `float`)."
            solution = (
                "Para unir texto con variables numéricas:\n"
                "- Convierte el número a texto con `str(variable)`: `\"Total: \" + str(cuenta)`\n"
                "- O utiliza f-strings: `f\"Total: {cuenta}\"`"
            )
        elif "not callable" in exc_msg:
            title = "**❌ Error de Tipos (TypeError): Objeto no ejecutable**"
            explanation = "Intentaste usar paréntesis `(...)` sobre una variable que no es una función."
            solution = "Comprueba si sin querer le asignaste un valor a un nombre de función estándar (por ejemplo `len = 10` o `print = 'hola'`)."
        elif "not subscriptable" in exc_msg:
            title = "**❌ Error de Tipos (TypeError): No indexable con corchetes `[]`**"
            explanation = "Intentaste acceder con corchetes `[i]` a un tipo que no lo permite (como un número entero o float)."
            solution = "Los corchetes `[]` sólo se usan con textos (`str`), listas (`list`), tuplas (`tuple`) o diccionarios (`dict`)."
        elif "not iterable" in exc_msg:
            title = "**❌ Error de Tipos (TypeError): Objeto no iterable**"
            explanation = "Intentaste recorrer con un bucle `for` o usar el operador `in` sobre un dato que no es una colección."
            solution = "Si deseas repetir un bucle un número de veces, usa `range(n)` en lugar de sólo el número."
        elif "missing" in exc_msg and "positional argument" in exc_msg:
            title = "**❌ Error de Tipos (TypeError): Faltan argumentos en la llamada**"
            explanation = f"La función esperaba más parámetros de los que proporcionaste: `{exc_msg}`."
            solution = "Revisa la definición de la función y asegúrate de proporcionarle todos los argumentos requeridos."
        else:
            title = f"**❌ Error de Tipos (TypeError):** `{exc_msg}`"
            explanation = "Se intentó realizar una operación entre tipos de datos incompatibles."
            solution = "Verifica los tipos de tus variables con `type(var)` y realiza las conversiones necesarias (`int()`, `float()`, `str()`)."

    elif exc_type == "ZeroDivisionError":
        title = "**❌ Error de División por Cero (ZeroDivisionError)**"
        explanation = "Se intentó realizar una división entre cero."
        solution = (
            "En bioinformática, esto suele ocurrir al calcular porcentajes (como el %GC) dividiendo entre la longitud `len(seq)` "
            "cuando la secuencia recibida está vacía (longitud 0).\n\n"
            "**✅ Solución:** Añade una condición previa al inicio de tu función:\n```python\nif len(secuencia) == 0:\n    return 0.0\n```"
        )

    elif exc_type == "IndexError":
        title = "**❌ Error de Índice Fuera de Rango (IndexError)**"
        explanation = "Intentaste acceder a una posición (índice) que supera la longitud de la lista o texto."
        solution = (
            "Recuerda que en Python los índices empiezan en `0` y terminan en `len(...) - 1`.\n"
            "Por ejemplo, una secuencia de 10 nucleótidos tiene índices de `0` a `9`. Acceder a `seq[10]` generará este error."
        )

    elif exc_type == "KeyError":
        title = f"**❌ Error de Clave (KeyError): Clave no encontrada** `{exc_msg}`"
        explanation = f"El diccionario no contiene la clave buscada: `{exc_msg}`."
        solution = (
            "Si estás traduciendo codones a aminoácidos:\n"
            "1. Asegúrate de pasar el codón en mayúsculas (`codon.upper()`).\n"
            "2. Verifica si la clave existe antes de consultarla (`if codon in codigo_genetico:`).\n"
            "3. O usa el método `.get()` con valor por defecto: `codigo_genetico.get(codon, '?')`."
        )

    elif exc_type == "AttributeError":
        title = f"**❌ Error de Atributo o Método (AttributeError):** `{exc_msg}`"
        explanation = "El tipo de dato que estás manipulando no cuenta con ese atributo o función."
        solution = (
            "1. Comprueba si escribiste correctamente el método (ejemplo: `.count()`, `.upper()`, `.lower()`, `.replace()`, `.append()`).\n"
            "2. Verifica el tipo real de la variable con `type(objeto)`."
        )

    elif exc_type == "ValueError":
        title = f"**❌ Error de Valor (ValueError):** `{exc_msg}`"
        explanation = "La función recibió un argumento del tipo esperado pero con un valor o formato no válido."
        solution = "Revisa los valores pasados a la función para verificar que cumplan con los formatos esperados."

    elif exc_type == "UnboundLocalError":
        title = "**❌ Error de Variable Local (UnboundLocalError)**"
        explanation = f"Intentaste utilizar una variable dentro de una función antes de asignarle un valor: `{exc_msg}`."
        solution = "Asegúrate de inicializar la variable (ejemplo: `contador = 0`) antes de usarla o modificarla dentro de la función."

    elif exc_type in ("RuntimeError", "EOFError") and ("input()" in exc_msg or "EOF" in exc_msg):
        title = "**🛑 Uso de input() en la plataforma interactiva**"
        explanation = (
            "Has llamado a la función `input()` para solicitar datos al usuario. "
            "En esta plataforma interactiva web no existe una consola de terminal tradicional donde escribir durante la ejecución."
        )
        solution = (
            "En los retos de PyBioLearn, el auto-evaluador prueba tu función automáticamente llamándola con casos de prueba biológicos en segundo plano.\n\n"
            "**✅ Solución:** Elimina las líneas finales donde usas `input()` y las llamadas sueltas. Deja únicamente la definición de la función requerida:\n"
            "```python\ndef calcular_gc(secuencia: str) -> float:\n    # Tu lógica aquí...\n    return round(gc_pct, 2)\n```\n"
            "Al hacer clic en **'🧪 Validar Solución'**, el sistema evaluará tu función con todas las secuencias de prueba automáticamente."
        )

    # Ensamblar reporte pedagógico limpio
    report = (
        f"{header}\n"
        f"{line_snippet}\n"
        f"{title}\n\n"
        f"**💬 Explicación:**\n{explanation}\n\n"
        f"**💡 Diagnóstico y Solución sugerida:**\n{solution}\n"
    )

    return report


def format_test_exception(exc: Exception, target_function: str) -> str:
    """Traduce errores ocurridos durante la evaluación de casos de prueba biológicos."""
    exc_type = type(exc).__name__
    exc_msg = str(exc)

    if isinstance(exc, ZeroDivisionError):
        return "⚠️ División por cero (ZeroDivisionError): ¿Verificaste si la secuencia de entrada está vacía o su longitud es 0?"
    elif isinstance(exc, IndexError):
        return f"⚠️ Índice fuera de límites (IndexError): {exc_msg}. La función intentó acceder a una posición inexistente."
    elif isinstance(exc, KeyError):
        return f"⚠️ Clave no encontrada en diccionario (KeyError: {exc_msg}). El codón o identificador evaluado no existe en el diccionario."
    elif isinstance(exc, TypeError):
        return f"⚠️ Error de tipos (TypeError): {exc_msg}. Comprueba los tipos de datos recibidos y devueltos."
    elif isinstance(exc, AttributeError):
        return f"⚠️ Método no encontrado (AttributeError): {exc_msg}."
    else:
        return f"⚠️ Error en ejecución ({exc_type}): {exc_msg}"


def format_pedagogical_warning(raw_warning: str) -> str:
    """Traduce avisos de Python y Biopython (warnings) a un formato claro y formativo en español."""
    if "BiopythonWarning" in raw_warning and "Partial codon" in raw_warning:
        return (
            "🧬 **Aviso de Biopython (BiopythonWarning): Codón parcial / incompleto**\n\n"
            "La secuencia que intentaste traducir tiene una longitud que **no es múltiplo de 3**.\n"
            "- En biología molecular, cada aminoácido está codificado por un triplete de 3 nucleótidos (codón).\n"
            "- Al no ser múltiplo de 3, los nucleótidos sobrantes al final no alcanzan a formar un codón completo.\n\n"
            "💡 **Solución recomendada:**\n"
            "1. Recorta los nucleótidos sobrantes antes de traducir:\n"
            "   ```python\n"
            "   adn_completo = adn[:len(adn) - (len(adn) % 3)]\n"
            "   proteina = adn_completo.translate()\n"
            "   ```\n"
            "2. O asegúrate de que la longitud de la secuencia sea divisible entre 3 (ej: 30, 33 o 36 nucleótidos)."
        )
    return f"ℹ️ **Aviso del intérprete (Warning):**\n```\n{raw_warning.strip()}\n```"


def execute_code(code_str: str, custom_globals: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Ejecuta código Python capturando la salida estándar (stdout), errores traducidos didácticamente (stderr)
    y avisos del sistema (warnings), eliminando trazas del sistema runner.py.
    """
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    def _mock_input(prompt: str = "") -> str:
        raise RuntimeError(
            "⚠️ En la plataforma interactiva web no debes usar input(). "
            "El auto-evaluador prueba tu función directamente llamándola con diferentes secuencias biológicas de prueba. "
            "Por favor, elimina las llamadas a input() de tu código."
        )

    # Preparar entorno seguro
    exec_globals = {
        "__name__": "__main__",
        "__builtins__": __builtins__,
        "input": _mock_input,
    }
    if custom_globals:
        exec_globals.update(custom_globals)

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    old_stdin = sys.stdin
    success = True
    error_msg = ""

    # 1. Compilación previa para atrapar SyntaxError e IndentationError limpiamente
    try:
        compiled = compile(code_str, "<string>", "exec")
    except (SyntaxError, IndentationError) as exc:
        return {
            "success": False,
            "stdout": "",
            "stderr": format_pedagogical_error(exc, code_str),
            "warnings": "",
            "globals": exec_globals
        }

    # 2. Ejecución capturando runtime errors y redirigiendo stdout/stderr/stdin
    try:
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        sys.stdin = io.StringIO()
        exec(compiled, exec_globals)
    except Exception as exc:
        success = False
        error_msg = format_pedagogical_error(exc, code_str)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        sys.stdin = old_stdin

    raw_stderr = stderr_capture.getvalue()
    warnings_out = ""
    # Si la ejecución fue exitosa pero hubo texto en stderr, son warnings de librerías (como Biopython)
    if success and raw_stderr:
        warnings_out = format_pedagogical_warning(raw_stderr)
        raw_stderr = ""

    return {
        "success": success,
        "stdout": stdout_capture.getvalue(),
        "stderr": error_msg if not success else raw_stderr,
        "warnings": warnings_out,
        "globals": exec_globals
    }


def grade_exercise(
    user_code: str,
    target_function: str,
    test_cases: List[Dict[str, Any]],
    custom_globals: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Evalúa el código del estudiante contra una batería de casos de prueba biológicos.
    """
    run_res = execute_code(user_code, custom_globals=custom_globals)

    if not run_res["success"]:
        return {
            "all_passed": False,
            "stdout": run_res["stdout"],
            "stderr": run_res["stderr"],
            "feedback": "⚠️ Ocurrió un error al compilar o ejecutar tu código. Revisa los detalles explicados abajo.",
            "test_results": []
        }

    env = run_res["globals"]
    if target_function not in env or not callable(env[target_function]):
        return {
            "all_passed": False,
            "stdout": run_res["stdout"],
            "stderr": run_res["stderr"],
            "feedback": f"❌ No se encontró la función `{target_function}` definida o no es una función ejecutable.",
            "test_results": []
        }

    func = env[target_function]
    test_results = []
    all_passed = True

    for tc in test_cases:
        tc_name = tc.get("name", "Prueba")
        args = tc.get("args", ())
        kwargs = tc.get("kwargs", {})
        expected = tc.get("expected")
        tolerance = tc.get("tolerance")
        custom_validator = tc.get("validator")

        try:
            passed = False
            got = None

            if custom_validator and callable(custom_validator):
                if args or kwargs:
                    got = func(*args, **kwargs)
                    passed = bool(custom_validator(got))
                else:
                    passed = bool(custom_validator(func))
            else:
                got = func(*args, **kwargs)
                if tolerance is not None and isinstance(got, (int, float)) and isinstance(expected, (int, float)):
                    passed = math.isclose(float(got), float(expected), abs_tol=tolerance)
                else:
                    passed = (got == expected)

            if not passed:
                all_passed = False

            test_results.append({
                "name": tc_name,
                "passed": passed,
                "input_desc": f"args={args}, kwargs={kwargs}" if kwargs else f"{args}",
                "expected": expected if expected is not None else "(Validación personalizada)",
                "got": got,
                "error": None
            })
        except Exception as e:
            all_passed = False
            test_results.append({
                "name": tc_name,
                "passed": False,
                "input_desc": f"args={args}, kwargs={kwargs}" if kwargs else f"{args}",
                "expected": expected,
                "got": None,
                "error": format_test_exception(e, target_function)
            })

    feedback = "🎉 ¡Excelente trabajo! Todos los casos de prueba se han superado correctamente." if all_passed else "🔍 Algunos casos de prueba no pasaron. Revisa los detalles abajo e inténtalo de nuevo."

    return {
        "all_passed": all_passed,
        "stdout": run_res["stdout"],
        "stderr": run_res["stderr"],
        "feedback": feedback,
        "test_results": test_results
    }
