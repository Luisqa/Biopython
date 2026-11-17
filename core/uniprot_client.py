"""
Cliente para la API REST de UniProt (Knowledgebase UniProtKB).
Inspirado en el skill uniprot-database.
Incluye caché offline para proteínas modelo (Insulina, Hemoglobina, p53, GFP).
"""

import requests
from typing import Dict, Any, List, Optional

UNIPROT_BASE = "https://rest.uniprot.org/uniprotkb"

LOCAL_UNIPROT_CACHE = {
    "P01308": {
        "accession": "P01308",
        "entry_name": "INS_HUMAN",
        "protein_name": "Insulin",
        "gene": "INS",
        "organism": "Homo sapiens (Human)",
        "length": 110,
        "mass": 11981,
        "function": "La insulina disminuye la concentración de glucosa en sangre. Aumenta la permeabilidad celular a monosacáridos, aminoácidos y ácidos grasos.",
        "subcellular_location": "Secreted (Vesícula secretora)",
        "go_terms": [
            {"id": "GO:0005179", "name": "hormone activity", "type": "Molecular Function"},
            {"id": "GO:0005576", "name": "extracellular region", "type": "Cellular Component"},
            {"id": "GO:0008283", "name": "cell population proliferation", "type": "Biological Process"},
            {"id": "GO:0006006", "name": "glucose metabolic process", "type": "Biological Process"}
        ],
        "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
    },
    "P68871": {
        "accession": "P68871",
        "entry_name": "HBB_HUMAN",
        "protein_name": "Hemoglobin subunit beta",
        "gene": "HBB",
        "organism": "Homo sapiens (Human)",
        "length": 147,
        "mass": 15998,
        "function": "Participa en el transporte de oxígeno desde los pulmones a los tejidos periféricos. Las mutaciones causan anemia falciforme y beta-talasemia.",
        "subcellular_location": "Cytoplasm",
        "go_terms": [
            {"id": "GO:0005344", "name": "oxygen carrier activity", "type": "Molecular Function"},
            {"id": "GO:0020037", "name": "heme binding", "type": "Molecular Function"},
            {"id": "GO:0015671", "name": "oxygen transport", "type": "Biological Process"}
        ],
        "sequence": "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH"
    },
    "P04637": {
        "accession": "P04637",
        "entry_name": "P53_HUMAN",
        "protein_name": "Cellular tumor antigen p53",
        "gene": "TP53",
        "organism": "Homo sapiens (Human)",
        "length": 393,
        "mass": 43653,
        "function": "Supresor tumoral 'guardián del genoma'. Regula el ciclo celular, induciendo detención en G1/S o apoptosis en respuesta a daño en el ADN.",
        "subcellular_location": "Nucleus, Cytoplasm, Mitochondrion",
        "go_terms": [
            {"id": "GO:0003677", "name": "DNA binding", "type": "Molecular Function"},
            {"id": "GO:0006915", "name": "apoptotic process", "type": "Biological Process"},
            {"id": "GO:0006281", "name": "DNA repair", "type": "Biological Process"}
        ],
        "sequence": "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHERCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENLRKKGEPHHELPPGSTKRALPNNTSSSPQPKKKPLDGEYFTLQIRGRERFEMFRELNEALELKDAQAGKEPGGSRAHSSHLKSKKGQSTSRHKKLMFKTEGPDSD"
    }
}


def search_uniprot(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Busca entradas en UniProtKB según texto libre, símbolo de gen o nombre de proteína.
    """
    url = f"{UNIPROT_BASE}/search"
    params = {
        "query": query,
        "format": "json",
        "size": limit,
        "fields": "accession,id,protein_name,gene_names,organism_name,length"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            results = []
            for item in data.get("results", []):
                acc = item.get("primaryAccession", "")
                entry_name = item.get("uniProtkbId", "")
                
                # Nombre de proteína
                p_desc = item.get("proteinDescription", {})
                p_name = "Desconocido"
                if "recommendedName" in p_desc:
                    p_name = p_desc["recommendedName"].get("fullName", {}).get("value", "")
                elif "submissionNames" in p_desc and p_desc["submissionNames"]:
                    p_name = p_desc["submissionNames"][0].get("fullName", {}).get("value", "")
                    
                # Genes
                genes = [g.get("geneName", {}).get("value", "") for g in item.get("genes", []) if "geneName" in g]
                gene_str = ", ".join(genes) if genes else "N/A"
                
                org = item.get("organism", {}).get("scientificName", "")
                length = item.get("sequence", {}).get("length", 0)
                
                results.append({
                    "accession": acc,
                    "entry_name": entry_name,
                    "protein_name": p_name,
                    "gene": gene_str,
                    "organism": org,
                    "length": length
                })
            return results
    except Exception:
        pass
        
    # Búsqueda en caché local
    cached = []
    q_low = query.lower()
    for acc, val in LOCAL_UNIPROT_CACHE.items():
        if (q_low in acc.lower() or 
            q_low in val["entry_name"].lower() or 
            q_low in val["protein_name"].lower() or 
            q_low in val["gene"].lower()):
            cached.append({
                "accession": val["accession"],
                "entry_name": val["entry_name"],
                "protein_name": val["protein_name"],
                "gene": val["gene"],
                "organism": val["organism"],
                "length": val["length"]
            })
    return cached


def get_uniprot_entry(accession: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene los detalles completos de una proteína (función, localización, GO, secuencia).
    """
    clean_acc = accession.strip().upper()
    
    # Comprobar primero en caché
    if clean_acc in LOCAL_UNIPROT_CACHE:
        return LOCAL_UNIPROT_CACHE[clean_acc]
        
    url = f"{UNIPROT_BASE}/{clean_acc}.json"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            item = resp.json()
            
            p_desc = item.get("proteinDescription", {})
            p_name = "Proteína sin nombre"
            if "recommendedName" in p_desc:
                p_name = p_desc["recommendedName"].get("fullName", {}).get("value", "")
                
            genes = [g.get("geneName", {}).get("value", "") for g in item.get("genes", []) if "geneName" in g]
            gene_str = ", ".join(genes) if genes else "N/A"
            
            org = item.get("organism", {}).get("scientificName", "")
            seq_info = item.get("sequence", {})
            seq = seq_info.get("value", "")
            mass = seq_info.get("molWeight", 0)
            
            # Extraer función
            comments = item.get("comments", [])
            function_text = "Función no especificada en el resumen."
            subcell_text = "No indicada"
            for c in comments:
                if c.get("commentType") == "FUNCTION":
                    texts = [t.get("value", "") for t in c.get("texts", [])]
                    if texts:
                        function_text = " ".join(texts)
                elif c.get("commentType") == "SUBCELLULAR LOCATION":
                    locs = [sub.get("location", {}).get("value", "") for sub in c.get("subcellularLocations", [])]
                    if locs:
                        subcell_text = ", ".join(locs)
                        
            # GO terms
            go_terms = []
            for xref in item.get("uniProtKBCrossReferences", []):
                if xref.get("database") == "GO":
                    go_id = xref.get("id", "")
                    term_name = "GO Term"
                    term_type = "GO"
                    for prop in xref.get("properties", []):
                        if prop.get("key") == "GoTerm":
                            term_name = prop.get("value", "")
                            if term_name.startswith("F:"):
                                term_type = "Molecular Function"
                                term_name = term_name[2:]
                            elif term_name.startswith("P:"):
                                term_type = "Biological Process"
                                term_name = term_name[2:]
                            elif term_name.startswith("C:"):
                                term_type = "Cellular Component"
                                term_name = term_name[2:]
                    go_terms.append({"id": go_id, "name": term_name, "type": term_type})
                    
            return {
                "accession": clean_acc,
                "entry_name": item.get("uniProtkbId", clean_acc),
                "protein_name": p_name,
                "gene": gene_str,
                "organism": org,
                "length": len(seq),
                "mass": mass,
                "function": function_text,
                "subcellular_location": subcell_text,
                "go_terms": go_terms[:10],
                "sequence": seq
            }
    except Exception:
        pass
        
    return None
