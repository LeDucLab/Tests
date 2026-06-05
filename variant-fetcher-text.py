import streamlit as st
import requests

st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant as: chr pos ref alt (e.g. chr1 123456 A T)")

# -----------------------------
# INPUT
# -----------------------------
st.subheader("Variant Input")

variant_input = st.text_input(
    "Variant (chr pos ref alt)",
    placeholder="chr22 28695868 C T"
)

chromosome = position = reference = alternate = None

if variant_input:
    parts = variant_input.strip().replace(",", " ").split()

    if len(parts) != 4:
        st.error("Invalid format. Use: chr pos ref alt")
    else:
        chromosome, position, reference, alternate = parts

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
# FETCH DATA BUTTON
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
        # CORE FIELDS
        # -----------------------------
        gene = variant.get("gene_symbol", "UnknownGene")
        hgvs_c = consequence_block.get("hgvs_c", "NA")
        hgvs_p = consequence_block.get("hgvs_p", "NA")

        exon_rank = consequence_block.get("exon_rank")
        exon_count = consequence_block.get("exon_count")

        acmg = variant.get("acmg_classification", "NA")

        # IMPORTANT: nested consequence list
        consequence_list = consequence_block.get("consequences", [])
        is_frameshift = "frameshift_variant" in consequence_list

        # -----------------------------
        # OUTPUT HEADER
        # -----------------------------
        st.subheader("ACMG Result")

        st.write(f"**Classification:** {acmg}")

        # -----------------------------
        # FRAMESHIFT REPORT
        # -----------------------------
        if is_frameshift:

            exon_text = "Exon XX von XX"
            if exon_rank and exon_count:
                exon_text = f"Exon {exon_rank} von {exon_count}"

            gene_md = f"*{gene}*"
            hgvs_md = f"{hgvs_c}, ({hgvs_p})"

            report = f"""
Die o. g. Leseraster-Variante im {gene_md}-Gen ({hgvs_md}) führt durch eine Leserasterverschiebung (Frameshift) zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins in {exon_text}.

[NMD]Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet, da mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden muss.

[ODER]
Am ehesten wird ein C-terminal [um >10%] verkürztes, möglicherweise // wahrscheinlich funktionsverändertes Protein gebildet [, da es zum Verlust der funktionell kritischen XXX-Domäne kommt (PMID XXX)]. Hingegen muss nicht mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden (PMID: 33277042). 

Eine tatsächliche Auswirkung der Variante wurde bislang nicht funktionell untersucht. // durch funktionelle Untersuchungen bestätigt (PMID XXX). 

Diese Variante wurde in ClinVar als: {variant.get("clinvar_classification","NA")} beschrieben.

In gnomAD wurde die Variante mit einer Allelzahl von {variant.get("allele_count_reference_population","NA")} beobachtet.

Gemäß ACMG-Kriterien ({variant.get("acmg_criteria","NA")}) ergibt sich eine Bewertung als {acmg}.
"""

            st.markdown("### 🧬 Klinischer Bericht (Frameshift)")
            st.write(report)

        else:
            st.info("No frameshift variant detected — no frameshift report generated.")

        # -----------------------------
        # OPTIONAL RAW JSON BUTTON
        # -----------------------------
        with st.expander("Show raw JSON (optional)"):
            st.json(data)

    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
