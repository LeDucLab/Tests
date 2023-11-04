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

# Letter Structure
#Beratungsgrund
beratung_line = f"**Beratungsgrund:** V.a. genetisch bedingte {questio}"

#Begrüßung
if Titel== "Herr":
    hello_line = f"Sehr geehrter {Titel} {Name},"
elif Titel != "Herr":
    hello_line = f"Sehr geehrte {Titel} {Name},"

#Date of Beratung
first_line= f"am {current_datetime.strftime('%d.%m.%Y')} stellten Sie Ihren Sohn/Ihre Tochter  in unserer genetischen Sprechstunde vor."
# Create a button
if st.button("Zur Vorlage"):
    # Display text based on the selected option
    if council == "Erstberatung" and Titel == "Herr" and person == "Kind" and disease == "unspezifisch" and analysis == "Exom" :
        st.write("**Beratungsgrund:** V.a. genetisch bedingte", question)
        st.markdown(beratung_line, unsafe_allow_html=True)
        st.write("Sehr geehrter", Titel, Name,",")
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
