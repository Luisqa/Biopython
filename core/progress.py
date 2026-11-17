"""
Módulo de gestión del progreso del estudiante en PyBioLearn.
Guarda y carga el estado de los ejercicios completados en progress.json.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

PROGRESS_FILE = Path(__file__).resolve().parent.parent / "progress.json"


def load_progress() -> Dict[str, Any]:
    """Carga el progreso guardado o inicializa uno nuevo."""
    default_progress = {
        "completed_exercises": [],
        "points": 0,
        "current_module": 1,
        "completed_modules": [],
        "quiz_scores": {},
        "notes": {},
        "saved_codes": {},
        "sandbox_code": ""
    }
    
    if not PROGRESS_FILE.exists():
        save_progress(default_progress)
        return default_progress
    
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Asegurar compatibilidad con claves nuevas
            for key, val in default_progress.items():
                if key not in data:
                    data[key] = val
            return data
    except Exception:
        return default_progress


def save_progress(data: Dict[str, Any]) -> None:
    """Guarda el progreso en el archivo progress.json."""
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando progreso: {e}")


def mark_exercise_completed(exercise_id: str, points: int = 10) -> bool:
    """
    Marca un ejercicio como completado si no lo estaba ya.
    Retorna True si es la primera vez que se completa.
    """
    progress = load_progress()
    if exercise_id not in progress["completed_exercises"]:
        progress["completed_exercises"].append(exercise_id)
        progress["points"] += points
        save_progress(progress)
        return True
    return False


def is_exercise_completed(exercise_id: str) -> bool:
    """Verifica si un ejercicio ya ha sido superado."""
    progress = load_progress()
    return exercise_id in progress["completed_exercises"]


def get_progress_summary(total_exercises: int = 25) -> Dict[str, Any]:
    """Obtiene un resumen estadístico del avance del alumno."""
    progress = load_progress()
    completed_count = len(progress["completed_exercises"])
    pct = round((completed_count / max(1, total_exercises)) * 100, 1)
    return {
        "completed_count": completed_count,
        "total_exercises": total_exercises,
        "percentage": min(100.0, pct),
        "points": progress["points"],
        "level": get_student_level(progress["points"])
    }


def get_student_level(points: int) -> str:
    """Calcula el nivel y rango del estudiante según sus puntos."""
    if points < 30:
        return "🌱 Principiante en Python Biológico"
    elif points < 80:
        return "🧬 Explorador de Secuencias"
    elif points < 150:
        return "🔬 Analista Bioinformático Junior"
    elif points < 230:
        return "💻 Desarrollador de Pipelines Ómicos"
    else:
        return "🚀 Maestro en Python Bioinformático"


def save_user_code(exercise_id: str, code: str) -> None:
    """Guarda de forma persistente el código del estudiante para un ejercicio específico."""
    progress = load_progress()
    if "saved_codes" not in progress:
        progress["saved_codes"] = {}
    progress["saved_codes"][exercise_id] = code
    save_progress(progress)


def get_saved_code(exercise_id: str, default_code: str = "") -> str:
    """Recupera el código guardado de un ejercicio o retorna el código base inicial."""
    progress = load_progress()
    saved = progress.get("saved_codes", {})
    return saved.get(exercise_id, default_code)


def save_sandbox_code(code: str) -> None:
    """Guarda de forma persistente el código del laboratorio libre (Sandbox)."""
    progress = load_progress()
    progress["sandbox_code"] = code
    save_progress(progress)


def get_sandbox_code(default_code: str = "") -> str:
    """Recupera el código guardado del sandbox o retorna el ejemplo por defecto."""
    progress = load_progress()
    saved = progress.get("sandbox_code", "")
    return saved if saved else default_code


def reset_progress() -> None:
    """Reinicia todo el progreso del estudiante."""
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()
    load_progress()
