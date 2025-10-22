import streamlit as st
try:
    import requests
except ImportError:
    st.error("The 'requests' package is not installed. Add 'requests' to your 'requirements.txt' file and redeploy the app.")
    st.stop()
import re

# Streamlit app configuration
st.set_page_config(page_title="Automated Variant ACMG Retrieval", page_icon="🧬")

# Title and description
st.title("Automated Franklin Genoox ACMG Classification Retrieval")
st.write("Enter variant details to generate a Franklin Genoox URL and attempt to retrieve ACMG classification criteria.")

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

# Optional input for cookies
st.subheader("Authentication (Optional)")
cookies = st.text_area("Browser Cookies (if required)", placeholder="Paste cookies from a logged-in browser session (e.g., name1=value1; name2=value2)", help="Copy cookies from your browser's developer tools (Network tab > Cookies) after logging into Franklin Genoox.")

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
                for cookie in cookies.split(";"):
                    if "=" in cookie:
                        name, value = cookie.strip().split("=", 1)
                        cookies_dict[name] = value

            # Send request to the URL
            response = requests.get(api_url, headers=headers, cookies=cookies_dict, timeout=10)

            # Check if the request was successful
            if response.status_code == 200:
                # Get the page text
                page_text = response.text.lower()

                # Search for ACMG classification terms using regex
                acmg_terms = [
                    r"pathogenic",
                    r"likely pathogenic",
                    r"benign",
                    r"likely benign",
                    r"uncertain significance",
                    r"\b(P[MSB]\d|BA\d|BP\d)\b"  # Matches ACMG criteria like PM1, PS2, BA1, BP4
                ]
                found_terms = []
                for pattern in acmg_terms:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    if matches:
                        found_terms.extend(matches)

                st.subheader("ACMG Classification Results")
                if found_terms:
                    st.success("Data retrieved successfully!")
                    st.write("**Detected ACMG Terms and Criteria:**")
                    st.write(", ".join(set(found_terms)))  # Remove duplicates
                else:
                    st.warning("No ACMG classification or criteria found. The page may require login or have a different structure.")
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
- **Dependencies**: Ensure 'streamlit' and 'requests' are listed in your 'requirements.txt' file.
- **Authentication**: Franklin Genoox likely requires login. Provide browser cookies from a logged-in session (copy from browser developer tools).
- **Parsing**: The script searches for ACMG terms (e.g., Pathogenic, Benign) and criteria (e.g., PM1, PS2) using regex. If results are inaccurate, inspect the page's HTML and adjust the regex patterns.
- **Terms of Service**: Web scraping may violate Franklin Genoox's terms. Contact their support for API access if needed.
- **Variant Format**: Ensure the format is correct (e.g., chr17-41276044-ACT-A).
""")
