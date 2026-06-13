import streamlit as st
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant in hg38 as e.g. chr11 108325416 C T or chr11-108325416 C>T")

# -----------------------------
# INIT SESSION STATE
# -----------------------------
if "data" not in st.session_state:
    st.session_state["data"] = None

# -----------------------------
# INPUT
# -----------------------------
import re

variant_input = st.text_input(
    "Variant",
    placeholder="chr11-108325416 C>T"
)

chromosome = position = reference = alternate = None

if variant_input:

    text = variant_input.strip()

    # Format: chr11-108325416 C>T
    m = re.match(
        r"^(chr[\w]+)-(\d+)\s+([ACGT]+)>([ACGT]+)$",
        text,
        re.IGNORECASE
    )

    if m:
        chromosome, position, reference, alternate = m.groups()

    else:
        # Format: chr11 108325416 C T
        parts = text.replace(",", " ").split()

        if len(parts) == 4:
            chromosome, position, reference, alternate = parts
        else:
            st.error(
                "Use either:\n"
                "chr11-108325416 C>T\n"
                "or\n"
                "chr11 108325416 C T"
            )
# -----------------------------
# API
# -----------------------------
base_url = "https://api.genebe.net/cloud/api-public/v1/variant"

params = {
    "chr": chromosome if chromosome and chromosome.startswith("chr") else f"chr{chromosome}" if chromosome else "",
    "pos": position or "",
    "ref": reference or "",
    "alt": alternate or "",
    "useRefseq": "true",
    "useEnsembl": "true",
    "omitAcmg": "false",
    "omitCsq": "false",
    "genome": "hg38"
}
# -----------------------------
# CLINVAR API
# -----------------------------
def fetch_clinvar_json(query: str):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    # 1. search
    search = requests.get(
        base + "esearch.fcgi",
        params={"db": "clinvar", "term": query, "retmode": "json", "retmax": 5},
        timeout=15
    ).json()

    ids = search.get("esearchresult", {}).get("idlist", [])

    if not ids:
        return {"search": search, "summary": None}

    # 2. summary (THIS is JSON)
    summary = requests.get(
        base + "esummary.fcgi",
        params={"db": "clinvar", "id": ",".join(ids), "retmode": "json"},
        timeout=15
    ).json()

    return {
        "search": search,
        "summary": summary
    }
def fetch_clinvar_counts(query: str):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    search = requests.get(
        base + "esearch.fcgi",
        params={"db": "clinvar", "term": query, "retmode": "json", "retmax": 5},
        timeout=15
    ).json()

    ids = search.get("esearchresult", {}).get("idlist", [])

    if not ids:
        return {"P": 0, "LP": 0, "VUS": 0, "O": 0}

    p = lp = vus = o = 0

    for clinvar_id in ids[:5]:

        fetch = requests.get(
            base + "efetch.fcgi",
            params={"db": "clinvar", "id": clinvar_id, "retmode": "xml"},
            timeout=15
        )

        try:
            root = ET.fromstring(fetch.text)
        except Exception:
            continue

        for sig in root.findall(".//ClinicalSignificance/Description"):
            if sig.text is None:
                continue

            val = sig.text.lower()

            if val == "pathogenic":
                p += 1
            elif "likely pathogenic" in val:
                lp += 1
            elif "uncertain" in val:
                vus += 1
            elif "benign" in val:
                o += 1
            else:
                o += 1

    return {"P": p, "LP": lp, "VUS": vus, "O": o}
    
# -----------------------------
# FETCH
# -----------------------------
if st.button("Retrieve ACMG Information"):

    if not all([chromosome, position, reference, alternate]):
        st.error("Please enter a valid variant.")
        st.stop()

    try:
        response = requests.get(base_url, params=params, timeout=15)

        if response.status_code != 200:
            st.error(f"API error: {response.status_code}")
            st.text(response.text[:500])
            st.stop()

        data = response.json()
        st.session_state["data"] = data

        variant = data.get("variants", [{}])[0]

        # IMPORTANT FIX: correct consequence extraction
        csq = variant.get("consequences", [{}])[0]

        effects = csq.get("consequences", []) or csq.get("effects", [])

        # -----------------------------
        # TYPE DETECTION
        # -----------------------------
        is_frameshift = "frameshift_variant" in effects
        is_nonsense = "stop_gained" in effects
        is_missense = "missense_variant" in effects

        if is_frameshift:
            variant_type = "frameshift"
        elif is_nonsense:
            variant_type = "nonsense"
        elif is_missense:
            variant_type = "missense"
        else:
            st.info("No supported variant type detected.")
            st.stop()

        # -----------------------------
        # CORE FIELDS
        # -----------------------------
        gene = csq.get("gene_symbol", variant.get("gene_symbol", "UnknownGene"))
        #transcript = csq.get("transcript", csq.get("feature", "NA"))
        transcript = variant.get("transcript",csq.get("transcript", csq.get("feature", "NA")))


        hgvs_c = csq.get("hgvs_c", "NA")
        hgvs_p = csq.get("hgvs_p", "NA")

        exon_rank = csq.get("exon_rank")
        exon_count = csq.get("exon_count")

        acmg = variant.get("acmg_classification", "NA")
        acmg_criteria = variant.get("acmg_criteria", "NA").replace(",", ", ")

        gene_md = f"*{gene}*"
        hgvs_md = f"{transcript}:{hgvs_c}, p({hgvs_p})"

        exon_text = (
            f"Exon {exon_rank} von {exon_count}"
            if exon_rank and exon_count
            else "Exon XX von XX"
        )

        # -----------------------------
        # ClinVar parsing
        # -----------------------------
        #clinvar_summary = variant.get("clinvar_submissions_summary", "")

        #p = us = o = "0"

        #for item in clinvar_summary.split():
            #if item.startswith("P:"):
               # p = item.replace("P:", "")
            #elif item.startswith("US:"):
             #   us = item.replace("US:", "")
            #elif item.startswith("O:"):
              #  o = item.replace("O:", "")
        #clinvar_data = fetch_clinvar_counts(f"{chromosome} {position} {reference} {alternate}")
        #query = csq.get("hgvs_c", f"{gene} {chromosome}:{position}{reference}>{alternate}")
        query = f"{transcript}:{hgvs_c}"
        clinvar_data = fetch_clinvar_counts(query)
        clinvar_json = fetch_clinvar_json(query)
       

        p = clinvar_data["P"]
        lp = clinvar_data["LP"]
        vus = clinvar_data["VUS"]
        o = clinvar_data["O"]
        clinvar_text = (
            f"Diese Variante wurde in ClinVar {p}× pathogen, {lp}× wahrscheinlich pathogen, {vus}× unklar, {o}× benign/sonstige klassifiziert."
        )
        #clinvar_text = (
         #   f"Diese Variante wurde in ClinVar {p}× pathogen, {us}× unklar, {o}× benign/sonstige klassifiziert."
        #)

        # -----------------------------
        # gnomAD
        # -----------------------------
        af = variant.get("frequency_reference_population")

        gnomad_text = (
            f"In der Populationsdatenbank gnomAD v4.1.1 beträgt die Allelfrequenz {af}."
            if af
            else "In der Populationsdatenbank gnomAD v4.1.1 ist die Variante nicht vorhanden."
        )

        # -----------------------------
        # REPORT TEMPLATES
        # -----------------------------
        if variant_type == "frameshift":

            report = f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. Leseraster-Variante im {gene_md}-Gen ({hgvs_md}) führt durch eine Leserasterverschiebung (Frameshift) zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins in {exon_text}.

[NMD] Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet, da mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden muss.
[ODER][kein NMD]Am ehesten wird ein C-terminal [um >10%] verkürztes, möglicherweise // wahrscheinlich funktionsverändertes Protein gebildet [, da es zum Verlust der funktionell kritischen XXX-Domäne kommt (PMID XXX)]. Hingegen muss nicht mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden (PMID: 33277042).

Eine tatsächliche Auswirkung der Variante wurde bislang nicht funktionell untersucht. 
[ODER] Eine tatsächliche Auswirkung der Variante wurde durch funktionelle Untersuchungen bestätigt (PMID XXX). 

{clinvar_text}
{gnomad_text}

Gemäß aktuellen ClinGen-/ACMG-Empfehlungen zur Variantenbewertung (PMIDs 25741868, 30192042) sind die Kriterien({acmg_criteria}) erfüllt, sodass sich eine Bewertung als {acmg} ergibt.
"""

        elif variant_type == "nonsense":

            report = f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. Nonsense-Variante im {gene_md}-Gen ({hgvs_md}) führt zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins in {exon_text}.

[NMD] Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet, da mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden muss.
[ODER][kein NMD]Am ehesten wird ein C-terminal [um >10%] verkürztes, möglicherweise // wahrscheinlich funktionsverändertes Protein gebildet [, da es zum Verlust der funktionell kritischen XXX-Domäne kommt (PMID XXX)]. Hingegen muss nicht mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden (PMID: 33277042).

Eine tatsächliche Auswirkung der Variante wurde bislang nicht funktionell untersucht. 
[ODER] Eine tatsächliche Auswirkung der Variante wurde durch funktionelle Untersuchungen bestätigt (PMID XXX). 

{clinvar_text}
{gnomad_text}

Gemäß aktuellen ClinGen-/ACMG-Empfehlungen zur Variantenbewertung (PMIDs 25741868, 30192042) sind die Kriterien({acmg_criteria}) erfüllt, sodass sich eine Bewertung als {acmg} ergibt.
"""

        elif variant_type == "missense":
            # -----------------------------
            # COMPUTATIONAL SCORES
            # -----------------------------
            revel = variant.get("revel_score")
            alphamissense = variant.get("alphamissense_score")
            comp_call = variant.get("computational_prediction_selected")

            # choose score source
            if revel is not None:
                score_text = f"REVEL-Score {revel} (PMID: 27666373)"
            elif alphamissense is not None:
                score_text = f"AlphaMissense-Score {alphamissense} (PMID: 37733863)"
            else:
                score_text = "kein verfügbarer Score"

            # map computational prediction into German phrasing if present
            comp_map = {
        "Pathogenic": "hoch wahrscheinlich",
        "Likely pathogenic": "moderat wahrscheinlich",
        "Benign": "unwahrscheinlich",
        "Likely benign": "niedrig wahrscheinlich",
        "Uncertain significance": "unklar"}
            comp_class = comp_map.get(comp_call, "unklar")

            report = f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. Missense-Variante im {gene_md}-Gen ({hgvs_md}) führt zu einem Aminosäureaustausch im korrespondierenden Protein.

[Das Gen weist empirisch eine // keine signifikante Intoleranz gegenüber genetischer Variation auf (Z-Score >3,09 // <3,10, PMID: 27535533). für PP2 nur alleine verwenden wenn lt. spezifischer VCEP zulässig, sonst zusätzlich regionaler Constraint erforderlich (s.u.)]
[ODER]
[Das Gen weist empirisch zwar eine allgemein, die betroffene Proteindomäne jedoch keine regional signifikante Intoleranz gegenüber genetischer Variation auf (Z-Score >3,09, PMID: 27535533; MCR missense OE > 0,37, PMID: 38645134) [ODER] MetaDome dN/dS-Score >0,52, PMID: 31116477).] 
[ODER]
[Das Gen und die betroffene Proteindomäne weisen empirisch eine signifikante Intoleranz gegenüber genetischer Variation auf (Z-Score >3,09 PMID: 27535533; MCR missense OE ≤ 0,37, PMID: 38645134) [ODER] MetaDome dN/dS-Score <0,53, PMID: 31116477).]
[ggf. PM1 ergänzen] 

Die bioinformatische Proteineffektprädiktion beurteilt eine Pathogenität der Variante als {comp_class} ({score_text}).

Eine tatsächliche Auswirkung der Variante wurde bislang nicht funktionell untersucht. 
[ODER] Eine tatsächliche Auswirkung der Variante wurde durch funktionelle Untersuchungen bestätigt (PMID XXX). 

{clinvar_text}
{gnomad_text}

Gemäß aktuellen ClinGen-/ACMG-Empfehlungen zur Variantenbewertung (PMIDs 25741868, 30192042) sind die Kriterien({acmg_criteria}) erfüllt, sodass sich eine Bewertung als {acmg} ergibt.
"""
        # -----------------------------
        # OUTPUT (ONLY HERE!)
        # -----------------------------
        st.subheader("🧬 Klinischer Bericht")
        st.write(report)

    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")

# -----------------------------
# RAW JSON VIEW BUTTON
# -----------------------------
if st.button("Show ClinVar JSON"):

    if not all([chromosome, position, reference, alternate]):
        st.warning("Enter a variant first.")
        st.stop()

    variant = st.session_state.get("variant", {})
    csq = st.session_state.get("csq", {})

    gene = csq.get("gene_symbol", "UnknownGene")
    hgvs_c = csq.get("hgvs_c", "NA")

    query = f"{transcript}:{hgvs_c}"

    clinvar_json = fetch_clinvar_json(query)

    st.subheader("🧬 ClinVar JSON (ESearch + ESummary)")
    st.json(clinvar_json)

    clinvar_json = fetch_clinvar_json(query)

    st.subheader("🧬 ClinVar JSON (ESearch + ESummary)")
    st.json(clinvar_json)
