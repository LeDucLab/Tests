import streamlit as st
from datetime import datetime


# Create a Streamlit app
st.title("Briefe Textbausteine")

# Get the current date and time
current_datetime = datetime.now()

#Get patient data
 # Create a selectbox to choose an option for the gender
Titel = st.selectbox("Titel", ["Frau", "Herr", "Familie"])

Vorname = st.text_input("Vorame")
Name = st.text_input("Name")



# Add a selectbox for choosing an option
option = st.selectbox("Wählen Sie die Art der Beratung", ["Erstberatung Exom", "Erstberatung NDD", "Erstberatung NDD+Epilepsie", "Erstberatung gezielt", "Erstberatung CA unauff"])

# Create a button
if st.button("Zur Vorlage"):
    # Display text based on the selected option
    if option == "Erstberatung Exom" and Titel == "Herr":
        st.write("**Beratungsgrund:** V.a. genetisch bedingte XX")
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
    elif option == "Erstberatung Exom" and Titel != "Herr":
        st.write("**Beratungsgrund:** V.a. genetisch bedingte XX")
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
    elif option == "Option 2":
        st.write("You chose Option 2!")
    elif option == "Option 3":
        st.write("You chose Option 3!")

# You can also add more text or content below the button
st.write("This is some additional text below the button and options.")
