import streamlit as st
import requests

st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant as: chr pos ref alt (e.g. chr1 123456 A T)")

# -----------------------------
# SESSION STATE (IMPORTANT)
# -----------------------------
if "api_data" not in st.session_state:
    st.session_state.api_data = None


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
# URL PREVIEW
# -----------------------------
st.subheader("Generated API URL")

if all([chromosome, position, reference, alternate]):
    display_url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    st.success("URL generated successfully!")
    st.markdown(f"[Open API URL]({display_url})")
else:
    st.warning("Enter a valid variant to generate URL")


# -----------------------------
# REPORT GENERATOR
# -----------------------------
def generate_report(gene, hgvs, consequence_type):

    gene_fmt = f"*{gene}* ({hgvs})"

    if consequence_type == "frameshift":
        return f"""
Die o. g. Leseraster-Variante im {gene_fmt}-Gen führt durch eine Leserasterverschiebung (Frameshift) zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des Proteins.

Sehr wahrscheinlich wird kein funktionsfähiges Protein gebildet (NMD wahrscheinlich).

Die funktionelle Auswirkung gilt daher als loss-of-function.
"""

    elif consequence_type == "nonsense":
        return f"""
Die o. g. Nonsense-Variante im {gene_fmt}-Gen führt zu einem vorzeitigen Stopcodon und damit zu einer verkürzten Proteintranslation.

Sehr wahrscheinlich erfolgt ein mRNA-Abbau durch Nonsense-mediated decay (NMD).

Funktionsverlust ist wahrscheinlich.
"""

    elif consequence_type == "missense":
        return f"""
Die o. g. Missense-Variante im {gene_fmt}-Gen führt zu einem Aminosäureaustausch im Protein.

Die funktionelle Relevanz hängt von Struktur und Konservierung ab.

Weitere Analysen sind erforderlich.
"""

    else:
        return f"""
Die o. g. Variante im {gene_fmt}-Gen konnte keinem bekannten Konsequenztyp zugeordnet werden.
"""


# -----------------------------
# FETCH DATA (FIXED TRY/EXCEPT)
# -----------------------------
if st.button("Retrieve ACMG Information"):

    if not all([chromosome, position, reference, alternate]):
        st.error("Please enter a valid variant.")

    else:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }

            response = requests.get(base_url, headers=headers, params=params, timeout=15)

            if response.status_code != 200:
                st.error(f"API Error: {response.status_code}")
                st.text(response.text[:500])

            else:
                data = response.json()

                # SAVE FOR DEBUG BUTTON
                st.session_state.api_data = data

                variant_data = (data.get("variants") or [{}])[0]

                acmg_classification = variant_data.get("acmg_classification", "Not found")
                acmg_criteria = variant_data.get("acmg_criteria", "Not found")
                allele_freq = variant_data.get("frequency_reference_population", "Not found")
                allele_count = variant_data.get("allele_count_reference_population", "Not found")
                revel = variant_data.get("revel_score", "Not found")

                consequences_block = variant_data.get("consequences") or []

                hgvs_c = "Not found"
                gene_name = variant_data.get("gene") or variant_data.get("gene_name") or "Unknown"

                consequence_type = None

                # -----------------------------
                # CONSEQUENCE PARSING
                # -----------------------------
                if consequences_block:
                    first = consequences_block[0]
                    hgvs_c = first.get("hgvs_c", "Not found")

                    csq_list = first.get("consequences", [])

                    if isinstance(csq_list, list) and csq_list:
                        csq = csq_list[0]

                        if "frameshift" in csq:
                            consequence_type = "frameshift"
                        elif "stop_gained" in csq:
                            consequence_type = "nonsense"
                        elif "missense" in csq:
                            consequence_type = "missense"
                        else:
                            consequence_type = "other"

                # -----------------------------
                # OUTPUT
                # -----------------------------
                st.subheader("ACMG Summary")

                st.write(f"- **ACMG Klassifizierung**: {acmg_classification}")
                st.write(f"- **ACMG Kriterien**: {acmg_criteria}")
                st.write(f"- **Allel Frequenz**: {allele_freq}")
                st.write(f"- **Allel Anzahl**: {allele_count}")
                st.write(f"- **REVEL Score**: {revel}")
                st.write(f"- **HGVS_c**: {hgvs_c}")
                st.write(f"- **Consequence Type**: {consequence_type}")

                st.subheader("Automated Clinical Report")

                report = generate_report(
                    gene=gene_name,
                    hgvs=hgvs_c,
                    consequence_type=consequence_type
                )

                st.text(report)


        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)}")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")


# -----------------------------
# DEBUG JSON BUTTON (SAFE)
# -----------------------------
st.subheader("Debug")

if st.session_state.api_data is not None:
    if st.button("Show Raw JSON Response"):
        st.json(st.session_state.api_data)
else:
    st.info("No API response yet. Run 'Retrieve ACMG Information' first.")
