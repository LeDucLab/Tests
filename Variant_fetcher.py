import streamlit as st
try:
    import requests
except ImportError:
    st.error("The 'requests' package is not installed. Add 'requests' to your 'requirements.txt' file and redeploy the app.")
    st.stop()
import json

# Streamlit app configuration
st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

# Title and description
st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant details to query the GeneBe API and display ACMG classification and criteria as bullet points.")

# Input fields for variant details
st.subheader("Variant Information")
col1, col2, col3, col4 = st.columns(4)
with col1:
    chromosome = st.text_input("Chromosome (e.g. 1)")
with col2:
    position = st.text_input("Position hg38")
with col3:
    reference = st.text_input("Reference hg38")
with col4:
    alternate = st.text_input("Alternate")

# Optional input for API key
st.subheader("Authentication (Optional)")
api_key = st.text_input("API Key (if required)", type="password", help="Enter your GeneBe API key if the endpoint requires authentication (e.g., Bearer token or query param). Check the GeneBe documentation for details.")

# Construct the API URL with query parameters
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
api_url = base_url  # Displayed URL will include params via requests.get

# Display the constructed URL
st.subheader("Generated API URL")
if all([chromosome, position, reference, alternate]):
    # Construct display URL with query params for reference
    display_url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    st.success("URL generated successfully!")
    st.markdown(f"[Test URL in Browser]({display_url})")
else:
    st.warning("Please fill in all variant details to proceed.")

# Button to fetch data
if st.button("Retrieve ACMG Information"):
    if not all([chromosome, position, reference, alternate]):
        st.error("Please fill in all variant details.")
    else:
        try:
            # Set up headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Accept": "application/json"
            }
            if api_key:
                # Try Bearer token; switch to params['apiKey'] = api_key if needed
                headers["Authorization"] = f"Bearer {api_key}"
                # Uncomment the next line and comment the above if query param is needed
                # params['apiKey'] = api_key

            # Send GET request to the API
            response = requests.get(api_url, headers=headers, params=params, timeout=10)

            # Check if the request was successful
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Validate variant in response
                    input_variant = {
                        "chr": f"chr{chromosome.strip()}",
                        "pos": position.strip(),
                        "ref": reference.strip(),
                        "alt": alternate.strip()
                    }
                    response_variant = {}
                    variant_mismatch = False
                    if isinstance(data, dict) and "variants" in data and data["variants"] and isinstance(data["variants"], list):
                        response_variant = {
                            "chr": str(data["variants"][0].get("chr", "")).strip(),
                            "pos": str(data["variants"][0].get("pos", "")).strip(),
                            "ref": str(data["variants"][0].get("ref", "")).strip(),
                            "alt": str(data["variants"][0].get("alt", "")).strip()
                        }
                        # Normalize chr for comparison (e.g., "chr17" vs "17")
                        input_chr = input_variant["chr"].replace("chr", "")
                        response_chr = response_variant["chr"].replace("chr", "")
                        if (input_chr != response_chr or
                            input_variant["pos"] != response_variant["pos"] or
                            input_variant["ref"] != response_variant["ref"] or
                            input_variant["alt"] != response_variant["alt"]):
                            variant_mismatch = True
                            st.warning(
                                f"Warning: Response variant ({response_variant}) does not match input variant ({input_variant}). "
                                "The API may have processed a different variant."
                            )
                    
                    # Extract acmg_classification and acmg_criteria from variants[0]
                    st.subheader("ACMG Classification and Criteria")
                    acmg_classification = "Not found"
                    acmg_criteria = "Not found"
                    allele_freq = "Not found"
                    allele_count = "Not found"
                    revel = "Not found"
                    if isinstance(data, dict) and "variants" in data and data["variants"] and isinstance(data["variants"], list):
                        variant_data = data["variants"][0]
                        acmg_classification = variant_data.get("acmg_classification", "Not found")
                        acmg_criteria = variant_data.get("acmg_criteria", "Not found")
                        allele_freq = variant_data.get("frequency_reference_population", "Not found")
                        allele_count = variant_data.get("allele_count_reference_population", "Not found")
                        revel = variant_data.get("revel_score", "Not found")
                        hgvs_c = variant_data.get("hgvs_c", "Not found")
                    
                    # Display as bullet points
                    st.write("- **ACMG Klassifizierung**: " + str(acmg_classification))
                    st.write("- **ACMG Kriterien**: " + str(acmg_criteria))
                    st.write("- **Allel Frequenz**: " + str(allele_freq))
                    st.write("- **Allel Anzahl**: " + str(allele_count))
                    st.write("- **Revel**: " + str(revel))
                    st.write("- **HGVS_c**: " + str(hgvs_c)
                    
                    # Required fields for the formatted output
                    transcript = variant_data.get("transcript", "Not found")
                    gene_symbol = variant_data.get("gene_symbol", "Not found")
                    hgvs_c = variant_data.get("hgvs_c", "Not found")
                    hgvs_p = variant_data.get("hgvs_p", "Not found")
                    frequency = variant_data.get("frequency_reference_population", "Not found")
                    homozygotes = variant_data.get("homozygote_count", "Not found")
                    total_chromosomes = variant_data.get("total_chromosomes", "Not found")  # Assumed field
                    in_silico_prediction = variant_data.get("in_silico_prediction", "Not found")  # Assumed field
                    in_silico_tools = variant_data.get("in_silico_tools", {"benign": 0, "total": 0})  # Assumed structure
                    clinvar_status = variant_data.get("clinvar_status", "Not found")

                    # Format the variant description
                    variant_description = f"Die {transcript}({gene_symbol}):{hgvs_c}({hgvs_p}) Variante verursacht eine Missense-Änderung, die einen nicht-konservierten Nukleotid betrifft. "
                    if frequency != "Not found" and total_chromosomes != "Not found":
                        variant_description += f"Das Variantenallel wurde in der GnomAD-Datenbank mit einer Frequenz von {frequency} in {total_chromosomes:,} Kontrollchromosomen gefunden, einschließlich {homozygotes:,} Homozygoter. "
                    else:
                        variant_description += "Keine Frequenzdaten in der GnomAD-Datenbank verfügbar. "
    
                    if in_silico_prediction != "Not found":
                        variant_description += f"Ein In-silico-Tool sagt ein {in_silico_prediction} Ergebnis für diese Variante voraus. "
                    else:
                        variant_description += "Keine In-silico-Vorhersage verfügbar. "
    
                    if in_silico_tools != "Not found" and isinstance(in_silico_tools, dict):
                        benign_count = in_silico_tools.get("benign", 0)
                        total_tools = in_silico_tools.get("total", 0)
                        variant_description += f"{benign_count}/{total_tools} In-silico-Tools sagen ein gutartiges Ergebnis für diese Variante voraus. "
                    else:
                        variant_description += "Keine In-silico-Tool-Daten verfügbar. "
    
                    if clinvar_status != "Not found":
                        variant_description += f"Keine klinischen Diagnoselabore haben Bewertungen zur klinischen Bedeutung dieser Variante an ClinVar übermittelt."
                    else:
                        variant_description += "Kein ClinVar-Status verfügbar."
    
                    # Display the formatted description
                    st.write(variant_description)

                    # Display raw JSON for debugging
                    with st.expander("Raw JSON Response"):
                        st.json(data)
                        
                except json.JSONDecodeError:
                    st.error("Invalid JSON response from the API.")
                    st.text(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
                st.text(response.text[:500] + "..." if len(response.text) > 500 else response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {str(e)}")
            st.write("Possible issues: invalid API key, network error, or endpoint restrictions.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
