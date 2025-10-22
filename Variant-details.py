See new posts

i cannot fetch the api, so in the script make the variant search like this https://franklin.genoox.com/clinical-db/variant/snp/chr17-41276044-ACT-A?app=assessment-tools, where the last part is the variant. After that is searched, one should retrieve the acmg classification criteria; write a streamlit for that

Below is a Streamlit script that constructs a URL for variant search based on user input in the format chr{chromosome}-{position}-{reference}-{alternate} and fetches the ACMG classification criteria from the Franklin Genoox API. Since you mentioned you cannot fetch the API directly, the script will focus on constructing the URL correctly and provide a placeholder for handling the API response, assuming you have access to the API or a way to retrieve the data manually. The script includes error handling and user-friendly input fields.python

import streamlit as st
import requests
import json

# Streamlit app configuration
st.set_page_config(page_title="Variant ACMG Classification", page_icon="🧬")

# Title and description
st.title("Variant ACMG Classification Finder")
st.write("Enter variant details to construct a Franklin Genoox API URL and retrieve ACMG classification criteria.")

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

# Construct the variant string
variant = f"chr{chromosome}-{position}-{reference}-{alternate}"

# Construct the API URL
base_url = "https://franklin.genoox.com/clinical-db/variant/snp"
api_url = f"{base_url}/{variant}?app=assessment-tools"

# Display the constructed URL
st.subheader("Generated API URL")
st.write(f"[Open URL]({api_url})")

# Placeholder for API key input (if required)
api_key = st.text_input("API Key (if required)", type="password")

# Button to fetch data
if st.button("Fetch ACMG Classification"):
    if not all([chromosome, position, reference, alternate]):
        st.error("Please fill in all variant details.")
    else:
        try:
            # Attempt to fetch data from the API
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            response = requests.get(api_url, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                
                # Placeholder for extracting ACMG classification
                # Adjust the parsing based on the actual API response structure
                acmg_classification = data.get("acmg_classification", "No ACMG classification found")
                
                st.subheader("ACMG Classification Results")
                if acmg_classification != "No ACMG classification found":
                    st.success("Classification retrieved successfully!")
                    st.json(data)  # Display raw JSON for debugging
                    st.write("**ACMG Classification Criteria:**")
                    st.write(acmg_classification)
                else:
                    st.warning("No ACMG classification data available in the response.")
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
                st.write(response.text)
                
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {str(e)}")
            st.write("Please check the API URL or your API key (if required).")
        except json.JSONDecodeError:
            st.error("Invalid JSON response from the API.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

# Additional instructions
st.subheader("Notes")
st.write("""
- Ensure the variant format is correct (e.g., chr17-41276044-ACT-A).
- If the API requires authentication, provide a valid API key.
- The API response parsing assumes a field like 'acmg_classification'. Adjust the code based on the actual API response structure.
- If you cannot access the API, manually open the generated URL in a browser to retrieve the data.
""")

How the Script WorksUser Interface:The Streamlit app provides input fields for chromosome, position, reference allele, and alternate allele.
These inputs are used to construct a variant string in the format chr{chromosome}-{position}-{reference}-{alternate}.
The constructed URL is displayed as a clickable link.

URL Construction:The base URL is https://franklin.genoox.com/clinical-db/variant/snp.
The variant string is appended, followed by ?app=assessment-tools, as specified (e.g., https://franklin.genoox.com/clinical-db/variant/snp/chr17-41276044-ACT-A?app=assessment-tools).

API Fetching:A placeholder is included for fetching data using the requests library.
An optional API key input is provided for authentication, as some APIs require it.
The script attempts to parse the JSON response and extract the ACMG classification (assuming a field like acmg_classification exists).

Error Handling:Validates that all input fields are filled.
Handles API request errors, invalid JSON responses, and unexpected errors.
Displays user-friendly error messages.

Output:Displays the generated URL.
If the API call is successful, it shows the ACMG classification criteria and the raw JSON response for debugging.
If the API call fails, it provides error details and suggests checking the URL or API key.

NotesAPI Access: Since you mentioned you cannot fetch the API, you can use the generated URL to manually access the Franklin Genoox page in a browser. If you have API access, provide the API key or modify the headers based on the API's authentication requirements.
Response Parsing: The script assumes the API returns a JSON with an acmg_classification field. You’ll need to adjust the parsing logic based on the actual API response structure, which you can inspect by manually accessing the URL or checking the API documentation.
Dependencies: Ensure you have streamlit and requests installed (pip install streamlit requests).
Running the App: Save the script (e.g., as app.py) and run it with streamlit run app.py. Open the provided local URL (usually http://localhost:8501) in your browser.
API Limitations: If the API requires specific headers, cookies, or a subscription, update the headers dictionary accordingly. If you don’t have API access, the script still generates the correct URL for manual use.

If you have the API response structure or additional details (e.g., authentication requirements), I can refine the parsing logic or provide further guidance. Let me know!

i do not have api access

Since you don't have API access, the Streamlit script below will focus on constructing the Franklin Genoox URL in the format https://franklin.genoox.com/clinical-db/variant/snp/chr{chromosome}-{position}-{reference}-{alternate}?app=assessment-tools based on user input and allow you to open it manually to retrieve the ACMG classification criteria. The script will not attempt to fetch the API directly, as you confirmed you cannot access it. Instead, it provides a user-friendly interface to generate the URL and includes guidance for manually retrieving the data.python

import streamlit as st

# Streamlit app configuration
st.set_page_config(page_title="Variant URL Generator", page_icon="🧬")

# Title and description
st.title("Franklin Genoox Variant URL Generator")
st.write("Enter variant details to generate a Franklin Genoox URL for retrieving ACMG classification criteria.")

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

# Construct the variant string
variant = f"chr{chromosome}-{position}-{reference}-{alternate}"

# Construct the URL
base_url = "https://franklin.genoox.com/clinical-db/variant/snp"
api_url = f"{base_url}/{variant}?app=assessment-tools"

# Display the constructed URL
st.subheader("Generated URL")
if all([chromosome, position, reference, alternate]):
    st.success("URL generated successfully!")
    st.markdown(f"[Open URL in Browser]({api_url})")
else:
    st.warning("Please fill in all variant details to generate the URL.")

# Instructions for manual retrieval
st.subheader("How to Retrieve ACMG Classification")
st.write("""
1. Click the generated URL above to open it in your browser.
2. Log in to Franklin Genoox if required (you may need an account).
3. Navigate to the variant details page.
4. Look for the ACMG classification criteria, typically listed under variant assessment or classification sections.
5. If no ACMG classification is available, check the variant's associated reports or annotations.
""")

# Additional notes
st.subheader("Notes")
st.write("""
- Ensure the variant format is correct (e.g., chr17-41276044-ACT-A).
- The URL is constructed for the Franklin Genoox platform, which may require authentication.
- If the URL does not work, verify your input details or check if Franklin Genoox has updated its URL structure.
- Contact Franklin Genoox support for access issues or if no classification data is available.
""")

How the Script WorksUser Interface:Provides input fields for chromosome, position, reference allele, and alternate allele (pre-filled with your example: chr17-41276044-ACT-A).
Constructs the variant string in the format chr{chromosome}-{position}-{reference}-{alternate}.

URL Construction:Builds the URL using the base https://franklin.genoox.com/clinical-db/variant/snp and appends the variant string and ?app=assessment-tools (e.g., https://franklin.genoox.com/clinical-db/variant/snp/chr17-41276044-ACT-A?app=assessment-tools).
Displays the URL as a clickable link if all inputs are provided.

Manual Retrieval Guidance:Since you lack API access, the script includes instructions for manually opening the URL in a browser and navigating the Franklin Genoox platform to find the ACMG classification criteria.
Alerts the user if any input fields are empty.

Error Handling:Ensures all input fields are filled before generating the URL.
Provides notes on verifying the variant format and troubleshooting potential issues with the Franklin Genoox platform.

How to UseInstall Streamlit:Ensure you have Streamlit installed: pip install streamlit.

Run the Script:Save the script as app.py.
Run it with streamlit run app.py.
Open the provided URL (usually http://localhost:8501) in your browser.

Enter Variant Details:Input the chromosome, position, reference, and alternate alleles.
The script generates the URL, which you can click to open in your browser.

Retrieve ACMG Classification:Follow the on-screen instructions to log in to Franklin Genoox (if required) and locate the ACMG classification criteria on the variant page.
If the platform requires an account or specific permissions, ensure you have access or contact Franklin Genoox support.

NotesDependencies: Requires only streamlit (pip install streamlit).
Franklin Genoox Access: The script assumes you have access to the Franklin Genoox platform via a browser. If you need an account or encounter access issues, you may need to contact their support or verify your credentials.
URL Validation: The URL format matches your provided example. If Franklin Genoox changes its URL structure, you may need to update the base_url or query parameters.
ACMG Classification: The classification criteria (e.g., Pathogenic, Benign) are typically found in the variant details or assessment section of the Franklin Genoox page. Check for annotations like PM1, PS2, or other ACMG criteria codes.

If you need help with specific Franklin Genoox navigation steps or have additional details about the platform's interface, let me know, and I can tailor the instructions further!

the retrieval should be automatic

Since you don't have API access, automating the retrieval of ACMG classification criteria from the Franklin Genoox platform is challenging, as direct API calls are not possible, and the platform likely requires browser-based authentication (e.g., login credentials) or restricts automated access. However, I can provide a Streamlit script that automates the URL construction and attempts to scrape the ACMG classification criteria from the Franklin Genoox variant page using web scraping techniques (e.g., with requests and beautifulsoup4). Be aware that web scraping may be against Franklin Genoox's terms of service, and the platform may require authentication, which complicates automation. The script will include a fallback for manual retrieval if scraping fails.ApproachURL Construction: The script will construct the URL in the format https://franklin.genoox.com/clinical-db/variant/snp/chr{chromosome}-{position}-{reference}-{alternate}?app=assessment-tools.
Web Scraping: It will attempt to fetch the page content using requests and parse it with beautifulsoup4 to extract ACMG classification criteria.
Authentication Handling: Since you don't have API access and the platform may require login, the script includes an optional field for cookies or session tokens (if you can provide them from a logged-in browser session).
Fallback: If scraping fails due to authentication or other issues, it provides the URL for manual retrieval with clear instructions.
Limitations: Without knowing the exact HTML structure of the Franklin Genoox page, the script assumes the ACMG classification is in a common HTML element (e.g., a <div> with a class like acmg-classification). You'll need to adjust the parsing logic based on the actual page structure.

Streamlit Scriptpython

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


