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

        # ✅ STORE IN SESSION STATE (IMPORTANT FIX)
        st.session_state["data"] = response.json()
        data = st.session_state["data"]

        variant = data.get("variants", [{}])[0]

        # -----------------------------
        # CONSEQUENCE EXTRACTION (FIXED)
        # -----------------------------
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
        transcript = csq.get("transcript", csq.get("feature", "NA"))

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
            f"Diese Variante wurde in ClinVar {p}× pathogen, {us}× unklar, {o}× benign/sonstige klassifiziert."
        )

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

[NMD] Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet.
[ODER] Alternativ kann ein C-terminal verkürztes Protein entstehen.

Eine tatsächliche Auswirkung wurde bislang nicht funktionell untersucht.

{clinvar_text}
{gnomad_text}

Gemäß ClinGen-/ACMG-Kriterien ({acmg_criteria}) ergibt sich eine Bewertung als {acmg}.
"""

        elif variant_type == "nonsense":

            report = f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. Nonsense-Variante im {gene_md}-Gen ({hgvs_md}) führt zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins in {exon_text}.

[NMD] Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet.
[ODER] Alternativ kann ein verkürztes Protein entstehen.

Eine tatsächliche Auswirkung wurde bislang nicht funktionell untersucht.

{clinvar_text}
{gnomad_text}

Gemäß ClinGen-/ACMG-Kriterien ({acmg_criteria}) ergibt sich eine Bewertung als {acmg}.
"""

        elif variant_type == "missense":

            report = f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. Missense-Variante im {gene_md}-Gen ({hgvs_md}) führt zu einem Aminosäureaustausch im korrespondierenden Protein.

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

    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")

# -----------------------------
# RAW JSON VIEW (FIXED)
# -----------------------------
st.markdown("---")
st.subheader("🔍 Raw JSON (Debug / Transparency)")

if "data" in st.session_state:
    show_json = st.checkbox("Show full API response")

    if show_json:
        st.json(st.session_state["data"])
else:
    st.info("Run a variant query to load JSON data.")
