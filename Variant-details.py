import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# Streamlit app configuration
st.set_page_config(page_title="Automated Variant ACMG Retrieval", page_icon="🧬")

# Title and description
st.title("Automated Franklin Genoox ACMG Classification Retrieval")
st.write("Enter variant details to generate a URL and attempt to automatically retrieve ACMG classification criteria.")

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

# Optional input for cookies or session token
st.subheader("Authentication (Optional)")
cookies = st.text_area("Browser Cookies (if required)", placeholder="Paste cookies from a logged-in browser session", help="Copy cookies from your browser's developer tools after logging into Franklin Genoox.")

# Construct the variant string and URL
variant = f"chr{chromosome}-{position}-{reference}-{alternate}"
base_url = "https://franklin.genoox.com/clinical-db/variant/snp"
api_url = f"{base_url}/{variant}?app=assessment-tools"

# Display the constructed URL
st.subheader("Generated URL")
if all([chromosome, position, reference, alternate]):
    st.success("URL generated successfully!")
    st.markdown(f"[Open URL in Browser]({api_url})")
else:
    st.warning("Please fill in all variant details to proceed.")

# Button to attempt automated retrieval
if st.button("Retrieve ACMG Classification"):
    if not all([chromosome, position, reference, alternate]):
        st.error("Please fill in all variant details.")
    else:
        try:
            # Set up headers and cookies
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
            }
            cookies_dict = {}
            if cookies:
                # Parse cookies string (e.g., "name1=value1; name2=value2")
                for cookie in cookies.split(";"):
                    if "=" in cookie:
                        name, value = cookie.strip().split("=", 1)
                        cookies_dict[name] = value

            # Send request to the URL
            response = requests.get(api_url, headers=headers, cookies=cookies_dict, timeout=10)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the page with BeautifulSoup
                soup = BeautifulSoup(response.text, "html.parser")

                # Attempt to find ACMG classification (adjust based on actual HTML structure)
                # This is a placeholder; inspect the page to find the correct element
                acmg_element = soup.find("div", class_=re.compile("acmg|classification", re.I))
                acmg_classification = acmg_element.get_text(strip=True) if acmg_element else "No ACMG classification found"

                # Alternative: Search for common ACMG terms (e.g., Pathogenic, Benign)
                page_text = soup.get_text().lower()
                acmg_terms = ["pathogenic", "likely pathogenic", "benign", "likely benign", "uncertain significance"]
                found_terms = [term for term in acmg_terms if term in page_text]

                st.subheader("ACMG Classification Results")
                if acmg_classification != "No ACMG classification found" or found_terms:
                    st.success("Data retrieved successfully!")
                    if acmg_classification != "No ACMG classification found":
                        st.write("**ACMG Classification:**")
                        st.write(acmg_classification)
                    if found_terms:
                        st.write("**Detected ACMG Terms:**")
                        st.write(", ".join(found_terms))
                else:
                    st.warning("No ACMG classification found. The page may require login or have a different structure.")
                    st.markdown(f"Please check manually: [Open URL]({api_url})")
            else:
                st.error(f"Failed to fetch page. Status code: {response.status_code}")
                st.write("The page may require authentication or may not be accessible.")
                st.markdown(f"Please check manually: [Open URL]({api_url})")

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching page: {str(e)}")
            st.write("Possible issues: authentication required, network error, or site restrictions.")
            st.markdown(f"Please check manually: [Open URL]({api_url})")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.markdown(f"Please check manually: [Open URL]({api_url})")

# Instructions for manual retrieval
st.subheader("Manual Retrieval Instructions")
st.write("""
If automated retrieval fails:
1. Click the generated URL to open it in your browser.
2. Log in to Franklin Genoox if required (you may need an account).
3. Navigate to the variant details page.
4. Look for ACMG classification criteria (e.g., Pathogenic, Benign, or criteria like PM1, PS2).
5. If no classification is available, check variant reports or annotations.
""")

# Additional notes
st.subheader("Notes")
st.write("""
- **Authentication**: Franklin Genoox likely requires login. Provide browser cookies from a logged-in session (copy from browser developer tools).
- **Web Scraping**: The script assumes ACMG data is in a div with a class like 'acmg' or 'classification'. Inspect the page's HTML (using browser developer tools) to find the correct element and update the script.
- **Limitations**: Web scraping may violate Franklin Genoox's terms of service. Use responsibly and consider contacting their support for API access.
- **Dependencies**: Install `streamlit`, `requests`, and `beautifulsoup4` (`pip install streamlit requests beautifulsoup4`).
- **Variant Format**: Ensure the format is correct (e.g., chr17-41276044-ACT-A).
""")
