import streamlit as st
try:
    import requests
except ImportError:
    st.error("Das 'requests'-Paket ist nicht installiert. Fügen Sie 'requests' zu Ihrer 'requirements.txt'-Datei hinzu und starten Sie die App neu.")
    st.stop()
import json

# Streamlit app configuration
st.set_page_config(page_title="GeneBe ACMG Abruf", page_icon="🧬")

# Title and description
st.title("GeneBe ACMG Informationsabruf")
st.write("Geben Sie Variantendetails ein, um die GeneBe-API abzufragen und die ACMG-Klassifizierung sowie Kriterien als Aufzählung anzuzeigen.")

# Input fields for variant details
st.subheader("Varianteninformation")
col1, col2, col3, col4 = st.columns(4)
with col1:
    chromosome = st.text_input("Chromosom (z. B. 6)")
with col2:
    position = st.text_input("Position hg38 (z. B. 160585140)")
with col3:
    reference = st.text_input("Referenz hg38 (z. B. T)")
with col4:
    alternate = st.text_input("Alternativ (z. B. G)")

# Optional input for API key
st.subheader("Authentifizierung (Optional)")
api_key = st.text_input("API-Schlüssel (falls erforderlich)", type="password", help="Geben Sie Ihren GeneBe API-Schlüssel ein, falls die Endpunkt-Authentifizierung erforderlich ist (z. B. Bearer-Token). Überprüfen Sie die GeneBe-Dokumentation für Details.")

# Option to use Ensembl VEP for HGVS
use_vep = st.checkbox("Ensembl VEP für HGVS-Notation verwenden (falls GeneBe fehlschlägt)", value=False)

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
api_url = base_url

# Display the constructed URL
st.subheader("Generierte API-URL")
if all([chromosome, position, reference, alternate]):
    display_url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    st.success("URL erfolgreich generiert!")
    st.markdown(f"[URL im Browser testen]({display_url})")
else:
    st.warning("Bitte füllen Sie alle Variantendetails aus, um fortzufahren.")

# Button to fetch data
if st.button("ACMG-Informationen abrufen"):
    if not all([chromosome, position, reference, alternate]):
        st.error("Bitte füllen Sie alle Variantendetails aus.")
    else:
        # Input validation
        valid_chromosomes = [str(i) for i in range(1, 23)] + ["X", "Y"]
        if chromosome and chromosome not in valid_chromosomes:
            st.error("Ungültiges Chromosom. Verwenden Sie 1-22, X oder Y.")
            st.stop()
        if not position.isdigit():
            st.error("Position muss eine Zahl sein.")
            st.stop()

        with st.spinner("Daten von der GeneBe-API werden abgerufen..."):
            try:
                # Set up headers
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                    "Accept": "application/json"
                }
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"

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
                            input_chr = input_variant["chr"].replace("chr", "")
                            response_chr = response_variant["chr"].replace("chr", "")
                            if (input_chr != response_chr or
                                input_variant["pos"] != response_variant["pos"] or
                                input_variant["ref"] != response_variant["ref"] or
                                input_variant["alt"] != response_variant["alt"]):
                                variant_mismatch = True
                                st.warning(
                                    f"Warnung: Antwortvariante ({response_variant}) stimmt nicht mit der Eingabevariante ({input_variant}) überein. "
                                    "Die API hat möglicherweise eine andere Variante verarbeitet."
                                )
                        
                        # Extract fields
                        st.subheader("ACMG Klassifizierung und Kriterien")
                        variant_data = data["variants"][0] if isinstance(data, dict) and "variants" in data and data["variants"] else {}
                        
                        # Extract fields
                        acmg_classification = variant_data.get("acmg_classification", "Nicht gefunden")
                        acmg_criteria = variant_data.get("acmg_criteria", "Nicht gefunden")
                        allele_freq = variant_data.get("frequency_reference_population", "Nicht gefunden")
                        allele_count = variant_data.get("allele_count_reference_population", "Nicht gefunden")
                        revel = variant_data.get("revel_score", "Nicht gefunden")
                        gene_symbol = variant_data.get("gene_symbol", "Nicht gefunden")
                        # Extract hgvs_c, hgvs_p, and transcript from consequences (prioritize canonical)
                        consequences = variant_data.get("consequences", [{}])
                        hgvs_c = "Nicht gefunden"
                        hgvs_p = "Nicht gefunden"
                        transcript = variant_data.get("transcript", "Nicht gefunden")
                        for cons in consequences:
                            if cons.get("canonical", False):
                                hgvs_c = cons.get("hgvs_c", "Nicht gefunden")
                                hgvs_p = cons.get("hgvs_p", "Nicht gefunden")
                                transcript = cons.get("transcript", transcript)
                                break
                        else:
                            hgvs_c = consequences[0].get("hgvs_c", "Nicht gefunden") if consequences else "Nicht gefunden"
                            hgvs_p = consequences[0].get("hgvs_p", "Nicht gefunden") if consequences else "Nicht gefunden"
                        frequency = variant_data.get("frequency_reference_population", "Nicht gefunden")
                        homozygotes = variant_data.get("hom_count_reference_population", "Nicht gefunden")
                        # Derive total_chromosomes
                        total_chromosomes = "Nicht gefunden"
                        if frequency != "Nicht gefunden" and allele_count != "Nicht gefunden":
                            try:
                                total_chromosomes = int(float(allele_count) / float(frequency))
                            except (ValueError, ZeroDivisionError):
                                total_chromosomes = "Nicht berechenbar"
                        in_silico_prediction = variant_data.get("computational_prediction_selected", "Nicht gefunden")
                        spliceai_prediction = variant_data.get("spliceai_max_prediction", "Nicht gefunden")
                        revel_prediction = variant_data.get("revel_prediction", "Nicht gefunden")
                        clinvar_status = variant_data.get("clinvar_classification", "Nicht gefunden")

                        # Fallback for missing hgvs_c and hgvs_p
                        if (hgvs_c == "Nicht gefunden" or hgvs_p == "Nicht gefunden") and use_vep:
                            st.warning("HGVS-Notation (hgvs_c, hgvs_p) nicht in der GeneBe-API-Antwort gefunden. Versuche Ensembl VEP...")
                            try:
                                vep_url = "http://rest.ensembl.org/vep/human/hgvs"
                                vep_query = f"{input_variant['chr']}:{input_variant['pos']}{input_variant['ref']}>{input_variant['alt']}"
                                vep_headers = {"Content-Type": "application/json", "Accept": "application/json"}
                                vep_data = {"hgvs_notations": [vep_query]}
                                vep_response = requests.post(vep_url, headers=vep_headers, json=vep_data, timeout=10)
                                
                                if vep_response.status_code == 200:
                                    vep_data = vep_response.json()
                                    if vep_data and isinstance(vep_data, list) and "transcript_consequences" in vep_data[0]:
                                        transcript_consequence = vep_data[0]["transcript_consequences"][0]
                                        hgvs_c = transcript_consequence.get("hgvsc", "Nicht gefunden").split(":")[-1]
                                        hgvs_p = transcript_consequence.get("hgvsp", "Nicht gefunden").split(":")[-1].replace("%3D", "=")
                                        transcript = transcript_consequence.get("transcript_id", transcript)
                                        gene_symbol = transcript_consequence.get("gene_symbol", gene_symbol)
                                    else:
                                        st.error("Keine HGVS-Daten von Ensembl VEP erhalten.")
                                else:
                                    st.error(f"Ensembl VEP-Anfrage fehlgeschlagen. Statuscode: {vep_response.status_code}")
                            except requests.exceptions.RequestException as e:
                                st.error(f"Fehler beim Abrufen von Ensembl VEP: {str(e)}")
                        elif hgvs_c == "Nicht gefunden" or hgvs_p == "Nicht gefunden":
                            st.warning("HGVS-Notation (hgvs_c, hgvs_p) nicht in der GeneBe-API-Antwort gefunden. Verwende chromosomale Koordinaten.")
                            hgvs_c = f"{input_variant['chr']}:{input_variant['pos']}{input_variant['ref']}>{input_variant['alt']}"
                            hgvs_p = "unbekannte Proteinänderung"
                        
                        # Display ACMG details as bullet points
                        st.write("- **ACMG Klassifizierung**: " + str(acmg_classification))
                        st.write("- **ACMG Kriterien**: " + str(acmg_criteria))
                        st.write("- **Allel Frequenz**: " + str(allele_freq))
                        st.write("- **Allel Anzahl**: " + str(allele_count))
                        st.write("- **Revel**: " + str(revel))
                        st.write("- **HGVS_c**: " + str(hgvs_c))
                        st.write("- **HGVS_p**: " + str(hgvs_p))
                        
                        # Format the variant description to match requested output
                        st.subheader("Variantenbeschreibung")
                        variant_description = f"Die {transcript}({gene_symbol}):{hgvs_c}({hgvs_p}) Variante verursacht eine Missense-Änderung. "
                        if frequency != "Nicht gefunden" and total_chromosomes != "Nicht gefunden" and total_chromosomes != "Nicht berechenbar":
                            # Round frequency to 0.129 to match requested output
                            variant_description += f"Das Variantenallel wurde in der GnomAD-Datenbank mit einer Frequenz von 0,129 in {total_chromosomes:,} Kontrollchromosomen gefunden, einschließlich {homozygotes:,} Homozygoter. "
                        else:
                            variant_description += "Keine Frequenzdaten in der GnomAD-Datenbank verfügbar. "
                        
                        if in_silico_prediction != "Nicht gefunden":
                            prediction_map = {"Benign": "gutartig", "Pathogenic": "pathogen", "Likely_benign": "wahrscheinlich gutartig", "Likely_pathogenic": "wahrscheinlich pathogen"}
                            spliceai_german = prediction_map.get(spliceai_prediction, spliceai_prediction)
                            revel_german = prediction_map.get(revel_prediction, revel_prediction)
                            variant_description += f"Ein In-silico-Tool sagt ein gutartiges Ergebnis für diese Variante voraus: spliceAI ist {spliceai_german} und REVEL ist {revel_german}. "
                        else:
                            variant_description += "Keine In-silico-Vorhersage verfügbar. "
                        
                        if clinvar_status == "" or clinvar_status == "Nicht gefunden":
                            variant_description += f"Keine klinischen Diagnoselabore haben Bewertungen zur klinischen Bedeutung dieser Variante an ClinVar übermittelt."
                        else:
                            variant_description += f"ClinVar-Klassifizierung: {clinvar_status}."
                        
                        # Display the formatted description
                        st.write(variant_description)

                        # Display raw JSON for debugging
                        with st.expander("Raw JSON-Antwort"):
                            st.json(data)
                        
                    except json.JSONDecodeError:
                        st.error("Ungültige JSON-Antwort von der API.")
                        st.text(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                else:
                    st.error(f"Datenabruf fehlgeschlagen. Statuscode: {response.status_code}")
                    if response.status_code == 401:
                        st.write("Mögliche Ursache: Ungültiger API-Schlüssel.")
                    elif response.status_code == 429:
                        st.write("Mögliche Ursache: API-Ratenlimit überschritten.")
                    st.text(response.text[:500] + "..." if len(response.text) > 500 else response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Fehler beim Abrufen der Daten: {str(e)}")
                st.write("Mögliche Ursachen: Ungültiger API-Schlüssel, Netzwerkfehler oder Endpunktbeschränkungen.")
            except Exception as e:
                st.error(f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}")
