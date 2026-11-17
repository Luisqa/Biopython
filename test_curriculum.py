"""
Verificador automático del currículo y auto-grader de PyBioLearn.
Prueba todas las soluciones de los retos para asegurar que pasen el 100% de los casos de prueba.
"""

import importlib
from core.runner import grade_exercise

MODULES = [
    "modules.module_01_basics",
    "modules.module_02_control",
    "modules.module_03_structures",
    "modules.module_04_functions",
    "modules.module_05_files",
    "modules.module_06_oop",
    "modules.module_07_data_viz",
    "modules.module_08_biopython",
    "modules.module_09_databases",
    "modules.module_10_project",
]

def main():
    total_exercises = 0
    total_passed = 0
    print("Iniciando validación del currículo de PyBioLearn...\n" + "="*60)
    
    for mod_name in MODULES:
        mod = importlib.import_module(mod_name)
        info = mod.MODULE_INFO
        print(f"\n📂 {info['title']}")
        
        for ex in info["exercises"]:
            total_exercises += 1
            ex_id = ex["id"]
            target = ex["target_function"]
            solution = ex["solution"]
            tests = ex["test_cases"]
            
            res = grade_exercise(solution, target, tests)
            if res["all_passed"]:
                total_passed += 1
                print(f"  ✅ {ex['title']} ({len(tests)} tests OK)")
            else:
                print(f"  ❌ FALLO en {ex['title']}")
                print(f"     Feedback: {res['feedback']}")
                for tc in res["test_results"]:
                    if not tc["passed"]:
                        print(f"     - Falló caso '{tc['name']}': Esperado={tc['expected']}, Obtenido={tc['got']}")
                if res["stderr"]:
                    print(f"     Error traceback: {res['stderr']}")
                    
    print("\n" + "="*60)
    print(f"RESULTADO: {total_passed}/{total_exercises} retos superados al 100%.")
    assert total_passed == total_exercises, "No todos los retos pasaron."
    print("¡TODO EL CURRÍCULO ESTÁ VALIDADO Y FUNCIONA A LA PERFECCIÓN!")

if __name__ == "__main__":
    main()
