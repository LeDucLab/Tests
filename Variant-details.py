import streamlit as st
import requests
import json
import re

# Streamlit app title
st.title("Variant Data Fetcher")

# Input field for variant
variant = st.text_input("Enter Variant (e.g., chr3-10183824-A-G):", "")

# Function to validate variant format
def is_valid_variant(variant):
    pattern = r"^chr[\dXYMT]+-\d+-[A-Z]-[A-Z]$"
    return re.match(pattern, variant) is not None

# Function to fetch variant data
def fetch_variant_data(variant):
    # Strip whitespace from variant
    variant = variant.strip()
    
    # Validate variant format
    if not is_valid_variant(variant):
        return {"error": "Invalid variant format. Use chr<chromosome>-<position>-<ref>-<alt> (e.g., chr3-10183824-A-G)"}
    
    url = f"https://api.genoox.com/v2/search/snp/?search_text={variant}"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, data="")
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error: {str(e)}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {str(e)}"}

# Button to trigger API call
if st.button("Fetch Variant Data"):
    if variant:
        with st.spinner("Fetching data..."):
            result = fetch_variant_data(variant)
        
        # Display results
        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Data fetched successfully!")
            st.json(result)  # Display the JSON response
    else:
        st.warning("Please enter a variant to search.")

# Instructions
st.markdown("""
### Instructions
1. Enter the variant in the format: `chr<chromosome>-<position>-<ref>-<alt>` (e.g., chr3-10183824-A-G).
2. Click the "Fetch Variant Data" button to retrieve the data.
3. The response from the API will be displayed in JSON format.
4. Ensure the variant format is correct (e.g., chr3, chrX, 1+ digits for position, single letters for ref/alt).
""")
