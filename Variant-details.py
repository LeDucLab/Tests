import streamlit as st
try:
    import requests
except ImportError:
    st.error("The 'requests' package is not installed. Add 'requests' to your 'requirements.txt' file and redeploy the app.")
    st.stop()
import re

# Streamlit app configuration
st.set_page_config(page_title="Automated Franklin ACMG Retrieval", page_icon="🧬")

# Title and description
st.title("Automated Franklin ACMG Classification Retrieval")
st.write("Enter variant details to generate a Franklin Genoox URL and retrieve the 'Franklin ACMG Classification' and the two lines below it.")

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
st.subheader("Authentication (Required for Franklin Genoox)")
cookies = st.text_area("Browser Cookies", placeholder="Paste cookies from a logged-in browser session (e.g., name1=value1; name2=value2)", help="Log in to Franklin Genoox, open developer tools (F12 > Network), refresh the variant page, select the request to the URL, and copy the 'Cookie' header from the Request Headers.")

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
            else:
                st.warning("No cookies provided. Franklin Genoox likely requires login, so scraping may fail.")

            # Send request to the URL
            response = requests.get(api_url, headers=headers, cookies=cookies_dict, timeout=10)

            # Check if the request was successful
            if response.status_code == 200:
                # Get the page text
                page_text = response.text

                # Debugging: Show a snippet of the page content
                st.subheader("Debug: Page Content Snippet")
                st.text(page_text[:500] + "..." if len(page_text) > 500 else page_text)

                # Check for login page indicators
                login_indicators = ["sign in", "login", "authenticate", "unauthorized"]
                if any(indicator in page_text.lower() for indicator in login_indicators):
                    st.error("The fetched page appears to be a login page. Please provide valid cookies from a logged-in session.")
                    st.markdown(f"Please check manually: [Open URL]({api_url})")
                else:
                    # Search for "Franklin ACMG Classification" and two lines below
                    pattern = r"Franklin ACMG Classification.*?([\s\S]*?)(?:<[^>]+>|\n|$)(?:[\s\S]*?)(?:<[^>]+>|\n|$)(?:[\s\S]*?)(?:<[^>]+>|\n|$)"
                    match = re.search(pattern, page_text, re.IGNORECASE | re.DOTALL)
                    
                    st.subheader("ACMG Classification Results")
                    if match:
                        # Split into lines and take the first two non-empty ones after the header
                        lines = [line.strip() for line in match.group(0).splitlines() if line.strip()]
                        classification_lines = [line for line in lines if line.lower() != "franklin acmg classification"][:2]
                        
                        if classification_lines:
                            st.success("Data retrieved successfully!")
                            st.write("**Franklin ACMG Classification Lines:**")
                            st.write(f"Line 1: {classification_lines[0] if len(classification_lines) > 0 else 'Not found'}")
                            st.write(f"Line 2: {classification_lines[1] if len(classification_lines) > 1 else 'Not found'}")
                        else:
                            st.warning("Found 'Franklin ACMG Classification' but no valid lines below it.")
                            st.markdown(f"Please check manually: [Open URL]({api_url})")
                    else:
                        # Fallback: Search for ACMG terms and criteria
                        acmg_terms = [
                            r"pathogenic",
                            r"likely pathogenic",
                            r"benign",
                            r"likely benign",
                            r"uncertain significance",
                            r"\b(P[MSB]\d|BA\d|BP\d)\b"
                        ]
                        found_terms = []
                        for pattern in acmg_terms:
                            matches = re.findall(pattern, page_text.lower(), re.IGNORECASE)
                            if matches:
                                found_terms.extend(matches)
                        
                        if found_terms:
                            st.success("No exact 'Franklin ACMG Classification' match, but related terms found:")
                            st.write("**Detected ACMG Terms and Criteria:**")
                            st.write(", ".join(set(found_terms)))
                        else:
                            st.warning("No 'Franklin ACMG Classification' or related terms found. The page may use JavaScript rendering or require login.")
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
4. Look for the 'Franklin ACMG Classification' section and note the two lines below it (e.g., classification like 'Pathogenic' and criteria like 'PM1, PS2').
5. If no classification is available, check variant reports or annotations.
""")

# Debugging and troubleshooting
st.subheader("Troubleshooting")
st.write("""
- **Authentication**: The debug snippet shows a login page. Provide valid cookies from a logged-in session (F12 > Network > Cookies).
- **JavaScript Rendering**: If the content is missing, the page may load data via JavaScript. Try manual retrieval or contact Franklin Genoox for API access.
- **HTML Structure**: If no data is found, inspect the page's HTML (F12 > Elements) around 'Franklin ACMG Classification' and share the structure to refine the regex.
- **Terms of Service**: Web scraping may violate Franklin Genoox's terms. Contact their support for API access.
- **Deployment**: Ensure 'streamlit' and 'requests' are in 'requirements.txt' and redeploy the app.
""")
