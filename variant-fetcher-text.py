import streamlit as st
import requests
import json

st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant as: chr pos ref alt (e.g. chr1 123456 A T)")

# -----------------------------
# INPUT
# -----------------------------
st.subheader("Variant Input")

variant_input = st.text_input(
    "Variant (chr pos ref alt)",
    placeholder="chr1 123456 A T"
)

chromosome = position = reference = alternate = None

if variant_input:
    parts = variant_input.strip().replace(",", " ").split()

    if len(parts) != 4:
        st.error("Invalid format. Use: chr pos ref alt")
    else:
        chromosome, position, reference, alternate = parts

# -----------------------------
# API CONFIG
# -----------------------------
base_url = "https://api.genebe.net/cloud/api-public/v1/variant"

params = {
    "chr": f"chr{chromosome}" if chromosome else "",
    "pos": position if position else "",
    "ref": reference if reference else "",
    "alt": alternate if alternate else "",
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
# REPORT TEMPLATES
# -----------------------------
def frameshift_report(gene, hgvs, acmg):
    return f"""
Die o. g. Leseraster-Variante im {gene}-Gen ({hgvs}) führt durch eine Leserasterverschiebung (Frameshift) zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins.

Sehr wahrscheinlich wird kein Protein gebildet, da mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet wird.

Gemäß ClinGen-/ACMG-Empfehlungen sind die Kriterien {acmg} erfüllt.
"""

def nonsense_report(gene, hgvs, acmg):
    return f"""
Die o. g. Nonsense-Variante im {gene}-Gen ({hgvs}) führt zum Auftreten eines vorzeitigen Stopcodons.

Sehr wahrscheinlich kein Protein durch NMD.

ACMG Kriterien: {acmg}
"""

def missense_report(gene, hgvs, acmg, revel):
    return f"""
Die o. g. Missense-Variante im {gene}-Gen ({hgvs}) führt zu einem Aminosäureaustausch.

REVEL Score: {revel}

ACMG Kriterien: {acmg}
"""

# -----------------------------
# RUN
# -----------------------------
if st.button("Retrieve ACMG Information"):

    if not all([chromosome, position, reference, alternate]):
        st.error("Please enter valid variant first.")
    else:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }

            response = requests.get(base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                st.subheader("Raw API Response")
                st.json(data)

                variant_data = data["variants"][0] if data.get("variants") else {}

                st.subheader("Variant Data")
                st.json(variant_data)

                # -----------------------------
                # SAFE EXTRACTION
                # -----------------------------
                gene_name = variant_data.get("gene_symbol", "XXX")
                hgvs = variant_data.get("hgvs_c", "XXX")
                acmg = variant_data.get("acmg_classification", "Not found")
                revel = variant_data.get("revel_score", "Not found")

                # -----------------------------
                # FIXED CONSEQUENCE PARSING
                # -----------------------------
                consequences = variant_data.get("consequences", [])

                consequence = "unknown"

                if (
                    isinstance(consequences, list)
                    and len(consequences) > 0
                    and isinstance(consequences[0], dict)
                ):
                    inner = consequences[0].get("consequences", [])

                    if isinstance(inner, list) and len(inner) > 0:
                        consequence = inner[0]  # <-- FIXED LINE

                st.subheader("DEBUG: Parsed Consequence")
                st.write(consequence)

                # -----------------------------
                # REPORT SELECTION
                # -----------------------------
                c = str(consequence).lower()

                if "frameshift" in c:
                    report = frameshift_report(gene_name, hgvs, acmg)

                elif "stop" in c or "nonsense" in c:
                    report = nonsense_report(gene_name, hgvs, acmg)

                elif "missense" in c:
                    report = missense_report(gene_name, hgvs, acmg, revel)

                else:
                    report = f"""
Keine spezifische Vorlage gefunden.

Consequence: {consequence}
Gene: {gene_name}
HGVS: {hgvs}
ACMG: {acmg}
"""

                # -----------------------------
                # OUTPUT
                # -----------------------------
                st.subheader("Generated Clinical Report")
                st.write(report)

                st.subheader("Key Data")
                st.write({
                    "gene": gene_name,
                    "hgvs": hgvs,
                    "consequence": consequence,
                    "acmg": acmg,
                    "revel": revel
                })

                with st.expander("Raw JSON"):
                    st.json(data)

            else:
                st.error(f"API Error: {response.status_code}")
                st.text(response.text[:500])

        except Exception as e:
            st.error(f"Error: {e}")
