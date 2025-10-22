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
    chromosome = st.text_input("Chromosome (e.g., 17)")
with col2:
    position = st.text_input("Position on hg38 (e.g., 41276044)")
with col3:
    reference = st.text_input("Reference (e.g., ACT)")
with col4:
    alternate = st.text_input("Alternate (e.g., A)")

# Optional input for API key
st.subheader("Authentication (Optional)")
api_key = st.text_input("API Key (if required)", type="password", help="Enter your GeneBe API key if the endpoint requires authentication (e.g., Bearer token or query param). Check the GeneBe documentation for details.")

# Construct the API URL with query parameters
base_url = "https://api.genebe.net/cloud/api-public/v1/variant"
params = {
    "chr": f"chr{chromosome}" if chromosome else "",
    "pos": position,
    "ref": reference,
    "alt": alternate,
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
                        "chr": f"chr{chromosome}",
                        "pos": int(position) if position.isdigit() else position,
                        "ref": reference,
                        "alt": alternate
                    }
                    response_variant = {}
                    if isinstance(data, dict) and "variants" in data and data["variants"] and isinstance(data["variants"], list):
                        response_variant = {
                            "chr": data["variants"][0].get("chr"),
                            "pos": data["variants"][0].get("pos"),
                            "ref": data["variants"][0].get("ref"),
                            "alt": data["variants"][0].get("alt")
                        }
                        if response_variant != input_variant:
                            st.warning(
                                f"Warning: Response variant ({response_variant}) does not match input variant ({input_variant}). "
                                "The API may have normalized the variant."
                            )
                    
                    # Extract acmg_classification and acmg_criteria from variants[0]
                    st.subheader("ACMG Classification and Criteria")
                    acmg_classification = "Not found"
                    acmg_criteria = "Not found"
                    if isinstance(data, dict) and "variants" in data and data["variants"] and isinstance(data["variants"], list):
                        variant_data = data["variants"][0]
                        acmg_classification = variant_data.get("acmg_classification", "Not found")
                        acmg_criteria = variant_data.get("acmg_criteria", "Not found")
                    
                    # Display as bullet points
                    st.write("- **ACMG Klassifizierung**: " + str(acmg_classification))
                    st.write("- **ACMG Kriterien**: " + str(acmg_criteria))

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

# Additional notes
st.subheader("Notes")
st.write("""
- **API Endpoint**: Uses GET /cloud/api-public/v1/variant with query parameters (e.g., chr=chr17, pos=41276044, ref=ACT, alt=A, genome=hg38).
- **Authentication**: If the endpoint requires an API key, provide it in the input field (Bearer token or query param). Check GeneBe documentation for details.
- **Response Parsing**: Extracts 'acmg_classification' and 'acmg_criteria' from the first item in the 'variants' list. If the structure changes, share the JSON response to adjust the script.
- **Variant Mismatch**: The API may normalize the input variant (e.g., ACT to ACC). Check the response variant details in the JSON.
- **Dependencies**: Ensure 'streamlit' and 'requests' are listed in your 'requirements.txt' file.
- **Terms of Service**: Ensure compliance with GeneBe's API usage policies. Contact support if you need an API key.
""")
