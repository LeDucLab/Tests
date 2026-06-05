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

        # -----------------------------
        # NEW JSON STRUCTURE HANDLING
        # -----------------------------
        acmg_by_gene = variant.get("acmg_by_gene", [{}])[0]

        gene = acmg_by_gene.get("gene_symbol", "UnknownGene")
        transcript = acmg_by_gene.get("transcript", "NA")

        hgvs_c = acmg_by_gene.get("hgvs_c", "NA")
        hgvs_p = acmg_by_gene.get("hgvs_p", "NA")

        # FINAL HGVS FORMAT
        hgvs_full = f"{transcript}:{hgvs_c}, p.({hgvs_p.replace('p.', '')})"

        # -----------------------------
        # VARIANT TYPE (FROM EFFECTS)
        # -----------------------------
        effects = acmg_by_gene.get("effects", [])
        effects = [e.lower() for e in effects]

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
            st.info(f"Unsupported variant type: {effects}")
            st.stop()

        # -----------------------------
        # ACMG DATA
        # -----------------------------
        acmg = acmg_by_gene.get("verdict", variant.get("acmg_classification", "NA"))

        acmg_criteria_list = acmg_by_gene.get("criteria", [])
        acmg_criteria = ", ".join(acmg_criteria_list)

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
        # CORE STRINGS
        # -----------------------------
        gene_md = f"*{gene}*"

        # -----------------------------
        # REPORTS
        # -----------------------------
        if variant_type in ["frameshift", "nonsense"]:

            label = "Leseraster-Variante (Frameshift)" if variant_type == "frameshift" else "Nonsense-Variante"

            report = f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. {label} im {gene_md}-Gen ({hgvs_full}) führt zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins.

[NMD] Sehr wahrscheinlich kommt es zu Nonsense-Mediated mRNA Decay (NMD).
[ODER] Alternativ kann ein C-terminal verkürztes Protein entstehen.

Eine funktionelle Auswirkung wurde bislang nicht untersucht.

{clinvar_text}
{gnomad_text}

Gemäß ClinGen-/ACMG-Kriterien ({acmg_criteria}) ergibt sich eine Bewertung als {acmg}.
"""

        elif variant_type == "missense":

            report = f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. Missense-Variante im {gene_md}-Gen ({hgvs_full}) führt zu einem Aminosäureaustausch im Protein.

Die funktionelle Relevanz hängt von Struktur, Domäne und Konservierung ab.

Eine funktionelle Auswirkung wurde bislang nicht untersucht.

{clinvar_text}
{gnomad_text}

Gemäß ClinGen-/ACMG-Kriterien ({acmg_criteria}) ergibt sich eine Bewertung als {acmg}.
"""

        # -----------------------------
        # OUTPUT
        # -----------------------------
        st.subheader("🧬 Klinischer Bericht")
        st.markdown(report)

        # RAW JSON (optional)
        with st.expander("Show Raw JSON"):
            st.json(data)

    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
