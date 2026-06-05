import streamlit as st
import requests
import json

st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant as: chr pos ref alt (e.g. chr1 123456 A T)")

# -----------------------------
# VARIANT INPUT
# -----------------------------
st.subheader("Variant Input")
variant_input = st.text_input(
    "Variant (chr pos ref alt)",
    placeholder="chr1 123456 A T"
)

chromosome = position = reference = alternate = None

# -----------------------------
# PARSE VARIANT
# -----------------------------
if variant_input:
    parts = variant_input.strip().replace(",", " ").split()

    if len(parts) != 4:
        st.error("Invalid format. Use: chr pos ref alt (e.g. chr1 123456 A T)")
    else:
        chromosome, position, reference, alternate = parts

# -----------------------------
# API CONFIG
# -----------------------------
base_url = "https://api.genebe.net/cloud/api-public/v1/variant"

params = {
    "chr": f"chr{chromosome.strip()}" if chromosome else "",
    "pos": position.strip() if position else "",
    "ref": reference.strip() if reference else "",
    "alt": alternate.strip() if alternate else "",
    "useRefseq": "true",
    "useEnsembl": "true",
    "omitAcmg": "false",
    "omitCsq": "false",
    "omitBasic": "false",
    "omitAdvanced": "false",
    "omitNormalization": "false",
    "allGenes": "false",
    "customAnnotations": "empty",
    "genome": "hg38"
}

# -----------------------------
# URL DISPLAY
# -----------------------------
st.subheader("Generated API URL")

if all([chromosome, position, reference, alternate]):
    display_url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    st.success("URL generated successfully!")
    st.markdown(f"[Test URL in Browser]({display_url})")
else:
    st.warning("Enter a valid variant to generate URL.")

# -----------------------------
# FETCH DATA
# -----------------------------
if st.button("Retrieve ACMG Information"):

    if not all([chromosome, position, reference, alternate]):
        st.error("Please enter a valid variant in space-separated format.")
    else:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }

            response = requests.get(base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                st.subheader("ACMG Classification and Report")

                variant_data = data["variants"][0] if data.get("variants") else {}

                # -----------------------------
                # SAFE EXTRACTION
                # -----------------------------
                acmg_classification = variant_data.get("acmg_classification", "Not found")
                acmg_criteria = variant_data.get("acmg_criteria", "Not found")

                gene_name = variant_data.get("gene_symbol", "XXX")
                hgvs = variant_data.get("hgvs_c", "XXX")

                allele_freq = variant_data.get("frequency_reference_population", "Not found")
                allele_count = variant_data.get("allele_count_reference_population", "Not found")
                revel = variant_data.get("revel_score", "Not found")

                consequences = variant_data.get("consequences", [{}])
                consequence = consequences[0].get("consequence", "unknown") if consequences else "unknown"
                hgvs_c = consequences[0].get("hgvs_c", hgvs) if consequences else hgvs

                # -----------------------------
                # REPORT TEMPLATES
                # -----------------------------

                frameshift_report = f"""
Die o. g. Leseraster-Variante im {gene_name}-Gen ({hgvs_c}) führt durch eine Leserasterverschiebung (Frameshift) zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins.

[NMD] Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet, da mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet wird.

[ODER]
[kein NMD] Am ehesten wird ein C-terminal verkürztes, möglicherweise funktionsverändertes Protein gebildet.

Gemäß ClinGen-/ACMG-Empfehlungen sind die Kriterien {acmg_criteria} erfüllt, sodass sich eine Bewertung ergibt.
"""

                nonsense_report = f"""
Die o. g. Nonsense-Variante im {gene_name}-Gen ({hgvs_c}) führt zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins.

[NMD] Sehr wahrscheinlich kein Protein durch NMD.

[ODER]
[kein NMD] Verkürztes Protein möglich.

Gemäß ClinGen-/ACMG-Empfehlungen sind die Kriterien {acmg_criteria} erfüllt.
"""

                missense_report = f"""
Die o. g. Missense-Variante im {gene_name}-Gen ({hgvs_c}) führt zu einem Aminosäureaustausch im korrespondierenden Protein.

Die bioinformatische Bewertung ergibt einen REVEL-Score von {revel}.

Gemäß ClinGen-/ACMG-Empfehlungen sind die Kriterien {acmg_criteria} erfüllt.
"""

                # -----------------------------
                # SELECT REPORT
                # -----------------------------
                consequence_lower = str(consequence).lower()

                if "frameshift_variant" in consequence_lower:
                    report = frameshift_report

                elif "stop_gained" in consequence_lower or "nonsense" in consequence_lower:
                    report = nonsense_report

                elif "missense" in consequence_lower:
                    report = missense_report

                else:
                    report = f"""
Keine spezifische Vorlage verfügbar.

Consequence: {consequence}

ACMG Klassifikation: {acmg_classification}

ACMG Kriterien: {acmg_criteria}
"""

                # -----------------------------
                # OUTPUT
                # -----------------------------
                st.subheader("Generated Clinical Report")
                st.write(report)

                st.subheader("Key Variant Data")
                st.write(f"- ACMG Classification: {acmg_classification}")
                st.write(f"- Gene: {gene_name}")
                st.write(f"- HGVS: {hgvs_c}")
                st.write(f"- Consequence: {consequence}")
                st.write(f"- REVEL: {revel}")
                st.write(f"- Allele Frequency: {allele_freq}")
                st.write(f"- Allele Count: {allele_count}")

                with st.expander("Raw JSON Response"):
                    st.json(data)

            else:
                st.error(f"Failed: {response.status_code}")
                st.text(response.text[:500])

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)}")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
