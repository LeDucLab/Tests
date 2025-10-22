import streamlit as st
import requests
import json

# Streamlit app title
st.title("Variant Data Fetcher")

# Input field for variant
variant = st.text_input("Enter Variant (e.g., chr3-10183824-A-G):", "")

# Function to fetch variant data
def fetch_variant_data(variant):
    url = f"https://api.genoox.com/v2/search/snp/?search_text={variant}"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, data="")
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Button to trigger API call
if st.button("Fetch Variant Data"):
    if variant:
        with st.spinner("Fetching data..."):
            result = fetch_variant_data(variant)
        
        # Display results
        if "error" in result:
            st.error(f"Error: {result['error']}")
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
""")
