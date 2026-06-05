import streamlit as st
import requests
import json

st.set_page_config(page_title="GeneBe ACMG Debug", page_icon="🧬")

st.title("GeneBe ACMG Debug Tool")
st.write("Debugging API response structure (especially consequences field)")

# -----------------------------
# INPUT
# -----------------------------
st.subheader("Variant Input")
variant_input = st.text_input("Variant (chr pos ref alt)", "chr1 123456 A T")

chromosome = position = reference = alternate = None

if variant_input:
    parts = variant_input.strip().replace(",", " ").split()

    if len(parts) == 4:
        chromosome, position, reference, alternate = parts
    else:
        st.error("Invalid format. Use: chr pos ref alt")

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
# RUN REQUEST
# -----------------------------
if st.button("Fetch & Debug API Response"):

    if not all([chromosome, position, reference, alternate]):
        st.error("Please enter valid variant first.")
    else:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }

            response = requests.get(base_url, headers=headers, params=params, timeout=10)

            st.subheader("HTTP Status")
            st.write(response.status_code)

            if response.status_code == 200:
                data = response.json()

                st.subheader("FULL API RESPONSE (RAW)")
                st.json(data)

                # -----------------------------
                # Extract variant safely
                # -----------------------------
                variant_data = data["variants"][0] if data.get("variants") else {}

                st.subheader("VARIANT DATA")
                st.json(variant_data)

                # -----------------------------
                # CRITICAL DEBUG: consequences
                # -----------------------------
                st.subheader("CONSEQUENCES FIELD (IMPORTANT DEBUG)")

                consequences = variant_data.get("consequences", None)

                st.write("Type:", type(consequences))
                st.write("Value:")

                st.json(consequences)

                # show first element if exists
                if isinstance(consequences, list) and len(consequences) > 0:
                    st.subheader("FIRST CONSEQUENCE OBJECT")

                    first = consequences[0]
                    st.json(first)

                    st.subheader("AVAILABLE KEYS IN FIRST CONSEQUENCE")
                    st.write(list(first.keys()))

                else:
                    st.warning("No consequences list found or it's empty.")

                # -----------------------------
                # Try common fields explicitly
                # -----------------------------
                st.subheader("TRY COMMON KEYS")

                if isinstance(consequences, list) and consequences:
                    first = consequences[0]

                    st.write("term:", first.get("term"))
                    st.write("consequence:", first.get("consequence"))
                    st.write("biotype:", first.get("biotype"))
                    st.write("impact:", first.get("impact"))

            else:
                st.error("API request failed")
                st.text(response.text[:500])

        except Exception as e:
            st.error(f"Error: {e}")
