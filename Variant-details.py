import streamlit as st
try:
    import requests
except ImportError:
    st.error("The 'requests' package is not installed. Add 'requests' to your 'requirements.txt' file and redeploy the app.")
    st.stop()
import json

# Streamlit app configuration
st.set_page_config(page_title="GeneBe Variant Information Retrieval", page_icon="🧬")

# Title and description
st.title("GeneBe Variant Information Retrieval")
st.write("Enter variant details to query the GeneBe API and display all available information about the variant.")

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
api_key = st.text_input("API Key (if required)", type="password", help="Enter your GeneBe API key if the endpoint requires authentication (e.g., Bearer token or query param). Check the GeneBe Swagger UI or documentation for details.")

# Construct the variant string and API URL
variant = f"chr{chromosome}-{position}-{reference}-{alternate}"
base_url = "https://api.genebe.net/v1/public/variant"
api_url = f"{base_url}/{variant}"

# Display the constructed URL
st.subheader("Generated API URL")
if all([chromosome, position, reference, alternate]):
    st.success("URL generated successfully!")
    st.markdown(f"[Test URL in Browser]({api_url})")
    st.write("For manual testing, use the Swagger UI: https://api.genebe.net/cloud/gb-api-doc/swagger-ui/index.html#/variant-public-controller/variant_2")
else:
    st.warning("Please fill in all variant details to proceed.")

# Button to fetch data
if st.button("Retrieve Variant Information"):
    if not all([chromosome, position, reference, alternate]):
        st.error("Please fill in all variant details.")
    else:
        try:
            # Set up headers and params
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Accept": "application/json"
            }
            params = {}
            if api_key:
                # Try Bearer token; switch to params['apiKey'] = api_key if GeneBe uses query param
                headers["Authorization"] = f"Bearer {api_key}"
                # Uncomment the next line and comment the above if query param is needed
                # params['apiKey'] = api_key

            # Send GET request to the API
            response = requests.get(api_url, headers=headers, params=params, timeout=10)

            # Check if the request was successful
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    st.subheader("Variant Information")
                    if isinstance(data, dict):
                        st.success("Data retrieved successfully!")
                        # Display all key-value pairs in a table-like format
                        st.write("**Variant Details:**")
                        for key, value in data.items():
                            # Handle nested dictionaries or lists
                            if isinstance(value, (dict, list)):
                                st.write(f"**{key}:**")
                                st.json(value)
                            else:
                                st.write(f"**{key}:** {value}")
                    elif isinstance(data, list):
                        st.success("Data retrieved successfully!")
                        st.write("**Variant Details (List Format):**")
                        for i, item in enumerate(data):
                            st.write(f"**Item {i+1}:**")
                            if isinstance(item, dict):
                                for key, value in item.items():
                                    if isinstance(value, (dict, list)):
                                        st.write(f"**{key}:**")
                                        st.json(value)
                                    else:
                                        st.write(f"**{key}:** {value}")
                            else:
                                st.write(item)
                    else:
                        st.warning("Unexpected response format.")
                        st.json(data)
                    
                    # Display raw JSON for debugging
                    with st.expander("Raw JSON Response"):
                        st.json(data)
                        
                except json.JSONDecodeError:
                    st.error("Invalid JSON response from the API.")
                    st.text(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                    st.markdown(f"Test manually in Swagger UI: [GeneBe Swagger UI](https://api.genebe.net/cloud/gb-api-doc/swagger-ui/index.html#/variant-public-controller/variant_2)")
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
                st.text(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                st.markdown(f"Test manually in Swagger UI: [GeneBe Swagger UI](https://api.genebe.net/cloud/gb-api-doc/swagger-ui/index.html#/variant-public-controller/variant_2)")

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {str(e)}")
            st.write("Possible issues: invalid API key, network error, or endpoint restrictions.")
            st.markdown(f"Test manually in Swagger UI: [GeneBe Swagger UI](https://api.genebe.net/cloud/gb-api-doc/swagger-ui/index.html#/variant-public-controller/variant_2)")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.markdown(f"Test manually in Swagger UI: [GeneBe Swagger UI](https://api.genebe.net/cloud/gb-api-doc/swagger-ui/index.html#/variant-public-controller/variant_2)")

# Instructions for manual retrieval
st.subheader("Manual Retrieval Instructions")
st.write("""
If the API call fails:
1. Open the Swagger UI: https://api.genebe.net/cloud/gb-api-doc/swagger-ui/index.html#/variant-public-controller/variant_2
2. Find the `/variant` endpoint and enter the variant ID (e.g., chr17-41276044-ACT-A).
3. Add your API key if required (check GeneBe documentation or contact support).
4. Execute the request and review the response for all variant details.
5. If the endpoint requires authentication, sign up for an API key at genebe.net.
""")

# Additional notes
st.subheader("Notes")
st.write("""
- **API Endpoint**: Uses GET /v1/public/variant/{variant} (e.g., https://api.genebe.net/v1/public/variant/chr17-41276044-ACT-A).
- **Authentication**: If the endpoint requires an API key, provide it in the input field (Bearer token or query param). Check GeneBe documentation for details.
- **Response Parsing**: Displays all fields from the JSON response. If the structure differs, inspect the response in Swagger UI and share it to adjust the script.
- **Dependencies**: Ensure 'streamlit' and 'requests' are listed in your 'requirements.txt' file.
- **Terms of Service**: Ensure compliance with GeneBe's API usage policies. Contact support if you need an API key.
- **Variant Format**: Uses chr{chromosome}-{position}-{reference}-{alternate}. Confirm in Swagger UI if a different format is required.
""")
