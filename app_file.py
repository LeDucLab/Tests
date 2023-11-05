import streamlit as st
from datetime import datetime


# Create a Streamlit app
st.title("Arzt Brief Generator")

# Get the current date and time
current_datetime = datetime.now()

#Get patient data
# Create a selectbox to choose an option for the gender
st.markdown("### Patienten Daten")
col1, col2, col3= st.columns(3)
Titel = col1.selectbox("Titel", ["Frau", "Herr", "Familie"])

Vorname = col2.text_input("Vorame")
Name = col3.text_input("Name")

st.markdown("### Fragestellung")
question = st.text_input("Fragestellung")

# Add a selectbox for choosing the type of counciling
st.markdown("### Art der Beratung und Analyse")
col1, col2, col3, col4 = st.columns(4)
council = col1.selectbox("Art der Beratung", ["Erstberatung", "Befundbesprechung"])
person = col2.selectbox("Patiententyp", ["Kind", "Erwachsen"])
disease = col3.selectbox("Fragestellung", ["NDD +/- Epilepsie", "unspezifisch", "HNPCC", "FBrEK", "SCA", "HTT"])
analysis = col4.selectbox("Art der genetischen Testung", ["Exom", "Exom+CNV+CA", "gezielt", "HNPCC", "FBrEK", "SCA", "HTT"])

# Add anamnesis button
if council == "Erstberatung" and disease == "unspezifisch":
    st.markdown("### Anamnese")
    default_text = """In Bezug af die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:"""
    free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)
elif council == "Erstberatung" and disease == "NDD +/- Epilepsie":
    st.markdown("### Anamnese")
    default_text = """In Bezug af die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:
    - Geburtshintergrund: Geburtsart XX, Geburtstermin XX, Geburtsmaßen
    - Meilensteine der motorischen Entwicklung: Drehen XX, Sitzen XX, Gehen XX
    - Meilensteine der sprachlichen Entwicklung: esrte Laute/Worte XX, aktueller Status XX
    - Soziale Entwicklung: Kita/Schulbesuch XX, Interaktion mit der Familie/Gleichaltrigen XX
    - Aktuelle Symptome und Beobachtungen: Art der Entwicklungsverzögerung XX, Verhaltensauffälligkeiten XX, Kommunikationsfähigkeiten XX, Epilepsie XX
    - Bisherige Untersuchungen und Interventionen: Frühere Arztbesuche oder Therapieansätze XX, Diagnosen oder Empfehlungen XX"""
    free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)
    
#Add Familienanamnese button
st.markdown("### Familienanamnese")
familienanamnese = st.selectbox("Familienanamnese", ["auffällig", "unauffällig"])
if familienanamnese == "unauffällig":
    family="""Sie berichteten keine für die Fragestellung relevanten Krankheitsbilder in Ihrer Familie."""
elif familienanamnese == "auffällig":
    fam_text="""Hinsichtlich der aktuellen Fragestellung berichteten Sie, dass bei XX eine XX vorliegt. Unterlagen zu den genannten Familienmitgliedern liegen uns nicht vor. Ein drei Generationen umfassender Stammbaum befindet sich im Anhang."""
    family=st.text_area("Relevante Erkrankungen in der Familie", fam_text)

#Add Körperliche Untersuchung
st.markdown("### Körperliche Untersuchung")
if person == "Kind":
    body_text= """Wir sahen XX im Alter von XX Jahren. Ihre/Seine Körpermaße zur Vorstellung betrugen: [pedz] (https://www.pedz.de/de/bmi.html). Fazial ergaben sich keine Auffälligkeiten/Fazial fielen … auf."""
    body=st.text_area("Untersuchung", body_text)


  
    
    

# Letter Structure for all types of letters
#Beratungsgrund
beratung_line = f"**Beratungsgrund:** V.a. genetisch bedingte {question}"

#Begrüßung
if Titel== "Herr":
    hello_line = f"Sehr geehrter {Titel} {Name},"
elif Titel != "Herr":
    hello_line = f"Sehr geehrte {Titel} {Name},"

#Date of Beratung
first_line= f"am {current_datetime.strftime('%d.%m.%Y')} stellten Sie Ihren Sohn/Ihre Tochter in unserer genetischen Sprechstunde vor."
#Eigenanamnese
anamnese_first_line="""**Eigenanamnese:**\n
In Bezug af die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:\n"""


# Create a button
if st.button("Zur Vorlage"):
    # Display text based on the selected option
    if council == "Erstberatung" and Titel == "Herr" and person == "Kind" and disease == "unspezifisch" and analysis == "Exom" :
        #st.write("**Beratungsgrund:** V.a. genetisch bedingte", question)
        st.markdown(beratung_line, unsafe_allow_html=True)
        #st.write("Sehr geehrter", Titel, Name,",")
        st.markdown(hello_line, unsafe_allow_html=True)
        #st.write("am", current_datetime.strftime('%d.%m.%Y'), "stellten Sie Ihren Sohn/Ihre Tochter  in unserer genetischen Sprechstunde vor.")
        st.markdown(first_line, unsafe_allow_html=True)
        st.write("**Eigenanamnese:**")
        #st.write("Sie berichteten, dass XX nach un/auffälliger Schwangerschaft in der Schwangerschaftswoche (per Sectio/als hypotrophes Neugeborenes/mit …) geboren wurde. Ihre/Seine Geburtsmaße betrugen … [Daten aus pedz].")
        st.markdown(free_anamnesis, unsafe_allow_html=True)
        st.write ("**Familienanamnese:**")
        st.markdown(family, unsafe_allow_html=True)
        #st.write("Hinsichtlich der aktuellen Fragestellung berichteten Sie, dass bei XX eine XX vorliegt. Unterlagen zu den genannten Familienmitgliedern liegen uns nicht vor. Ein drei Generationen umfassender Stammbaum befindet sich im Anhang. Sie berichteten keine für die Fragestellung relevanten Krankheitsbilder in Ihrer Familie.")
        st.write("**Körperliche Untersuchung:**")
        st.markdown(body, unsafe_allow_html=True)
        #st.write("Wir sahen XX im Alter von  Jahren. Ihre/Seine Körpermaße zur Vorstellung betrugen:[Daten aus pedz]. Fazial ergeben sich keine Auffälligkeiten/Fazial fielen … auf.")
        st.write("**Beurteilung:**")
        st.write("Bei Ihrem Sohn/Ihrer Tochter besteht der Verdacht auf eine genetisch bedingte Entwicklungsstörung/Intelligenzminderung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Exomdiagnostik mit Beurteilung der hierfür ursächlichen Genen bei ihm/ihr. Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen.")
        st.write("Wir hoffen, Sie mit unserem Gespräch und diesem Brief vorerst ausreichend informiert zu haben. Bei Rückfragen stehen wir gerne auch telefonisch zur Verfügung.")
        st.write("Mit freundlichen Grüßen")
        st.write("")
        st.write("PD Dr. D. Le Duc, MD/PhD", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("<font size='2'>FÄ für Humangenetik</font>", unsafe_allow_html=True)
    elif council == "Erstberatung" and Titel != "Herr" and person == "Kind" and disease == "unspezifisch" and analysis == "Exom" :
        st.write("**Beratungsgrund:** V.a. genetisch bedingte", question)
        st.write("Sehr geehrte", Titel, Name,",")
        st.write("am", current_datetime.strftime('%d.%m.%Y'), "stellten Sie Ihren Sohn/Ihre Tochter  in unserer genetischen Sprechstunde vor.")
        st.write("**Eigenanamnese:**")
        st.write("Sie berichteten, dass XX nach un/auffälliger Schwangerschaft in der Schwangerschaftswoche (per Sectio/als hypotrophes Neugeborenes/mit …) geboren wurde. Ihre/Seine Geburtsmaße betrugen … [Daten aus pedz].")
        st.write ("**Familienanamnese:**")
        st.write("Hinsichtlich der aktuellen Fragestellung berichteten Sie, dass bei XX eine XX vorliegt. Unterlagen zu den genannten Familienmitgliedern liegen uns nicht vor. Ein drei Generationen umfassender Stammbaum befindet sich im Anhang. Sie berichteten keine für die Fragestellung relevanten Krankheitsbilder in Ihrer Familie.")
        st.write("**Körperliche Untersuchung:**")
        st.write("Wir sahen XX im Alter von  Jahren. Ihre/Seine Körpermaße zur Vorstellung betrugen:[Daten aus pedz]. Fazial ergeben sich keine Auffälligkeiten/Fazial fielen … auf.")
        st.write("**Beurteilung:**")
        st.write("Bei Ihrem Sohn/Ihrer Tochter besteht der Verdacht auf eine genetisch bedingte Entwicklungsstörung/Intelligenzminderung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Exomdiagnostik mit Beurteilung der hierfür ursächlichen Genen bei ihm/ihr. Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen.")
        st.write("Wir hoffen, Sie mit unserem Gespräch und diesem Brief vorerst ausreichend informiert zu haben. Bei Rückfragen stehen wir gerne auch telefonisch zur Verfügung.")
        st.write("Mit freundlichen Grüßen")
        st.write("")
        st.write("PD Dr. D. Le Duc, MD/PhD")
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("<font size='2'>FÄ für Humangenetik</font>", unsafe_allow_html=True)
   # elif council == "Erstberatung" and Titel == "Herr" and person == "Kind" and disease == "NDD +/- Epilepsie" and analysis == "Exom+CNV+CA" :
        
       
   
# elif option == "Option 2":
    #    st.write("You chose Option 2!")
    #elif option == "Option 3":
     #   st.write("You chose Option 3!")

# You can also add more text or content below the button
st.write("This is some additional text below the button and options.")

#elif council == "Erstberatung" and disease == "NDD +/- Epilepsie":
#    st.markdown("### Anamnese")
#    st.markdown("Geburtshintergrund")
#   col1, col2, col3 = st.columns(3)
#    Geburtsart=col1.text_input("Geburtsart")
#    Geburtstermin=col2.text_input("Geburtstermin")
#    Geburtsmaßen=col3.text_input("Geburtsmaßen")
#    st.markdown("Frühe Entwicklung")
#    st.markdown("Meilensteine der motorischen Entwicklung")
#    col1, col2, col3 = st.columns(3)
#    Drehen=col1.text_input("Drehen")
#    Sitzen=col2.text_input("Sitzen")
#    Gehen=col3.text_input("Gehen")
#    st.markdown("Meilensteine der sprachlichen Entwicklung")
#    col1, col2 = st.columns(2)
#    Words=col1.text_input("Erste Laute/Worte")
#    Aktuell=col2.text_input("Aktueller Status")
#    st.markdown("Soziale Entwicklung")
#    col1, col2 = st.columns(2)
#    Kita=col1.text_input("Kita/Schulbbesuch")
#    Interaktion=col2.text_input("Interaktion mit Familie/Gleichaltrigen")
#    st.markdown("Aktuelle Symptome und Beobachtungen")
#    col1, col2= st.columns(2)
#    Entwicklung=col1.text_input("Art der Entwicklungsverzögerung")
#    Verhalten=col2.text_input("Verhaltensauffälligkeiten")
#    Kommunikation=col1.text_input("Kommunikationsfähigkeiten")
#    Epilepsie=col2.text_input("Epilepsie")
#    st.markdown("Bisherige Untersuchungen und Interventionen")
#    Vorbefunde=st.text_area("Frühere Arztbesuche oder Therapieansätze")
#    Diagnose=st.text_area("Diagnosen oder Empfehlungen")
