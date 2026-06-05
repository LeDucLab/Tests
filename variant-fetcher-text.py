import streamlit as st
import requests
import json

st.set_page_config(page_title="GeneBe ACMG Retrieval", page_icon="🧬")

st.title("GeneBe ACMG Information Retrieval")
st.write("Enter variant as: chr pos ref alt (e.g. chr1 123456 A T)")

# -----------------------------
# VARIANT INPUT
# -----------------------------
st.subheader("Variant Input")
variant_input = st.text_input(
    "Variant (chr pos ref alt)",
    placeholder="chr1 123456 A T"
)

chromosome = position = reference = alternate = None

if variant_input:
    parts = variant_input.strip().replace(",", " ").split()

    if len(parts) == 4:
        chromosome, position, reference, alternate = parts
    else:
        st.error("Invalid format. Use: chr pos ref alt")

# -----------------------------
# API CONFIG
# -----------------------------
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

# -----------------------------
# REPORT TEMPLATE
# -----------------------------
def build_report(v, c):
    gene = v.get("gene_symbol", "NA")
    hgvs_c = c.get("hgvs_c", "NA")
    hgvs_p = c.get("hgvs_p", "NA")
    exon_rank = c.get("exon_rank", "NA")
    exon_count = c.get("exon_count", "NA")

    clinvar = v.get("clinvar_classification", "NA")
    acmg = v.get("acmg_criteria", "NA")
    classification = v.get("acmg_classification", "NA")

    af = v.get("gnomad_exomes_af", "NA")
    ac_exome = v.get("gnomad_exomes_ac", "NA")
    ac_genome = v.get("gnomad_genomes_ac", "NA")

    return f"""
Vor Bewertung auf aktuelle VCEP prüfen: https://cspec.genome.network/cspec/ui/svi/

Die o. g. Leseraster-Variante im {gene}-Gen ({hgvs_c}; {hgvs_p}) führt durch eine Leserasterverschiebung (Frameshift) zum Auftreten eines vorzeitigen Stopcodons und zum Abbruch der Translation des korrespondierenden Proteins in Exon {exon_rank} von {exon_count}.

[NMD] Sehr wahrscheinlich wird von dem betroffenen Allel kein Protein gebildet, da mit einem vorzeitigen Abbau der mRNA per Nonsense Mediated mRNA Decay (NMD) gerechnet werden muss.

Diese Variante wurde in ClinVar beschrieben als: {clinvar}.

In gnomAD ist die Variante mit einer Allelfrequenz von {af} nachweisbar (Exome AC: {ac_exome}, Genomes AC: {ac_genome}).

ACMG-Kriterien: {acmg}

Gesamtbewertung: {classification}
"""

# -----------------------------
# URL DISPLAY
# -----------------------------
st.subheader("Generated API URL")

if all([chromosome, position, reference, alternate]):
    display_url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    st.success("URL generated successfully!")
    st.markdown(f"[Test URL in Browser]({display_url})")
else:
    st.warning("Enter a valid variant to generate URL.")

# -----------------------------
# FETCH DATA
# -----------------------------
if st.button("Retrieve ACMG Information"):

    if not all([chromosome, position, reference, alternate]):
        st.error("Please enter a valid variant.")
    else:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }

            response = requests.get(base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                st.subheader("ACMG Classification and Criteria")

                variant_data = data["variants"][0] if data.get("variants") else {}
                consequences = variant_data.get("consequences", [{}])
                consequence = consequences[0] if consequences else {}

                st.write(f"- **ACMG Klassifizierung**: {variant_data.get('acmg_classification')}")
                st.write(f"- **ACMG Kriterien**: {variant_data.get('acmg_criteria')}")
                st.write(f"- **Allel Frequenz**: {variant_data.get('frequency_reference_population')}")
                st.write(f"- **Allel Anzahl**: {variant_data.get('allele_count_reference_population')}")
                st.write(f"- **Revel**: {variant_data.get('revel_score')}")
                st.write(f"- **HGVS_c**: {consequence.get('hgvs_c')}")

                # -----------------------------
                # FRAMESHIFT-CONDITIONAL REPORT
                # -----------------------------
                st.subheader("Generated Clinical Report")

                is_frameshift = "frameshift_variant" in consequence.get("consequences", [])

                if is_frameshift:
                    report = build_report(variant_data, consequence)

                    st.text_area("Report", report, height=500)

                    st.download_button(
                        "Download Report",
                        report,
                        file_name="acmg_report.txt"
                    )
                else:
                    st.info("No frameshift_variant detected → No clinical report generated.")

                with st.expander("Raw JSON Response"):
                    st.json(data)

            else:
                st.error(f"Failed: {response.status_code}")
                st.text(response.text[:500])

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)}")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
