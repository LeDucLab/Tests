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
        # CONSEQUENCE TYPE FIX
        # -----------------------------
        consequence_list = consequence_block.get("consequences", [])

        is_frameshift = "frameshift_variant" in consequence_list
        is_nonsense = "stop_gained" in consequence_list
        is_missense = "missense_variant" in consequence_list

        # fallback safety
        variant_type = None
        if is_frameshift:
            variant_type = "frameshift"
        elif is_nonsense:
            variant_type = "nonsense"
        elif is_missense:
            variant_type = "missense"

        if not variant_type:
            st.info("No supported consequence detected (frameshift, nonsense, missense).")
            st.stop()

        # -----------------------------
        # CORE FIELDS
        # -----------------------------
        gene = consequence_block.get(
            "gene_symbol",
            variant.get("gene_symbol", "UnknownGene")
        )

        hgvs_c = consequence_block.get("hgvs_c", "NA")
        hgvs_p = consequence_block.get("hgvs_p", "NA")

        exon_rank = consequence_block.get("exon_rank")
        exon_count = consequence_block.get("exon_count")

        acmg = variant.get("acmg_classification", "NA")
        acmg_criteria = variant.get("acmg_criteria", "NA").replace(",", ", ")

        gene_md = f"*{gene}*"
        hgvs_md = f"{hgvs_c}, {hgvs_p}"
        exon_text = f"Exon {exon_rank} von {exon_count}" if exon_rank and exon_count else "Exon XX von XX"

        # -----------------------------
        # ClinVar
        # -----------------------------
        clinvar_summary = variant.get("clinvar_submissions_summary", "")

        p = us = o = "0"

        for item in clinvar_summary.split():
            if item.startswith("P:"):
                p = item.replace("P:", "")
            elif item.startswith("US:"):
                us = item.replace("US:", "")
            elif item.startswith("O:"):
                o = item.replace("O:", "")

        clinvar_text = (
            f"Diese Variante wurde in ClinVar {p}× pathogen, {us}× VUS, {o}× benign/sonstige klassifiziert."
        )

        # -----------------------------
        # gnomAD
        # -----------------------------
        af = variant.get("frequency_reference_population")
        gnomad_text = (
            f"In gnomAD ist die Variante mit AF {af} beschrieben."
            if af else
            "In gnomAD ist die Variante nicht oder sehr selten beschrieben."
        )

        # -----------------------------
        # REPORT TEMPLATES
        # -----------------------------

        if variant_type in ["frameshift", "nonsense"]:

            variant_label = (
                "Leseraster-Variante (Frameshift)"
                if variant_type == "frameshift"
                else "Nonsense-Variante"
            )

            report = f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. {variant_label} im {gene_md}-Gen ({hgvs_md}) führt zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins in {exon_text}.

[NMD] Sehr wahrscheinlich kommt es zu Nonsense-Mediated mRNA Decay (NMD).
[ODER] Alternativ kann ein C-terminal verkürztes Protein entstehen.

Eine funktionelle Auswirkung wurde bislang nicht untersucht.
{clinvar_text}
{gnomad_text}

Gemäß ClinGen-/ACMG-Kriterien ({acmg_criteria}) ergibt sich eine Bewertung als {acmg}.
"""

        # -----------------------------
        # MISSENSE TEMPLATE (BASIC SCAFFOLD)
        # -----------------------------
        elif variant_type == "missense":

            consequence = "Missense-Variante"

            report = f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. {consequence} im {gene_md}-Gen ({hgvs_md}) führt zu einem Aminosäureaustausch im korrespondierenden Protein.

Die funktionelle Relevanz hängt von Domäne, Konservierung und Strukturkontext ab.
Eine funktionelle Auswirkung wurde bislang nicht untersucht.

{clinvar_text}
{gnomad_text}

Gemäß ClinGen-/ACMG-Kriterien ({acmg_criteria}) ergibt sich eine Bewertung als {acmg}.
"""

        # -----------------------------
        # OUTPUT
        # -----------------------------
        st.subheader("🧬 Klinischer Bericht")
        st.write(report)

        # raw JSON
        with st.expander("Show Raw JSON"):
            st.json(data)

    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
