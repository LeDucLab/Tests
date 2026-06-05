import streamlit as st
import requests
import json

st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant as: chr pos ref alt (e.g. chr1 123456 A T)")

# -----------------------------
# SINGLE INPUT FIELD
# -----------------------------
st.subheader("Variant Input")
variant_input = st.text_input(
    "Variant (chr pos ref alt)",
    placeholder="chr1 123456 A T"
)

# Optional API key
st.subheader("Authentication (Optional)")
api_key = st.text_input(
    "API Key (if required)",
    type="password",
    help="Enter your GeneBe API key if needed."
)

# -----------------------------
# PARSE VARIANT
# -----------------------------
chromosome = position = reference = alternate = None

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
# FETCH BUTTON
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

            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            response = requests.get(base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                st.subheader("ACMG Classification and Criteria")

                variant_data = data["variants"][0] if "variants" in data and data["variants"] else {}

                acmg_classification = variant_data.get("acmg_classification", "Not found")
                acmg_criteria = variant_data.get("acmg_criteria", "Not found")
                allele_freq = variant_data.get("frequency_reference_population", "Not found")
                allele_count = variant_data.get("allele_count_reference_population", "Not found")
                revel = variant_data.get("revel_score", "Not found")

                consequences = variant_data.get("consequences", [{}])
                hgvs_c = consequences[0].get("hgvs_c", "Not found") if consequences else "Not found"

                st.write(f"- **ACMG Klassifizierung**: {acmg_classification}")
                st.write(f"- **ACMG Kriterien**: {acmg_criteria}")
                st.write(f"- **Allel Frequenz**: {allele_freq}")
                st.write(f"- **Allel Anzahl**: {allele_count}")
                st.write(f"- **Revel**: {revel}")
                st.write(f"- **HGVS_c**: {hgvs_c}")

                with st.expander("Raw JSON Response"):
                    st.json(data)

            else:
                st.error(f"Failed: {response.status_code}")
                st.text(response.text[:500])

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)}")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
