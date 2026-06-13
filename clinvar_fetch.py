import streamlit as st
import requests
import xml.etree.ElementTree as ET
import re

st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant in hg38 as e.g. chr11 108325416 C T or chr11-108325416 C>T")

# -----------------------------
# SESSION STATE
# -----------------------------
if "data" not in st.session_state:
    st.session_state["data"] = None
if "variant" not in st.session_state:
    st.session_state["variant"] = None
if "csq" not in st.session_state:
    st.session_state["csq"] = None

# -----------------------------
# INPUT
# -----------------------------
variant_input = st.text_input("Variant", placeholder="chr11-108325416 C>T")

chromosome = position = reference = alternate = None

if variant_input:
    text = variant_input.strip()

    m = re.match(
        r"^(chr[\w]+)-(\d+)\s+([ACGT]+)>([ACGT]+)$",
        text,
        re.IGNORECASE
    )

    if m:
        chromosome, position, reference, alternate = m.groups()
    else:
        parts = text.replace(",", " ").split()
        if len(parts) == 4:
            chromosome, position, reference, alternate = parts
        else:
            st.error("Use chr11-108325416 C>T or chr11 108325416 C T")

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
# CLINVAR API (FIXED QUERY LOGIC)
# -----------------------------
def fetch_clinvar_json(query: str):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    search = requests.get(
        base + "esearch.fcgi",
        params={"db": "clinvar", "term": query, "retmode": "json", "retmax": 10},
        timeout=15
    ).json()

    ids = search.get("esearchresult", {}).get("idlist", [])

    summary = None
    if ids:
        summary = requests.get(
            base + "esummary.fcgi",
            params={"db": "clinvar", "id": ",".join(ids), "retmode": "json"},
            timeout=15
        ).json()

    return {"search": search, "summary": summary}


def fetch_clinvar_counts(query: str):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    search = requests.get(
        base + "esearch.fcgi",
        params={"db": "clinvar", "term": query, "retmode": "json", "retmax": 10},
        timeout=15
    ).json()

    ids = search.get("esearchresult", {}).get("idlist", [])

    if not ids:
        return {"P": 0, "LP": 0, "VUS": 0, "O": 0}, search

    p = lp = vus = o = 0

    for cid in ids[:5]:
        fetch = requests.get(
            base + "efetch.fcgi",
            params={"db": "clinvar", "id": cid, "retmode": "xml"},
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

            if "pathogenic" == val:
                p += 1
            elif "likely pathogenic" in val:
                lp += 1
            elif "uncertain" in val:
                vus += 1
            elif "benign" in val:
                o += 1
            else:
                o += 1

    return {"P": p, "LP": lp, "VUS": vus, "O": o}, search


# -----------------------------
# FETCH
# -----------------------------
if st.button("Retrieve ACMG Information"):

    if not all([chromosome, position, reference, alternate]):
        st.error("Invalid variant")
        st.stop()

    response = requests.get(base_url, params=params, timeout=15)

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    data = response.json()
    st.session_state["data"] = data

    variant = data["variants"][0]
    csq = variant.get("consequences", [{}])[0]

    # STORE CORRECTLY
    st.session_state["variant"] = variant
    st.session_state["csq"] = csq

    effects = csq.get("consequences", []) or csq.get("effects", [])

    gene = csq.get("gene_symbol", "UnknownGene")
    transcript = variant.get("transcript", "NA")
    hgvs_c = csq.get("hgvs_c", "NA")

    # -----------------------------
    # FIXED ClinVar QUERY (IMPORTANT)
    # -----------------------------
    clinvar_query = f"{chromosome} {position} {reference} {alternate}"

    clinvar_counts, clinvar_search = fetch_clinvar_counts(clinvar_query)
    clinvar_json = fetch_clinvar_json(clinvar_query)

    st.subheader("🔍 DEBUG ClinVar query")
    st.write(clinvar_query)
    st.json(clinvar_search)

    st.subheader("🧬 ClinVar JSON")
    st.json(clinvar_json)

    st.success("GeneBe + ClinVar fetched successfully")

# -----------------------------
# RAW VIEW
# -----------------------------
if st.button("Show stored GeneBe JSON"):
    st.json(st.session_state.get("data"))
