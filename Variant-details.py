import streamlit as st
try:
    import requests
except ImportError:
    st.error("The 'requests' package is not installed. Add 'requests' to your 'requirements.txt' file and redeploy the app.")
    st.stop()
import json

# Streamlit app configuration
st.set_page_config(page_title="Automated GeneBe ACMG Retrieval", page_icon="🧬")

# Title and description
st.title("Automated GeneBe ACMG Classification Retrieval")
st.write("Enter variant details to query the GeneBe API and retrieve ACMG classification criteria.")

# Input fields for variant details
st.subheader("Variant Information")
col1, col2, col3, col4 = st.columns(4)
with col1:
    chromosome = st.text_input("Chromosome (e.g., 17)", value="17")
with col2:
    position = st.text_input("Position (e.g., 41276044)", value="41276044")
with col3:
    reference = st.text_input("Reference (e.g., ACT)", value="ACT")
with col4:
    alternate = st.text_input("Alternate (e.g., A)", value="A")

# Optional input for API key
st.subheader("Authentication (Optional)")
api_key = st.text_input("API Key (if required)", type="password", help="Enter your GeneBe API key if the endpoint requires authentication (e.g., Bearer token).")

# Construct the variant string and API URL
variant = f"chr{chromosome}-{position}-{reference}-{alternate}"
base_url = "https://api.genebe.net/v1/public/variant"
api_url = f"{base_url}/{variant}"

# Display the constructed URL
st.subheader("Generated API URL")
if all([chromosome, position, reference, alternate]):
    st.success("URL generated successfully!")
    st.markdown(f"[Open URL in Browser]({api_url})")
    st.write("For testing: Use Swagger UI at https://api.genebe.net/cloud/gb-api-doc/swagger-ui/index.html")
else:
    st.warning("Please fill in all variant details to proceed.")

# Button to fetch data
if st.button("Retrieve ACMG Classification"):
    if not all([chromosome, position, reference, alternate]):
        st.error("Please fill in all variant details.")
    else:
        try:
            # Set up headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Accept": "application/json"
            }
            params = {}
            if api_key:
                # Try Bearer token first; adjust if GeneBe uses query param (e.g., params['apiKey'] = api_key)
                headers["Authorization"] = f"Bearer {api_key}"

            # Send GET request to the API
            response = requests.get(api_url, headers=headers, params=params, timeout=10)

            # Check if the request was successful
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Extract ACMG classification (adjust fields based on actual response structure)
                    acmg_classification = data.get("acmgClassification", data.get("classification", "No ACMG classification found"))
                    acmg_criteria = data.get("criteria", data.get("acmgCriteria", "No criteria found"))
                    
                    st.subheader("ACMG Classification Results")
                    if acmg_classification != "No ACMG classification found":
                        st.success("Data retrieved successfully!")
                        st.write("**ACMG Classification:**")
                        st.write(acmg_classification)
                        st.write("**ACMG Criteria:**")
                        st.write(acmg_criteria)
                    else:
                        st.warning("No ACMG classification data available in the response.")
                    
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

# Instructions
st.subheader("Notes")
st.write("""
- **API Endpoint**: Uses GET /v1/public/variant/{variant} (e.g., https://api.genebe.net/v1/public/variant/chr17-41276044-ACT-A).
- **Authentication**: If required, provide your API key. Check GeneBe docs for exact format (Bearer token or query param).
- **Response Parsing**: Assumes JSON fields like 'acmgClassification' and 'criteria'. Adjust the script if the structure differs (e.g., inspect response in Swagger UI).
- **Dependencies**: Install `streamlit` and `requests` (`pip install streamlit requests`).
- **Testing**: Use Swagger UI (https://api.genebe.net/cloud/gb-api-doc/swagger-ui/index.html) to test the endpoint manually.
- **Terms of Service**: Ensure compliance with GeneBe's API usage policies.
""")
