"""
PyBioLearn: Plataforma Interactiva de Aprendizaje de Python Aplicado a la Bioinformática.
Combina un curso modular progresivo (Python estándar -> Bioinformática) con retos interactivos,
auto-evaluador de código, exploradores de NCBI, UniProt, EMBL-EBI OLS y vinculación con Tutorial-1.83.pdf.
"""

import sys
import io
import importlib
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt

# Importar utilidades del núcleo
from core.progress import (
    load_progress,
    mark_exercise_completed,
    is_exercise_completed,
    get_progress_summary,
    reset_progress,
    save_user_code,
    get_saved_code,
    save_sandbox_code,
    get_sandbox_code
)
from core.runner import execute_code, grade_exercise
from core.ncbi_client import search_ncbi, fetch_ncbi_fasta
from core.uniprot_client import search_uniprot, get_uniprot_entry
from core.ols_client import search_ols, get_term_details
from core.tutorial_helper import get_available_chapters, get_chapter_info, get_pdf_status

# Configuración de página de Streamlit
st.set_page_config(
    page_title="PyBioLearn: Python para Bioinformática",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para una interfaz científica moderna
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #10B981, #06B6D4, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .badge-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 15px;
    }
    .dual-box-py {
        background-color: #1e293b;
        border-left: 4px solid #3b82f6;
        padding: 12px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
    }
    .dual-box-bio {
        background-color: #1e293b;
        border-left: 4px solid #10b981;
        padding: 12px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
    }
    .terminal-out {
        background-color: #0B1120;
        color: #38BDF8;
        font-family: 'Courier New', Courier, monospace;
        padding: 12px;
        border-radius: 6px;
        border: 1px solid #1E293B;
        white-space: pre-wrap;
    }
    textarea {
        font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', 'Courier New', monospace !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        tab-size: 4 !important;
        -moz-tab-size: 4 !important;
    }
    iframe[height="0"] {
        position: absolute !important;
        height: 0px !important;
        width: 0px !important;
        border: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Módulos del curso disponibles
MODULE_FILES = {
    1: "modules.module_01_basics",
    2: "modules.module_02_control",
    3: "modules.module_03_structures",
    4: "modules.module_04_functions",
    5: "modules.module_05_files",
    6: "modules.module_06_oop",
    7: "modules.module_07_data_viz",
    8: "modules.module_08_biopython",
    9: "modules.module_09_databases",
    10: "modules.module_10_project"
}


def render_sidebar():
    """Renderiza el menú lateral con estadísticas del estudiante y navegación."""
    with st.sidebar:
        st.markdown("<h2 style='margin-bottom:0;'>🧬 PyBioLearn</h2>", unsafe_allow_html=True)
        st.markdown("<small style='color:#94a3b8;'>Python aplicado a la Bioinformática</small>", unsafe_allow_html=True)
        st.divider()
        
        # Resumen de Progreso
        summary = get_progress_summary(total_exercises=24)
        st.markdown(f"**Nivel:** {summary['level']}")
        st.markdown(f"**Puntuación:** ⭐ `{summary['points']} pts`")
        
        # Barra de progreso
        st.progress(summary["percentage"] / 100.0)
        st.caption(f"Retos superados: **{summary['completed_count']}** de **{summary['total_exercises']}** ({summary['percentage']}%)")
        
        st.divider()
        st.markdown("### 🧭 Navegación")
        modo = st.radio(
            "Selecciona la sección:",
            [
                "📚 Curso Modular (Módulos 1 - 10)",
                "💻 Laboratorio Libre (Sandbox)",
                "🌐 Explorador NCBI Entrez",
                "🔬 Explorador UniProtKB",
                "🌳 Explorador EMBL-EBI OLS",
                "📖 Visor Tutorial Biopython (PDF)"
            ],
            index=0
        )
        
        st.divider()
        # Estado del archivo PDF en la carpeta
        pdf_info = get_pdf_status()
        if pdf_info["exists"]:
            st.success(f"📄 **Tutorial Biopython v1.83 vinculado** ({pdf_info['size_mb']} MB)")
        else:
            st.warning("⚠️ Tutorial-1.83.pdf no detectado en el directorio.")
            
        with st.expander("⚙️ Opciones"):
            if st.button("Reiniciar mi Progreso", type="secondary"):
                reset_progress()
                st.rerun()
                
    return modo


def render_course_module():
    """Renderiza la vista principal del curso modular de Python + Bioinformática."""
    st.markdown("<div class='main-title'>Curso Modular: Python desde Cero para Bioinformática</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Combina la teoría general de Python con ejercicios, ejemplos y datos biológicos reales.</div>", unsafe_allow_html=True)
    
    # Selector de Módulo
    nombres_modulos = [
        "Módulo 1: Fundamentos de Python y Secuencias Biológicas",
        "Módulo 2: Control de Flujo, Filtros y Motivos de Restricción",
        "Módulo 3: Estructuras de Datos y el Código Genético",
        "Módulo 4: Funciones, Modularidad y Diseño de Primers",
        "Módulo 5: Entrada/Salida de Archivos (FASTA, FASTQ, N50)",
        "Módulo 6: Programación Orientada a Objetos (POO)",
        "Módulo 7: Análisis de Datos con Pandas y RNA-seq",
        "Módulo 8: El Ecosistema Biopython (Tutorial Oficial v1.83)",
        "Módulo 9: Bases de Datos (NCBI, UniProt y EMBL-EBI OLS)",
        "Módulo 10: Proyecto Final - Pipeline de Anotación Ómica"
    ]
    
    seleccion = st.selectbox("📚 Selecciona el Módulo:", nombres_modulos, index=0)
    num_modulo = int(seleccion.split(":")[0].replace("Módulo", "").strip())
    
    # Cargar módulo dinámicamente
    mod_path = MODULE_FILES.get(num_modulo)
    module_obj = importlib.import_module(mod_path)
    info = module_obj.MODULE_INFO
    
    # Cabecera del módulo
    st.markdown(f"### {info['title']}")
    st.info(f"💡 **Objetivo**: {info['summary']}\n\n📖 **Referencia Tutorial Biopython**: `{info.get('biopython_ref', 'N/A')}`")
    
    # Pestañas de contenido del módulo
    tab_teoria, tab_retos, tab_datos = st.tabs(["📘 Teoría y Aplicación", "🧪 Laboratorio de Retos", "📂 Datos de Ejemplo"])
    
    with tab_teoria:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='dual-box-py'>", unsafe_allow_html=True)
            st.markdown(info["theory_python"])
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='dual-box-bio'>", unsafe_allow_html=True)
            st.markdown(info["theory_bio"])
            st.markdown("</div>", unsafe_allow_html=True)
            
    with tab_retos:
        render_challenges(info["exercises"])
        
    with tab_datos:
        render_sample_data_viewer()


def render_challenges(exercises: list):
    """Renderiza el auto-grader interactivo y editor de código para los retos del módulo."""
    if not exercises:
        st.write("No hay ejercicios para este módulo.")
        return
        
    titulos = [f"{'✅ ' if is_exercise_completed(ex['id']) else '⏳ '}{ex['title']}" for ex in exercises]
    ej_sel = st.selectbox("🎯 Selecciona el Reto Práctico:", titulos)
    idx = titulos.index(ej_sel)
    ex = exercises[idx]
    
    st.markdown(f"#### {ex['title']}")
    st.markdown(ex["description"])
    
    completed = is_exercise_completed(ex["id"])
    if completed:
        st.success("🎉 ¡Ya has completado este ejercicio con éxito!")
        
    st.markdown("##### 💻 Tu Solución en Python:")
    
    # Clave de estado para recordar el código del alumno (persistente en disco)
    code_key = f"code_{ex['id']}"
    if code_key not in st.session_state:
        st.session_state[code_key] = get_saved_code(ex["id"], ex["starter_code"])
        
    user_code = st.text_area(
        "Editor de Código:",
        value=st.session_state[code_key],
        height=220,
        key=f"text_area_{ex['id']}",
        help="Escribe tu código Python aquí y haz clic en 'Ejecutar', 'Validar' o 'Guardar'."
    )
    st.session_state[code_key] = user_code
    
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1.3, 1.2, 1])
    
    with col_btn1:
        btn_run = st.button("▶ Ejecutar", key=f"run_{ex['id']}")
    with col_btn2:
        btn_grade = st.button("🧪 Validar Solución", type="primary", key=f"grade_{ex['id']}")
    with col_btn3:
        btn_save = st.button("💾 Guardar Código", key=f"save_{ex['id']}")
    with col_btn4:
        btn_reset = st.button("🔄 Reiniciar", key=f"reset_{ex['id']}")
        
    if btn_save:
        save_user_code(ex["id"], user_code)
        st.success("💾 ¡Código guardado correctamente! Se recuperará automáticamente cuando vuelvas a este reto.")

    if btn_reset:
        st.session_state[code_key] = ex["starter_code"]
        save_user_code(ex["id"], ex["starter_code"])
        st.rerun()
        
    # Ejecución simple (Sandbox)
    if btn_run:
        save_user_code(ex["id"], user_code)
        st.markdown("##### 📤 Salida de Ejecución:")
        res = execute_code(user_code)
        if res["stdout"]:
            st.code(res["stdout"], language="text")
        if res.get("warnings"):
            st.warning(res["warnings"])
        if res["stderr"]:
            st.error(res["stderr"])
        if not res["stdout"] and not res["stderr"] and not res.get("warnings"):
            st.info("El código se ejecutó sin errores pero no imprimió nada en la consola. Usa `print()` para ver resultados.")
            
    # Validación automática (Auto-Grader)
    if btn_grade:
        save_user_code(ex["id"], user_code)
        st.markdown("##### 🧪 Evaluación Automática de Casos de Prueba:")
        with st.spinner("Evaluando con casos de prueba biológicos..."):
            grade_res = grade_exercise(user_code, ex["target_function"], ex["test_cases"])
            
        if grade_res["all_passed"]:
            is_new = mark_exercise_completed(ex["id"], points=10)
            st.balloons()
            st.success(f"🏆 {grade_res['feedback']} +10 puntos añadidos.")
        else:
            st.warning(grade_res["feedback"])
            
        if grade_res["stderr"]:
            st.error(grade_res["stderr"])
                
        # Detalle caso a caso
        for tc in grade_res["test_results"]:
            icon = "✅" if tc["passed"] else "❌"
            with st.container():
                st.markdown(f"**{icon} {tc['name']}**")
                if not tc["passed"]:
                    st.caption(f"Entrada: `{tc['input_desc']}`")
                    st.caption(f"Esperado: `{tc['expected']}` | Obtenido: `{tc['got']}`")
                    if tc["error"]:
                        st.caption(f"⚠️ `{tc['error']}`")
                        
    # Pistas y Solución
    st.divider()
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        with st.expander("💡 Ver Pistas"):
            for i, p in enumerate(ex.get("hints", []), 1):
                st.markdown(f"**Pista {i}:** {p}")
    with col_h2:
        with st.expander("🔓 Ver Solución Explicada"):
            st.code(ex["solution"], language="python")


def render_sandbox():
    """Entorno libre de ejecución de Python con Biopython, Pandas y Matplotlib."""
    st.markdown("<div class='main-title'>💻 Laboratorio Libre (Python & Bio Sandbox)</div>", unsafe_allow_html=True)
    st.markdown("Escribe cualquier fragmento de código Python y pruébalo con `Bio`, `pandas`, `requests` o `matplotlib`.")
    
    snippet_default = """from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd

# 1. Crear una secuencia con Biopython (30 nucleótidos = 10 codones completos)
adn = Seq("ATGCGATCGATCGTAGCTAGCTAGCTAGCT")
print("Secuencia:", adn)
print("Reverso complementario:", adn.reverse_complement())
print("Proteína traducida:", adn.translate())

# 2. Cargar datos de expresión de ejemplo
df = pd.read_csv("data/expression_counts.tsv", sep="\\t")
print("\\nPrimeros genes del dataset RNA-seq:")
print(df[["Symbol", "Control_1", "Treated_1"]].head())
"""
    sandbox_key = "sandbox_code"
    if sandbox_key not in st.session_state:
        st.session_state[sandbox_key] = get_sandbox_code(snippet_default)

    code = st.text_area("Editor Sandbox:", value=st.session_state[sandbox_key], height=260, key="sandbox_text_area")
    st.session_state[sandbox_key] = code

    col_s1, col_s2, col_s3 = st.columns([1.3, 1.2, 1])
    with col_s1:
        btn_s_run = st.button("▶ Ejecutar en el Sandbox", type="primary", key="sandbox_run")
    with col_s2:
        btn_s_save = st.button("💾 Guardar Script", key="sandbox_save")
    with col_s3:
        btn_s_reset = st.button("🔄 Restaurar Ejemplo", key="sandbox_reset")

    if btn_s_save:
        save_sandbox_code(code)
        st.success("💾 ¡Script del sandbox guardado con éxito! Se cargará la próxima vez que entres.")

    if btn_s_reset:
        st.session_state[sandbox_key] = snippet_default
        save_sandbox_code(snippet_default)
        st.rerun()

    if btn_s_run:
        save_sandbox_code(code)
        res = execute_code(code)
        if res["stdout"]:
            st.markdown("##### 📤 Salida:")
            st.code(res["stdout"], language="text")
        if res.get("warnings"):
            st.warning(res["warnings"])
        if res["stderr"]:
            st.error(res["stderr"])


def render_ncbi_explorer():
    """Explorador interactivo en vivo de NCBI Entrez E-utilities."""
    st.markdown("<div class='main-title'>🌐 Explorador NCBI Entrez (E-utilities)</div>", unsafe_allow_html=True)
    st.markdown("Consulta y descarga registros de nucleótidos y proteínas directamente desde NCBI (GenBank, RefSeq).")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Buscar en NCBI (Gen, Organismo o Accession):", value="HBB[Gene] AND human[Organism]")
    with col2:
        db = st.selectbox("Base de datos:", ["nucleotide", "protein"])
        
    if st.button("🔍 Buscar en NCBI"):
        with st.spinner("Consultando servidores de NCBI E-utilities..."):
            results = search_ncbi(query, db=db, retmax=5)
            
        if results:
            st.success(f"Se encontraron {len(results)} registros:")
            for item in results:
                with st.expander(f"📄 {item.get('title', item.get('id'))}"):
                    st.write(f"**ID/Accession:** `{item.get('accession', item.get('id'))}` | **Organismo:** `{item.get('organism')}` | **Longitud:** `{item.get('length')} pb/aa`")
                    if st.button("📥 Descargar FASTA", key=f"fetch_{item.get('id')}"):
                        fasta = fetch_ncbi_fasta(item.get("accession", item.get("id")), db=db)
                        st.code(fasta, language="text")
        else:
            st.info("No se encontraron registros. Prueba con IDs modelo como `NM_000518.5` o `NC_045512.2`.")


def render_uniprot_explorer():
    """Explorador interactivo de UniProtKB."""
    st.markdown("<div class='main-title'>🔬 Explorador UniProtKB</div>", unsafe_allow_html=True)
    st.markdown("Descubre anotaciones biológicas curadas de proteínas humanas y de organismos modelo.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Buscar proteína en UniProt (ID, Gen o Nombre):", value="P01308")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_search = st.button("🔍 Buscar en UniProt")
        
    if btn_search or query:
        # Si parece un accession directo de 6 caracteres
        clean_q = query.strip().upper()
        entry = get_uniprot_entry(clean_q)
        if entry:
            st.success(f"Proteína encontrada: **{entry['protein_name']}** ({entry['gene']})")
            c1, c2, c3 = st.columns(3)
            c1.metric("Longitud (aa)", entry["length"])
            c2.metric("Masa Molecular (Da)", f"{entry['mass']:,}")
            c3.metric("Organismo", entry["organism"])
            
            st.markdown(f"**Función Biológica:**\n> {entry['function']}")
            st.markdown(f"**Localización Subcelular:** `{entry['subcellular_location']}`")
            
            if entry.get("go_terms"):
                st.markdown("**Términos de Gene Ontology (GO):**")
                df_go = pd.DataFrame(entry["go_terms"])
                st.dataframe(df_go, use_container_width=True)
                
            with st.expander("Ver Secuencia Primaria de Aminoácidos"):
                st.code(entry["sequence"], language="text")
        else:
            # Búsqueda general
            results = search_uniprot(query, limit=5)
            if results:
                st.write(f"Resultados encontrados para '{query}':")
                for r in results:
                    st.write(f"- **`{r['accession']}`** - {r['protein_name']} (*{r['organism']}*) | Gen: `{r['gene']}`")
            else:
                st.info("Prueba con proteínas modelo como `P01308` (Insulina), `P68871` (Hemoglobina) o `P04637` (p53).")


def render_ols_explorer():
    """Explorador de Ontologías Biomédicas de EMBL-EBI OLS."""
    st.markdown("<div class='main-title'>🌳 Explorador EMBL-EBI OLS (Ontologías)</div>", unsafe_allow_html=True)
    st.markdown("Busca términos en Gene Ontology (GO), Disease Ontology (DOID) y Human Phenotype (HP).")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Término a buscar:", value="apoptosis")
    with col2:
        ont = st.selectbox("Ontología:", ["Todas", "go", "doid", "hp"], index=1)
        
    if st.button("🔍 Buscar en OLS"):
        ont_param = None if ont == "Todas" else ont
        results = search_ols(query, ontology=ont_param, rows=5)
        if results:
            for r in results:
                with st.expander(f"📌 [{r['ontology']}] {r['obo_id']}: {r['label']}"):
                    st.markdown(f"**Definición:**\n{r['description']}")
                    if r.get("synonyms"):
                        st.caption(f"Sinónimos: {', '.join(r['synonyms'])}")
        else:
            st.info("No se encontraron términos. Prueba con 'diabetes', 'DNA repair' o 'oxygen transport'.")


def render_tutorial_viewer():
    """Visor y guía del tutorial oficial Biopython v1.83 presente en la carpeta."""
    st.markdown("<div class='main-title'>📖 Guía de Biopython (Tutorial-1.83.pdf)</div>", unsafe_allow_html=True)
    
    pdf_info = get_pdf_status()
    if pdf_info["exists"]:
        st.success(f"Archivo detectado: `{pdf_info['filename']}` ({pdf_info['size_mb']} MB) en el directorio de trabajo.")
    
    st.markdown("Acceso rápido a los capítulos clave del manual oficial con código listo para probar:")
    
    capitulos = get_available_chapters()
    opciones = [f"{cap}: {get_chapter_info(cap)['title']}" for cap in capitulos]
    seleccion = st.selectbox("Selecciona un Capítulo del Tutorial:", opciones)
    cap_num = int(seleccion.split(":")[0])
    
    info = get_chapter_info(cap_num)
    if info:
        st.markdown(f"### {info['title']}")
        st.info(f"📍 **Referencia:** {info['pages']} | {info['pdf_ref']}\n\n{info['summary']}")
        
        st.markdown("#### Conceptos Clave del Capítulo:")
        for kc in info["key_concepts"]:
            st.markdown(f"- {kc}")
            
        st.markdown("#### Ejemplo Práctico extraído del Tutorial:")
        st.code(info["code_example"], language="python")
        
        if st.button("▶ Probar este ejemplo en el Sandbox"):
            res = execute_code(info["code_example"])
            st.markdown("##### Salida:")
            if res["stdout"]:
                st.code(res["stdout"], language="text")
            if res["stderr"]:
                st.error(res["stderr"])


def render_sample_data_viewer():
    """Visualizador de los archivos biológicos de muestra incluidos en data/."""
    st.markdown("#### 📂 Archivos de Muestra en la Carpeta `data/`")
    archivos = ["data/sample_dna.fasta", "data/sample_reads.fastq", "data/sample_record.gb", "data/expression_counts.tsv"]
    archivo_sel = st.selectbox("Elige un archivo biológico para inspeccionar:", archivos)
    
    p = Path(archivo_sel)
    if p.exists():
        contenido = p.read_text(encoding="utf-8")
        st.caption(f"Ruta: `{p.resolve()}` | Tamaño: {len(contenido)} caracteres")
        if archivo_sel.endswith(".tsv"):
            df = pd.read_csv(p, sep="\t")
            st.dataframe(df, width="stretch")
        else:
            st.code(contenido[:1500] + ("\n... [Contenido truncado para previsualización]" if len(contenido) > 1500 else ""), language="text")
    else:
        st.warning(f"Archivo {archivo_sel} no encontrado.")


def inject_code_editor_enhancements():
    """
    Inyecta comportamiento de editor de código en los textareas de Streamlit:
    1. Al presionar Enter tras dos puntos ':', sangra la nueva línea con 4 espacios automáticamente.
    2. Conserva la sangría de la línea anterior en saltos normales.
    3. Al presionar Tab, inserta 4 espacios en vez de cambiar de foco.
    """
    js_code = """
    <script>
    (function() {
        function setupEditorKeys() {
            try {
                const parentDoc = window.parent.document;
                const textareas = parentDoc.querySelectorAll('textarea');
                textareas.forEach(ta => {
                    if (ta.dataset.autoindentAttached === "true") return;
                    ta.dataset.autoindentAttached = "true";
                    
                    ta.addEventListener('keydown', function(e) {
                        // 1. Tecla Tab -> 4 espacios
                        if (e.key === 'Tab') {
                            e.preventDefault();
                            const start = this.selectionStart;
                            const end = this.selectionEnd;
                            const value = this.value;
                            const newValue = value.substring(0, start) + "    " + value.substring(end);
                            
                            const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                            if (setter) {
                                setter.call(this, newValue);
                            } else {
                                this.value = newValue;
                            }
                            this.dispatchEvent(new Event('input', { bubbles: true }));
                            this.selectionStart = this.selectionEnd = start + 4;
                            return;
                        }
                        
                        // 2. Tecla Enter tras ':' o con sangría previa
                        if (e.key === 'Enter') {
                            const start = this.selectionStart;
                            const value = this.value;
                            
                            // Texto de la línea actual hasta el cursor
                            const lastNewline = value.lastIndexOf('\\n', start - 1);
                            const currentLine = value.substring(lastNewline + 1, start);
                            
                            // Detectar sangría actual
                            const indentMatch = currentLine.match(/^[ ]*/);
                            const currentIndent = indentMatch ? indentMatch[0] : "";
                            
                            // Si la línea termina en ':', sumar 4 espacios de sangría
                            const trimmedLine = currentLine.trimEnd();
                            const extraIndent = trimmedLine.endsWith(':') ? "    " : "";
                            const totalIndent = currentIndent + extraIndent;
                            
                            if (totalIndent.length > 0) {
                                e.preventDefault();
                                const end = this.selectionEnd;
                                const insertText = "\\n" + totalIndent;
                                const newValue = value.substring(0, start) + insertText + value.substring(end);
                                
                                const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                                if (setter) {
                                    setter.call(this, newValue);
                                } else {
                                    this.value = newValue;
                                }
                                this.dispatchEvent(new Event('input', { bubbles: true }));
                                this.selectionStart = this.selectionEnd = start + insertText.length;
                            }
                        }
                    });
                });
            } catch(err) {
                // Silencioso
            }
        }
        setInterval(setupEditorKeys, 300);
    })();
    </script>
    """
    components.html(js_code, height=0, width=0)


def main():
    inject_code_editor_enhancements()
    modo = render_sidebar()
    
    if "Curso Modular" in modo:
        render_course_module()
    elif "Sandbox" in modo:
        render_sandbox()
    elif "NCBI" in modo:
        render_ncbi_explorer()
    elif "UniProtKB" in modo:
        render_uniprot_explorer()
    elif "EMBL-EBI" in modo:
        render_ols_explorer()
    elif "Tutorial Biopython" in modo:
        render_tutorial_viewer()


if __name__ == "__main__":
    main()
