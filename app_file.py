import streamlit as st
from datetime import datetime

tab1, tab2= st.tabs(["Beratung", "Krankheitsbild Textbausteine"])

with tab1:
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
    col1, col2, col3= st.columns(3)
    council = col1.selectbox("Art der Beratung", ["Erstberatung", "Befundbesprechung"])
    person = col2.selectbox("Patiententyp", ["Kind", "Erwachsen"])
    disease = col3.selectbox("Krankheitsbild", ["NDD +/- Epilepsie", "unspezifisch", "HNPCC", "FBrEK", "SCA", "HTT"])
    
    # Add anamnesis button
    if council == "Erstberatung" and disease == "unspezifisch":
        st.markdown("### Anamnese")
        default_text = """In Bezug af die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:"""
        free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)
    elif council == "Erstberatung" and disease == "NDD +/- Epilepsie":
        st.markdown("### Anamnese")
        default_text = """In Bezug af die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:
        - Geburtshintergrund: Geburtsart XX, Geburtstermin XX, Geburtsmaßen XX
        - Meilensteine der motorischen Entwicklung: Drehen XX, Sitzen XX, Gehen XX
        - Meilensteine der sprachlichen Entwicklung: esrte Laute/Worte XX, aktueller Status XX
        - Soziale Entwicklung: Kita/Schulbesuch XX, Interaktion mit der Familie/Gleichaltrigen XX
        - Aktuelle Symptome und Beobachtungen: Art der Entwicklungsverzögerung XX, Verhaltensauffälligkeiten XX, Kommunikationsfähigkeiten XX, Epilepsie XX
        - Bisherige Untersuchungen und Interventionen: Frühere Arztbesuche oder Therapieansätze XX, Diagnosen oder Empfehlungen XX"""
        free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)
    elif council == "Erstberatung" and disease == "HNPCC":
        st.markdown("### Anamnese")
        default_text = """In Bezug af die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:
        - Diagnose eines Darmkrebs im Alter von XX (Brief XX von XX)
        - Behandlung: operative Tumorentfernung, adjuvante Chemotherapie
        - Pathologische Untersuchung am Tumormaterial: unauffällige Befunde bezüglich einer Mikrosatelliteninstabilität und in der Immunhistochemie der Mismatch-Repair-Proteine (Arztbrief vom …, Klinik). / In der pathologischen Untersuchung am Tumormaterial wurde eine … Mikrosatelliteninstabilität sowie in der Immunhistochemie wurde ein Verlust der Kernexpression für XX nachgewiesen. Weiterhin wurde am Tumormaterial die somatische Variante p.Val600Gly im BRAF-Gen (nicht) nachgewiesen (Arztbrief vom …, Klinik)."""
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
        body_text= """Wir sahen XX im Alter von XX Jahren. Ihre/Seine Körpermaße zur Vorstellung betrugen: [pedz] (https://www.pedz.de/de/bmi.html). Fazial ergaben sich keine Auffälligkeiten/Fazial fielen XX auf."""
        body=st.text_area("Untersuchung", body_text)
    elif person == "Erwachsen":
        body_box= st.selectbox("Körperliche Untersuchung", ["Ja", "Nein"])
    
    #Add Anaylsis
    st.markdown("### Genetische Diagnostik")
    analysis = st.selectbox("Art der genetischen Testung", ["Exom", "Exom+CNV+CA", "gezielt", "Cancer Panel", "Repeat Expansion", "keine"])
    if analysis == "Exom":
        beurteilung="""Bei Ihrem Sohn/Ihrer Tochter/Ihnen besteht der Verdacht auf eine genetisch bedingte Entwicklungsstörung/Intelligenzminderung/Erkrankung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Exomdiagnostik mit Beurteilung der hierfür ursächlichen Genen. Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."""
    elif analysis == "Exom+CNV+CA" and disease=="NDD +/- Epilepsie":
        beurteilung="""Bei Ihrem Sohn/Ihrer Tochter/Ihnen besteht der Verdacht auf eine genetisch bedingte Entwicklungsverzögerung/Entwicklungsstörung/Intelligenzminderung mit Epilepsie. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine konventionelle Chromosomenanalyse, eine molekulargenetische Diagnostik im FMR1-Gen bezüglich des Fragilen-X-Syndroms, eine genomweite molekulargenetische Analyse von Dosisveränderungen (Copy Number Repeats, vergleichbar mit Arraydiagnostik) sowie eine molekulargenetische Multigen-Paneldiagnostik in den für eine genetisch bedingte Entwicklungsverzögerung/Entwicklungsstörung/Intelligenzminderung ursächlichen Genen bei ihm/ihr. 
    Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."""
    elif analysis == "gezielt":
        beurteilung="""Bei  Ihren Angehörigen/ Ihrer Mutter / Ihrem Vater / Ihrer Großmutter / Ihrem Großvater / väterlicherseits/ mütterlicherseits wurde im Vorfeld die o.g. pathogene Variante im XX-Gen nachgewiesen. Somit weist Ihr Sohn/Ihre Tochter // weisen Sie mit XX%iger Wahrscheinlichkeit die in Ihrer Familie bekannte pathogene Variante ebenfalls auf.  Mit Ihrem Einverständnis veranlassten wir die gezielte Diagnostik auf die o.g. pathogene XX-Variante bei Ihrem Sohn/Ihrer Tochter/Ihnen. Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."""
        
    
      
        
        
    
    # Letter Structure for all types of letters
    #Beratungsgrund
    if analysis != "gezielt":
        beratung_line = f"**Beratungsgrund:** V.a. genetisch bedingte {question}"
    elif analysis == "gezielt":
        beratung_line = f"**Beratungsgrund:** Eine (wahrscheinlich) pathogene Variante c.XX, p.XX im XX-Gen in der Familienanamnese"
    
    #Begrüßung
    if Titel== "Herr":
        hello_line = f"Sehr geehrter {Titel} {Name},"
    elif Titel != "Herr":
        hello_line = f"Sehr geehrte {Titel} {Name},"

    #Date of Beratung
    first_line= f"am {current_datetime.strftime('%d.%m.%Y')} stellten Sie sich/Ihren Sohn/Ihre Tochter in unserer genetischen Sprechstunde vor."

    #Info zum Krankheitsbild
    if disease=="HNPCC":
        disease_info_line="""Dickdarmkrebs (Kolonkarzinom) zählt zu den häufigsten bösartigen Tumoren in Westeuropa. Die meisten Fälle treten sporadisch auf und sind vermutlich multifaktoriell verursacht. In ca. 3-5 % der Fälle ist eine familiäre Häufung durch eine monogene, autosomal dominant erbliche Ursache zu erklären. Beim familiären Darmkrebs unterscheidet man mehrere Unterformen. Hierzu zählen die FAP (Familiäre Adenomatöse Poly-posis) mit hunderten bis tausenden Polypen im Darm, die MUTYH-assoziierte Polyposis mit zehn bis eini-gen hundert Polypen im Darm und das HNPCC-Syndrom (auch Lynch-Syndrom genannt) ohne Polyposis. Das Lynch-Syndrom ist ein Tumorprädispositionssyndrom, das mit einem erhöhten Risiko für kolorektale Karzinome, Karzinome des weiteren Verdauungstrakts, Endometriumkarzinome, Karzinome des Harntrakts, Ovarialkarzinome und Hirntumoren einhergeht.

Ursächlich für das Lynch-Syndrom sind pathogene Varianten in den Genen MLH1, MSH2, MSH6, PMS2 und EPCAM. Diese werden autosomal dominant vererbt. Das bedeutet, dass heterozygote Anlageträger die Erkrankung ausbilden. Damit besteht für die Nachkommen von Anlageträgern eine 50%ige Wahrscheinlichkeit, diese zu erben und die Erkrankung ebenfalls auszubilden. Es ist eine unvollständige Penetranz bekannt. Das bedeutet, nicht jeder Anlageträger bildet die Erkrankung aus.
Um Patienten mit einem HNPCC-Syndrom (hereditäres nicht-polypöses Kolonkarzinom) zu identifizieren, wurden klinische Kriterien definiert. Sind in einer Familie die Amsterdam-Kriterien für HNPCC (Auftreten von Kolonkarzinom, Nierenbecken- oder Ureterkarzinom und anderen assoziierten Tumorerkrankungen bei drei Familienangehörigen in zwei aufeinanderfolgenden Generationen, ein Familienmitglied erstgradig verwandt mit den beiden anderen, Erkrankungsalter bei einem Betroffenen vor dem 50. Lebensjahr) erfüllt, kann bereits klinisch die Diagnose eines HNPCC-Syndroms gestellt werden.
Die Bethesda-Kriterien für HNPCC (Kolonkarzinom vor dem 50. Lebensjahr, synchrones oder metachrones Auftreten von Kolonkarzinom oder anderen assoziierten Tumorerkrankungen, Kolonkarzinom mit spezieller MSI-H-Histologie, Patient mit Kolonkarzinom mit einem erstgradig Verwandten mit Kolonkarzinom oder assoziierter Tumorerkrankung vor dem 50. Lebensjahr, Patient mit Kolonkarzinom mit min. zwei erst- oder zweitgradig Verwandten mit Kolonkarzinom oder assoziierter Tumorerkrankung) stellen hingegen lediglich klinische Verdachtskriterien dar. 

Bei Verdacht auf ein HNPCC-Syndrom können zunächst molekularpathologische und immunhistochemische Untersuchungen am Tumormaterial erfolgen, bevor eine molekulargenetische Analyse der o.g. Gene anhand einer Blutprobe des Patienten durchgeführt wird (Kohlmann et Gruber. GeneReviews. 2018).

Seltenere Tumorprädispositionssyndrome sind das Peutz-Jeghers-Syndrom, das durch multiple Hamartome und melanotische Pigmentflecken gekennzeichnet ist und das PTEN-Hamartoma-Tumor-Syndrom, das mit einer Makrozephalie, Hamartomen der Schleimhaut und einem erhöhten Risiko für Schilddrüsen-, Nierenzell- und Mammakarzinome einhergeht."""
    
    
    #Final lines
    last_line=""""Wir hoffen, Sie mit unserem Gespräch und diesem Brief vorerst ausreichend informiert zu haben. Bei Rückfragen stehen wir gerne auch telefonisch zur Verfügung.\n
    Mit freundlichen Grüßen,\n
    PD Dr. D. Le Duc, MD/PhD"""
    

    
    # Create a button
    if st.button("Zur Vorlage"):
        # Display text based on the selected option
        if council == "Erstberatung" and person == "Kind":
            st.markdown(beratung_line, unsafe_allow_html=True)
            st.markdown(hello_line, unsafe_allow_html=True)
            st.write("**Eigenanamnese:**")
            st.markdown(free_anamnesis, unsafe_allow_html=True)
            st.write ("**Familienanamnese:**")
            st.markdown(family, unsafe_allow_html=True)
            st.write("**Körperliche Untersuchung:**")
            st.markdown(body, unsafe_allow_html=True)
            st.write("**Beurteilung:**")
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown(last_line, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("<font size='2'>FÄ für Humangenetik</font>", unsafe_allow_html=True)
        elif council == "Erstberatung" and person == "Erwachsen" and body_box == "Nein":
            st.markdown(beratung_line, unsafe_allow_html=True)
            st.markdown(hello_line, unsafe_allow_html=True)
            st.write("**Eigenanamnese:**")
            st.markdown(free_anamnesis, unsafe_allow_html=True)
            st.write ("**Familienanamnese:**")
            st.markdown(family, unsafe_allow_html=True)
            st.write("**Beurteilung:**")
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown(last_line, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("<font size='2'>FÄ für Humangenetik</font>", unsafe_allow_html=True)
    
       # elif council == "Erstberatung" and Titel == "Herr" and person == "Kind" and disease == "NDD +/- Epilepsie" and analysis == "Exom+CNV+CA" :
            
           
       
    # elif option == "Option 2":
        #    st.write("You chose Option 2!")
        #elif option == "Option 3":
         #   st.write("You chose Option 3!")
    
    # You can also add more text or content below the button
    st.write("This is some additional text below the button and options.")

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    
    
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
