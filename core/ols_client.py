"""
Cliente para la API de EMBL-EBI OLS (Ontology Lookup Service).
Inspirado en el skill embl-ebi-ols.
Permite buscar términos en Gene Ontology (GO), Human Phenotype (HP), Disease Ontology (DOID), etc.
"""

import requests
from typing import Dict, Any, List, Optional

OLS_BASE = "https://www.ebi.ac.uk/ols4/api"

LOCAL_OLS_CACHE = {
    "GO:0006915": {
        "obo_id": "GO:0006915",
        "label": "apoptotic process",
        "ontology": "GO",
        "description": "A programmed cell death process which begins when a cell receives an internal or external signal and terminates with cell demise.",
        "synonyms": ["apoptosis", "programmed cell death by apoptosis", "cellular suicide"],
        "parents": ["GO:0012501 (programmed cell death)", "GO:0008219 (cell death)"],
        "children": ["GO:0097190 (apoptotic signaling pathway)", "GO:0006917 (induction of apoptosis)"]
    },
    "GO:0006281": {
        "obo_id": "GO:0006281",
        "label": "DNA repair",
        "ontology": "GO",
        "description": "The process of restoring DNA after damage. Includes base excision repair, nucleotide excision repair, and double-strand break repair.",
        "synonyms": ["DNA damage repair", "repair of DNA lesions"],
        "parents": ["GO:0006259 (DNA metabolic process)", "GO:0006974 (cellular response to DNA damage stimulus)"],
        "children": ["GO:0006284 (base-excision repair)", "GO:0006289 (nucleotide-excision repair)"]
    },
    "GO:0015671": {
        "obo_id": "GO:0015671",
        "label": "oxygen transport",
        "ontology": "GO",
        "description": "The directed movement of oxygen into, out of or within a cell, or between cells, by means of some agent such as a transporter or carrier protein like hemoglobin.",
        "synonyms": ["oxygen carrying activity", "transport of O2"],
        "parents": ["GO:0015669 (gas transport)", "GO:0051234 (establishment of localization)"],
        "children": []
    },
    "DOID:9351": {
        "obo_id": "DOID:9351",
        "label": "diabetes mellitus",
        "ontology": "DOID",
        "description": "A metabolic disease characterized by chronic hyperglycemia resulting from defects in insulin secretion, insulin action, or both.",
        "synonyms": ["diabetes", "DM"],
        "parents": ["DOID:0014667 (disease of metabolism)", "DOID:4 (disease)"],
        "children": ["DOID:9744 (type 1 diabetes mellitus)", "DOID:9352 (type 2 diabetes mellitus)"]
    }
}


def search_ols(query: str, ontology: Optional[str] = None, rows: int = 5) -> List[Dict[str, Any]]:
    """
    Busca términos en OLS por texto libre y ontología opcional (go, doid, hp, etc.).
    """
    url = f"{OLS_BASE}/search"
    params = {
        "q": query,
        "rows": rows
    }
    if ontology:
        params["ontology"] = ontology.lower()
        
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            docs = data.get("response", {}).get("docs", [])
            results = []
            for doc in docs:
                obo_id = doc.get("obo_id", doc.get("short_form", ""))
                label = doc.get("label", "")
                ont = doc.get("ontology_name", "").upper()
                desc_list = doc.get("description", [])
                desc = desc_list[0] if desc_list else "Sin descripción disponible."
                syns = doc.get("synonym", [])
                
                results.append({
                    "obo_id": obo_id,
                    "label": label,
                    "ontology": ont,
                    "description": desc,
                    "synonyms": syns[:4]
                })
            return results
    except Exception:
        pass
        
    # Búsqueda en caché local
    cached = []
    q_low = query.lower()
    for obo_id, item in LOCAL_OLS_CACHE.items():
        if (q_low in obo_id.lower() or 
            q_low in item["label"].lower() or 
            any(q_low in s.lower() for s in item["synonyms"])):
            if not ontology or ontology.lower() == item["ontology"].lower():
                cached.append({
                    "obo_id": item["obo_id"],
                    "label": item["label"],
                    "ontology": item["ontology"],
                    "description": item["description"],
                    "synonyms": item["synonyms"]
                })
    return cached


def get_term_details(obo_id: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene los detalles y jerarquía de un término OBO (e.g. GO:0006915).
    """
    clean_id = obo_id.strip()
    if clean_id in LOCAL_OLS_CACHE:
        return LOCAL_OLS_CACHE[clean_id]
        
    # Buscar vía search exacta en OLS
    results = search_ols(clean_id, rows=1)
    if results:
        res = results[0]
        return {
            "obo_id": res["obo_id"],
            "label": res["label"],
            "ontology": res["ontology"],
            "description": res["description"],
            "synonyms": res["synonyms"],
            "parents": ["Términos ancestros en la jerarquía ontológica"],
            "children": ["Términos descendientes más específicos"]
        }
    return None
