import streamlit as st
import requests

st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant as: chr pos ref alt (e.g. chr22 28695868 C T)")

# -----------------------------
# INPUT
# -----------------------------
variant_input = st.text_input(
    "Variant (chr pos ref alt)",
    placeholder="chr22 28695868 C T"
)

chromosome = position = reference = alternate = None

if variant_input:
    parts = variant_input.strip().replace(",", " ").split()

    if len(parts) == 4:
        chromosome, position, reference, alternate = parts
    else:
        st.error("Invalid format. Use: chr pos ref alt")

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

        variant = data.get("variants", [{}])[0]
        consequence_block = variant.get("consequences", [{}])[0]

        # -----------------------------
        # CONSEQUENCE TYPE (FIXED)
        # -----------------------------
        consequence_type = ""
        if (
            isinstance(consequence_block, dict)
            and "consequences" in consequence_block
            and consequence_block["consequences"]
        ):
            consequence_type = consequence_block["consequences"][0]

        is_frameshift = consequence_type == "frameshift_variant"

        # -----------------------------
        # CORE FIELDS
        # -----------------------------
        gene = variant.get("gene_symbol", "UnknownGene")
        hgvs_c = consequence_block.get("hgvs_c", "NA")
        hgvs_p = consequence_block.get("hgvs_p", "NA")

        exon_rank = consequence_block.get("exon_rank")
        exon_count = consequence_block.get("exon_count")

        acmg = variant.get("acmg_classification", "NA")

        # -----------------------------
        # ClinVar PARSING (NEW)
        # -----------------------------
        clinvar_summary = variant.get("clinvar_submissions_summary", "")

        clinvar_path = "0"
        clinvar_us = "0"
        clinvar_other = "0"

        if clinvar_summary:
            parts = clinvar_summary.split()

            for p in parts:
                if p.startswith("P:"):
                    clinvar_path = p.replace("P:", "")
                elif p.startswith("US:"):
                    clinvar_us = p.replace("US:", "")
                elif p.startswith("O:"):
                    clinvar_other = p.replace("O:", "")

        clinvar_text = f"""
Diese Variante wurde in der ClinVar-Datenbank bislang mit {clinvar_path} Einträgen als pathogen, mit {clinvar_us} Einträgen als unklare Signifikanz und mit {clinvar_other} Einträgen als benigne bzw. sonstige klassifiziert.
"""

        # -----------------------------
        # OUTPUT
        # -----------------------------
        st.subheader("ACMG Result")
        st.write(f"**Classification:** {acmg}")

        if is_frameshift:

            exon_text = f"Exon {exon_rank} von {exon_count}" if exon_rank and exon_count else "Exon XX von XX"

            gene_md = f"*{gene}*"
            hgvs_md = f"{hgvs_c} ({hgvs_p})"

            report = f"""
Die o. g. Leseraster-Variante im {gene_md}-Gen ({hgvs_md}) führt durch eine Leserasterverschiebung (Frameshift) zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins in {exon_text}.

[NMD]Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet, da mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden muss.

[ODER]
Am ehesten wird ein C-terminal verkürztes, möglicherweise funktionsverändertes Protein gebildet.

{clinvar_text}

Allelzahl gnomAD: {variant.get("allele_count_reference_population","NA")}.

ACMG Kriterien: {variant.get("acmg_criteria","NA")} → Bewertung: {acmg}.
"""

            st.markdown("### 🧬 Klinischer Frameshift-Bericht")
            st.write(report)

        else:
            st.info(f"Kein Frameshift erkannt (Typ: {consequence_type})")

        # -----------------------------
        # RAW JSON (optional only)
        # -----------------------------
        with st.expander("Raw JSON"):
            st.json(data)

    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
