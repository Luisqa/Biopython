"""
Cliente ligero para interactuar con NCBI Entrez E-utilities (efetch, esearch).
Inspirado en el skill ncbi-sequence-fetch y Bio.Entrez.
Incluye soporte para caché y modo offline con datos biológicos reales.
"""

import time
import requests
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# Base de datos local offline de respaldo para pruebas rápidas sin conexión
LOCAL_NCBI_CACHE = {
    "NM_000518.5": {
        "title": "Homo sapiens hemoglobin subunit beta (HBB), mRNA",
        "length": 628,
        "organism": "Homo sapiens",
        "fasta": ">NM_000518.5 Homo sapiens hemoglobin subunit beta (HBB), mRNA\nACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACCATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGGACCCAGAGGTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGGCAACCCTAAGGTGAAGGCTCATGGCAAGAAAGTGCTCGGTGCCTTTAGTGATGGCCTGGCTCACCTGGACAACCTCAAGGGCACCTTTGCCACACTGAGTGAGCTGCACTGTGACAAGCTGCACGTGGATCCTGAGAACTTCAGGCTCCTGGGCAACGTGCTGGTCTGTGTGCTGGCCCATCACTTTGGCAAAGAATTCACCCCACCAGTGCAGGCTGCCTATCAGAAAGTGGTGGCTGGTGTGGCTAATGCCCTGGCCCACAAGTATCACTAAGCTCGCTTTCTTGCTGTCCAATTTCTATTAAAGGTTCCTTTGTTCCCTAAGTCCAACTACTAAACTGGGGGATATTATGAAGGGCCTTGAGCATCTGGATTCTGCCTAATAAAAAACATTTATTTTCATTGCAA"
    },
    "NC_045512.2": {
        "title": "Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1, complete genome",
        "length": 29903,
        "organism": "Severe acute respiratory syndrome coronavirus 2",
        "fasta": ">NC_045512.2 Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1 (Fragment)\nATTAAAGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAACGAACTTTAAAATCTGTGTGGCTGTCACTCGGCTGCATGCTTAGTGCACTCACGCAGTATAATTAATAACTAATTACTGTCGTTGACAGGACACGAGTAACTCGTCTATCTTCTGCAGGCTGCTTACGGTTTCGTCCGTGTTGCAGCCGATCATCAGCACATCTAGGTTTCGTCCGGGTGTGACCGAAAGGTAAGATGGAGAGCCTTGTCCCTGGTTTCAACGAGAAAACACACGTCCAACTCAGTTTGCCTGTTTTACAGGTTCGCGACGTGCTCGTACGTGGCTTTGGAGACTCCGTGGAGGAGGTCTTATCAGAGGCACGTCAACATCTTAAAGATGGCACTTGTGGCTTAGTAGAAGTTGAAAAAGGCGTTTTGCCTCAACTTGAACAGCCCTATGTGTTCATCAAACGTTCGGATGCTCGAACTGCACCTCATGGTCATGTTATGGTTGAGCTGGTAGCAGAACTCGAAGGCATTCAGTACGGTCGTAGTGGTGAGACACTTGGTGTCCTTGTCCCTCATGTGGGCGAAATACCAGTGGCTTACCGCAAGGTTCTTCTTCGTAAGAACGGTAATAAAGGAGCTGGTGGCCATAGTTACGGCGCCGATCTAAAGTCATTTGACTTAGGCGACGAGCTTGGCACTGATCCTTATGAAGATTTTCAAGAAAACTGGAACACTAAACATAGCAGTGGTGTTACCCGTGAACTCATGCGTGAGCTTAACGGAGGG"
    },
    "NP_000509.1": {
        "title": "hemoglobin subunit beta [Homo sapiens]",
        "length": 147,
        "organism": "Homo sapiens",
        "fasta": ">NP_000509.1 hemoglobin subunit beta [Homo sapiens]\nMVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH"
    }
}


def search_ncbi(query: str, db: str = "nucleotide", retmax: int = 5, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Busca IDs de registros en NCBI según una consulta de texto o gen.
    """
    params = {
        "db": db,
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    if api_key:
        params["api_key"] = api_key
        
    try:
        resp = requests.get(f"{NCBI_BASE}/esearch.fcgi", params=params, timeout=10)
        time.sleep(0.35)  # Respetar límite de 3 req/seg
        if resp.status_code == 200:
            data = resp.json()
            id_list = data.get("esearchresult", {}).get("idlist", [])
            # Obtener resúmenes (esummary)
            if id_list:
                return get_ncbi_summaries(id_list, db=db, api_key=api_key)
            return []
    except Exception as e:
        # Fallback offline
        results = []
        for acc, item in LOCAL_NCBI_CACHE.items():
            if query.lower() in acc.lower() or query.lower() in item["title"].lower():
                results.append({
                    "id": acc,
                    "title": item["title"],
                    "organism": item["organism"],
                    "length": item["length"]
                })
        return results
    return []


def get_ncbi_summaries(id_list: List[str], db: str = "nucleotide", api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """Obtiene títulos y metadatos de una lista de IDs."""
    params = {
        "db": db,
        "id": ",".join(id_list),
        "retmode": "json"
    }
    if api_key:
        params["api_key"] = api_key
        
    try:
        resp = requests.get(f"{NCBI_BASE}/esummary.fcgi", params=params, timeout=10)
        time.sleep(0.35)
        if resp.status_code == 200:
            data = resp.json().get("result", {})
            summaries = []
            for uid in id_list:
                if uid in data:
                    item = data[uid]
                    summaries.append({
                        "id": uid,
                        "title": item.get("title", ""),
                        "accession": item.get("caption", uid),
                        "organism": item.get("organism", ""),
                        "length": item.get("slen", 0)
                    })
            return summaries
    except Exception:
        pass
    return [{"id": uid, "title": f"Registro {uid}", "accession": uid, "organism": "Desconocido", "length": 0} for uid in id_list]


def fetch_ncbi_fasta(accession_or_id: str, db: str = "nucleotide", api_key: Optional[str] = None) -> str:
    """
    Descarga la secuencia en formato FASTA desde NCBI.
    """
    clean_id = accession_or_id.strip()
    params = {
        "db": db,
        "id": clean_id,
        "rettype": "fasta",
        "retmode": "text"
    }
    if api_key:
        params["api_key"] = api_key
        
    try:
        resp = requests.get(f"{NCBI_BASE}/efetch.fcgi", params=params, timeout=10)
        time.sleep(0.35)
        if resp.status_code == 200 and ">" in resp.text:
            return resp.text.strip()
    except Exception:
        pass
        
    # Verificar en caché offline
    for acc, item in LOCAL_NCBI_CACHE.items():
        if clean_id.lower() in acc.lower() or acc.lower() in clean_id.lower():
            return item["fasta"]
            
    return f">Error_Fallback_{clean_id}\nNo se pudo conectar a NCBI E-utilities. Verifica tu conexión a internet o el ID ingresado."
