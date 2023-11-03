import streamlit as st


# Create a Streamlit app
st.title("Briefe Textbausteine")

# Add a selectbox for choosing an option
option = st.selectbox("Wählen Sie die Art der Beratung", ["Erstberatung Exom", "Erstberatung NDD", "Erstberatung NDD+Epilepsie", "Erstberatung gezielt", "Erstberatung CA unauff"])

# Create a button
if st.button("Zu Vorlage"):
    # Display text based on the selected option
    if option == "Erstberatung Exom":
        st.write("Beratungsgrund: V.a. genetisch bedingte XX")
        st.write("Sehr geehrte Frau/Herr XX,")
        st.write("am", current_datetime, "stellten Sie Ihren Sohn/Ihre Tochter  in unserer genetischen Sprechstunde vor.")
      
     # Eigenanamnese:
      #Sie berichteten, dass  nach un/auffälliger Schwangerschaft in der Schwangerschaftswoche (per Sectio/als hypotrophes Neugeborenes/mit …) geboren wurde. Ihre/Seine Geburtsmaße betrugen … [Daten aus pedz].

      #Familienanamnese:
      #Hinsichtlich der aktuellen Fragestellung berichteten Sie, dass bei Unterlagen zu den genannten Familienmitgliedern liegen uns nicht vor. Ein drei Generationen umfassender Stammbaum befindet sich im Anhang.
      #Sie berichteten keine für die Fragestellung relevanten Krankheitsbilder in Ihrer Familie.

      #Körperliche Untersuchung:
     # Wir sahen im Alter von  Jahren. Ihre/Seine Körpermaße zur Vorstellung betrugen:[Daten aus pedz]. Fazial ergeben sich keine Auffälligkeiten/Fazial fielen … auf.

     # Beurteilung:
      #Bei Ihrem Sohn/Ihrer Tochter besteht der Verdacht auf ein . Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen bei ihm/ihr. Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen.")
    elif option == "Option 2":
        st.write("You chose Option 2!")
    elif option == "Option 3":
        st.write("You chose Option 3!")

# You can also add more text or content below the button
st.write("This is some additional text below the button and options.")
