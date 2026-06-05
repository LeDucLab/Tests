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
        acmg_by_gene = variant.get("acmg_by_gene", [{}])[0]

        # -----------------------------
        # CORE DATA
        # -----------------------------
        gene = acmg_by_gene.get("gene_symbol", "UnknownGene")
        transcript = acmg_by_gene.get("transcript", "NA")

        hgvs_c = acmg_by_gene.get("hgvs_c", "NA")
        hgvs_p = acmg_by_gene.get("hgvs_p", "NA")

        hgvs_full = f"{transcript}:{hgvs_c}, p.({hgvs_p.replace('p.', '')})"

        exon_rank = acmg_by_gene.get("exon_rank")
        exon_count = acmg_by_gene.get("exon_count")

        exon_text = (
            f"Exon {exon_rank} von {exon_count}"
            if exon_rank and exon_count
            else "Exon XX von XX"
        )

        gene_md = f"*{gene}*"

        # -----------------------------
        # EFFECTS → VARIANT TYPE
        # -----------------------------
        effects = acmg_by_gene.get("effects", [])
        effects = [e.lower() for e in effects]

        variant_type = None

        if "frameshift_variant" in effects:
            variant_type = "frameshift"
        elif "stop_gained" in effects:
            variant_type = "nonsense"
        elif "missense_variant" in effects:
            variant_type = "missense"

        if not variant_type:
            st.info(f"Unsupported variant type: {effects}")
            st.stop()

        # -----------------------------
        # ACMG DATA
        # -----------------------------
        acmg = acmg_by_gene.get("verdict", "NA")
        acmg_criteria = acmg_by_gene.get("criteria", [])
        acmg_criteria = ", ".join(acmg_criteria)

        # -----------------------------
        # CLINVAR
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
            f"Diese Variante wurde in ClinVar {p}× pathogen, "
            f"{us}× unklare Signifikanz und {o}× benign/sonstige klassifiziert."
        )

        # -----------------------------
        # gnomAD
        # -----------------------------
        af = variant.get("frequency_reference_population")

        gnomad_text = (
            f"In gnomAD ist die Variante mit einer Allelfrequenz von {af} beschrieben."
            if af
            else "In gnomAD ist die Variante nicht oder nur sehr selten beschrieben."
        )

        # -----------------------------
        # REPORTS
        # -----------------------------
        if variant_type == "frameshift":

            report = f"""
Die o. g. Leseraster-Variante im {gene_md}-Gen ({hgvs_full}) führt durch eine Leserasterverschiebung (Frameshift) zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins in {exon_text}.

[NMD] Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet, da mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden muss.

[ODER] Am ehesten wird ein C-terminal verkürztes, möglicherweise funktionsverändertes Protein gebildet.

Eine tatsächliche Auswirkung wurde bislang nicht untersucht.

{clinvar_text}
{gnomad_text}

Gemäß ClinGen-/ACMG-Empfehlungen ({acmg_criteria}) ergibt sich eine Bewertung als {acmg}.
"""

        elif variant_type == "nonsense":

            report = f"""
Die o. g. Nonsense-Variante im {gene_md}-Gen ({hgvs_full}) führt zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins in {exon_text}.

[NMD] Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet, da mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden muss.

[ODER] Am ehesten wird ein C-terminal verkürztes, möglicherweise funktionsverändertes Protein gebildet.

Eine tatsächliche Auswirkung wurde bislang nicht untersucht.

{clinvar_text}
{gnomad_text}

Gemäß ClinGen-/ACMG-Empfehlungen ({acmg_criteria}) ergibt sich eine Bewertung als {acmg}.
"""

        elif variant_type == "missense":

            report = f"""
Die o. g. Missense-Variante im {gene_md}-Gen ({hgvs_full}) führt zu einem Aminosäureaustausch im korrespondierenden Protein.

Eine funktionelle Auswirkung wurde bislang nicht untersucht.

{clinvar_text}
{gnomad_text}

Gemäß ClinGen-/ACMG-Empfehlungen ({acmg_criteria}) ergibt sich eine Bewertung als {acmg}.
"""

        # -----------------------------
        # OUTPUT
        # -----------------------------
        st.subheader("🧬 Klinischer Bericht")
        st.markdown(report)

        with st.expander("Show Raw JSON"):
            st.json(data)

    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
