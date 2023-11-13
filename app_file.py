import streamlit as st
from datetime import datetime
import pandas as pd
#from docx import Document

#Create a custom Paragraph spacing and lower the fonts
custom_css = """
<style>
.custom-paragraph {
    margin: 0; \* Remove default paragraph margin */
    margin-bottom: 0.5em; \* Add a custom margin-bottom to control spacing */
}
h1, h2, h3, h4, h5, h6 {
    font-size: 14px; \* Change the font size to your desired value */
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


tab1, tab2, tab3, tab4= st.tabs(["EBM_Erstberatung", "EBM_Befundbesprechung", "Schwangerschaft / Kinderwunsch", "Krankheitsbild Textbausteine"])

with tab1:
    ########################################
    # Create the first tab for Erstberatung#
    ########################################
    
    st.markdown("<h1 style='font-size: 30px;'>Erstberatungsbrief</h1>", unsafe_allow_html=True)

    # Get the current date and time#
    ################################
    current_datetime = datetime.now()

    ##################
    #Get patient data#
    ##################
    
    # Create a selectbox to choose an option for the gender#
    ########################################################
    st.markdown("### Patienten Daten")
    col1, col2, col3= st.columns(3)
    Titel = col1.selectbox("Titel", ["Frau", "Herr", "Familie"])        
    Vorname = col2.text_input("Vorame")
    Name = col3.text_input("Name")

    # Create a text area to input the question for counciling#
    ##########################################################
    #st.markdown("### Fragestellung") # if we wanted to create an extra title, however it brings too much input on the screen
    question = st.text_input("Fragestellung")
        
    # Add a selectbox for choosing the type of counciling#
    ######################################################
    #st.markdown("### Art der Beratung und Analyse")
    col1, col2, col3= st.columns(3)
    council = col1.selectbox("Art der Beratung", ["Erstberatung"])
    person = col2.selectbox("Patiententyp", ["Kind", "Erwachsen"])
    disease = col3.selectbox("Krankheitsbild", ["NDD +/- Epilepsie", "unspezifisch", "HNPCC", "SCA", "HTT", "Marfan/EDS", "Geschlechtsinkongruenz"])
    if person=="Kind": # we need this to adapt how we address it in the letter
        child= col2.selectbox("Kind", ["Tochter", "Sohn"])
        Name_child = col2.text_input("Vorname", key="Name_child")
    
    #######################
    # Add anamnesis button#
    #######################

    #Case 1: disease ist unspecific and we can add free comments#
    #############################################################
    if disease == "unspezifisch":
        st.markdown("### Anamnese")
        default_text = """In Bezug auf die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:<br>
        - Symptome XX seit XX<br>
        - Krankheitsgeschichte: neurologische Diagnostik –⁠ XX, cMRT Untersuchung –⁠ keine pathologische Befunde (Arztbrief vom XX, Klinik XX)<br>
        Sie berichteten, dass bei Ihnen keine für die Fragestellung relevanten Symptome/ Erkrankungen/ keine Tumorerkrankungen bekannt seien."""
        free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)

    #Case 2: disease is NDD#
    ########################
    elif disease == "NDD +/- Epilepsie":
        st.markdown("### Anamnese")
        default_text = """In Bezug auf die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:<br>
        - Geburtshintergrund: Geburtsart XX, Geburtstermin XX, Geburtsmaßen XX<br>
        - Meilensteine der motorischen Entwicklung: Drehen XX, Sitzen XX, Gehen XX<br>
        - Meilensteine der sprachlichen Entwicklung: esrte Laute/Worte XX, aktueller Status XX<br>
        - Soziale Entwicklung: Kita/Schulbesuch XX, Interaktion mit der Familie/Gleichaltrigen XX<br>
        - Aktuelle Symptome und Beobachtungen: Art der Entwicklungsverzögerung XX, Verhaltensauffälligkeiten XX, Kommunikationsfähigkeiten XX, Epilepsie XX<br>
        - Bisherige Untersuchungen und Interventionen: Frühere Arztbesuche oder Therapieansätze XX, Diagnosen oder Empfehlungen XX"""
        free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)

    #Case 3: disease is HNPCC#
    ##########################
    elif disease == "HNPCC":
        st.markdown("### Anamnese")
        default_text = """In Bezug auf die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:<br>
        - Diagnose eines Darmkrebs im Alter von XX (Brief XX vom XX)<br>
        - Behandlung: operative Tumorentfernung, adjuvante Chemotherapie<br>
        - Pathologische Untersuchung am Tumormaterial: unauffällige Befunde bezüglich einer Mikrosatelliteninstabilität und in der Immunhistochemie der Mismatch-Repair-Proteine (Brief vom XX, Klinik XX).<br>
        In der pathologischen Untersuchung am Tumormaterial wurde eine Mikrosatelliteninstabilität sowie in der Immunhistochemie wurde ein Verlust der Kernexpression für XX nachgewiesen. Weiterhin wurde am Tumormaterial die somatische Variante p.Val600Gly im BRAF-Gen (XX nicht) nachgewiesen (Brief vom XX, Klinik).<br>"""
        free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)

    #Case 4: disease is SCA#
    ########################
    elif disease == "SCA":
        st.markdown("### Anamnese")
        default_text = """In Bezug auf die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:<br>
        - Typische Symptome einer spinozerebellären Ataxie: Gangstörung im Alter von XX, Dysarthrie im Alter von XX, Orientierungsstörungen –⁠ XX, Augenbewegungsstörungen –⁠ XX<br>
        - Krankheitsgeschichte: neurologische Diagnostik –⁠ XX, cMRT Untersuchung –⁠ keine pathologische Befunde (Arztbrief vom XX, Klinik XX)"""
        free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)

    #Case 5: disease is HTT#
    ########################
    elif disease == "HTT":
        st.markdown("### Anamnese")
        default_text = """Sie berichteten, dass bei Ihnen keine für die Huntington-Erkrankung typischen psychiatrischen oder motorischen Störungen bekannt seien.<br>
        In Bezug auf die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:<br>
        - Typische Symptome einer Huntington Erkrankung: Motorische Symptome wie unkontrollierte Bewegungen (Chorea), Muskelsteifigkeit, Verlust der Koordination im Alter von XX, kognitive Einschränkung und Gedächtnisstörungen im Alter von XX, psychiatrische Manifestationen wie Depression, Ängstlichkeit, Stimmungsschwankungen, Persönlichkeitsveränderungen im Alter von XX <br>
        - Krankheitsgeschichte: neurologische Diagnostik –⁠ XX, cMRT Untersuchung –⁠ keine pathologische Befunde (Arztbrief vom XX, Klinik XX)"""
        free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)

    #Case 5: disease is Geschlechtsinkongruenz#
    ###########################################
    elif disease == "Geschlechtsinkongruenz":
        st.markdown("### Anamnese")
        default_text = """In Bezug auf die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:<br>
        - Geschlechtsidentität und Entwicklung: keine Auffälligkeiten in der Pubertät, erste Zeichen einer Geschlechtsinkongruenz in XX<br>
        - Soziale und familiäre Akzeptanz: familiäre Unterstuzung, Akzeptanz durch Freundekreis<br>
        - Vorerkrankungen: keine<br>
        - Psychische Gesundheit: Depression, Stimmungsschwankungen<br>
        - Transition, weitere Aspekte: Hormontherapie seit XX, eine Geschlechtsumwandlungoperation ist geplannt XX"""
        free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)

    #Case 6: disease is Marfan/EDS#
    ###############################
    elif disease == "Marfan/EDS":
        st.markdown("### Anamnese")
        default_text = """In Bezug auf die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:<br>
        - Systemische Ghent-Kriterien anamnestisch:<br>
            - spontaner Pneumothorax (2P) ⁠–⁠ nein/ja<br>
            - Duralektasie (2P) ⁠–⁠ nein/ja<br>
            - Protrusio acetabulae (Hüftauffälligkeiten) (2P) –⁠ nein/ja<br>
            - Dehnungsstreifen (1P) –⁠ nein/ja⁠⁠<br>
            <br>
        - Symptome eines Ehler-Danlos-Syndroms:<br>
            - Organ- oder Gefäßrupturen ⁠–⁠ nein/ja<br>
            - Hernien ⁠–⁠ nein/ja<br>
            - Pneumothorax ⁠–⁠ nein/ja<br>
            - Gelenks(sub)luxationen ⁠–⁠ nein/ja<br>
            - Hämatomneigung/Dehnungsstreifen ⁠–⁠ nein/ja<br>
            - atrophe Narbenbildung ⁠–⁠ nein/ja<br>
            - Akrogerie ⁠–⁠ nein/ja<br>
        - Kariologische Untersuchung ⁠–⁠ unauffällig XX (Brief vom XX, Klinik XX)<br>
        - Augenärztliche Untersuchungund ⁠–⁠ unauffällig XX (Brief vom XX, Klinik XX)"""
        free_anamnesis= st.text_area("Relevante Symptome und Vorgeschichte für die aktuelle Fragestellung", default_text)
         
        
    #Add Familienanamnese button#
    #############################
    st.markdown("### Familienanamnese")
    familienanamnese = st.selectbox("", ["auffällig", "unauffällig"])
    if familienanamnese == "unauffällig":
        family="""Sie berichteten keine für die Fragestellung relevanten Krankheitsbilder in Ihrer Familie."""
    elif familienanamnese == "auffällig":
        fam_text="""Hinsichtlich der aktuellen Fragestellung berichteten Sie, dass bei XX eine XX vorliegt. Unterlagen zu den genannten Familienmitgliedern liegen uns nicht vor. Ein drei Generationen umfassender Stammbaum befindet sich im Anhang."""
        family=st.text_area("Relevante Erkrankungen in der Familie", fam_text)
    
    #Add Körperliche Untersuchung#
    ##############################
    st.markdown("### Körperliche Untersuchung")
    if person == "Kind":
        body_text="""Wir sahen XX im Alter von XX Jahren. Ihre/Seine Körpermaße zur Vorstellung betrugen: [pedz] (https://www.pedz.de/de/bmi.html). Fazial ergaben sich keine Auffälligkeiten/Fazial fielen XX auf."""
        body=st.text_area("", body_text)
    elif person == "Erwachsen":
        body_box= st.selectbox("Körperliche Untersuchung", ["Ja", "Nein"])
        if body_box=="Ja" and disease=="Marfan/EDS": # specific check upfor Marfan/EDS
            body_text="""Die systemischen Kriterien der // https://marfan.org/dx/score/ // revidierten Ghent-Kriterien ergaben XX von 20 Punkten (positiv für XX) (≥ 7 Punkte zeigt systemische Beteiligung an; Loeys et al., 2010, PMID: 20591885). Der Z-Score der Aortenwurzeldurchmesser (XX mm) beträgt XX (Normwert ≤ 2). Die Verhältnisse zwischen Ober- und Unterlänge sowie Armspanne zu Körpergröße ergaben un/auffällige Werte (OL/UL XX; AS/KG XX).<br>
            Der Beighton Hypermobilitäts-Score ergab XX von 9 Punkten // https://www.ndr.de/ratgeber/gesundheit/Hypermobilitaet-Wenn-Gelenke-nicht-stabil-sind,hypermobilitaet106.html // (3–4 Punkte zeigte eine moderate Hypermobilität, ≥ 5 Punkte generalisierte Hypermobilität)."""
            body=st.text_area("", body_text)
        elif body_box=="Ja" and disease!="Marfan/EDS":
            body_text=""""""
            body=st.text_area("", body_text)
    
    #Add Anaylsis#
    ##############
    st.markdown("### Genetische Diagnostik") #genetic diagnosis is based on type of disease
    if disease == "NDD +/- Epilepsie":
        analysis = st.selectbox("Art der genetischen Testung", ["Exom", "Exom+CNV+CA", "gezielt", "keine"])
    elif disease == "unspezifisch":
        analysis = st.selectbox("Art der genetischen Testung", ["Exom", "Exom+CNV+CA", "gezielt", "Cancer Panel", "Repeat Expansion", "CA", "keine"])
    elif disease == "HNPCC":
        analysis = st.selectbox("Art der genetischen Testung", ["Cancer Panel", "gezielt", "keine"])
    elif disease == "SCA":
        analysis = st.selectbox("Art der genetischen Testung", ["Repeat Expansion +/- Exom", "gezielt", "keine"])
    elif disease == "HTT":
        analysis = st.selectbox("Art der genetischen Testung", ["Repeat Expansion", "gezielt", "keine"])
    elif disease == "Marfan/EDS":
        analysis = st.selectbox("Art der genetischen Testung", ["Exom", "gezielt", "keine"])
    elif disease == "Geschlechtsinkongruenz":
        analysis = st.selectbox("Art der genetischen Testung", ["CA"])

    #Case 1: analysis is Exom in NDD or unspecific disease#
    #######################################################
    if analysis == "Exom" and disease != "Marfan/EDS":
        if person=="Kind":
            beurteilung=f"Bei {Name_child} besteht der Verdacht auf eine genetisch bedingte Entwicklungsstörung/Intelligenzminderung/Erkrankung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Exomdiagnostik mit Beurteilung der hierfür ursächlichen Genen.<br> Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."
        elif person=="Erwachsen":
            beurteilung="""Bei Ihnen besteht der Verdacht auf eine genetisch bedingte Erkrankung / Intelligenzminderung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Exomdiagnostik mit Beurteilung der hierfür ursächlichen Genen.<br> Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."""

    #Case 2: analysis is Exom in Marfan/EDS#
    ########################################
    elif  analysis == "Exom" and disease == "Marfan/EDS":
        if person=="Kind":
            beurteilung=f"Bei {Name_child} besteht der Verdacht auf eine eine genetisch bedingte Bindegewebeserkrankung. Die klinischen Kriterien für ein Marfan- bzw. ein Ehlers-Danlos-Syndrom sind bei {Name_child} nicht erfüllt/erfüllt XX. Zur Abklärung von weiteren/einer XX genetisch bedingten Bindegewebeserkrankungen/Bindegewebeserkrankung ist aus der Sicht unseres Fachgebietes eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen.<br> Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."
        elif person=="Erwachsen":
            beurteilung="""Bei Ihnen besteht der Verdacht auf eine eine genetisch bedingte Bindegewebeserkrankung. Die klinischen Kriterien für ein Marfan- bzw. ein Ehlers-Danlos-Syndrom sind bei Ihnen nicht erfüllt/erfüllt XX. Zur Abklärung von weiteren/einer XX genetisch bedingten Bindegewebeserkrankungen/Bindegewebeserkrankung ist aus der Sicht unseres Fachgebietes eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen.<br> Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."""
        
    #Case 3: analysis is Exom+CNV+CA in NDD#
    ########################################
    elif analysis == "Exom+CNV+CA" and disease=="NDD +/- Epilepsie":
        if person=="Kind":
            beurteilung=f"Bei {Name_child} besteht der Verdacht auf eine genetisch bedingte Entwicklungsverzögerung/Entwicklungsstörung/Intelligenzminderung XX mit Epilepsie. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine konventionelle Chromosomenanalyse, eine molekulargenetische Diagnostik im <i>FMR1</i>-Gen bezüglich des Fragilen-X-Syndroms, eine genomweite molekulargenetische Analyse von Dosisveränderungen (Copy Number Repeats, vergleichbar mit Arraydiagnostik) sowie eine molekulargenetische Exomdiagnostik in den für eine genetisch bedingte Entwicklungsverzögerung/Entwicklungsstörung/Intelligenzminderung XX mit Epilepsie ursächlichen Genen bei {Name_child}.<br> Weiterhin besteht bei einem unauffälligen Ergebnis der Routinediagnostik die Möglichkeit der Teilnahme an einem Forschungsprojekt des Instituts für Humangenetik am Uniklinikum Leipzig. In diesem Rahmen könnte eine Trio-Genom-Diagnostik auf Forschungsbasis durchgeführt werden. Hierbei wird das Erbmaterial des betroffenen Patienten im Vergleich zu seinen Eltern untersucht. Es können vor allem beim Indexpatienten neu entstandene genetische Veränderungen, jedoch auch andere Ursachen wie z.B. autosomal rezessiv erbliche genetische Erkrankungen detektiert werden. Die Klärungsrate mittels Trio-Analyse bei Patienten mit einer Intelligenzminderung, Epilepsie bzw. dem V.a. eine übergeordnete genetische Erkrankung kann bis zu 50 % und mehr betragen (Vissers <i>et al</i>., Nat Rev Genet 2016, PMID: 26503795). Wir halten eine entsprechende Diagnostik ebenfalls für indiziert.<br> Wir nahmen Ihnen beiden, Frau und Herr {Name}, bereits eine Blutprobe ab, um gegebenenfalls eine Segregationsanalyse oder eine Trio-Analyse durchführen zu können. Sie gaben uns dazu bereits Ihr schriftliches Einverständnis. Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."
        elif person=="Erwachsen":
            beurteilung=f"Bei Ihnen besteht der Verdacht auf eine genetisch bedingte Intelligenzminderung XX mit Epilepsie. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine konventionelle Chromosomenanalyse, eine molekulargenetische Diagnostik im <i>FMR1</i>-Gen bezüglich des Fragilen-X-Syndroms, eine genomweite molekulargenetische Analyse von Dosisveränderungen (Copy Number Repeats, vergleichbar mit Arraydiagnostik) sowie eine molekulargenetische Exomdiagnostik in den für eine genetisch bedingte Intelligenzminderung XX mit Epilepsie ursächlichen Genen bei Ihnen. <br> Weiterhin besteht bei einem unauffälligen Ergebnis der Routinediagnostik die Möglichkeit der Teilnahme an einem Forschungsprojekt des Instituts für Humangenetik am Uniklinikum Leipzig. In diesem Rahmen könnte eine Trio-Genom-Diagnostik auf Forschungsbasis durchgeführt werden. Hierbei wird das Erbmaterial des betroffenen Patienten im Vergleich zu seinen Eltern untersucht. Es können vor allem beim Indexpatienten neu entstandene genetische Veränderungen, jedoch auch andere Ursachen wie z.B. autosomal rezessiv erbliche genetische Erkrankungen detektiert werden. Die Klärungsrate mittels Trio-Analyse bei Patienten mit einer Intelligenzminderung, Epilepsie bzw. dem V.a. eine übergeordnete genetische Erkrankung kann bis zu 50 % und mehr betragen (Vissers <i>et al</i>., Nat Rev Genet 2016, PMID: 26503795). Wir halten eine entsprechende Diagnostik ebenfalls für indiziert.<br> Wir nahmen bei Ihren Eltern bereits eine Blutprobe ab, um gegebenenfalls eine Segregationsanalyse oder eine Trio-Analyse durchführen zu können. Sie gaben uns dazu bereits Ihr schriftliches Einverständnis.<br> Sollten Ihre Eltern zur Verfügung stehen bitten wir um Rücksprache, bzw. die Zusendung von EDTA-Blut (min 2 ml Rörchen, beschriftet mit Name, Vorname, Geburtdatum) und ein schriftliches Einverständnis per Post. Das Blut der Eltern wird asserviert, um in Abhängigkeit von den Ergebnissen gegebenenfalls eine Segregationsanalyse oder eine Trio-Analyse durchführen zu können.<br> Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."

    #Case 4: analysis is Exom+CNV+CA in unspecific disease#
    #######################################################
    elif analysis == "Exom+CNV+CA" and disease=="unspezifisch":
        if person=="Kind":
            beurteilung=f"Bei {Name_child} besteht der Verdacht auf eine genetisch bedingte Erkrankung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine konventionelle Chromosomenanalyse, eine genomweite molekulargenetische Analyse von Dosisveränderungen (Copy Number Repeats, vergleichbar mit Arraydiagnostik) sowie eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen bei {Name_child}. <br> Wir nahmen Ihnen beiden, Frau und Herr {Name}, bereits eine Blutprobe ab, um gegebenenfalls eine Segregationsanalyse durchführen zu können. Sie gaben uns dazu bereits Ihr schriftliches Einverständnis. Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."
        elif person=="Erwachsen":
            beurteilung=f"Bei Ihnen besteht der Verdacht auf eine genetisch bedingte Erkrankung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine konventionelle Chromosomenanalyse, eine genomweite molekulargenetische Analyse von Dosisveränderungen (Copy Number Repeats, vergleichbar mit Arraydiagnostik) sowie eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen bei Ihnen. <br> Wir nahmen bei Ihren Eltern bereits eine Blutprobe ab, um gegebenenfalls eine Segregationsanalyse durchführen zu können. Sie gaben uns dazu bereits Ihr schriftliches Einverständnis.<br> Sollten Ihre Eltern zur Verfügung stehen bitten wir um Rücksprache, bzw. die Zusendung von EDTA-Blut (min 2 ml Rörchen, beschriftet mit Name, Vorname, Geburtdatum) und ein schriftliches Einverständnis per Post. Das Blut der Eltern wird asserviert, um in Abhängigkeit von den Ergebnissen gegebenenfalls eine Segregationsanalyse durchführen zu können.<br> Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."

    #Case 5: analysis is gezielt in all cases except HTT#
    #####################################################
    elif analysis == "gezielt" and disease !="HTT":
        beurteilung="""Bei  Ihren Angehörigen/ Ihrer Mutter / Ihrem Vater / Ihrer Großmutter / Ihrem Großvater / väterlicherseits/ mütterlicherseits wurde im Vorfeld die o.g. pathogene Variante im XX-Gen nachgewiesen.<br> Somit weist Ihr Sohn/Ihre Tochter // weisen Sie mit XX%iger Wahrscheinlichkeit die in Ihrer Familie bekannte pathogene Variante ebenfalls auf.  Mit Ihrem Einverständnis veranlassten wir die gezielte Diagnostik auf die o.g. pathogene XX-Variante bei Ihrem Sohn/Ihrer Tochter/Ihnen.<br> // Zur Abklärung einer möglichen Anlageträgerschaft bezüglich XX veranlassten wir bei Ihnen eine molekulargenetische Einzelgen-Diagnostik und MLPA-Untersuchung bezüglich Veränderungen im XX-Gen. // Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."""

    #Case 6: analysis is gezielt in HTT#
    ####################################
    elif analysis == "gezielt" and disease == "HTT":
        beurteilung="""Bei XX wurde mit dem Nachweis einer pathogenen CAG-Repeat-Verlängerung im <i>HTT</i>-Gen eine Huntington-Erkrankung molekulargenetisch nachgewiesen. Damit besteht für Sie eine 50%ige Wahrscheinlichkeit, diese geerbt zu haben und ebenfalls eine Huntington-Erkrankung auszubilden.<br> Im Rahmen der Beratung besprachen wir psychologische, soziale und versicherungsrechtliche Aspekte, die sich aus dem Ergebnis der genetischen Diagnostik ergeben könnten. Zudem empfahlen wir eine psychologische Beratung im Hinblick auf eine mögliche prädiktive Diagnostik im HTT-Gen. Sollten Sie sich nach angemessener Bedenkzeit für die molekulargenetische Untersuchung im HTT-Gen entscheiden, ist eine erneute Terminvereinbarung in unserer genetischen Sprechstunde zur Entnahme einer Blutprobe und Einleitung der genetischen Diagnostik möglich."""

    #Case 7: analysis is Cancer Panel in HNPCC#
    ###########################################
    elif analysis == "Cancer Panel" and disease == "HNPCC":
        beurteilung="""Bei Ihnen besteht der Verdacht auf eine genetisch bedingte Darmkrebserkrankung. Die Bethesda-Kriterien und Amsterdam-Kriterien sind erfüllt. Die molekularpathologischen Untersuchungen am Tumormaterial von Ihnen ergaben einen auffälligen Befund. Zur Abklärung veranlassten wir daher bei Ihnen eine molekulargenetische Paneldiagnostik in den für genetisch bedingten Darmkrebs ursächlichen Genen. <br> /Zur weiteren Abklärung forderten wir die molekularpathologische Untersuchung bezüglich einer Mikrosatelliteninstabilität, eine immunhistochemische Diagnostik sowie die molekularpathologische Diagnostik bezüglich der somatischen Mutation p.(Val600Glu) im BRAF-Gen an.<br> <br> Sobald die Befunde der eingeleiteten Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."""
    
    #Case 8: analysis is Cancer Panel in unspecific disease#
    ########################################################
    if analysis == "Cancer Panel" and disease == "unspezifisch":
        if person=="Kind":
            beurteilung=f"Bei {Name_child} besteht der Verdacht auf eine genetisch bedingte Krebserkrankung/Erkrankung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Paneldiagnostik mit Beurteilung der hierfür ursächlichen Genen.<br> Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."
        elif person=="Erwachsen":
            beurteilung="""Bei Ihnen besteht der Verdacht auf eine genetisch bedingte Krebserkrankung/Erkrankung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Paneldiagnostik mit Beurteilung der hierfür ursächlichen Genen.<br> Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."""

    #Case 9: analysis is Repeat Expansion +/- Exom in SCA#
    ######################################################
    elif analysis == "Repeat Expansion +/- Exom" and disease == "SCA":
        beurteilung="""Bei Ihnen besteht der Verdacht auf eine genetisch bedingte Ataxie. Wir veranlassten daher bei Ihnen die molekulargenetische Diagnostik bezüglich des Fragilen-X-assoziierten Tremor-Ataxie-Syndroms (FXTAS) im <i>FMR1</i>-Gen. Weiterhin werden wir die molekulargenetische Diagnostik bezüglich der Spinozerebellären Ataxie Typ 1, 2, 3, 6, 7, 8, 10, 12 und 17 sowie eine molekulargenetische Paneldiagnostik in weiteren hierfür ursächlichen Genen durchführen. Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."""

    #Case 10: analysis is Repeat Expansion in HTT#
    #############################################
    elif analysis == "Repeat Expansion" and disease == "HTT":
        beurteilung="""Bei Ihnen besteht der Verdacht auf eine Huntington Erkrankung. Wir veranlassten daher bei Ihnen eine molekulargenetische Diagnostik im Hinblick auf eine Huntington Erkrankung. Sollte diese Diagnostik unauffällig sein werden wir eine weiterführende genetische Diagnostik im Hinblick Huntington-like Erkrankungen einleiten. Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."""

    #Case 11: analysis is Repeat Expansion in unspecific disease#
    ############################################################
    elif analysis == "Repeat Expansion" and disease == "unspezifisch":
        beurteilung="""Bei Ihnen besteht der Verdacht auf eine genetisch bedingte so gennante Repeat Erkrankung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine molekulargenetische Diagnostik mit Beurteilung von Repeat-Verlängerungen im XX-Gen/ in den hierfür ursächlichen Genen.<br> Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."""

    #Case 12: analysis is CA in Geschlechtsinkongruenz#
    ################################################### 
    elif analysis == "CA" and disease == "Geschlechtsinkongruenz":
        beurteilung="""Zur Abklärung des genetischen Geschlechts veranlassten wir eine konventionelle Chromosomenanalyse. Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."""

    #Case 13: analysis is CA in unspecific disease#
    ###############################################
    elif analysis == "CA" and disease == "unspezifisch":
        if person=="Kind":
            beurteilung=f"Bei {Name_child} besteht der Verdacht auf eine Chromosomalestörung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine konventionelle Chromosomenanalyse bei {Name_child}.<br> Wir nahmen Ihnen beiden, Frau und Herr {Name}, bereits eine Blutprobe ab, um gegebenenfalls auch eine Chromosomen Untersuchung durchführen zu können. Sie gaben uns dazu bereits Ihr schriftliches Einverständnis. Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."
        elif person=="Erwachsen":
            beurteilung=f"Bei Ihnen besteht der Verdacht auf eine Chromosomalestörung. Aus der Sicht unseres Fachgebietes ist eine genetische Diagnostik indiziert. Wir veranlassten daher eine konventionelle Chromosomenanalyse.<br> Sobald die Befunde der genetischen Diagnostik vorliegen, werden wir Sie informieren und weiterführend Stellung nehmen."

    #Case 14: analysis is keine and disease is HNPCC#
    #################################################
    elif analysis == "keine" and disease == "HNPCC":
        beurteilung="""Wir besprachen, dass aufgrund Ihrer Angaben zur Eigen- und Familienanamnese die klinischen Kriterien (Bethesda- und Amsterdam-Kriterien) für ein HNPCC-Syndrom nicht erfüllt sind. Zudem erwiesen sich die im Vorfeld durchgeführten molekularpathologischen und immunhistochemischen Untersuchungen am Tumormaterial bei Ihnen als unauffällig. Hinweise auf ein polypöses Tumorprädispositionssyndrom ergaben sich bei Ihnen nicht.<br> Wir empfehlen Ihnen daher im Anschluss an die Tumornachsorge die Teilnahme an der Regelvorsorge für Darmkrebs/ eine Koloskopie alle 3–⁠5 Jahre. Das Risiko eines Verwandten ersten Grades eines Patienten mit kolorektalem Karzinom, ebenfalls an einem kolorektalen Karzinom zu erkranken, ist auch ohne das Vorliegen eines erblichen Tumorsyndroms statistisch erhöht. Ihre Verwandten ersten Grades sollten daher mit spätestens XX Jahren erstmals komplett koloskopiert werden (10 Jahre vor dem Alterszeitpunkt des Auftretens des Karzinoms beim Indexpatienten gemäß S3-Leitlinie Kolorektales Karzinom).<br> Sollten im weiteren Verlauf Sie bzw. andere Familienmitglieder an weiteren Krebserkrankungen erkranken, ist eine Wiedervorstellung in unserer Sprechstunde zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik möglich."""

    #Case 14: analysis is keine and disease is not HNPCC#
    #####################################################
    elif analysis == "keine" and disease != "HNPCC":
        if person=="Kind":
            beurteilung=f"Wir besprachen, dass aufgrund Ihrer Angaben zur Eigen- und Familienanamnese bei {Name_child} kein Verdacht auf eine genetisch bedingte Erkrankung besteht. Aus der Sicht unseres Fachgebietes ist keine genetische Diagnostik indiziert. Sollten im weiteren Verlauf {Name_child} bzw. andere Familienmitglieder weitere Symptome aufweisen/ an weiteren Krebserkrankungen erkranken, ist eine Wiedervorstellung in unserer Sprechstunde zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik möglich."
        elif person=="Erwachsen":
            beurteilung=f"Wir besprachen, dass aufgrund Ihrer Angaben zur Eigen- und Familienanamnese bei Ihnen kein Verdacht auf eine genetisch bedingte Erkrankung besteht. Aus der Sicht unseres Fachgebietes ist keine genetische Diagnostik indiziert. Sollten im weiteren Verlauf Sie bzw. andere Familienmitglieder weitere Symptome aufweisen/ an weiteren Krebserkrankungen erkranken, ist eine Wiedervorstellung in unserer Sprechstunde zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik möglich."

    #Add Signature boxes#
    #####################
    st.markdown("### Behandelnde Ärzte")
    col1, col2 = st.columns(2)
    Arzt1 = col1.selectbox("Arzt 1", ["Diana Le Duc", "Albrecht Kobelt"])
    Arzt2 = col2.selectbox("Arzt 2", ["Diana Le Duc", "Albrecht Kobelt"])
     
    
    #Letter Structure for all types of letters#
    ###########################################
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
    if person == "Kind":
        if child=="Sohn":
            first_line= f"am {current_datetime.strftime('%d.%m.%Y')} stellten Ihren Sohn, {Name_child}, in unserer genetischen Sprechstunde vor."
        elif child=="Tochter":
            first_line= f"am {current_datetime.strftime('%d.%m.%Y')} stellten Ihre Tochter, {Name_child}, in unserer genetischen Sprechstunde vor."
    elif person == "Erwachsen":
        first_line= f"am {current_datetime.strftime('%d.%m.%Y')} stellten Sie sich in unserer genetischen Sprechstunde vor."

    #Info zum Krankheitsbild
    if disease=="HNPCC":
        disease_info_line="""Dickdarmkrebs (Kolonkarzinom) zählt zu den häufigsten bösartigen Tumoren in Westeuropa. Die meisten Fälle treten sporadisch auf und sind vermutlich multifaktoriell verursacht. In ca. 3–⁠5 % der Fälle ist eine familiäre Häufung durch eine monogene, autosomal dominant erbliche Ursache zu erklären. Beim familiären Darmkrebs unterscheidet man mehrere Unterformen. Hierzu zählen die FAP (Familiäre Adenomatöse Poly-posis) mit hunderten bis tausenden Polypen im Darm, die MUTYH-assoziierte Polyposis mit zehn bis eini-gen hundert Polypen im Darm und das HNPCC-Syndrom (auch Lynch-Syndrom genannt) ohne Polyposis. Das Lynch-Syndrom ist ein Tumorprädispositionssyndrom, das mit einem erhöhten Risiko für kolorektale Karzinome, Karzinome des weiteren Verdauungstrakts, Endometriumkarzinome, Karzinome des Harntrakts, Ovarialkarzinome und Hirntumoren einhergeht.<br> Ursächlich für das Lynch-Syndrom sind pathogene Varianten in den Genen <i>MLH1</i>, <i>MSH2</i>, <i>MSH6</i>, <i>PMS2</i> und <i>EPCAM</i>. Diese werden autosomal dominant vererbt. Das bedeutet, dass heterozygote Anlageträger die Erkrankung ausbilden. Damit besteht für die Nachkommen von Anlageträgern eine 50%ige Wahrscheinlichkeit, diese zu erben und die Erkrankung ebenfalls auszubilden. Es ist eine unvollständige Penetranz bekannt. Das bedeutet, nicht jeder Anlageträger bildet die Erkrankung aus.<br> Um Patienten mit einem HNPCC-Syndrom (hereditäres nicht-polypöses Kolonkarzinom) zu identifizieren, wurden klinische Kriterien definiert. Sind in einer Familie die Amsterdam-Kriterien für HNPCC (Auftreten von Kolonkarzinom, Nierenbecken- oder Ureterkarzinom und anderen assoziierten Tumorerkrankungen bei drei Familienangehörigen in zwei aufeinanderfolgenden Generationen, ein Familienmitglied erstgradig verwandt mit den beiden anderen, Erkrankungsalter bei einem Betroffenen vor dem 50. Lebensjahr) erfüllt, kann bereits klinisch die Diagnose eines HNPCC-Syndroms gestellt werden.<br>Die Bethesda-Kriterien für HNPCC (Kolonkarzinom vor dem 50. Lebensjahr, synchrones oder metachrones Auftreten von Kolonkarzinom oder anderen assoziierten Tumorerkrankungen, Kolonkarzinom mit spezieller MSI-H-Histologie, Patient mit Kolonkarzinom mit einem erstgradig Verwandten mit Kolonkarzinom oder assoziierter Tumorerkrankung vor dem 50. Lebensjahr, Patient mit Kolonkarzinom mit min. zwei erst- oder zweitgradig Verwandten mit Kolonkarzinom oder assoziierter Tumorerkrankung) stellen hingegen lediglich klinische Verdachtskriterien dar.<br><br> Bei Verdacht auf ein HNPCC-Syndrom können zunächst molekularpathologische und immunhistochemische Untersuchungen am Tumormaterial erfolgen, bevor eine molekulargenetische Analyse der o.g. Gene anhand einer Blutprobe des Patienten durchgeführt wird (Kohlmann et Gruber. GeneReviews. 2018).<br><br> Seltenere Tumorprädispositionssyndrome sind das Peutz-Jeghers-Syndrom, das durch multiple Hamartome und melanotische Pigmentflecken gekennzeichnet ist und das PTEN-Hamartoma-Tumor-Syndrom, das mit einer Makrozephalie, Hamartomen der Schleimhaut und einem erhöhten Risiko für Schilddrüsen-, Nierenzell- und Mammakarzinome einhergeht."""
        
    #Final lines
    last_line="""Wir hoffen, Sie mit unserem Gespräch und diesem Brief vorerst ausreichend informiert zu haben. Bei Rückfragen stehen wir gerne auch telefonisch zur Verfügung.<br><br>Mit freundlichen Grüßen,<br><br>"""

    #Signatures
    if Arzt1 =="Diana Le Duc":
        signature="""PD Dr. D Le Duc, MD/PhD<br><small>FÄ für Humangenetik</small>"""# to work on

    #Anhang
    if familienanamnese == "auffällig":
        anhang="""<small>Anhang: Stammbaum</small>"""
    elif familienanamnese == "unauffällig":
        anhang=""""""
    

    
    # Create a button
    if st.button("Arzt Brief Erstberatung"):
        # Display text based on the selected option
        if person == "Kind":
            st.markdown(beratung_line, unsafe_allow_html=True)
            st.markdown(hello_line, unsafe_allow_html=True)
            st.markdown(first_line, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Eigenanamnese:</b></div>",  unsafe_allow_html=True)
            st.markdown(free_anamnesis, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Familienanamnese:</b></div>",  unsafe_allow_html=True)
            st.markdown(family, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Körperliche Untersuchung:</b></div>",  unsafe_allow_html=True)
            st.markdown(body, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Beurteilung und Procedere:</b></div>",  unsafe_allow_html=True)
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown(last_line, unsafe_allow_html=True)
            st.markdown(signature, unsafe_allow_html=True)
            st.markdown(anhang, unsafe_allow_html=True)
        elif person == "Erwachsen" and body_box=="Nein":
            st.markdown(beratung_line, unsafe_allow_html=True)
            st.markdown(hello_line, unsafe_allow_html=True)
            st.markdown(first_line, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Eigenanamnese:</b></div>",  unsafe_allow_html=True)
            st.markdown(free_anamnesis, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Familienanamnese:</b></div>",  unsafe_allow_html=True)
            st.markdown(family, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Beurteilung und Procedere:</b></div>",  unsafe_allow_html=True)
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown(last_line, unsafe_allow_html=True)
            st.markdown(signature, unsafe_allow_html=True)
            st.markdown(anhang, unsafe_allow_html=True)
        elif person == "Erwachsen" and body_box=="Ja":
            st.markdown(beratung_line, unsafe_allow_html=True)
            st.markdown(hello_line, unsafe_allow_html=True)
            st.markdown(first_line, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Eigenanamnese:</b></div>",  unsafe_allow_html=True)
            st.markdown(free_anamnesis, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Familienanamnese:</b></div>",  unsafe_allow_html=True)
            st.markdown(family, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Körperliche Untersuchung:</b></div>",  unsafe_allow_html=True)
            st.markdown(body, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Beurteilung und Procedere:</b></div>",  unsafe_allow_html=True)
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown(last_line, unsafe_allow_html=True)
            st.markdown(signature, unsafe_allow_html=True)
            st.markdown(anhang, unsafe_allow_html=True)
        elif person == "Erwachsen" and disease == "HNPCC":
            st.markdown(beratung_line, unsafe_allow_html=True)
            st.markdown(hello_line, unsafe_allow_html=True)
            st.markdown(first_line, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Eigenanamnese:</b></div>",  unsafe_allow_html=True)
            st.markdown(free_anamnesis, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Familienanamnese:</b></div>",  unsafe_allow_html=True)
            st.markdown(family, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Allgemeine Informationen zum Krankheitsbild:</b></div>",  unsafe_allow_html=True)
            st.markdown(disease_info_line, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Beurteilung und Procedere:</b></div>",  unsafe_allow_html=True)
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown(last_line, unsafe_allow_html=True)
            st.markdown(signature, unsafe_allow_html=True)
            st.markdown(anhang, unsafe_allow_html=True)

######################################################################################################################################################

with tab2:
    
    ##########################################
    # Create second tab for Befundbesprechung#
    ##########################################
    st.markdown("<h1 style='font-size: 30px;'>Befundbesprechungsbrief</h1>", unsafe_allow_html=True)
        
    # Get the current date and time#
    ################################
    current_datetime = datetime.now()
        
    #Get patient data#
    ##################
    # Create a selectbox to choose an option for the gender
    st.markdown("### Patienten Daten")
    col1, col2, col3= st.columns(3)
    Titel_2 = col1.selectbox("Titel", ["Frau", "Herr", "Familie"], key="Titel_2")     
    Vorname_2 = col2.text_input("Vorname",key="Vorname_2")
    Name_2 = col3.text_input("Name", key="Name_2")
        
    #st.markdown("### Fragestellung")
    question_2 = st.text_input("Fragestellung", key="question_2")
    
    #Add a selectbox for choosing the type of counciling
    #st.markdown("### Art der Beratung und Analyse")
    col1, col2, col3= st.columns(3)
    council_2 = col1.selectbox("Art der Beratung", ["Befundbesprechung"], key="council_2")
    person_2 = col2.selectbox("Patiententyp", ["Kind", "Erwachsen"], key="person_2")
    disease_2 = col3.selectbox("Krankheitsbild", ["NDD +/- Epilepsie", "unspezifisch", "HNPCC", "SCA", "HTT", "Marfan", "EDS-klassisch-COL5A1", "Geschlechtsinkongruenz"], key="disease_2")
    if person_2=="Kind":
        child_2=col2.selectbox("Kind", ["Tochter", "Sohn"], key="child_2")
        Name_child_2=col2.text_input("Vorname",key="Name_child_2")

    
    #Add a selectbox for choosing the type of analysis and result#
    ###############################################################
    if disease_2=="NDD +/- Epilepsie":
        analysis_2 = st.selectbox("Art der genetischen Testung", ["Exom", "Exom+CNV+CA", "Trio", "gezielt"], key="analysis_2")
    elif disease_2=="unspezifisch":
        analysis_2 = st.selectbox("Art der genetischen Testung", ["Exom", "Exom+CNV+CA", "Trio", "gezielt", "Cancer Panel", "Repeat Expansion", "CA"], key="analysis_2")
    elif disease_2=="HNPCC":
        analysis_2 = st.selectbox("Art der genetischen Testung", ["gezielt", "Cancer Panel"], key="analysis_2")
    elif disease_2=="SCA":
        analysis_2 = st.selectbox("Art der genetischen Testung", ["gezielt", "Repeat Expansion"], key="analysis_2")
    elif disease_2=="HTT":
        analysis_2 = st.selectbox("Art der genetischen Testung", ["gezielt", "Repeat Expansion"], key="analysis_2")
    elif disease_2=="Marfan":
        analysis_2 = st.selectbox("Art der genetischen Testung", ["Exom", "gezielt"], key="analysis_2")
    elif disease_2=="EDS-klassisch-COL5A1":
        analysis_2 = st.selectbox("Art der genetischen Testung", ["Exom", "gezielt"], key="analysis_2")
    elif disease_2=="Geschlechtsinkongruenz":
        analysis_2 = st.selectbox("Art der genetischen Testung", ["CA"], key="analysis_2")    
    
    #Add a type of result depending on analysis#
    ############################################
    if analysis_2 == "Exom":
        result_2 = st.selectbox ("Ergebnis",  ["unauffällig", "VUS", "auffällig"])
    elif analysis_2 == "Exom+CNV+CA":
        result_2 = st.selectbox ("Ergebnis",  ["unauffällig", "VUS", "auffällig"])
    elif analysis_2 == "Trio":
        result_2 = st.selectbox ("Ergebnis",  ["unauffällig", "VUS", "auffällig"])
    elif analysis_2 == "gezielt":
        result_2 = st.selectbox ("Ergebnis",  ["unauffällig", "auffällig"])
    elif analysis_2 == "Cancer Panel":
        result_2 = st.selectbox ("Ergebnis",  ["unauffällig", "VUS", "auffällig"])
    elif analysis_2 == "Repeat Expansion":
        result_2 = st.selectbox ("Ergebnis",  ["unauffällig", "auffällig"])
    elif analysis_2 == "CA":
        result_2 = st.selectbox ("Ergebnis",  ["unauffällig", "auffällig"])
    
    #Add the result in free text

    #Case 1 unauff. for all except gezielt and CA#
    ##############################################
    if result_2=="unauffällig" and analysis_2!="gezielt" and analysis_2!="CA" :
        result_default_text = """Kein Nachweis einer klinisch relevanten Variante in der molekulargenetischen Diagnostik"""
        result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)

    #Case 2 unauff. for gezielt#
    ############################
    elif result_2=="unauffällig" and analysis_2=="gezielt":
        result_default_text = """Ausschluss der familiär bekannten Variante im XX-Gen/ Kein Nachweis einer klinisch relevanten Variante im XX-Gen"""
        result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)

    #Case 3 unauff. for CA#
    #######################
    elif result_2=="unauffällig" and analysis_2=="CA":
        if disease == "Geschlechtsinkongruenz":
            result_default_text = """Genetisches Geschlecht: weiblich/ männlich"""
            result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)
        elif disease == "unspezifisch":
            if person_2=="Erwachsen":
                if Titel_2=="Frau":
                    result_default_text="""Strukturell und numerisch unauffälliger weiblicher Karyotyp"""
                    result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)
                elif Titel_2=="Mann":
                    result_default_text="""Strukturell und numerisch unauffälliger männlicher Karyotyp"""
                    result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)
                elif Titel_2=="Familie":
                    result_default_text="""Strukturell und numerisch unauffällige Karyotypen"""
                    result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)
            elif person_2=="Kind":
                if child_2=="Tochter":
                    result_default_text="""Strukturell und numerisch unauffälliger weiblicher Karyotyp"""
                    result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)
                elif child_2=="Sohn":
                    result_default_text="""Strukturell und numerisch unauffälliger männlicher Karyotyp"""
                    result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)
                    
                    
                
    #Case 4 VUS for Exome and Panel#
    ################################
    elif result_2=="VUS":
        result_default_text = """Nachweis einer Variante unklarer Signifikanz c.XX, p.(XX) im XX-Gen"""
        result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)

    #Case 5 auff. for Exome and Panel, and Repeat#
    ##############################################
    elif result_2=="auffällig" and analysis_2!="gezielt" and analysis !="CA":
        result_default_text = """Diagnose: XX, molekulargenetisch nachgewiesen"""
        result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)
    
    #Case 6 auff. for gezielt#
    ##########################
    elif result_2=="auffällig" and analysis_2=="gezielt":
        result_default_text = """Nachweis der familiär bekannten Variante c.XX, p.(XX) im XX-Gen/Heterozygoter Nachweis der familiär bekannten Variante c.XX,p.(XX) im XX-Gen"""
        result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)

    #Case 7 auff. for CA#
    #####################
    elif result_2=="auffällig" and analysis_2=="CA":
        result_default_text ="""Diagnose: Eine Trisomie XX/ Translokation XX, zytogenetisch nachgewiesen"""
        result_text=st.text_area("Ergebnis der genetischen Diagnostik", result_default_text)

     #Add Signature boxes
    st.markdown("### Behratende Ärzte")
    col1, col2 = st.columns(2)
    Arzt1_2 = col1.selectbox("Arzt 1", ["Diana Le Duc", "Albrecht Kobelt"], key="Arzt1_2")
    Arzt2_2 = col2.selectbox("Arzt 2", ["Diana Le Duc", "Albrecht Kobelt"],  key="Arzt2_2")

    ###########################################
    #Letter Structure for all types of letters#
    ###########################################
    
    #Beratungsgrund#
    ################
    if analysis_2 != "gezielt":
        beratung_line_2 = f"**Beratungsgrund:** V.a. genetisch bedingte {question_2}"
    elif analysis_2 == "gezielt":
        beratung_line_2 = f"**Beratungsgrund:** Eine (wahrscheinlich) pathogene Variante c.XX, p.XX im XX-Gen in der Familienanamnese"

    #Ergebnis#
    ##########
    ergebnis=f"**Ergebnis:** {result_text}"
    
    #Begrüßung#
    ###########
    if Titel_2== "Herr":
        hello_line_2 = f"Sehr geehrter {Titel} {Name},"
    elif Titel_2 != "Herr":
        hello_line_2 = f"Sehr geehrte {Titel} {Name},"
    
    #Date of Beratung#
    ##################

    #Case 1 unauff no meeting#
    ##########################
    if result_2=="unauffällig":
        if person_2=="Kind":
            if child_2=="Sohn":
                first_line_2=f"wir berichten vom Ergebnis der bei Ihrem Sohn, {Name_child_2}, durchgeführten genetischen Diagnostik. Zur Vorgeschichte verweisen wir auf unseren Brief vom XX."""
            elif child_2=="Tochter":
                first_line_2=f"wir berichten vom Ergebnis der bei Ihrer Tochter, {Name_child_2}, durchgeführten genetischen Diagnostik. Zur Vorgeschichte verweisen wir auf unseren Brief vom XX."""
        elif person_2=="Erwachsen":
            first_line_2=f"wir berichten vom Ergebnis der bei Ihnen durchgeführten genetischen Diagnostik. Zur Vorgeschichte verweisen wir auf unseren Brief vom XX."""
    
    #Case 2 auff meeting#
    #####################    
    elif result_2!="unauffällig":
        if person_2=="Kind":
            if child_2=="Sohn":
                first_line_2=f"am {current_datetime.strftime('%d.%m.%Y')} stellten Sie Ihren Sohn, {Name_child_2}, in unserer genetischen Sprechstunde vor. Zur Vorgeschichte verweisen wir auf unseren Brief vom XX."
            elif child_2=="Tochter":
                first_line_2=f"am {current_datetime.strftime('%d.%m.%Y')} stellten Sie Ihre Tochter, {Name_child_2}, in unserer genetischen Sprechstunde vor. Zur Vorgeschichte verweisen wir auf unseren Brief vom XX."
        elif person_2=="Erwachsen":
            first_line_2=f"am {current_datetime.strftime('%d.%m.%Y')} stellten Sie sich in unserer genetischen Sprechstunde vor. Zur Vorgeschichte verweisen wir auf unseren Brief vom XX."

    #Genetic diagnostic#
    ####################

    #Case 1 unauff, Exom+CNV+CA#
    ############################
    if result_2=="unauffällig" and analysis_2=="Exom+CNV+CA":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic="""Die anhand einer Blutprobe von Ihrem Sohn durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen männlichen Karyotyp (Befund vom XX). Zur weiteren Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihrem Sohn die molekulargenetische Diagnostik im <i>FMR1</i>-Gen bezüglich eines Fragilen-X-Syndroms durch. Diese ergab einen unauffälligen Befund (Befund vom XX). Auch die molekulargenetische Karyotypisierung mittels genomweiter CNV-Analyse ergab keinen Nachweis von klinisch relevanten Kopienzahlvarianten (Befund vom XX). Weiterhin führten wir eine molekulargenetische Exomdiagnostik bezüglich Veränderungen in den für seine Auffälligkeiten ursächlichen Genen durch. Diese ergab keinen Nachweis einer klinisch relevanten Variante (Befund vom XX)."""
            elif child_2=="Tochter":
                diagnostic="""Die anhand einer Blutprobe von Ihrer Tochter durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen weiblichen Karyotyp (Befund vom XX). Zur weiteren Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihrer Tochter die molekulargenetische Diagnostik im <i>FMR1</i>-Gen bezüglich eines Fragilen-X-Syndroms durch. Diese ergab einen unauffälligen Befund (Befund vom XX). Auch die molekulargenetische Karyotypisierung mittels genomweiter CNV-Analyse ergab keinen Nachweis von klinisch relevanten Kopienzahlvarianten (Befund vom XX). Weiterhin führten wir eine molekulargenetische Exomdiagnostik bezüglich Veränderungen in den für ihre Auffälligkeiten ursächlichen Genen durch. Diese ergab keinen Nachweis einer klinisch relevanten Variante (Befund vom XX)."""
        elif person_2=="Erwachsen":
            if Titel_2=="Herr":
                diagnostic="""Die anhand einer Blutprobe von Ihnen durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen männlichen Karyotyp (Befund vom XX). Zur weiteren Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihnen die molekulargenetische Diagnostik im <i>FMR1</i>-Gen bezüglich eines Fragilen-X-Syndroms durch. Diese ergab einen unauffälligen Befund (Befund vom XX). Auch die molekulargenetische Karyotypisierung mittels genomweiter CNV-Analyse ergab keinen Nachweis von klinisch relevanten Kopienzahlvarianten (Befund vom XX). Weiterhin führten wir eine molekulargenetische Exomdiagnostik bezüglich Veränderungen in den für Ihre Auffälligkeiten ursächlichen Genen durch. Diese ergab keinen Nachweis einer klinisch relevanten Variante (Befund vom XX)."""
            elif Titel_2=="Frau":
                diagnostic="""Die anhand einer Blutprobe von Ihnen durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen weiblichen Karyotyp (Befund vom XX). Zur weiteren Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihnen die molekulargenetische Diagnostik im <i>FMR1</i>-Gen bezüglich eines Fragilen-X-Syndroms durch. Diese ergab einen unauffälligen Befund (Befund vom XX). Auch die molekulargenetische Karyotypisierung mittels genomweiter CNV-Analyse ergab keinen Nachweis von klinisch relevanten Kopienzahlvarianten (Befund vom XX). Weiterhin führten wir eine molekulargenetische Exomdiagnostik bezüglich Veränderungen in den für Ihre Auffälligkeiten ursächlichen Genen durch. Diese ergab keinen Nachweis einer klinisch relevanten Variante (Befund vom XX)."""
            elif Titel_2=="Familie":
                diagnostic="""Die anhand einer Blutprobe von Ihnen durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen weiblichen/männlichen Karyotyp (Befund vom XX). Zur weiteren Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihnen die molekulargenetische Diagnostik im <i>FMR1</i>-Gen bezüglich eines Fragilen-X-Syndroms durch. Diese ergab einen unauffälligen Befund (Befund vom XX). Auch die molekulargenetische Karyotypisierung mittels genomweiter CNV-Analyse ergab keinen Nachweis von klinisch relevanten Kopienzahlvarianten (Befund vom XX). Weiterhin führten wir eine molekulargenetische Exomdiagnostik bezüglich Veränderungen in den für Ihre Auffälligkeiten ursächlichen Genen durch. Diese ergab keinen Nachweis einer klinisch relevanten Variante (Befund vom XX)."""


    #Case 2 unauff, Trio#
    #####################
    elif result_2=="unauffällig" and analysis_2=="Trio":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic="""Zur Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung bei Ihrem Sohn veranlassten wir eine Trio-Exom-Analyse auf Forschungsbasis. Hierbei ergab sich ein unauffälliger Befund (Befund vom XX, Institut für Humangenetik am Universitätsklinikum Leipzig)."""
            elif child_2=="Tochter":
                diagnostic="""Zur Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung bei Ihrem Sohn veranlassten wir eine Trio-Exom-Analyse auf Forschungsbasis. Hierbei ergab sich ein unauffälliger Befund (Befund vom XX, Institut für Humangenetik am Universitätsklinikum Leipzig)."""
        elif person_2=="Erwachsen":
            diagnostic="""Zur Abklärung des Verdachts auf eine genetisch bedingte Intellignzminderung bei Ihnen veranlassten wir eine Trio-Exom-Analyse auf Forschungsbasis. Hierbei ergab sich ein unauffälliger Befund (Befund vom XX, Institut für Humangenetik am Universitätsklinikum Leipzig)."""

    #Case 3 unauff, Exom#
    #####################
    elif result_2=="unauffällig" and analysis_2=="Exom":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic="""Zur Abklärung des Verdachts auf XX führten wir bei Ihrem Sohn eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei ergab sich ein unauffälliger Befund (Befund vom XX)."""
            elif child_2=="Tochter":
                diagnostic="""Zur Abklärung des Verdachts auf XX führten wir bei Ihrer Tochter eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei ergab sich ein unauffälliger Befund (Befund vom XX)."""
        elif person_2=="Erwachsen":
            diagnostic="""Zur Abklärung des Verdachts auf XX führten wir bei Ihnen eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei ergab sich ein unauffälliger Befund (Befund vom XX)."""

    #Case 4 unauff, gezielt#
    ########################
    elif result_2=="unauffällig" and analysis_2=="gezielt":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic="""Wir führten eine gezielte Diagnostik bezüglich der familiär bekannten (wahrscheinlich) pathogenen c.XX,p.(XX) im XX-Gen bei Ihrem Sohn durch. Hierbei konnte diese bei ihm nicht nachgewiesen werden (Befund vom XX)."""
            elif child_2=="Tochter":
                diagnostic="""Wir führten eine gezielte Diagnostik bezüglich der familiär bekannten (wahrscheinlich) pathogenen c.XX,p.(XX) im XX-Gen bei Ihrer Tochter durch. Hierbei konnte diese bei ihr nicht nachgewiesen werden (Befund vom XX)."""
        elif person_2=="Erwachsen":
            diagnostic="""Wir führten eine gezielte Diagnostik bezüglich der familiär bekannten (wahrscheinlich) pathogenen c.XX,p.(XX) im XX-Gen bei Ihnen durch. Hierbei konnte diese bei ihr nicht nachgewiesen werden (Befund vom XX). <br> /Zur Abklärung einer möglichen Anlageträgerschaft bezüglich XX veranlassten wir bei Ihnen eine molekulargenetische Einzelgen-Diagnostik und MLPA-Untersuchung bezüglich Veränderungen im XX-Gen. Diese ergab keinen Nachweis einer klinisch relevanten Variante im XX-Gen (Befund vom XX)."""

    #Case 5 unauff, Cancer Panel#
    #############################
    elif result_2=="unauffällig" and analysis_2=="Cancer Panel":
        if disease_2=="HNPCC":
            diagnostic_patho="""Zur Abklärung des Verdachts auf ein HNPCC-Syndrom // eine genetisch bedingte Darmkrebserkrankung veranlassten wir eine molekularpathologische Diagnostik bezüglich einer Mikrosatelliteninstabilität und eine immunhistochemische Untersuchung am Tumormaterial von Ihnen. Diese ergaben keinen Nachweis einer Mikrosatelliteninstabilität sowie eine unauffällige Immunhistochemie bezüglich MLH-1, MSH-2, MSH-6 und PMS-2 (Befund vom XX, XX). Die molekularpathologische Diagnostik am Tumormaterial bezüglich der <i>BRAF</i>-Variante c.1799T>A, p.(Val600Glu) ergab einen unauffälligen Befund (Befund vom XX, XX).<br><br> //Zur Abklärung des Verdachts auf ein eine genetisch bedingtes Kolonkarzinom veranlassten wir eine molekularpathologische Diagnostik bezüglich einer Mikrosatelliteninstabilität am Tumormaterial von Ihnen. Diese ergaben den Nachweis einer starken Mikrosatelliteninstabilität korrespondierend zum Verlaust der Kernexpression für PMS-2 und MLH-1. (Befund vom XX, XX). Die molekularpathologische MLH1-Promotormethylierungsanalyse erbrachte eine MLH1-Promotormethylierung. Die Mutationsanalyse am Tumormaterial bezüglich der <i>BRAF</i>-Variante c.1799T>A, p.(Val600Glu) ergab einen unauffälligen Befund (Befund vom XX, XX )."""
            diagnostic="""Zur weiteren Abklärung des Verdachts auf ein HNPCC-Syndrom // eine genetisch bedingte Darmkrebserkrankung führten wir bei Ihnen eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei ergab sich ein unauffälliger Befund (Befund vom XX)."""
        elif disease_2=="unspezifisch":
            diagnostic="""Zur Abklärung des Verdachts auf eine genetisch bedingte Kreberkrankung führten wir bei Ihnen eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei ergab sich ein unauffälliger Befund (Befund vom XX)."""

    #Case 6 unauff, Repeat Expansion#
    #################################
    elif result_2=="unauffällig" and analysis_2=="Repeat Expansion":
        if disease_2=="HTT":
            diagnostic="""Wir führten eine molekulargenetische Diagnostik bezüglich der Repeatanzahl im <i>HTT</i>-Gen bei Ihnen durch. Diese ergab einen unauffälligen Befund mit dem Nachweis von zwei Allelen mit XX CAG-Repeats (Befund vom XX)."""
        elif disease_2=="SCA":
             diagnostic="""Zur Abklärung des Verdachts auf eine genetisch bedingte Bewegungsstörung veranlassten wir an einer Probe von Ihnen zunächst eine molekulargenetische Diagnostik bezüglich der SCA 1, 2, 3, 6, und 17. Diese ergab keinen Nachweis einer Repeat-Expansion und somit einen unauffälligen Befund (Befund vom XX). Ergänzend veranlassten wir die molekulargenetische Diagnostik bezüglich der SCA 7, 8, 10 und 12. Diese ergab keinen Nachweis einer Repeat-Expansion und somit einen unauffälligen Befund (Befund vom XX). Auch die molekulargenetische Diagnostik bezüglich des Fragiles-X-assoziiertes-Tremor-Ataxie-Syndroms ergab keinen Nachweis einer CGG-Repeatverlängerung im <i>FMR1</i>-Gen und somit einen unauffälligen Befund (Befund vom XX). Weiterhin führten wir eine molekulargenetische Paneldiagnostik bezüglich Veränderungen in den Genen, welche mit Ihren Symptomen assoziiert sind, durch. Diese ergab keinen Nachweis einer klinisch relevanten Variante und somit einen unauffälligen Befund (Befund vom XX)."""
        elif disease_2=="unspezifisch":
            diagnostic="""Zur Abklärung des Verdachts auf eine genetisch bedingte Repeat-Erkrankung führten wir bei Ihnen eine molekulargenetische Diagnostik in den hierfür ursächlichen Genen durch. Hierbei ergab sich ein unauffälliger Befund (Befund vom XX)."""

    #Case 7 unauff, CA#
    ###################
    elif result_2=="unauffällig" and analysis_2=="CA": 
        if person_2=="Erwachsen":
            if Titel_2=="Herr":
                diagnostic="""Die durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen männlichen Karyotyp (Befund vom XX)."""
            elif Titel_2=="Frau":
                diagnostic="""Die durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen weiblichen Karyotyp (Befund vom XX)."""
            elif Titel_2=="Familie":
                diagnostic="""Die durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen weiblichen/männlichen Karyotyp (Befund vom XX)."""  
        elif person_2=="Kind":
            if child_2=="Sohn":
                diagnostic="""Die durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen männlichen Karyotyp (Befund vom XX)."""
            elif child_2=="Tochter":
                diagnostic="""Die durchgeführte konventionelle Chromosomenanalyse ergab einen strukturell und numerisch unauffälligen weiblichen Karyotyp (Befund vom XX)."""

    #Case 8 VUS, Exom, Exom+CNV+CA, Trio, Cancer Panel#
    ###################################################
    elif result_2=="VUS" and analysis_2=="Exom+CNV+CA":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihrem Sohn, {Name_child_2}, eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihrem Sohn nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
            elif child_2=="Tochter":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihrer Tochter, {Name_child_2}, eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihrer Tochter nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
        elif person_2=="Erwachsen":   
             diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihnen eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihnen nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihren Eltern nicht vor.<br> // Bei Ihrer Mutter/ Ihrem Vater war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
   
    elif result_2=="VUS" and analysis_2=="Exom":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihrem Sohn, {Name_child_2}, eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihrem Sohn nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
            elif child_2=="Tochter":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihrer Tochter, {Name_child_2}, eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihrer Tochter nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
        elif person_2=="Erwachsen":   
             diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihnen eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihnen nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihren Eltern nicht vor.<br> // Bei Ihrer Mutter/ Ihrem Vater war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."

    elif result_2=="VUS" and analysis_2=="Trio":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir auf Forschungsbasis bei Ihrem Sohn, {Name_child_2}, eine molekulargenetische Trio-Exomdiagnostik XX in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihrem Sohn nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
            elif child_2=="Tochter":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir auf Forschungsbasis bei Ihrer Tochter, {Name_child_2}, eine molekulargenetische Trio-Exomdiagnostik XX in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihrer Tochter nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
        elif person_2=="Erwachsen":   
             diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir auf Forschungsbasis bei Ihnen eine molekulargenetische Trio-Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihnen nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihren Eltern nicht vor.<br> // Bei Ihrer Mutter/ Ihrem Vater war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
    
    elif result_2=="VUS" and analysis_2=="Cancer Panel":
        if disease_2=="HNPCC":
            diagnostic_patho="""Zur Abklärung des Verdachts auf ein HNPCC-Syndrom // eine genetisch bedingte Darmkrebserkrankung veranlassten wir eine molekularpathologische Diagnostik bezüglich einer Mikrosatelliteninstabilität und eine immunhistochemische Untersuchung am Tumormaterial von Ihnen. Diese ergaben keinen Nachweis einer Mikrosatelliteninstabilität sowie eine unauffällige Immunhistochemie bezüglich MLH-1, MSH-2, MSH-6 und PMS-2 (Befund vom XX, XX). Die molekularpathologische Diagnostik am Tumormaterial bezüglich der <i>BRAF</i>-Variante c.1799T>A, p.(Val600Glu) ergab einen unauffälligen Befund (Befund vom XX, XX).<br> //Zur Abklärung des Verdachts auf ein genetisch bedingtes Kolonkarzinom veranlassten wir eine molekularpathologische Diagnostik bezüglich einer Mikrosatelliteninstabilität am Tumormaterial von Ihnen. Diese ergaben den Nachweis einer starken Mikrosatelliteninstabilität korrespondierend zum Verlaust der Kernexpression für PMS-2 und MLH-1. (Befund vom XX, XX). Die molekularpathologische MLH1-Promotormethylierungsanalyse erbrachte eine MLH1-Promotormethylierung. Die Mutationsanalyse am Tumormaterial bezüglich der <i>BRAF</i>-Variante c.1799T>A, p.(Val600Glu) ergab einen unauffälligen Befund (Befund vom XX, XX )."""
            diagnostic="""Zur weiteren Abklärung des Verdachts auf ein HNPCC-Syndrom // eine genetisch bedingte Darmkrebserkrankung führten wir bei Ihnen eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxx>, p.(XX) im XX-Gen bei Ihnen nachgewiesen (Befund vom XX)."""
        elif disease_2=="unspezifisch":
            diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte Krebserkrankung führten wir bei Ihnen eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote Variante unklarer Signifikanz c.xxxx>x, p.(XX) im XX-Gen bei Ihnen Tochter nachgewiesen (Befund vom XX)."

    #Case 8 auff, Exom, Exom+CNV+CA, Trio, Cancer Panel#
    ####################################################
    elif result_2=="auffällig" and analysis_2=="Exom+CNV+CA":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihrem Sohn, {Name_child_2}, eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihrem Sohn nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name}, nicht vor. Bei Ihnen, Herr/Frau {Name}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
            elif child_2=="Tochter":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihrer Tochter, {Name_child_2}, eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihrer Tochter nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name}, nicht vor. Bei Ihnen, Herr/Frau {Name}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
        elif person_2=="Erwachsen":   
             diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte Entwicklungsstörung führten wir bei Ihnen eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihnen nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihren Eltern nicht vor.<br> // Bei Ihrer Mutter/ Ihrem Vater war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."

    elif result_2=="auffällig" and analysis_2=="Exom":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihrem Sohn, {Name_child_2}, eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihrem Sohn nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
            elif child_2=="Tochter":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihrer Tochter, {Name_child_2}, eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante  c.xxxx>x, p.(XX) im XX-Gen bei Ihrer Tochter nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
        elif person_2=="Erwachsen":   
             diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihnen eine molekulargenetische Exomdiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihnen nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihren Eltern nicht vor.<br> // Bei Ihrer Mutter/ Ihrem Vater war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."

    elif result_2=="auffällig" and analysis_2=="Trio":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihrem Sohn, {Name_child_2}, eine molekulargenetische Trio-Exomdiagnostik XX in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihrem Sohn nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
            elif child_2=="Tochter":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihrer Tochter, {Name_child_2}, eine molekulargenetische Tri-Exomdiagnostik XX in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante  c.xxxx>x, p.(XX) im XX-Gen bei Ihrer Tochter nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."
        elif person_2=="Erwachsen":   
             diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihnen eine molekulargenetische Trio-Exomdiagnostik XX in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihnen nachgewiesen (Befund vom XX). Diese XX-Variante liegt bei Ihren Eltern nicht vor.<br> // Bei Ihrer Mutter/ Ihrem Vater war die o.g. Variante ebenfalls nachweisbar (Befund vom XX)."

    elif result_2=="auffällig" and analysis_2=="Cancer Panel":
        if disease_2=="HNPCC":
            diagnostic="""Zur Abklärung des Verdachts auf ein HNPCC-Syndrom // eine genetisch bedingte Darmkrebserkrankung führten wir bei Ihnen eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihnen nachgewiesen (Befund vom XX)."""
        elif disease_2=="unspezifisch":
             diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte Krebserkrankung führten wir bei Ihnen eine molekulargenetische Paneldiagnostik in den hierfür ursächlichen Genen durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihnen Tochter nachgewiesen (Befund vom XX)."

    #Case 9 auff, gezielt#
    ######################
    elif result_2=="auffällig" and analysis_2=="gezielt":
        if person_2=="Kind":
            if child_2=="Sohn":
                     diagnostic="""Wir führten eine gezielte Diagnostik bezüglich der familiär bekannten (wahrscheinlich) pathogenen c.XX,p.(XX) im XX-Gen Ihrem Sohn, {Name_child}, durch. Hierbei konnte diese bei ihm nachgewiesen werden (Befund vom XX)."""
            elif child_2=="Tochter":
                     diagnostic="""Wir führten eine gezielte Diagnostik bezüglich der familiär bekannten (wahrscheinlich) pathogenen c.XX,p.(XX) im XX-Gen Ihrer Tochter, {Name_child}, durch. Hierbei konnte diese bei ihr nachgewiesen werden (Befund vom XX)."""
        elif person_2=="Erwachsen":
             diagnostic="""Wir führten eine gezielte Diagnostik bezüglich der familiär bekannten (wahrscheinlich) pathogenen c.XX,p.(XX) im XX-Gen bei Ihnen durch. Hierbei konnte diese bei Ihnen nachgewiesen werden (Befund vom XX).<br> // Zur Abklärung einer möglichen Anlageträgerschaft bezüglich XX veranlassten wir bei Ihnen eine molekulargenetische Einzelgen-Diagnostik und MLPA-Untersuchung bezüglich Veränderungen im XX-Gen. Diese ergab eine heterozygote wahrscheinlich/pathogene Variante c.XX,p.(XX) im XX-Gen (Befund vom XX)."""

    #Case 10 auff, Repeat Expansion#
    ################################
    elif result_2=="auffällig" and analysis_2=="Repeat Expansion":
        if disease_2=="HTT":
            diagnostic="""Zur Abklärung des Verdachts auf eine Huntington-Erkrankung führten wir bei Ihnen eine molekulargenetische Diagnostik im <i>HTT</i>-Gen durch. Hierbei wurde eine pathogene heterozygote CAG-Repeatverlängerung auf XX CAG-Repeats im <i>HTT</i>-Gen bei Ihnen nachgewiesen (Befund vom XX)."""
        elif disease_2=="HTT":
            diagnostic="""Zur Abklärung des Verdachts auf eine genetisch bedingte Bewegungsstörung veranlassten wir an einer Probe von Ihnen eine molekulargenetische Repeat-Expansion Diagnostik bezüglich der SCA 1, 2, 3, 6, 7, 8, 10, 12 und 17 sowie des Fragiles-X-assoziiertes-Tremor-Ataxie-Syndroms. Hierbei wurde eine pathogene heterozygote XX-Repeatverlängerung auf XX XX-Repeats im XX-Gen bei Ihnen nachgewiesen (Befund vom XX). Weiterhin führten wir eine molekulargenetische Paneldiagnostik bezüglich Veränderungen in den Genen, welche mit Ihren Symptomen assoziiert sind, durch. Diese ergab keinen Nachweis einer klinisch relevanten Variante und somit einen unauffälligen Befund (Befund vom XX).<br> //Zur Abklärung des Verdachts auf eine genetisch bedingte Bewegungsstörung veranlassten wir an einer Probe von Ihnen eine molekulargenetische Repeat-Expansion Diagnostik bezüglich der SCA 1, 2, 3, 6, 7, 8, 10, 12 und 17 sowie des Fragiles-X-assoziiertes-Tremor-Ataxie-Syndroms. Diese ergab keinen Nachweis einer klinisch relevanten Variante und somit einen unauffälligen Befund (Befund vom XX). Weiterhin führten wir eine molekulargenetische Paneldiagnostik bezüglich Veränderungen in den Genen, welche mit Ihren Symptomen assoziiert sind, durch. Hierbei wurde die heterozygote wahrscheinlich/pathogene Variante c.xxxx>x, p.(XX) im XX-Gen bei Ihnen nachgewiesen (Befund vom XX)."""
        elif disease_2=="unspezifisch":
            diagnostic="""Zur Abklärung des Verdachts auf eine genetisch bedingte Repeat-Verlängerung-Erkrankung führten wir bei Ihnen zudem eine molekulargenetische Diagnostik im XX-Gen durch. Hierbei wurde eine pathogene heterozygote CAG-Repeatverlängerung auf XX XX-Repeats im XX-Gen bei Ihnen nachgewiesen (Befund vom XX)."""

    #Case 11 auff CA#
    #################
    elif result_2=="auffällig" and analysis_2=="CA":
        if person_2=="Kind":
            if child_2=="Sohn":
                diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihrem Sohn, {Name_child_2}, eine konventionelle Chromosomenanalyse. Hierbei wurde eine wahrscheinlich/pathogene Chromosomenveränderung/Trisomie XX bei Ihrem Sohn nachgewiesen (Befund vom XX). Diese Chromosomenveränderung liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war eine Translokation XX ebenfalls nachweisbar (Befund vom XX)."
            elif child_2=="Tochter":
                 diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihrer Tochter, {Name_child_2}, eine konventionelle Chromosomenanalyse. Hierbei wurde eine wahrscheinlich/pathogene Chromosomenveränderung/Trisomie XX bei Ihrer Tochter nachgewiesen (Befund vom XX). Diese Chromosomenveränderung liegt bei Ihnen, Herr und Frau {Name_2}, nicht vor.<br> // Bei Ihnen, XX Herr/Frau {Name_2}, war eine Translokation XX ebenfalls nachweisbar (Befund vom XX)."
        elif person_2=="Erwachsen":   
             diagnostic=f"Zur Abklärung des Verdachts auf eine genetisch bedingte XX führten wir bei Ihnen eine konventionelle Chromosomenanalyse. Hierbei wurde eine wahrscheinlich/pathogene Chromosomenveränderung/Trisomie XX bei Ihnen nachgewiesen (Befund vom XX). Diese Chromosomenveränderung liegt bei Ihren Eltern nicht vor.<br> // Bei Ihrer Mutter/ Ihrem Vater war eine Translokation XX ebenfalls nachweisbar (Befund vom XX)."
  
    #Info about disease#
    ####################
    if result_2!="unauffällig":
        if disease_2=="unspezifisch":
            disease_default_text = """- Klinisches Bild der Erkrankung<br>- Genetik und Vererbung<br>- Therapien"""
            disease_text=st.text_area("Allgemeine Informationen zum Krankheitsbild", disease_default_text)
            recommendation_default_text="""- Nach Diagnosestellung sollten folgende Untersuchungen erfolgen: XX<br> - Mit Nachweis der o.g. wahrscheinlich pathogenen Variante im XX-Gen besteht für Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik, dies gilt insbesondere für Ihre Geschwister und Ihre Kinder (XX ab Erreichen der Volljährigkeit). Eine Terminvereinbarung ist unter der o.g. Telefonnummer möglich. Eine gezielte Diagnostik auf die o.g. Variante im XX-Gen bei Ihren Eltern haben mit ihrem Einverständnis bereits eingeleitet. Sobald die Befunde der eingeleiteten Diagnostik vorliegen, werden wir Sie kontaktieren und weiterführend Stellung nehmen.<br> Viele Ratsuchende profitieren von Angeboten verschiedener Selbsthilfegruppen. Hier können Betroffene und Eltern von Kindern mit seltenen Erkrankungen Informationen erhalten, weitergeben und eine psychosoziale Betreuung in Anspruch nehmen. Selbsthilfegruppen für Angehörige und Patient:innen mit XX sind beispielsweise unter folgenden Adressen erreichbar:XX."""
            recommendation=st.text_area("Empfehlungen", recommendation_default_text, key="recommendation_un")
        elif disease_2=="NDD +/- Epilepsie":
            disease_default_text = """- Klinisches Bild der Erkrankung<br>- Genetik und Vererbung<br>- Therapien"""
            disease_text=st.text_area("Allgemeine Informationen zum Krankheitsbild", disease_default_text)
        elif disease_2=="HNPCC":
            disease_default_text = """Dickdarmkrebs (Kolonkarzinom) zählt zu den häufigsten bösartigen Tumoren in Westeuropa. Die meisten Fälle treten sporadisch auf und sind vermutlich multifaktoriell verursacht. In ca. 3⁠–5 % der Fälle ist eine familiäre Häufung durch eine monogene, autosomal dominant erbliche Ursache zu erklären. Beim familiären Darmkrebs unterscheidet man mehrere Unterformen. Hierzu zählen die FAP (Familiäre Adenomatöse Polyposis) mit hunderten bis tausenden Polypen im Darm, die MUTYH-assoziierte Polyposis mit zehn bis einigen hundert Polypen im Darm und das HNPCC-Syndrom (auch Lynch-Syndrom genannt) ohne Polyposis. Das Lynch-Syndrom ist ein Tumorprädispositionssyndrom, das mit einem erhöhten Risiko für kolorektale Karzinome, Karzinome des weiteren Verdauungstrakts, Endometriumkarzinome, Karzinome des Harntrakts, Ovarialkarzinome und Hirntumoren einhergeht.<br><br>Ursächlich für das Lynch-Syndrom sind pathogene Varianten in den Genen <i>MLH1</i>, <i>MSH2</i>, <i>MSH6</i>, <i>PMS2</i> und <i>EPCAM</i>. Diese werden autosomal dominant vererbt. Das bedeutet, dass heterozygote Anlageträger\*Innen die Erkrankung ausbilden. Damit besteht für die Nachkommen von Anlageträger\*Innenn eine 50 %ige Wahrscheinlichkeit, diese zu erben und die Erkrankung ebenfalls auszubilden. Es ist eine unvollständige Penetranz bekannt. Das bedeutet, nicht jeder Anlageträger\*Innen bildet die Erkrankung aus.<br><br>Um Patient\*Innen mit einem HNPCC-Syndrom (hereditäres nicht-polypöses Kolonkarzinom) zu identifizieren, wurden klinische Kriterien definiert. Sind in einer Familie die Amsterdam-Kriterien für HNPCC (Auftreten von Kolonkarzinom, Nierenbecken- oder Ureterkarzinom und anderen assoziierten Tumorerkrankungen bei drei Familienangehörigen in zwei aufeinanderfolgenden Generationen, ein Familienmitglied erstgradig verwandt mit den beiden anderen, Erkrankungsalter bei einem Betroffenen vor dem 50. Lebensjahr) erfüllt, kann bereits klinisch die Diagnose eines HNPCC-Syndroms gestellt werden.<br> Die Bethesda-Kriterien für HNPCC (Kolonkarzinom vor dem 50. Lebensjahr, synchrones oder metachrones Auftreten von Kolonkarzinom oder anderen assoziierten Tumorerkrankungen, Kolonkarzinom mit spezieller MSI-H-Histologie, Patient mit Kolonkarzinom mit einem erstgradig Verwandten mit Kolonkarzinom oder assoziierter Tumorerkrankung vor dem 50. Lebensjahr, Patient mit Kolonkarzinom mit min. zwei erst- oder zweitgradig Verwandten mit Kolonkarzinom oder assoziierter Tumorerkrankung) stellen hingegen lediglich klinische Verdachtskriterien dar.<br> Bei Verdacht auf ein HNPCC-Syndrom können zunächst molekularpathologische und immunhistochemische Untersuchungen am Tumormaterial erfolgen, bevor eine molekulargenetische Analyse der o.g. Gene anhand einer Blutprobe des Patient\*Innen durchgeführt wird (Kohlmann et Gruber. GeneReviews. 2018).<br><br>Seltenere Tumorprädispositionssyndrome sind das Peutz-Jeghers-Syndrom, das durch multiple Hamartome und melanotische Pigmentflecken gekennzeichnet ist und das PTEN-Hamartoma-Tumor-Syndrom, das mit einer Makrozephalie, Hamartomen der Schleimhaut und einem erhöhten Risiko für Schilddrüsen-, Nierenzell- und Mammakarzinome einhergeht."""
            disease_text=st.text_area("Allgemeine Informationen zum Krankheitsbild", disease_default_text)
        elif disease_2=="SCA":
            disease_default_text ="""Die Spinozerebelläre Ataxie 1 (SCA) ist charakterisiert durch eine progrediente Gang- und Sprechataxie, welche meistens im Erwachsenenalter (30.⁠–40. Lebensjahr) beginnt. Bei den Patient\*Innen fallen häufig zusätzlich eine Gleichgewichtsstörung, eine axonale sensorische Neuropathie, Augenauffälligkeiten (Nystagmus, hypermetrische Sakkaden) und eine milde Schluckstörung auf. Im weiteren Verlauf sind eine Muskelatrophie, Hyporeflexie, Bewegungsstörungen (wie Chorea oder Dystonie), bulbäre Dysfunktion und kognitive Defizite typisch. In der cMRT zeigt sich eine Atrophie des Kleinhirns und Hirnstamms. Der Krankheitsverlauf bis zum Versterben der betroffenen Patient\*Innen kann zwischen zehn und dreißig Jahren betragen.<br><br> Ursächlich sind CAG-Repeatexpansionen im <i>ATXN1</i>-Gen. Diese werden autosomal dominant vererbt. Das bedeutet, dass heterozygote Anlageträger\*Innen die Erkrankung ausbilden. Damit besteht für die Nachkommen von Anlageträger\*Innenn eine 50%ige Wahrscheinlichkeit diese zu erben und die Erkrankung ebenfalls auszubilden. Für die SCA1 ist eine Antizipation beschrieben, das bedeutet, es kann bei der Vererbung, insbesondere vom Vater auf sein Kind, zu einer Verlängerung der Repeat-Expansion kommen. Längere Repeatexpansionen korrelieren in der Regel mit einem früheren Beginn, einem schwereren Krankheitsverlauf und einem früheren Versterben. Eine individuelle Aussage zum Erkrankungsalter und zur Erkrankungsschwere ist jedoch nicht möglich.Bei 39 und mehr CAG-Repeats ohne Unterbrechung durch CAT-Repeats ist eine 100%ige Penetranz für das klassische Bild einer SCA1 beschrieben. Das bedeutet, dass beinahe alle Anlageträger\*Innen Symptome entwi-ckeln werden. Zwischen 36 und 38 CAG-Repeats ohne Unterbrechung durch CAT-Repeats spricht man von einem „intermediären Allel“, dabei sind die Anlageträger\*Innen nicht selbst von einer SCA1 betroffen, jedoch haben Nachkommen durch eine mögliche Antizipation ein erhöhtes Risiko für eine SCA1. Bei Personen mit 6 bis 35 CAG-Repeats oder mit 36 bis 44 CAG-Repeats mit Unterbrechung durch CAT-Repeats besteht kein erhöhtes Erkrankungsrisiko bezüglich einer SCA1.<br><br>Eine kausale Therapie ist bislang nicht bekannt. Medikamente können symptomatisch für neurologische und psychiatrische Symptome eingesetzt werden, welche den Krankheitsverlauf jedoch nicht beeinflussen (Opal et Ashizawa. GeneReviews. 2017)."""
            disease_text=st.text_area("Allgemeine Informationen zum Krankheitsbild", disease_default_text)
        elif disease_2=="HTT":
            disease_default_text ="""Die Huntington-Erkrankung ist eine progrediente neuropsychiatrische Erkrankung, welche meist zwischen dem 30. und 50. Lebensjahr beginnt. Oftmals treten zunächst psychiatrische Symptome wie eine Depression oder Angststörung und im Verlauf typische motorische Symptome auf. Zum breiten Spektrum der motorischen Symptome gehören unwillkürliche/ einschießende Bewegungen, später auch eine Bradykinese (Verlangsamung), Dystonie/ Muskelsteifheit, Gang- und Schluckstörungen. Im weiteren Verlauf der Erkrankung weisen die Betroffenen in aller Regel Schlafstörungen, eine fortschreitende Demenz und Wesensveränderungen auf. Im Spätstadium sind die Patient\*Innen voll pflegebedürftig. Die mediane Überlebensrate nach Beginn der ersten Symptome liegt zwischen 15 und 18 Jahren.<br><br> Ursächlich für eine Huntington-Erkrankung sind pathogene CAG-Repeatverlängerungen (40 und mehr Repeats) im <i>HTT</i>-Gen. Diese werden autosomal-dominant vererbt. Das bedeutet, dass heterozygote Anlageträger\*Innen mit einer pathogenen CAG-Repeatverlängerung die Erkrankung ausbilden. Für die Nachkommen von Anlageträger\*Innenn besteht eine 50%ige Wahrscheinlichkeit, die Repeatverlängerung zu erben und somit die Erkrankung ebenfalls auszubilden. Zwischen 36 und 39 Repeats ist eine inkomplette Penetranz beschrieben. Es erkranken also nicht alle Anlageträger\*Innen.<br> Weiterhin ist für die Huntington-Erkrankung ist eine Antizipation beschrieben, sodass es bei der Vererbung, insbesondere vom Vater auf sein Kind, zu einer Verlängerung der Repeatanzahl kommen kann. Längere Repeats korrelieren in der Regel mit einem früheren Symptombeginn, einem schwereren Krankheitsverlauf und einem früheren Versterben. Ab 60 Repeats ist ein Krankheitsbeginn noch vor dem Erwachsenenalter zu erwarten.<br><br>Eine kausale Therapie ist bislang nicht bekannt. Medikamente können symptomatisch für neurologische und psychiatrische Symptome eingesetzt werden, welche den Krankheitsverlauf jedoch nicht beeinflussen. Wirkstoffe aus klinischen Studien werden bisher in der Routinetherapie nicht eingesetzt (Caron et al. GeneReviews. 2018)."""
            disease_text=st.text_area("Allgemeine Informationen zum Krankheitsbild", disease_default_text)
        elif disease_2=="Marfan":
            disease_default_text = """Das Marfan-Syndrom ist eine Bindegewebserkrankung, die mit einem erhöhten Risiko für Erkrankungen unterschiedlicher Organsysteme einhergeht. Im Herzkreislaufsystem sind dies vor allem Aortenaneurysmen und Aortendissektionen. Im Skelettsystem stehen Großwuchs, eine Skoliose, eine Arachnodaktylie und Thoraxdeformitäten (Pectus carinatum, Pectus excavatum) im Vordergrund. Insgesamt bestehen häufig eine Gelenksüberbeweglichkeit sowie eine Hyperlaxizität der Haut, welche zur Neigung zu Hernien und Dehnungsstreifen führt. Zu den Komplikationen des Auges gehören eine in der Kindheit progrediente Myopie, Linsenluxationen, eine Netzhautablösung, Glaukome und Katarakte. Weiterhin besteht ein erhöhtes Risiko für einen Pneumothorax und eine Duraektasie (Erweiterung der Dura mit Rücken- oder Beinschmerzen). <br><br>Ursächlich für das Marfan-Syndrom sind pathogene Varianten im <i>FBN1</i>-Gen. Diese werden autosomal dominant vererbt. Das bedeutet, dass heterozygote Anlageträger\*Innen die Erkrankung ausbilden. Kinder von Anlageträgern haben eine 50%ige Wahrscheinlichkeit die pathogene Variante zu erben und ebenfalls die Erkrankung auszubilden. Es ist eine variable Expressivität beschrieben. Das bedeutet, die Ausprägung der klinischen Symptomatik kann auch innerhalb einer Familie sehr unterschiedlich sein.<br><br>Eine kausale Therapie für das Marfan-Syndrom steht derzeit nicht zur Verfügung. Es wird jedoch eine Behandlung mit Beta-blockern bzw. AT1-Rezeptor-Antagonisten empfohlen, um das Risiko für Aortenaneurysmen zu reduzieren (Dietz, GeneReviews. 2022)."""
            disease_text=st.text_area("Allgemeine Informationen zum Krankheitsbild", disease_default_text)
        elif disease_2=="EDS-klassisch-COL5A1":
            disease_default_text ="""Das klassische Ehlers-Danlos-Syndrom (cEDS) ist eine Bindegewebserkrankung, die durch eine Überdehnbarkeit der Haut, atrophische Narbenbildung und eine generalisierte Gelenkhypermobilität gekennzeichnet ist. Die Haut fühlt sich weich und teigig an, ist hyperextensibel, dehnt sich leicht aus und schnappt nach dem Loslassen wieder zurück. Die Haut ist fragil, was sich in einer Aufspaltung der Dermis nach relativ geringfügigen Traumata zeigt, insbesondere an Druckstellen (Knie, Ellbogen) und Bereichen, die zu Traumata neigen (Schienbeine, Stirn, Kinn). Die Wundheilung ist schlecht und eine ausgeprägte Narbenbildung nach scheinbar erfolgreicher primärer Wundheilung charakteristisch. Komplikationen der Gelenkhypermobilität, wie z. B. Verrenkungen von Schulter, Kniescheibe, Zehen, Hüfte, Speiche und Schlüsselbein, sin durch die Betroffenen selbst gut beherrschbar. Weitere Merkmale sind eine muskuläre Hypotonie mit verzögerter motorischer Entwicklung, Müdigkeit und Muskelkrämpfe sowie schnell auftretende Blutergüsse. Ein Mitralklappenprolaps kann in seltenen Fällen auftreten, ist aber in der Regel von geringer klinischer Bedeutung. Weiterhin wurden selten Erweiterungen der Aortenwurzel berichtet.<br><br>Ursächlich sind u.a. pathogene Varianten im <i>COL5A1</i>-Gen. Diese werden autosomal dominant vererbt. Das bedeutet, dass heterozygote Anlageträger\*Innen die Erkrankung ausbilden. Damit besteht für die Nachkommen von Anlageträger\*Innen eine 50%ige Wahrscheinlichkeit, diese zu erben und die Erkrankung ebenfalls auszubilden. Die Datenlage reicht aktuell nicht aus um die Penetranz, also die Wahrscheinlichkeit, dass Symptome ausgebildet werden, zu beurteilen.<br><br> Eine ursächliche Therapie ist zum gegenwärtigen Zeitpunkt nicht vorhanden (Malfait <i>et al</i>, GeneReviews, 2018)."""
            disease_text=st.text_area("Allgemeine Informationen zum Krankheitsbild", disease_default_text)
        elif disease_2=="Geschlechtsinkongruenz":
            disease_default_text ="""NO WAY!!!"""
            disease_text=st.text_area("Allgemeine Informationen zum Krankheitsbild", disease_default_text)
            recommendation_default_text="""NO WAY!<br> - Nach Diagnosestellung sollten folgende Untersuchungen erfolgen: XX<br> - Mit Nachweis der o.g. wahrscheinlich pathogenen Variante im XX-Gen besteht für Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik, dies gilt insbesondere für Ihre Geschwister und Ihre Kinder (XX ab Erreichen der Volljährigkeit). Eine Terminvereinbarung ist unter der o.g. Telefonnummer möglich. Eine gezielte Diagnostik auf die o.g. Variante im XX-Gen bei Ihren Eltern haben mit ihrem Einverständnis bereits eingeleitet. Sobald die Befunde der eingeleiteten Diagnostik vorliegen, werden wir Sie kontaktieren und weiterführend Stellung nehmen.<br> Viele Ratsuchende profitieren von Angeboten verschiedener Selbsthilfegruppen. Hier können Betroffene und Eltern von Kindern mit seltenen Erkrankungen Informationen erhalten, weitergeben und eine psychosoziale Betreuung in Anspruch nehmen. Selbsthilfegruppen für Angehörige und Patient:innen mit XX sind beispielsweise unter folgenden Adressen erreichbar:XX."""
            recommendation=st.text_area("Empfehlungen", recommendation_default_text, key="recommendation_in")

    #Beurteilung#
    #############

    #Case 1 unauff, Exom+CNV+CA, Trio, Exom#
    ########################################
    if result_2=="unauffällig" and analysis_2=="Exom+CNV+CA":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"In der bisher durchgeführten genetischen Diagnostik (Chromosomenanalyse, <i>FMR1</i>-Diagnostik, Array, Panel) konnte keine Ursache für die klinische Symptomatik bei Ihrem Sohn, {Name_child_2}, nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihrem Sohn können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."
            elif child_2=="Tochter":
                beurteilung=f"In der bisher durchgeführten genetischen Diagnostik (Chromosomenanalyse, <i>FMR1</i>-Diagnostik, Array, Panel) konnte keine Ursache für die klinische Symptomatik bei Ihrer Tochter, {Name_child_2}, nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihre Tochter können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."
        elif person_2=="Erwachsen":
            beurteilung=f"In der bisher durchgeführten genetischen Diagnostik (Chromosomenanalyse, <i>FMR1</i>-Diagnostik, Array, Panel) konnte keine Ursache für die klinische Symptomatik bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."

    elif result_2=="unauffällig" and analysis_2=="Trio":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"In der bisher durchgeführten genetischen Diagnostik (Chromosomenanalyse, <i>FMR1</i>-Diagnostik, Array, Panel, Trio-Exom Analyse XX) konnte keine Ursache für die klinische Symptomatik bei Ihrem Sohn, {Name_child_2}, nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihrem Sohn können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."
            elif child_2=="Tochter":
                beurteilung=f"In der bisher durchgeführten genetischen Diagnostik (Chromosomenanalyse, <i>FMR1</i>-Diagnostik, Array, Panel, Trio-Exom Analyse XX) konnte keine Ursache für die klinische Symptomatik bei Ihrer Tochter, {Name_child_2}, nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihre Tochter können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."
        elif person_2=="Erwachsen":
            beurteilung=f"In der bisher durchgeführten genetischen Diagnostik (Chromosomenanalyse, <i>FMR1</i>-Diagnostik, Array, Panel, Trio-Exom Analyse XX) konnte keine Ursache für die klinische Symptomatik bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."

    elif result_2=="unauffällig" and analysis_2=="Exom":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"In der bisher durchgeführten genetischen Diagnostik konnte keine Ursache für die klinische Symptomatik bei Ihrem Sohn, {Name_child_2}, nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihrem Sohn können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."
            elif child_2=="Tochter":
                beurteilung=f"In der bisher durchgeführten genetischen Diagnostik konnte keine Ursache für die klinische Symptomatik bei Ihrer Tochter, {Name_child_2}, nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihre Tochter können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."
        elif person_2=="Erwachsen":
            beurteilung=f"In der bisher durchgeführten genetischen Diagnostik konnte keine Ursache für die klinische Symptomatik bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."

    #Case 2 unauff, Cancer Panel#
    #############################
    elif result_2=="unauffällig" and analysis_2=="Cancer Panel": 
        if disease_2=="HNPCC":
            beurteilung="""Bei Ihnen besteht der Verdacht auf eine genetisch bedingte Darmkrebserkrankung. Die Bethesda-Kriterien sind erfüllt. Die molekularpathologischen und immunhistochemischen Untersuchungen am Tumormaterial von Ihnen ergaben unauffällige Befunde.// Die molekularpathologische Untersuchung am Tumormaterial bezüglich der Mikrosatelliten ergab keinen Hinweis auf eine Mikrosatelliteninstabilität. In der durchgeführten genetischen Diagnostik konnte keine Ursache für die klinische Symptomatik bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen.<br><br> Bei Ihnen besteht der Verdacht auf eine genetisch bedingte Darmkrebserkrankung/HNPCC-Syndrom. Die Bethesda-Kriterien sind erfüllt. Die molekularpathologischen Untersuchungen am Tumormaterial ergaben eine Mikrosatelliteninstabilität. Die immunhistochemischen Untersuchungen ergaben einen Verlust der Kernexpression für PMS-2 und MLH-1. Eine Ursache hierfür konnte in den molekularpathologischen Untersuchungen (BRAF, MLH1-Promotor-Methylierung) nicht nachgewiesen werden. Aus diesem Grund führten wir bei Ihnen eine molekulargenetische Paneldiagnostik in den für ein Lynch-Syndrom ursächlichen Genen durch. Hierbei konnte keine Ursache für die Tumorerkrankung bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Es bleibt die Möglichkeit, dass die Tumorerkrankung:<br>- durch eine Variante verursacht wurden, die mit den angewandten Untersuchungsverfahren nicht nachgewiesen werden konnte,<br>- durch eine Veränderung in einem anderen (bislang unbekannten) Gen verursacht wurden,<br>- nicht auf eine einzelne erbliche Ursache zurückzuführen sind.<br><br>Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen.<br><br>Bei Ihnen wurde ein Endometriumkarzinom diagnostiziert. Klinisch ergaben sich keine Hinweise auf ein Lynch-Syndrom, da die Bethesda- und die Amsterdam-Kriterien nicht erfüllt sind. In der molekularpathologischen Untersuchung des Endometriumkarzinoms konnte ein Ausfall der Mismatch-Repair-Proteine MLH-1 und PMS-2 und eine Mikrosatelliteninstabilität nachgewiesen werden. Als Ursache hierfür konnte eine somatische MLH1-Promotormethylierung molekularpathologisch nachgewiesen werden. Es ist somit mit einer hohen Wahrscheinlichkeit von einer sporadischen Genese des Endometriumkarzinoms auszugehen. Eine weiterführende genetische Diagnostik ist somit bei Ihnen nicht indiziert."""
        elif disease_2=="unspezifisch":
            beurteilung=f"In der bisher durchgeführten genetischen Diagnostik konnte keine Ursache für die klinische Symptomatik / Krebserkrankung XX bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."

    #Case 3 unauff, gezielt#
    ########################
    elif result_2=="unauffällig" and analysis_2=="gezielt":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"Bei Ihrem Sohn, {Name_child_2}, konnte die familiär bekannte pathogene XX-Variante nicht nachgewiesen werden. Eine XX auf Grundlage dieser Variante konnte somit bei ihm ausgeschlossen werden."
            elif child_2=="Tochter":
                beurteilung=f"Bei Ihrer Tochter, {Name_child_2}, konnte die familiär bekannte pathogene XX-Variante nicht nachgewiesen werden. Eine XX auf Grundlage dieser Variante konnte somit bei ihr ausgeschlossen werden."
        elif person_2=="Erwachsen":
            if Titel_2=="Herr":
                beurteilung=f"Bei Ihnen konnte die familiär bekannte pathogene XX-Variante/Repeat Expansion XX im XX-Gen nicht nachgewiesen werden. Eine XX auf Grundlage dieser Variante konnte somit bei Ihnen ausgeschlossen werden. <br>// Bei Ihnen konnte keine klinisch relevante Variante im XX-Gen nachgewiesen werden. Eine Anlageträgerschaft für XX kann damit weitgehend ausgeschlossen werden. Es besteht somit kein erhöhtes Risiko für XX bei einem gemeinsamen Kind mit Ihrer Partnerin."
            elif Titel_2=="Frau":
                beurteilung=f"Bei Ihnen konnte die familiär bekannte pathogene XX-Variante/Repeat Expansion XX im XX-Gen  nicht nachgewiesen werden. Eine XX auf Grundlage dieser Variante konnte somit bei Ihnen ausgeschlossen werden. <br>    // Bei Ihnen konnte keine klinisch relevante Variante im XX-Gen nachgewiesen werden. Eine Anlageträgerschaft für XX kann damit weitgehend ausgeschlossen werden. Es besteht somit kein erhöhtes Risiko für XX bei einem gemeinsamen Kind mit Ihrem Partner."
            elif Titel_2=="Familie":
                beurteilung=f"Bei Ihnen konnte die familiär bekannte pathogene XX-Variante/Repeat Expansion XX im XX-Gen  nicht nachgewiesen werden. Eine XX auf Grundlage dieser Variante konnte somit bei Ihnen ausgeschlossen werden. <br>// Bei Ihnen konnte keine klinisch relevante Variante im XX-Gen nachgewiesen werden. Eine Anlageträgerschaft für XX kann damit weitgehend ausgeschlossen werden. Es besteht somit kein erhöhtes Risiko für XX bei einem gemeinsamen Kind mit Ihrem Partner/Ihrer Partnerin."

    #Case 4 unauff, Repeat Expansion#
    #################################
    elif result_2=="unauffällig" and analysis_2=="Repeat Expansion":
        if disease_2=="HTT":
            beurteilung="""Bei Ihnen konnte eine Repeatexpansion im <i>HTT</i>-Gen nicht nachgewiesen werden. Eine Huntington-Erkrankung konnte somit ausgeschlossen werden.<br> In der bisher durchgeführten genetischen Diagnostik (<i>HTT</i>-Repeat-Expansion, Exom Diagnostik) konnte keine Ursache für die klinische Symptomatik bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Eine weiterführende molekulargenetische Diagnostik im Hinblick Huntington-like Erkrankungen haben wir in die Wege geleitet. Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen. <br> <br> // Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik.)"""
        elif disease_2=="SCA":
            beurteilung="""In der durchgeführten genetischen Diagnostik konnte keine Ursache für die klinische Symptomatik bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen.
Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."""
        elif disease_2=="unspezifisch":
            beurteilung="""In der durchgeführten genetischen Diagnostik konnte keine Ursache für die klinische Symptomatik bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen.
Wir empfehlen eine Wiedervorstellung in unserer genetischen Sprechstunde in zwei Jahren zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."""

    #Case 5 unauff, CA#
    ###################
    elif result_2=="unauffällig" and analysis_2=="CA":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"In der konventionellen Chromosomenanalyse konnte keine Ursache für die klinische Symptomatik bei Ihrem Sohn, {Name_child_2}, nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihrem Sohn können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Eine weiterführende molekulargenetische Diagnostik im XX haben wir in die Wege geleitet. Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."
            elif child_2=="Tochter":
                beurteilung=f"In der bisher durchgeführten genetischen Diagnostik konnte keine Ursache für die klinische Symptomatik bei Ihrer Tochter, {Name_child_2}, nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihre Tochter können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Eine weiterführende molekulargenetische Diagnostik im XX haben wir in die Wege geleitet. Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."
        elif person_2=="Erwachsen":
            if disease_2=="unspezifisch":
                beurteilung=f"In der bisher durchgeführten genetischen Diagnostik konnte keine Ursache für die klinische Symptomatik bei Ihnen nachgewiesen werden. Ein grundsätzlicher Ausschluss einer genetischen Ursache ist allerdings nicht möglich. Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Eine weiterführende molekulargenetische Diagnostik im XX haben wir in die Wege geleitet. Sobald der Befund der genetischen Diagnostik vorliegt, werden wir Sie informieren und weiterführend Stellung nehmen."
            elif disease_2=="Geschlechtsinkongruenz":
                beurteilung="""In den durchgeführten genetischen Untersuchungen konnte keine genetische Ursache für die abweichende Geschlechtsidentifikation nachgewiesen werden. Ihr genetisches Geschlecht ist weiblich/männlich. Dies erlaubt jedoch keine Aussage über die von Ihnen empfundene Geschlechtszugehörigkeit."""

    #Case 6 VUS, Exom+CNV+CA, Trio, Exom#
    #####################################
    elif result_2=="VUS" and analysis_2=="Exom+CNV+CA":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"Bei Ihrem Sohn,{Name_child_2} wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen. Die XX-Variante war bei Ihnen, Herr/Frau {Name}, ebenfalls nachweisbar. Das bedeutet diese XX-Variante wurde paternal/maternal vererbt. Aufgrund der guten Übereinstimmung des klinischen Phänotyps gehen wir eher von einer Ursächlichkeit der nachgewiesenen Variante aus. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."
            elif child_2=="Tochter":
                beurteilung=f"Bei Ihrer Tochter,{Name_child_2} wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen. Die XX-Variante war bei Ihnen, Herr/Frau {Name}, ebenfalls nachweisbar. Das bedeutet diese XX-Variante wurde paternal/maternal vererbt. Aufgrund der guten Übereinstimmung des klinischen Phänotyps gehen wir eher von einer Ursächlichkeit der nachgewiesenen Variante aus. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."
        elif person_2=="Erwachsen":
            beurteilung="""Bei Ihnen wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen (Befund vom XX). Bei einer VUS kann zum aktuellen Zeitpunkt nicht endgültig entschieden werden, ob es sich um eine benigne/ neutrale bzw. krankheitsverursachende genetische Veränderung handelt. Aufgrund o.g. Variante unklarer Signifikanz im XX-Gen ist das Vorliegen einer XX-Erkrankung bei Ihnen möglich. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."""

    elif result_2=="VUS" and analysis_2=="Exom":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"Bei Ihrem Sohn,{Name_child_2} wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen. Die XX-Variante war bei Ihnen, Herr/Frau {Name}, ebenfalls nachweisbar. Das bedeutet diese XX-Variante wurde paternal/maternal vererbt. Aufgrund der guten Übereinstimmung des klinischen Phänotyps gehen wir eher von einer Ursächlichkeit der nachgewiesenen Variante aus. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."
            elif child_2=="Tochter":
                beurteilung=f"Bei Ihrer Tochter,{Name_child_2} wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen. Die XX-Variante war bei Ihnen, Herr/Frau {Name}, ebenfalls nachweisbar. Das bedeutet diese XX-Variante wurde paternal/maternal vererbt. Aufgrund der guten Übereinstimmung des klinischen Phänotyps gehen wir eher von einer Ursächlichkeit der nachgewiesenen Variante aus. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."
        elif person_2=="Erwachsen":
            beurteilung="""Bei Ihnen wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen (Befund vom XX). Bei einer VUS kann zum aktuellen Zeitpunkt nicht endgültig entschieden werden, ob es sich um eine benigne/ neutrale bzw. krankheitsverursachende genetische Veränderung handelt. Aufgrund o.g. Variante unklarer Signifikanz im XX-Gen ist das Vorliegen einer XX-Erkrankung bei Ihnen möglich. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."""

    elif result_2=="VUS" and analysis_2=="Trio":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"Bei Ihrem Sohn,{Name_child_2} wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen. Die XX-Variante war bei Ihnen, Herr/Frau {Name}, ebenfalls nachweisbar. Das bedeutet diese XX-Variante wurde paternal/maternal vererbt. Aufgrund der guten Übereinstimmung des klinischen Phänotyps gehen wir eher von einer Ursächlichkeit der nachgewiesenen Variante aus. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."
            elif child_2=="Tochter":
                beurteilung=f"Bei Ihrer Tochter,{Name_child_2} wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen. Die XX-Variante war bei Ihnen, Herr/Frau {Name}, ebenfalls nachweisbar. Das bedeutet diese XX-Variante wurde paternal/maternal vererbt. Aufgrund der guten Übereinstimmung des klinischen Phänotyps gehen wir eher von einer Ursächlichkeit der nachgewiesenen Variante aus. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."
        elif person_2=="Erwachsen":
            beurteilung="""Bei Ihnen wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen (Befund vom XX). Bei einer VUS kann zum aktuellen Zeitpunkt nicht endgültig entschieden werden, ob es sich um eine benigne/ neutrale bzw. krankheitsverursachende genetische Veränderung handelt. Aufgrund o.g. Variante unklarer Signifikanz im XX-Gen ist das Vorliegen einer XX-Erkrankung bei Ihnen möglich. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."""

    #Case 7 VUS, Cancer Panel#
    ##########################
    elif result_2=="VUS" and analysis_2=="Cancer Panel":
        if disease_2=="unspezifisch":
            beurteilung="""Bei Ihnen wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen (Befund vom XX). Bei einer VUS kann zum aktuellen Zeitpunkt nicht endgültig entschieden werden, ob es sich um eine benigne/ neutrale bzw. krankheitsverursachende genetische Veränderung handelt. Aufgrund o.g. Variante unklarer Signifikanz im XX-Gen ist das Vorliegen einer XX-Erkrankung bei Ihnen möglich. Eine abschließende Beurteilung zur klinischen Relevanz der nachgewiesenen Variante ist derzeit nicht möglich. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."""
        elif disease_2=="HNPCC":
            beurteilung="""Bei Ihnen wurde die o.g. Variante unklarer Signifikanz (VUS) im XX-Gen nachgewiesen (Befund vom XX). Bei einer VUS kann zum aktuellen Zeitpunkt nicht endgültig entschieden werden, ob es sich um eine benigne/ neutrale bzw. krankheitsverursachende genetische Veränderung handelt. Aufgrund o.g. Variante unklarer Signifikanz im XX-Gen ist das Vorliegen eines XX-assoziierten Lynch-Syndroms bei Ihnen möglich.<br> Aufgrund der noch ungeklärten Ursache der Symptomatik bei Ihnen können wir keine sicheren Aussagen bezüglich des weiteren Verlaufs der Symptomatik bzw. im Hinblick auf ein mögliches Wiederholungsrisiko in der Familie treffen. Eine gezielte, prädiktive Diagnostik für weitere Familienangehörige ist bei einer Variante unklarer Signifikanz nicht möglich."""

    #Case 8 auff, Exom+CNV+CA, Trio, Exom#
    ######################################
    elif result_2=="auffällig" and analysis_2=="Exom+CNV+CA":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"Bei Ihrem Sohn, {Name_child_2}, wurde die o.g. wahrscheinlich/pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Die XX-Variante war bei Ihnen, Frau {Name_2}, sowie Herr {Name_2} nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Variante bei Ihrem Sohn aus. Der seltene Fall eines Keimzellmosaiks (Vorliegen der Variante in einem Anteil der Ei- oder Samenzellen) bei Ihnen mit einem geringen Wiederholungsrisiko (ca. 1 %) für weitere Kinder ist nicht auszuschließen.<br>//Bei Ihnen, Herr und Frau {Name_2}, wurde jeweils eine der o.g. pathogenen XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihnen, Herr und Frau {Name_2}, konnte bei Ihrem Sohn die Compound-Heterozygotie und somit das Vorliegen einer XX nachgewiesen werden."
            elif child_2=="Tochter":
                beurteilung=f"Bei Ihrer Tochter,{Name_child_2}, wurde die o.g. wahrscheinlich/pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Die XX-Variante war bei Ihnen, Frau {Name_2}, sowie Herr {Name_2} nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Variante bei Ihrer Tochter aus. Der seltene Fall eines Keimzellmosaiks (Vorliegen der Variante in einem Anteil der Ei- oder Samenzellen) bei Ihnen mit einem geringen Wiederholungsrisiko (ca. 1 %) für weitere Kinder ist nicht auszuschließen.<br>//Bei Ihnen, Herr und Frau {Name_2}, wurde jeweils eine der o.g. pathogenen  XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihnen, Herr und Frau {Name_2}, konnte bei Ihrem Sohn die Compound-Heterozygotie und somit das Vorliegen einer XX nachgewiesen werden."
        elif person_2=="Erwachsen":
            beurteilung=f"Bei Ihnen wurde die o.g. wahrscheinlich/pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Die XX-Variante war bei Ihren Eltern nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Variante bei Ihnen aus. Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich.) <br>//Bei Ihren Eltern wurde jeweils eine der o.g. pathogenen XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihren Eltern konnte bei Ihnen die Compound-Heterozygotie und somit das Vorliegen einer XX nachgewiesen werden. Kinder von Ihnen werden mit 100%iger Wahrscheinlichkeit eine der beiden o.g. Varianten im XX-Gen von Ihnen erben. Die Abschätzung des Wiederholungsrisikos für Ihre Kinder ist abhängig davon, ob Ihre Partnerin/Ihr Partner Anlageträgerin/Anlageträger für eine XX ist."

    elif result_2=="auffällig" and analysis_2=="Exom":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"Bei Ihrem Sohn, {Name_child_2}, wurde die o.g. wahrscheinlich/pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Die XX-Variante war bei Ihnen, Frau {Name_2}, sowie Herr {Name_2} nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Variante bei Ihrem Sohn aus. Der seltene Fall eines Keimzellmosaiks (Vorliegen der Variante in einem Anteil der Ei- oder Samenzellen) bei Ihnen mit einem geringen Wiederholungsrisiko (ca. 1 %) für weitere Kinder ist nicht auszuschließen.<br>//Bei Ihnen, Herr und Frau {Name_2}, wurde jeweils eine der o.g. pathogenen XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihnen, Herr und Frau {Name_2}, konnte bei Ihrem Sohn die Compound-Heterozygotie und somit das Vorliegen einer XX nachgewiesen werden."
            elif child_2=="Tochter":
                beurteilung=f"Bei Ihrer Tochter, {Name_child_2}, wurde die o.g. wahrscheinlich/pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Die XX-Variante war bei Ihnen, Frau {Name_2}, sowie Herr {Name_2} nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Variante bei Ihrer Tochter aus. Der seltene Fall eines Keimzellmosaiks (Vorliegen der Variante in einem Anteil der Ei- oder Samenzellen) bei Ihnen mit einem geringen Wiederholungsrisiko (ca. 1 %) für weitere Kinder ist nicht auszuschließen.<br>//Bei Ihnen, Herr und Frau {Name_2}, wurde jeweils eine der o.g. pathogenen  XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihnen, Herr und Frau {Name_2}, konnte bei Ihrem Sohn die Compound-Heterozygotie und somit das Vorliegen einer XX nachgewiesen werden."
        elif person_2=="Erwachsen":
            beurteilung="""Bei Ihnen wurde die o.g. pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich.)<br> Unter Annahme der Compound-Heterozygotie konnte somit eine XX molekulargenetisch nachgewiesen werden. / Bei Ihnen wurden die o.g. pathogenen XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihren Eltern konnte bei Ihnen die Compound-Heterozygotie und somit das Vorliegen eine XX nachgewiesen werden. Kinder von Ihnen werden mit 100%iger Wahrscheinlichkeit eine der beiden o.g. Varianten im XX-Gen von Ihnen erben. Die Abschätzung des Wiederholungsrisikos für Ihre Kinder ist abhängig davon, ob Ihre Partnerin/Ihr Partner Anlageträgerin/Anlageträger für eine XX ist."""

    elif result_2=="auffällig" and analysis_2=="Trio":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"Bei Ihrem Sohn,{Name_child_2}, wurde die o.g. wahrscheinlich/pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Die XX-Variante war bei Ihnen, Frau {Name_2}, sowie Herr {Name_2} nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Variante bei Ihrem Sohn aus. Der seltene Fall eines Keimzellmosaiks (Vorliegen der Variante in einem Anteil der Ei- oder Samenzellen) bei Ihnen mit einem geringen Wiederholungsrisiko (ca. 1 %) für weitere Kinder ist nicht auszuschließen.<br>//Bei Ihnen, Herr und Frau {Name_2}, wurde jeweils eine der o.g. pathogenen XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihnen, Herr und Frau {Name_2}, konnte bei Ihrem Sohn die Compound-Heterozygotie und somit das Vorliegen einer XX nachgewiesen werden."
            elif child_2=="Tochter":
                beurteilung=f"Bei Ihrer Tochter,{Name_child_2}, wurde die o.g. wahrscheinlich/pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Die XX-Variante war bei Ihnen, Frau {Name_2}, sowie Herr {Name_2} nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Variante bei Ihrer Tochter aus. Der seltene Fall eines Keimzellmosaiks (Vorliegen der Variante in einem Anteil der Ei- oder Samenzellen) bei Ihnen mit einem geringen Wiederholungsrisiko (ca. 1 %) für weitere Kinder ist nicht auszuschließen.<br>//Bei Ihnen, Herr und Frau {Name_2}, wurde jeweils eine der o.g. pathogenen  XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihnen, Herr und Frau {Name_2}, konnte bei Ihrem Sohn die Compound-Heterozygotie und somit das Vorliegen einer XX nachgewiesen werden."
        elif person_2=="Erwachsen":
            beurteilung=f"Bei Ihnen wurde die o.g. wahrscheinlich/pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Die XX-Variante war bei Ihren Eltern nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Variante bei Ihnen aus. Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich.) <br>//Bei Ihren Eltern wurde jeweils eine der o.g. pathogenen XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihren Eltern konnte bei Ihnen die Compound-Heterozygotie und somit das Vorliegen einer XX nachgewiesen werden. Kinder von Ihnen werden mit 100%iger Wahrscheinlichkeit eine der beiden o.g. Varianten im XX-Gen von Ihnen erben. Die Abschätzung des Wiederholungsrisikos für Ihre Kinder ist abhängig davon, ob Ihre Partnerin/Ihr Partner Anlageträgerin/Anlageträger für eine XX ist."

    #Case 8 auff, gezielt#
    ######################
    elif result_2=="auffällig" and analysis_2=="gezielt":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"Bei Ihrem Sohn,{Name_child_2}, wurde die familiär bekannte wahrscheinlich/pathogene XX-Variante nachgewiesen und somit eine XX molekulargenetisch bestätigt. Für Kinder von Ihrem Sohn besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich.<br> // Mit dem Nachweis der o.g. wahrscheinlich pathogenen Variante im XX-Gen besteht bei Ihrem Sohn eine Anlageträgerschaft für eine XX. Das Krankheitsbild folgt einem autosomal rezessiven Erbgang. Heterozygote Anlageträger\*Innen zeigen daher in der Regel keine Zeichen der Erkrankung. Das Wiederholungsrisiko für zukünftige Kinder von Ihrem Sohn, an einer XX zu erkranken, ist abhängig von einer möglichen Anlageträgerschaft bei der Partnerin. Soll seine Partnerin Anlageträgerin für XX sein, besteht ein 25%iges Risiko für zukünftige Kinder des Paares, an einer XX zu erkranken.)"
            elif child_2=="Tochter":
                beurteilung=f"Bei Ihrer Tochter,{Name_child_2}, wurde die familiär bekannte wahrscheinlich/pathogene XX-Variante nachgewiesen und somit eine XX molekulargenetisch bestätigt. Für Kinder von Ihrer Tochter besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich.<br> // Mit dem Nachweis der o.g. wahrscheinlich pathogenen Variante im XX-Gen besteht bei Ihrer Tochter eine Anlageträgerschaft für eine XX. Das Krankheitsbild folgt einem autosomal rezessiven Erbgang. Heterozygote Anlageträger\*Innen zeigen daher in der Regel keine Zeichen der Erkrankung. Das Wiederholungsrisiko für zukünftige Kinder von Ihrer Tochter, an einer XX zu erkranken, ist abhängig von einer möglichen Anlageträgerschaft beim Partner. Soll ihr Partner Anlageträger für XX sein, besteht ein 25%iges Risiko für zukünftige Kinder des Paares, an einer XX zu erkranken.)"
        elif person_2=="Erwachsen":
            if Titel_2=="Herr":
                beurteilung="""Bei Ihnen wurde die familiär bekannte wahrscheinlich/pathogene XX-Variante nachgewiesen und somit eine XX molekulargenetisch bestätigt. Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich. // Mit dem Nachweis der o.g. wahrscheinlich pathogenen Variante im XX-Gen besteht bei Ihnen eine Anlageträgerschaft für eine XX. Das Krankheitsbild folgt einem autosomal rezessiven Erbgang. Heterozygote Anlageträger\*Innen zeigen daher in der Regel keine Zeichen der Erkrankung. Das Wiederholungsrisiko für zukünftige Kinder von Ihnen, an einer XX zu erkranken, ist abhängig von einer möglichen Anlageträgerschaft bei der Partnerin. Soll Ihre Partnerin Anlageträgerin für XX sein, besteht ein 25%iges Risiko für zukünftige Kinder von Ihnen, an einer XX zu erkranken.)"""
            if Titel_2=="Frau":
                beurteilung="""Bei Ihnen wurde die familiär bekannte wahrscheinlich/pathogene XX-Variante nachgewiesen und somit eine XX molekulargenetisch bestätigt. Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich. // Mit dem Nachweis der o.g. wahrscheinlich pathogenen Variante im XX-Gen besteht bei Ihnen eine Anlageträgerschaft für eine XX. Das Krankheitsbild folgt einem autosomal rezessiven Erbgang. Heterozygote Anlageträger\*Innen zeigen daher in der Regel keine Zeichen der Erkrankung. Das Wiederholungsrisiko für zukünftige Kinder von Ihnen, an einer XX zu erkranken, ist abhängig von einer möglichen Anlageträgerschaft beim Partner. Soll Ihr Partner Anlageträger für XX sein, besteht ein 25%iges Risiko für zukünftige Kinder von Ihnen, an einer XX zu erkranken.)"""
            if Titel_2=="Familie":
                beurteilung="""Bei Ihnen wurde die familiär bekannte wahrscheinlich/pathogene XX-Variante nachgewiesen und somit eine XX molekulargenetisch bestätigt. Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich. // Mit dem Nachweis der o.g. wahrscheinlich pathogenen Variante im XX-Gen besteht bei Ihnen eine Anlageträgerschaft für eine XX. Das Krankheitsbild folgt einem autosomal rezessiven Erbgang. Heterozygote Anlageträger\*Innen zeigen daher in der Regel keine Zeichen der Erkrankung. Das Wiederholungsrisiko für zukünftige Kinder von Ihnen, an einer XX zu erkranken, ist abhängig von einer möglichen Anlageträgerschaft bei der Partnerin/ beim Partner. Soll Ihre Partnerin/Ihr Partner Anlageträger/Anlageträgerin für XX sein, besteht ein 25%iges Risiko für zukünftige Kinder von Ihnen, an einer XX zu erkranken.)"""

    #Case 9 auff, Cancer Panel#
    ###########################
    elif result_2=="auffällig" and analysis_2=="Cancer Panel":
        if disease_2=="HNPCC":
            gene_HNPCC = st.selectbox("Gen", ["MLH1", "MSH2", "MSH6", "PMS2", "EPCAM"], key="gene_HNPCC_2") # depending on gene different risks
            if gene_HNPCC=="MLH1":
                if Titel_2=="Herr": 
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>MLH1</i>-Variante und somit ein <i>MLH1</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht: Dickdarm (53%), Magen/Dünndarm (16%), Ureter/Niere (4%), Harnblase (5%), Prostata (7%), Gehirn (1%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>MLH1</i>-Gen ebenfalls zu erben und ein <i>MLH1</i>-assoziiertes Lynch-Syndrom auszubilden."""
                elif Titel_2=="Frau":
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>MLH1</i>-Variante und somit ein <i>MLH1</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht: Dickdarm (44%), Endometrium (35%), Eierstock (11%), Magen/Dünndarm (8%), Ureter/Niere (3%), Harnblase (3%), Gehirn (2%), Brust (11%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>MLH1</i>-Gen ebenfalls zu erben und ein <i>MLH1</i>-assoziiertes Lynch-Syndrom auszubilden."""
                elif Titel_2=="Familie":
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>MLH1</i>-Variante und somit ein <i>MLH1</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht:<br>  - MLH1 (female): Dickdarm (44%), Endometrium (35%), Eierstock (11%), Magen/Dünndarm (8%), Ureter/Niere (3%), Harnblase (3%), Gehirn (2%), Brust (11%)<br> - MLH1 (male): Dickdarm (53%), Magen/Dünndarm (16%), Ureter/Niere (4%), Harnblase (5%), Prostata (7%), Gehirn (1%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>MLH1</i>-Gen ebenfalls zu erben und ein <i>MLH1</i>-assoziiertes Lynch-Syndrom auszubilden."""

            elif gene_HNPCC=="MSH2":
                if Titel_2=="Herr": 
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>MSH2</i>-Variante und somit ein <i>MSH2</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht: Dickdarm (46%), Magen/Dünndarm (16%), Ureter/Niere (16%), Harnblase (9%), Prostata (16%), Gehirn (4%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>MSH2</i>-Gen ebenfalls zu erben und ein <i>MSH2</i>-assoziiertes Lynch-Syndrom auszubilden."""
                elif Titel_2=="Frau":
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>MSH2</i>-Variante und somit ein <i>MSH2</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht: Dickdarm (42%), Endometrium (46%), Eierstock (17%), Magen/Dünndarm (10%), Ureter/Niere (13%), Harnblase (7%), Gehirn (2%), Brust (13%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im  <i>MSH2</i>-Gen ebenfalls zu erben und ein <i>MSH2</i>-assoziiertes Lynch-Syndrom auszubilden."""
                elif Titel_2=="Familie":
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>MSH2</i>-Variante und somit ein <i>MSH2</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht:<br>  - MSH2(female): Dickdarm (42%), Endometrium (46%), Eierstock (17%), Magen/Dünndarm (10%), Ureter/Niere (13%), Harnblase (7%), Gehirn (2%), Brust (13%)<br> - MSH2(male): Dickdarm (46%), Magen/Dünndarm (16%), Ureter/Niere (16%), Harnblase (9%), Prostata (16%), Gehirn (4%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>MSH2</i>-Gen ebenfalls zu erben und ein  <i>MSH2</i>-assoziiertes Lynch-Syndrom auszubilden."""

            elif gene_HNPCC=="MSH6":
                if Titel_2=="Herr": 
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>MSH6</i>-Variante und somit ein <i>MSH6</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht: Dickdarm (12%), Magen/Dünndarm (4%), Ureter/Niere (2%), Harnblase (4%), Prostata (5%), Gehirn (2%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>MSH6</i>-Gen ebenfalls zu erben und ein <i>MSH6</i>-assoziiertes Lynch-Syndrom auszubilden."""
                elif Titel_2=="Frau":
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>MSH6</i>-Variante und somit ein <i>MSH6</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht: Dickdarm (20%), Endometrium (41%), Eierstock (11%), Magen/Dünndarm (2%), Ureter/Niere (6%), Harnblase (1%), Gehirn (1%), Brust (11%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>MSH6</i>-Gen ebenfalls zu erben und ein <i>MSH6</i>-assoziiertes Lynch-Syndrom auszubilden."""
                elif Titel_2=="Familie":
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>MSH6</i>-Variante und somit ein <i>MSH6</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht:<br>  - MSH6(female): Dickdarm (20%), Endometrium (41%), Eierstock (11%), Magen/Dünndarm (2%), Ureter/Niere (6%), Harnblase (1%), Gehirn (1%), Brust (11%)<br> - MSH6(male): Dickdarm (12%), Magen/Dünndarm (4%), Ureter/Niere (2%), Harnblase (4%), Prostata (5%), Gehirn (2%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>MSH6</i>-Gen ebenfalls zu erben und ein <i>MSH6</i>-assoziiertes Lynch-Syndrom auszubilden."""

            elif gene_HNPCC=="PMS2":
                if Titel_2=="Herr": 
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>PMS2</i>-Variante und somit ein <i>PMS2</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht: Dickdarm (3%), Magen/Dünndarm (4%), Prostata (5%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>PMS2</i>-Gen ebenfalls zu erben und ein <i>PMS2</i>-assoziiertes Lynch-Syndrom auszubilden."""
                elif Titel_2!="Herr": 
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>PMS2</i>-Variante und somit ein <i>PMS2</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht: Dickdarm (3%), Endometrium (13%), Eierstock (3%), Magen/Dünndarm (4%), Prostata (5%), Brust (8%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>PMS2</i>-Gen ebenfalls zu erben und ein <i>PMS2</i>-assoziiertes Lynch-Syndrom auszubilden."""

            elif gene_HNPCC=="EPCAM":
                if Titel_2=="Herr": 
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>EPCAM</i>-Variante und somit ein <i>EPCAM</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko eine Dickdarm Tumorerkrankung erhöht (75%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>EPCAM</i>-Gen ebenfalls zu erben und ein <i>EPCAM</i>-assoziiertes Lynch-Syndrom auszubilden."""
                elif Titel_2!="Herr": 
                    beurteilung="""Bei Ihnen wurde die o.g. pathogene <i>EPCAM</i>-Variante und somit ein <i>EPCAM</i>-assoziiertes Lynch-Syndrom molekulargenetisch nachgewiesen. Damit ist bei Ihnen das Lebenszeitrisiko für folgende Tumorerkrankungen erhöht: Dickdarm (75%), Endometrium (12%) (Idos <i>et</i> Valle, GeneReviews 2021, PMID: 20301390). Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im <i>EPCAM</i>-Gen ebenfalls zu erben und ein <i>EPCAM</i>-assoziiertes Lynch-Syndrom auszubilden."""

        elif disease_2=="unspezifisch":
            beurteilung=f"Bei Ihnen wurde die o.g. wahrscheinlich/pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich.) <br>//Bei Ihren Eltern wurde jeweils eine der o.g. pathogenen XX-Varianten molekulargenetisch nachgewiesen. Mit dem Nachweis des heterozygoten Vorliegens der beiden XX-Varianten bei Ihren Eltern konnte bei Ihnen die Compound-Heterozygotie und somit das Vorliegen einer XX nachgewiesen werden. Kinder von Ihnen werden mit 100%iger Wahrscheinlichkeit eine der beiden o.g. Varianten im XX-Gen von Ihnen erben. Die Abschätzung des Wiederholungsrisikos für Ihre Kinder ist abhängig davon, ob Ihre Partnerin/Ihr Partner Anlageträgerin/Anlageträger für eine XX ist."

    #Case 10 auff, Repeat Expansion#
    ################################
    elif result_2=="auffällig" and analysis_2=="Repeat Expansion":
        if disease=="HNPCC":
            beurteilung="""Bei Ihnen wurde die o.g. Repeatverlängerung im <i>HTT</i>-Gen und somit eine Huntington-Erkrankung molekulargenetisch nachgewiesen. Für Kinder und Geschwister von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Repeatverlängerung im <i>HTT</i>-Gen ebenfalls zu tragen und eine Huntington-Erkrankung auszubilden."""
        elif disease_2=="SCA":
            beurteilung="""Bei Ihnen wurde die o.g. Repeatverlängerung im xx-Gen und somit eine SCA Typ XX molekulargenetisch nachgewiesen. Für Kinder und Geschwister von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Repeatverlängerung im XX-Gen ebenfalls zu tragen und eine SCA Typ XX auszubilden. // Bei Ihnen wurde die o.g. pathogene XX-Variante und somit eine XX molekulargenetisch nachgewiesen. Für Kinder von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Variante im XX-Gen ebenfalls zu erben und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. (Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich.)"""
        elif disease_2=="SCA":
            beurteilung="""Bei Ihnen wurde die o.g. Repeatverlängerung im xx-Gen und somit eine XX molekulargenetisch nachgewiesen. Für Kinder und Geschwister von Ihnen besteht eine 50%ige Wahrscheinlichkeit die o.g. Repeatverlängerung im XX-Gen ebenfalls zu tragen und (mit einer hohen Wahrscheinlichkeit) eine XX auszubilden. XX(Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt unvollständigen Penetranz nicht möglich.)"""

    #Case 11 auff, CA#
    ##################
    elif result_2=="auffällig" and analysis_2=="CA":
        if person_2=="Kind":
            if child_2=="Sohn":
                beurteilung=f"Bei Ihrem Sohn,{Name_child_2}, wurde die o.g. Chromosomenveränderung und somit eine XX zytogenetisch nachgewiesen. Die Chromosomenveränderung war bei Ihnen, Frau {Name_2}, sowie Herr {Name_2} nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Veränderung bei Ihrem Sohn aus. Der seltene Fall eines Keimzellmosaiks (Vorliegen der Variante in einem Anteil der Ei- oder Samenzellen) bei Ihnen mit einem geringen Wiederholungsrisiko (ca. 1 %) für weitere Kinder ist nicht auszuschließen.<br>//Bei Ihnen, Herr und Frau {Name_2}, wurde eine Chromosmentranslokation XX nachgewiesen. Mit dem Nachweis der Translokation betseht ein erhöhtes Wiederholungsrisiko (ca. XX %) für weitere Kinder und ein erhöhtes Risiko für Aborte."
            elif child_2=="Tochter":
                beurteilung=f"Bei Ihrer Tochter,{Name_child_2}, wurde die o.g. Chromosomenveränderung und somit eine XX zytogenetisch nachgewiesen. Die Chromosomenveränderung war bei Ihnen, Frau {Name_2}, sowie Herr {Name_2} nicht nachweisbar. Das bedeutet, wir gehen von einer <i>de novo</i> Genese (Neuentstehung) der Veränderung bei Ihrem Sohn aus. Der seltene Fall eines Keimzellmosaiks (Vorliegen der Variante in einem Anteil der Ei- oder Samenzellen) bei Ihnen mit einem geringen Wiederholungsrisiko (ca. 1 %) für weitere Kinder ist nicht auszuschließen.<br>//Bei Ihnen, Herr und Frau {Name_2}, wurde eine Chromosmentranslokation XX nachgewiesen. Mit dem Nachweis der Translokation betseht ein erhöhtes Wiederholungsrisiko (ca. XX %) für weitere Kinder und ein erhöhtes Risiko für Aborte."
        elif person_2=="Erwachsen":
            beurteilung=f"Bei Ihnen wurde die o.g. Chromosomenveränderung und somit eine XX zytogenetisch nachgewiesen. Mit dem Nachweis der Translokation betseht ein erhöhtes Risiko (ca. XX %) für Aborte und Chromosomenveränderungen beim Nachkommen."

    #Recommendations#
    #################

    if result_2!="auffällig" and disease_2=="HNPCC":
        recommendation ="""Wir empfehlen Ihnen im Anschluss an die Tumornachsorge eine Koloskopie alle drei bis fünf Jahre. Das Risiko eines Verwandten ersten Grades eines Patienten mit kolorektalem Karzinom, ebenfalls an einem kolorektalen Karzinom zu erkranken, ist auch ohne das Vorliegen eines erblichen Tumorsyndroms statistisch erhöht. Ihren Eltern als erstgradig Angehörige empfehlen wir gemäß S3-Leitlinie Kolorektales Karzinom ebenfalls eine Koloskopie, bestenfalls im Rahmen der Regelvorsorge für Darmkrebs.<br> <br>// Verwandte ersten Grades (Eltern, Kinder und Geschwister) von Patienten mit kolorektalem Karzinom sollten in einem Lebensalter, das 10 Jahre vor dem Alterszeitpunkt des Auftretens des Karzinoms beim Indexpatienten liegt, erstmals komplett koloskopiert werden (spätestens im Alter von 40–⁠45 Jahren, S3-Leitlinie Kolorektales Karzinom).
Sollten im Verlauf Sie oder weitere Familienmitglieder an weiteren Krebserkrankungen erkranken, empfehlen wir eine Wiedervorstellung in unserer genetischen Sprechstunde zur Re-Evaluation und ggf. Einleitung einer weiterführenden genetischen Diagnostik."""
        
    elif result_2=="auffällig" and disease_2=="HNPCC":
        recommendation="""Nach der aktuellen Leitlinie empfehlen wir Ihnen auf Grundlage des molekulargenetisch nachgewiesenen Lynch-Syndroms folgende Vorsorgeuntersuchungen bezüglich des Risikos für ein kolorektales Karzinom, ein Magenkarzinom und ein Endometriumkarzinom (S3-Leitlinie Kolorektales Karzinom. 2019):<br> - Jährliche Koloskopie ab dem 25. Lebensjahr<br> - Regelmäßige Ösophagogastroduodenoskopie ab dem 35. Lebensjahr<br> - Jährlicher vaginaler Ultraschall ab dem 25. Lebensjahr<br> - Jährliche Endometriumbiopsie mit Pipelle-Methode ab dem 35. Lebensjahr<br> - Es besteht die Möglichkeit einer prophylaktischen Hyster- und Ovarektomie bei abgeschlossener Familienplanung ab dem 40. Lebensjahr (oder fünf Jahre vor dem frühesten Erkrankungsalter)<br><br> Das Risiko für die weiteren assoziierten Tumorerkrankungen ist im Vergleich zur Allgemeinbevölkerung geringer erhöht. Aus diesem Grund empfehlen wir Ihnen die Teilnahme an den allgemeinen gültigen Früherkennungsmaßnahmen der Regelversorgung.<br> Mit Nachweis der o.g. pathogenen Variante im XX-Gen besteht für Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik bezüglich der o.g. pathogenen Variante, dies gilt insbesondere für Ihre Geschwister und Ihre Kinder (ab Erreichen der Volljährigkeit). Diese Untersuchung kann gern im Rahmen unserer genetischen Sprechstunde stattfinden. Eine Terminvereinbarung ist unter der o. g. Telefonnummer möglich."""
        
    elif result_2!="unauffällig" and disease_2=="SCA":
        recommendation ="""Wir empfehlen die Anbindung an eine spezialisierte SCA-Sprechstunde. Nach Diagnosestellung werden Maßnahmen empfohlen (Opal <i>et</i> Ashizawa, GeneReviews. 2023): <br> - unterstützende Maßnahmen, einschließlich adaptiver Hilfsmittel, Physiotherapie, Ergotherapie sowie das Vermeiden von Übergewicht;<br> - intensive Rehabilitation (koordinierte Physiotherapie) kann von Nutzen sein;<br> - Sprachtherapie und Kommunikationshilfen bei Dysarthrie;<br> - ein videobasiertes Schluckröntgen zur Identifizierung der Nahrungskonsistenz, die am wenigsten wahrscheinlich Aspiration auslöst, sowie Ernährungshilfsmittel bei wiederholter Aspiration;<br> - kalorische Unterstützung bei Gewichtsverlust, Vitaminzusätze nach Bedarf;<br> - Psychotherapie, neuropsychologische Rehabilitation und/oder standardmäßige psychiatrische Behandlungen bei kognitiven und psychiatrischen Erscheinungen;<br> - bei Bedarf Pharmakotherapie und/oder Überweisung zur Schmerztherapie.<br><br> Wir empfehlen eine neurologische Beurteilung auf das Fortschreiten der Ataxie und physiatrische, ergotherapeutische sowie physiotherapeutische Beurteilung hinsichtlich Mobilität und Selbsthilfefähigkeiten, kognitive Funktion.Weiterhin empfehlen wir kontinuierliche neurologische Betreeung.<br><br> Substanzen/Umstände zu vermeiden: Alkohol, Medikamente, die bekanntermaßen Nervenschäden verursachen können (z. B. Isoniazid, hohe Dosen Vitamin B6) und Umstände, die zu körperlichem Schaden führen könnten, wie das Bedienen von Maschinen oder das Klettern in große Höhen.<br> Mit Nachweis der o.g. Repeatverlängerung/ pathogenen Variante im XX-Gen besteht für Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik ⁠– dies gilt insbesondere für Ihre Geschwister und Ihre Kinder (ab Erreichen der Volljährigkeit). Diese Untersuchung kann gern im Rahmen unserer genetischen Sprechstunde stattfinden. Eine Terminvereinbarung ist unter der o. g. Telefonnummer möglich."""
        
    elif result_2!="unauffällig" and disease_2=="HTT":
        recommendation ="""Wir empfehlen Ihnen die weitere Betreuung durch unsere Kollegen des Fachbereichs Neurologie/Psychiatrie beziehungsweise eine Mitbetreuung an einem Huntington-Zentrum. Am Beratungstag händigten wir Ihnen eine Liste mit Huntington-Zentren und Kliniken sowie Kontaktdaten der Leipziger Selbsthilfegruppe aus.<br> Weiterhin besteht die Möglichkeit der psychologischen Mitbetreuung durch unsere Kollegen aus dem Zentrum für psychische Gesundheit. Eine Terminvereinbarung für einen Beratungstermin ist unter der Telefonnummer XX möglich.<br> Mit Nachweis der o.g. Repeatverlängerung im <i>HTT</i>-Gen besteht für Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik ⁠– dies gilt insbesondere für Ihre Geschwister und Ihre Kinder (ab Erreichen der Volljährigkeit). Diese Untersuchung kann gern im Rahmen unserer genetischen Sprechstunde stattfinden. Eine Terminvereinbarung ist unter der o. g. Telefonnummer möglich."""
    elif result_2!="unauffällig" and disease_2=="Marfan":
        recommendation = """Wir empfehlen die Anbindung an eine spezialisierte Marfan-Sprechstunde bzw. ein sozialpädiatrisches Zentrum.<br> Nach Diagnosestellung werden folgende Untersuchungen empfohlen (Dietz, GeneReviews. 2022):<br> - kardiologische Untersuchung inkl. Echokardiographie<br> - Bestimmung der Körpermaße<br> - augenärztliche Untersuchung hinsichtlich Katarakt und Glaukom<br> - körperliche Untersuchung hinsichtlich Thoraxdeformitäten, Skoliose, Hernien<br> - zahnärztliche Untersuchung<br> - bei unteren Rückenschmerzen, Beinschmerzen, Beinschwäche oder Taubheitsgefühlen neurologische Untersuchung und bildgebende Diagnostik hinsichtlich durale Ektasie<br> - bei Zyanose, Brustenge oder Dyspnoe Röntgen-Thorax hinsichtlich eines Pneumothorax<br><br> Im Verlauf werden folgende Untersuchungen empfohlen (Dietz, GeneReviews. 2022):<br> - min. jährliche kardiologische Untersuchung inkl. Echokardiographie<br> - regelmäßige Bestimmung der Körpermaße<br> - jährliche augenärztliche Untersuchung hinsichtlich Katarakt und Glaukom<br> - regelmäßige körperliche Untersuchung hinsichtlich Thoraxdeformitäten, Skoliose, Hernien<br> - jährliche zahnärztliche Untersuchung<br><br> Eine Behandlung mit Betablockern bzw. AT1-Rezeptor-Antagonisten sollte unter regelmäßiger kardiologischer Kontrolle erwogen werden. Kontaktsportarten, Coffein, Vasokonstriktoren, wie Triptane, Augenlasern (LASIK Behandlung) sollten vermieden werden.<br> Für weitere Informationen zum Krankheitsbild und die Kontaktaufnahme mit anderen Betroffenen möchten wir auf die Selbsthilfegruppe Marfan Hilfe (Deutschland) e.V. hinweisen.<br><br> Bei Kinderwunsch kann eine genetische Beratung hinsichtlich der Wiederholungswahrscheinlichkeit in Anspruch genommen werden. Diese kann gern im Rahmen unserer Sprechstunde stattfinden. Eine Terminvereinbarung ist unter der o.g. Telefonnummer möglich.<br> Mit Nachweis der o.g. pathogenen Variante im <i>FBN1</i>-Gen besteht für leibliche Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik. Diese Untersuchung kann gern im Rahmen unserer genetischen Sprechstunde stattfinden. Eine Terminvereinbarung ist unter der o. g. Telefonnummer möglich."""
    elif result_2!="unauffällig" and disease_2=="EDS-klassisch-COL5A1":
        recommendation = """Nach Diagnosestellung sollten folgende Untersuchungen erfolgen (Malfait <i>et al</i>, GeneReviews, 2018):<br> - Dermatologische Vorstellung zur Beurteilung der Hyperextensibilität der Haut, atropher Narben und Blutergüsse sowie anderer dermatologischer cEDS-Manifestationen<br> - Orthopädische Vorstellung zur Bewertung der Gelenkbeweglichkeit mit Hilfe des Beighton-Scores<br> - Kardiologische Vorstellung zur Durchführung eines Echokardiogramms mit Messung des Aortendurchmessers<br> - Gerinnungsdignostik bei leichten Blutergüssen<br><br> Im Verlauf sollten folgende Untersuchungen erfolgen (Malfait <i>et al</i>, GeneReviews, 2018):<br> - Im Falle von echokardiographischen Auffälligkeiten Wiederholung des Echokardiogramms jährlich<br><br> Eine Verbesserung der Gelenkstabilität und damit Schutz vor Verletzungen kann durch Sportarten erreicht werden, die insbesondere den Muskeltonus unterstützen. Beispiele hierfür sind Gehen, Radfahren, Aerobic mit geringer Belastung, Schwimmen oder Wassergymnastik sowie einfache Bewegungsübungen ohne zusätzlichen Widerstand. Sportarten mit starker Gelenkbelastung (Kontaktsportarten, Kampfsportarten, Fußball, Laufen) sollten eher vermieden werden.   Wir empfehlen zudem eine physiotherapeutische Behandlung zur Verbesserung der Gelenkstabilität.<br> Bei Personen mit Muskelhypotonie und Gelenkinstabilität mit chronischen Schmerzen kann Verhaltens- und Psychotherapie dabei helfen, Akzeptanz und Bewältigungsstrategien zu entwickeln. Wunden sollten spannungsfrei verschlossen werden, vorzugsweise in zwei Schichten. Tiefe Stiche sollten großzügig gesetzt werden. Hautnähte sollten doppelt so lange wie üblich belassen werden, und eine zusätzliche Fixierung der angrenzenden Haut kann helfen, eine Dehnung der Narbe zu verhindern.<br><br> Im Falle einer verlängerten Blutungszeit kann DDAVP (Deamino-Delta-D-Arginin-Vasopressin) z.B. bei Nasenbluten oder vor operativen Eingriffen eingesetzt werden. Die Einnahme von Acetylsalicylsäure (Aspirin) sollte vermieden werden.<br><br> Mit Nachweis der o.g. wahrscheinlich pathogenen Variante im <i>COL5A1</i>-Gen besteht für Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik, dies gilt insbesondere für Ihre Schwester XX. Eine Terminvereinbarung ist unter der o.g. Telefonnummer möglich. Eine gezielte Diagnostik auf die o.g. Variante im <i>COL5A1</i>-Gen bei Ihren Eltern haben mit ihrem Einverständnis bereits eingeleitet. Sobald die Befunde der eingeleiteten Diagnostik vorliegen, werden wir Sie kontaktieren und weiterführend Stellung nehmen.<br><br> Viele Ratsuchende profitieren von Angeboten verschiedener Selbsthilfegruppen. Hier können Betroffene und Eltern von Kindern mit seltenen Erkrankungen Informationen erhalten, weitergeben und eine psychosoziale Betreuung in Anspruch nehmen. Selbsthilfegruppen für Angehörige und Patient\:Innen mit Ehlers-Danlos-Syndrom sind beispielsweise unter folgenden Adressen erreichbar: https://www.ehlers-danlos-initiative.de/ oder https://www.bundesverband-eds.de/de/."""
    #elif result_2!="unauffällig" and disease=="unspezifisch":
        #recommendation_default_text="""- Nach Diagnosestellung sollten folgende Untersuchungen erfolgen: XX<br> - Mit Nachweis der o.g. wahrscheinlich pathogenen Variante im XX-Gen besteht für Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik, dies gilt insbesondere für Ihre Geschwister und Ihre Kinder (XX ab Erreichen der Volljährigkeit). Eine Terminvereinbarung ist unter der o.g. Telefonnummer möglich. Eine gezielte Diagnostik auf die o.g. Variante im XX-Gen bei Ihren Eltern haben mit ihrem Einverständnis bereits eingeleitet. Sobald die Befunde der eingeleiteten Diagnostik vorliegen, werden wir Sie kontaktieren und weiterführend Stellung nehmen.<br> Viele Ratsuchende profitieren von Angeboten verschiedener Selbsthilfegruppen. Hier können Betroffene und Eltern von Kindern mit seltenen Erkrankungen Informationen erhalten, weitergeben und eine psychosoziale Betreuung in Anspruch nehmen. Selbsthilfegruppen für Angehörige und Patient:innen mit XX sind beispielsweise unter folgenden Adressen erreichbar:XX."""
        #recommendation=st.text_area("Empfehlungen", recommendation_default_text, key="recommendation_un")
    #elif result_2!="unauffällig" and disease=="Geschlechtsinkongruenz":
        #recommendation_default_text="""NO WAY!<br> - Nach Diagnosestellung sollten folgende Untersuchungen erfolgen: XX<br> - Mit Nachweis der o.g. wahrscheinlich pathogenen Variante im XX-Gen besteht für Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik, dies gilt insbesondere für Ihre Geschwister und Ihre Kinder (XX ab Erreichen der Volljährigkeit). Eine Terminvereinbarung ist unter der o.g. Telefonnummer möglich. Eine gezielte Diagnostik auf die o.g. Variante im XX-Gen bei Ihren Eltern haben mit ihrem Einverständnis bereits eingeleitet. Sobald die Befunde der eingeleiteten Diagnostik vorliegen, werden wir Sie kontaktieren und weiterführend Stellung nehmen.<br> Viele Ratsuchende profitieren von Angeboten verschiedener Selbsthilfegruppen. Hier können Betroffene und Eltern von Kindern mit seltenen Erkrankungen Informationen erhalten, weitergeben und eine psychosoziale Betreuung in Anspruch nehmen. Selbsthilfegruppen für Angehörige und Patient:innen mit XX sind beispielsweise unter folgenden Adressen erreichbar:XX."""
        #recommendation=st.text_area("Empfehlungen", recommendation_default_text, key="recommendation_in")
    

    #Final lines
    last_line_2="""Wir hoffen, Sie mit unserem Gespräch und diesem Brief vorerst ausreichend informiert zu haben. Bei Rückfragen stehen wir gerne auch telefonisch zur Verfügung.<br><br>Mit freundlichen Grüßen,<br><br>"""

    #Signatures
    if Arzt1_2 =="Diana Le Duc":
        signature="""PD Dr. D Le Duc, MD/PhD<br><small>FÄ für Humangenetik</small>"""

    #Anhang
    anhang_2="""<small>Befund vom XX</small>"""
    
        

    
    if st.button("Arzt Brief Befundbesprechung"):
        # Display text based on the selected option
        if council_2 == "Befundbesprechung" and result_2=="unauffällig" and disease_2!="HNPCC":
            st.markdown(beratung_line_2, unsafe_allow_html=True)
            st.markdown(ergebnis, unsafe_allow_html=True)
            st.markdown(hello_line_2, unsafe_allow_html=True)
            st.markdown(first_line_2, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Genetische Diagnostik:</b></div>",  unsafe_allow_html=True)
            st.markdown(diagnostic, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Beurteilung und Empfehlungen</b></div>",  unsafe_allow_html=True)
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown(last_line_2, unsafe_allow_html=True)
            st.markdown(signature, unsafe_allow_html=True)
            st.markdown(anhang_2, unsafe_allow_html=True)
        elif council_2 == "Befundbesprechung" and result_2=="unauffällig" and disease_2=="HNPCC":
            st.markdown(beratung_line_2, unsafe_allow_html=True)
            st.markdown(ergebnis, unsafe_allow_html=True)
            st.markdown(hello_line_2, unsafe_allow_html=True)
            st.markdown(first_line_2, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Molekularpathologische Diagnostik:</b></div>",  unsafe_allow_html=True)
            st.markdown(diagnostic_patho, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Genetische Diagnostik:</b></div>",  unsafe_allow_html=True)
            st.markdown(diagnostic, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Beurteilung und Empfehlungen</b></div>",  unsafe_allow_html=True)
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown(last_line_2, unsafe_allow_html=True)
            st.markdown(signature, unsafe_allow_html=True)
            st.markdown(anhang_2, unsafe_allow_html=True)
        elif council_2 == "Befundbesprechung" and result_2!="unauffällig" and disease_2!="HNPCC":
            st.markdown(beratung_line_2, unsafe_allow_html=True)
            st.markdown(ergebnis, unsafe_allow_html=True)
            st.markdown(hello_line_2, unsafe_allow_html=True)
            st.markdown(first_line_2, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Genetische Diagnostik:</b></div>",  unsafe_allow_html=True)
            st.markdown(diagnostic, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Allgemeine Informationen zum Krankheitsbild:</b></div>",  unsafe_allow_html=True)
            st.markdown(disease_text, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Beurteilung</b></div>",  unsafe_allow_html=True)
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Empfehlung</b></div>",  unsafe_allow_html=True)
            st.markdown(recommendation, unsafe_allow_html=True)
            st.markdown(last_line_2, unsafe_allow_html=True)
            st.markdown(signature, unsafe_allow_html=True)
            st.markdown(anhang_2, unsafe_allow_html=True)
        elif council_2 == "Befundbesprechung" and result_2!="unauffällig" and disease_2=="HNPCC":
            st.markdown(beratung_line_2, unsafe_allow_html=True)
            st.markdown(ergebnis, unsafe_allow_html=True)
            st.markdown(hello_line_2, unsafe_allow_html=True)
            st.markdown(first_line_2, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Genetische Diagnostik:</b></div>",  unsafe_allow_html=True)
            st.markdown(diagnostic, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Allgemeine Informationen zum Krankheitsbild:</b></div>",  unsafe_allow_html=True)
            st.markdown(disease_text, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Beurteilung</b></div>",  unsafe_allow_html=True)
            st.markdown(beurteilung, unsafe_allow_html=True)
            st.markdown("<div class='custom-paragraph'><b>Empfehlung</b></div>",  unsafe_allow_html=True)
            st.markdown(recommendation, unsafe_allow_html=True)
            st.markdown(last_line_2, unsafe_allow_html=True)
            st.markdown(signature, unsafe_allow_html=True)
            st.markdown(anhang_2, unsafe_allow_html=True)
        
with tab3:
    ############################################################
    # Create the third tab for Schwangerschaft and Kinderwunsch#
    ############################################################

    st.markdown("<h1 style='font-size: 30px;'>Schwangerschaft und Kinderwunsch</h1>", unsafe_allow_html=True)

    # Get the current date and time#
    ################################
    current_datetime_3 = datetime.now()

    ##################
    #Get patient data#
    ##################
    
    # Create a selectbox to choose an option for the gender#
    ########################################################
    st.markdown("### Patienten Daten")
    col1, col2, col3= st.columns(3)
    Titel_3 = col1.selectbox("Titel", ["Frau", "Herr", "Familie"], key="Titel_3")        
    Vorname_3 = col2.text_input("Vorame", key="Vorname_3")
    Name_3 = col3.text_input("Name", key="Name_3")

    pregnancy=col1.text_input("Schwangerschaftswoche", key="pregnancy_3")
    delivery=col2.text_input("Errechneter Geburtstermin", key="delivery_3")
    regel=col3.text_input("Erster Tag der letzter Regel", key="regel_3")
    

    # Add a selectbox for choosing the type of counciling#
    ######################################################
    #st.markdown("### Art der Beratung und Analyse")
    col1, col2, col3= st.columns(3)
    council_3 = col1.selectbox("Art der Beratung", ["Erstberatung", "Befundbesprechung"], key="council_3")
    if council_3=="Erstberatung":
        question_3 = col2.selectbox("Fragestellung", ["SS normales Risiko", "SS erhöhtes Risiko", "SS Fehlbildung", "SS Familienanamnese auff.", "Aborte", "Kinderwunsch", "PID", "Planung Nabelschnurblut"], key="question_3")
        data_risk = {'Age': ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55"],
                'Risk': ["1:1589", "1:1587", "1:1585", "1:1582", "1:1578", "1:1572", "1:1565", "1:1556", "1:1544", "1:1528", "1:1507", "1:1481", "1:1447", "1:1404", "1:1351", "1:1286", "1:1208", "1:1119", "1:1018", "1:909", "1:796", "1:683", "1:574", "1:474", "1:384", "1:307", "1:242", "1:189", "1:146", "1:112", "1:85", "1:65", "1:49", "1:37", "1:28", "1:21", "1:15", "1:11", "1:8", "1:6", "1:4", "1:3", "1:2", "1:1", "1:"]}
        df = pd.DataFrame(data_risk)
        maternal_age_3=st.selectbox('Mütterliches Alter bei der Geburt:', df['Age'])
        risk_value = df[df['Age'] == maternal_age_3]['Risk'].values[0]
        st.write(f'Das allgemeine altersabhängige Risiko bezüglich des Auftretens einer Chromosomenveränderung, insbesondere einer Trisomie 21 (Down-Syndrom) beim Kind ist bei einem mütterlichen Alter bei der Geburt von {maternal_age_3} – {risk_value}')
    elif council_3=="Befundbesprechung":
        question_3=col2.selectbox("Analysis", ["CA", "Schnelltest + CA", "Schnelltest + CA + Trio", "Schnelltest + CA + gezielt", "NIPT"], key="analysis_3")
        result_3 = col3.selectbox("Ergebnis", ["unauffällig", "auffälliig"], key="result_3")
    
    #Start building the parts of the letter#
    ########################################
    #Beratungsgrund and Anamnese#

    if question_3=="SS normales Risiko":
        question_3_default_text=f"Aktuelle Schwangerschaft in SSW {pregnancy}, ET {delivery}"
        beratung_3 = st.text_area("Beratungsgrund", question_3_default_text)
        anamnese_3_default_text=f"Sie berichteten, dass Sie aktuell in Woche {pregnancy} schwanger sind. Der erste Tag der letzten Regel war der {regel}. Der rechnerische Entbindungstermin ist der {delivery}. Die Geburt solle am XX Klinikum stattfinden, wo Sie sich diesbezüglich am XX in der gynäkologischen und anästhesiologischen Sprechstunde vorstellten. Dem Mutterpass entnehmen wir eine unauffällige Schwangerschaft mit unauffälligem Ersttrimesterscreening/ unauffälliger Feindiagnostik am XX 17.02.2020 (Befund vom XX, Klinikum XX). Bei Ihnen, Frau {Name_3}, sowie Ihrem Partner seien keine relevanten Erkrankungen bekannt. Sie seien nicht miteinander verwandt." 
        anamnese_3 = st.text_area("Beratungsgrund", anamnese_3_default_text)
    
    elif question_3=="SS erhöhtes Risiko":
        question_3_default_text=f"1. Erhöhtes maternales altersabhängiges Risiko für eine Trisomie 21 beim Fetus<br> 2. Aktuelle Schwangerschaft in SSW {pregnancy}, ET {delivery}"
        beratung_3 = st.text_area("Beratungsgrund", question_3_default_text)
        anamnese_3_default_text=f"Sie berichteten, dass Sie aktuell in Woche {pregnancy} schwanger sind. Der erste Tag der letzten Regel war der {regel}. Der rechnerische Entbindungstermin ist der {delivery}. Die Geburt solle am XX Klinikum stattfinden, wo Sie sich diesbezüglich am XX in der gynäkologischen und anästhesiologischen Sprechstunde vorstellten. Dem Mutterpass entnehmen wir eine unauffällige Schwangerschaft mit unauffälligem Ersttrimesterscreening/ unauffälliger Feindiagnostik am XX 17.02.2020 (Befund vom XX, Klinikum XX). Bei Ihnen, Frau {Name_3}, sowie Ihrem Partner seien keine relevanten Erkrankungen bekannt. Sie seien nicht miteinander verwandt." 
        anamnese_3 = st.text_area("Beratungsgrund", anamnese_3_default_text)
    
    elif question_3=="SS Fehlbildung":
        question_3_default_text=f"1. V.a. eine genetisch bedingte Fehlbildung beim Fetus<br> 2. Aktuelle Schwangerschaft in SSW {pregnancy}, ET {delivery}"
        beratung_3 = st.text_area("Beratungsgrund", question_3_default_text)
        anamnese_3_default_text=f"Sie berichteten, dass Sie aktuell in Woche {pregnancy} schwanger sind. Der erste Tag der letzten Regel war der {regel}. Der rechnerische/sonographisch korrigierte Entbindungstermin ist am {delivery} (rechnerisch: ). Bei der sonographischen Untersuchung im Rahmen einer regulären Vorsorgeuntersuchung wurde eine Fehlbidung des XX beim Fetus festgestellt (Brief vom XX, XX). Bei Ihnen, Frau {Name_3}, sowie Ihrem Partner seien keine für die Fragestellung relevanten Erkrankungen bekannt. Sie seien nicht miteinander verwandt."
        anamnese_3 = st.text_area("Beratungsgrund", anamnese_3_default_text)
        
    elif question_3=="SS Familienanamnese auff.":
        question_3_default_text=f"1. XX in der Familienanamnese aufgrund einer pathogene Variante im XX Gen<br> 2. Aktuelle Schwangerschaft in SSW {pregnancy}, ET {delivery}"
        beratung_3 = st.text_area("Beratungsgrund", question_3_default_text)
        anamnese_3_default_text=f"Sie berichteten, dass Sie aktuell in Woche {pregnancy} schwanger sind. Der erste Tag der letzten Regel war der {regel}. Der rechnerische/sonographisch korrigierte Entbindungstermin ist am {delivery} (rechnerisch: ). Die Schwangerschaft sei durch die Gynäkologin bestätigt worden. Die Ausstellung des Mutterpasses steht aus. Bei Ihnen, Frau {Name_3}, sowie Ihrem Partner seien keine für die Fragestellung relevanten Erkrankungen bekannt. Sie seien nicht miteinander verwandt."
        anamnese_3 = st.text_area("Beratungsgrund", anamnese_3_default_text)
        
    elif question_3=="Aborte":
        question_3_default_text=f"Habituelle Aborte"
        beratung_3 = st.text_area("Beratungsgrund", question_3_default_text)
        anamnese_3_default_text=f"In Bezug auf die aktuelle Fragestellung wurden folgende Aspkete in der Anamnese erfasst:<br> - XX Aborte in der XX Schwangerschaftswoche<br> - Schwangerschaft sonographisch ohne Auffälligkeiten bestätigt / nicht bestätigt<br> - genetische Diagnostik ist bei keiner der Fehlgeburten erfolgt / Die zytogenetische Diagnostik anhand des Abortmaterials ergab den Nachweis einer XX, im Sinne eines XX (Befund vom XX)<br> - endokrinologische, gynäkologische, immunologische Untersuchungen und und Gerinnungsdiagnostik sind unauffällig (Briefe vom XX) / sind nicht erfolgt<br> -weitere für die Fragestellung relevante Erkrankungen seien bei Ihnen, Frau {Name_3} und Ihrem Partner nicht bekannt."
        anamnese_3 = st.text_area("Beratungsgrund", anamnese_3_default_text)

    elif question_3=="Kinderwunsch":
        question_3_default_text=f"Unerfüllter Kinderwunsch"
        beratung_3 = st.text_area("Beratungsgrund", question_3_default_text)
        anamnese_3_default_text=f"Seit XX bestehe in Ihrer Partnerschaft ein unerfüllter Kinderwunsch. Eine endokrinologische, gynäkologische, immunologische Untersuchung und Gerinnungsdiagnostik sind unauffällig (Briefe vom XX) // sind nicht erfolgt. Weitere für die Fragestellung relevante Erkrankungen seien bei Ihnen, Frau {Name_3} und Ihrem Partner nicht bekannt."
        anamnese_3 = st.text_area("Beratungsgrund", anamnese_3_default_text)
    
    elif question_3=="PID":
        question_3_default_text=f"Präimplantationsdiagnostik bei XX in der Familienanamnese"
        beratung_3 = st.text_area("Beratungsgrund", question_3_default_text)
        anamnese_3_default_text=f"Sie berichteten, dass bei Ihnen/bei Ihrem Partner, Frau {Name_3}, eine (wahrscheinlich) pathogene c.XX, p.(XX) Variante im XX-Gen nachgewiesen wurde (Befund vom XX). Sie erwägen deshalb eine Präimplantationsdiagnostik. Weitere für die Fragestellung relevante Erkrankungen seien bei Ihnen, Frau {Name_3} und Ihrem Partner nicht bekannt."
        anamnese_3 = st.text_area("Beratungsgrund", anamnese_3_default_text)
    
    elif question_3=="Planung Nabelschnurblut":
        question_3_default_text=f"Aktuelle Schwangerschaft in SSW {pregnancy}, ET {delivery}"
        beratung_3 = st.text_area("Beratungsgrund", question_3_default_text)
        anamnese_3_default_text=f"Sie berichteten, dass bei Ihnen/bei Ihrem Partner, Frau {Name_3}, eine (wahrscheinlich) pathogene c.XX, p.(XX) Variante im XX-Gen nachgewiesen wurde (Befund vom XX). Sie sind aktuell in Woche {pregnancy} schwanger. Der erste Tag der letzten Regel war der {regel}. Der rechnerische/sonographisch korrigierte Entbindungstermin ist am {delivery} (rechnerisch: ). Dem Mutterpass entnehmen wir eine unauffällige Schwangerschaft mit unauffälligem Ersttrimesterscreening/ unauffälliger Feindiagnostik am XX 17.02.2020 (Befund vom XX, Klinikum XX). Die Geburt solle am XX Klinikum stattfinden, wo Sie sich diesbezüglich am XX in der gynäkologischen und anästhesiologischen Sprechstunde vorstellten. Bei Ihnen, Frau {Name_3}, sowie Ihrem Partner seien keine für die Fragestellung relevanten Erkrankungen bekannt. Sie seien nicht miteinander verwandt."

    #Family history#
    ################
    if council_3=="Erstberatung":
        familienanamnese_3 = st.selectbox("Familienanamnese", ["auffällig", "unauffällig"], key="familienanamnese_3")
        if familienanamnese_3 == "unauffällig":
            family_3="""Sie berichteten keine für die Fragestellung relevanten Krankheitsbilder in Ihrer Familie."""
        elif familienanamnese_3 == "auffällig":
            fam_text_3="""Hinsichtlich der aktuellen Fragestellung berichteten Sie, dass bei XX eine XX vorliegt. Unterlagen zu den genannten Familienmitgliedern liegen uns nicht vor. Ein drei Generationen umfassender Stammbaum befindet sich im Anhang."""
            family_3=st.text_area("Relevante Erkrankungen in der Familie", fam_text_3, key="family_3")

    #Information about the diagostic#
    #################################
    diagnostic_info_3="""Bei den Methoden zur vorgeburtlichen genetischen Diagnostik unterscheidet man grundlegend die nichtinvasiven Verfahren (NIPT) von den invasiven Verfahren (Chorionzottenbiopsie, Fruchtwasseruntersuchung). <br><br>Als invasive Untersuchungsmethoden stehen die Chorionzottenbiopsie (CVS) und die Fruchtwasseruntersuchung (Amniozentese; AC) zur Verfügung. Der Vorteil der Chorionzottenbiopsie ist, dass sie bereits ab Schwangerschaftswoche 10+0 durchgeführt werden kann. Eine Fruchtwasseruntersuchung ist ab Schwangerschaftswoche 15+0 möglich. Wir besprachen, dass für beide Eingriffe jeweils ein Fehlgeburtsrisiko von 0,35 % angegeben wird (Beta <i>et al</i>., Minerva Ginecol., 2018). An dem jeweils gewonnen fetalen Material kann eine Chromosomenanalyse zur Bestimmung zahlenmäßiger oder grobstruktureller Veränderungen der Chromosomen durchgeführt werden. Nicht mit Sicherheit detektierbar sind Mosaikbefunde (paralleles Vorliegen verschiedener Zelllinien) oder Strukturveränderungen der Chromosomen unterhalb der lichtmikroskopischen Nachweisgrenze. Weiterhin besteht die Möglichkeit der Durchführung einer molekulargenetischen Diagnostik mit gleichzeitiger Untersuchung aller Gene (Exom). Die Untersuchung wird als Trio (gleichzeitige Untersuchung der DNA des Feten und der Eltern) durchgeführt, sodass eine Beurteilung der identifizierten Varianten schnell und effektiv erfolgen kann.<br><br>Ein weiteres nichtinvasives Untersuchungsverfahren ist der Nicht-invasive Pränataltest (NIPT), der ab Schwangerschaftswoche 9+0 beziehungsweise 10+0 zur Verfügung steht. Die im mütterlichen Blut in geringer Menge vorhandene fetale DNA wird hierbei mittels NGS-Verfahren (Next Generation Sequencing) untersucht. Gegenwärtig sind Analysen von zahlenmäßigen Chromosomenveränderungen (z.B. Trisomie 13, 18, 21), Mikrodeletions- und Mikroduplikationssyndromen (z.B. Mikrodeletionssyndrom 22q11.2) und Einzelgenerkrankungen (z.B. Mukoviszidose, spinale Muskelatrophie, Sichelzellkrankheit oder Thalassämien) möglich. Das Ergebnis des Tests liegt je nach Anbieter nach ein bis zwei Wochen vor. Sollte das Testergebnis auffällig sein, muss eine invasive Untersuchung zur Sicherung der Diagnose angeschlossen werden. Aktuell werden die Kosten für diesen Test von den gesetzlichen Krankenkassen nicht standardmäßig übernommen."""

    diagnostic_info_non_invasive_3="""Folgende nichtinvasive Methoden der Pränataldiagnostik stehen weiterhin zur Verfügung, jedoch ist der Nachweis einer spezifischen Chromosomenveränderung damit nicht möglich: Zwischen der 11. und 14. Schwangerschaftswoche kann das Erst-Trimester-Screening (First-Trimester-Screening, FTS) durchgeführt werden. Dabei liegt der optimale Untersuchungszeitraum zwischen der 12+0 und 13+0 Schwangerschaftswoche. Mittels einer Ultraschalluntersuchung wird die sogenannte Nackentransparenz (Abstand der Nackenhaut von der Wirbelsäule) beim Kind gemessen und gleichzeitig das PAPP-A (Pregnancy associated plasma protein A) und das freie ß-hCG (humanes Choriongonadotropin) aus dem mütterlichen Blut bestimmt. Aus diesen Parametern wird dann Ihr individuelles statistisches Risiko für eine Chromosomenveränderung beim Kind berechnet. Aktuell werden die Kosten für diesen Test von den gesetzlichen Krankenkassen nicht standardmäßig übernommen. 
Unabhängig davon, welche Untersuchungen man in der Schwangerschaft durchführen lässt, kann zwischen der 18. bis 22. Schwangerschaftswoche eine Ultraschallfeindiagnostik erfolgen, wobei die regelrechte Entwicklung aller Organe und des Skelettsystems beurteilt werden kann. Ob Fehlbildungen bereits pränatal im Ultraschall zu erkennen sind, kann nicht mit Sicherheit gesagt werden."""



    
    
           
           
        
        


        

   # st.header("A cat")
    #st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab4:
    ##########################################
    # Create the fourth tab for Textbausteine##
    #########################################
    
    st.title("Text blocks for diseases, genes, brainstorming etc. (Under development)")

    #Make a list of all genes, notions for which we have text#
    names = ["15q11.2-q13 - Angelman-Syndrom", "ABCA4", "ABCC6", "Mikrodeletionssyndrom 16p11.2", "Mikrodeletionssyndrom 16p12.2"]

    def search(query):
        # returning a list of names that contain the query
        results = [name for name in names if query.lower() in name.lower()]
        return results

    #User input for search query with autocomplete#
    ################################################
    search_query = st.text_input("Enter your search query:")
    suggested_queries = search(search_query)
    # Autocomplete dropdown
    selected_query = st.selectbox("Select a suggested query:", suggested_queries, index=0) #it makes things easier to see for what we could return a result
    display_query = st.text_input("Displayed query:", value=selected_query)

    # Search button#
    ################
    if st.button("Search"):
        if display_query=="15q11.2-q13 - Angelman-Syndrom":
            disease_info_default_text_3="""Das Angelman-Syndrom (AS) ist gekennzeichnet durch eine schwere Entwicklungsverzögerung, einer Intelligenzminderung mit häufiger deutlicher Einschränkung der Sprachentwicklung, Gangstörungen, Tremor und einem einzigartigen Verhalten mit einem fröhlichen Auftreten und häufigem Lachen. Weitere häufige Verhaltensänderungen umfassen auch Hypermotorik, ADHS und Schlafstörungen. Personen mit AS sind in bis zu 80% der Fälle von Epilepsien betroffen, die in der Regel im Kindesalter bis zum 5. Lebensjahr symptomatisch werden. Zudem wurden Fütterungsstörungen, eine Obstipationsneigung, sowie stereotype Kau- bzw. Mundbewegungen wie Zungenstoßen und ein übermäßiger Speichelfluss beschrieben. Ursächlich für ein AS sind Störungen der elterlichen genetischen Prägung („Imprinting“) der Region 15q11.2-q13. Durch eine Analyse des elternspezifischen DNA-Methylierungsmustern („Imprinting“) in der Chromosomenregion 15q11.2-q13 werden etwa 80% der Personen mit AS erkannt, einschließlich derjenigen deren AS durch eine Deletion der Region, einer uniparentalen Disomie oder einem Imprinting-Defekt verursacht ist. Bis zu ca. 75% der AS-Fälle sind einer Deletion des maternalen <i>UBE3A</i>-Allels in der Regi-on 15q11.2-q13 zuzuordnen und weitere 3⁠–⁠7% einer uniparentale Disomie (beide Allele wurden von einem Eltern-teil vererbt). Weiterhin sind pathogene Varianten des <i>UBE3A</i>-Allels in ca. 11% der Fälle nachweisbar, sowie Imprinting-Defekte mit und ohne Beeinflussung des Imprinting-Centers in 3⁠–⁠4%. Imprinting-Defekte ohne Beeinflussung des Imprinting-Centers treten sporadisch auf. Es gibt Hinweise, dass AS Betroffene mit Imprinting-Defekten von einer weniger schweren Symptomatik betroffen sind als jene mit Deletionen.<br> Die Therapie eines AS richtet sich nach der auftretenden Symptomatik und konzentriert sich häufig auf die Kontrolle einer etwaigen epileptischen Symptomatik, sowie einer intensiven multidisziplinären Förderung durch Ergo-, Logo- und Physiotherapie. Eine kausale Therapie ist zum aktuellen Zeitpunkt nicht bekannt (Dagli <i>et al</i>. 2021, GeneReviews PMID: 20301323)."""
            recommendation_default_text_3="""Nach Diagnosestellung sollten folgende Untersuchungen je nach Bedarf und bereits erfolgter Durchführung erfolgen (Dagli <i>et al</i>. 2021, GeneReviews PMID: 20301323):<br>- Neurologische Vorstellung mit EEG Untersuchung und ggf. MRT-Schädel<br> - Neuropädiatrische Baseline-Evaluation mit Beurteilung der motorischen, kognitiven, verbalen und nonverbalen Entwicklung, sowie potentiellen Verhaltensauffälligkeiten bezüglich ADHS, Autismus und Schlafstörungen<br> - Augenärztliche Vorstellung hinsichtlich Strabismus, Sehfähigkeit und okulärem Albinismus<br> - Orthopädische Vorstellung mit Beurteilung von Gangstörungen, Skoliosen, muskulärer Hypotonie und Fußdeformitäten<br> - Bei Reflux, Schluckstörungen oder Ernährungsstörungen ggf. gastroenterologische Vorstellung<br><br> Im Verlauf sollten folgende Untersuchungen erfolgen (Dagli <i>et al</i>. 2021, GeneReviews PMID: 20301323):<br> - Regelmäßige neuropädiatrische Beurteilung und Beurteilung der motorischen, kognitiven und psychosozialen Entwicklung durch ein sozialpädiatrisches Zentrum oder Anbindung an ein auf Angelman-Syndrom spezialisiertes Zentrum wie sie in München, Aachen und Leipzig etabliert sind. Ein Informationsflyer des Angelman-Zentrums in Leipzig ist diesem Schreiben beigelegt.<br> - Intensive Frühfördermaßnahmen durch Physio-, Ergo- und Logotherapie nach Bedarf<br> - Regelmäßige augenärztliche Kontrollen nach augenärztlicher Maßgabe<br> - Jährliche orthopädische Beurteilung der Wirbelsäule bezüglich einer Skoliose und ggf. weiteren orthopädischen Symptomen."""

        elif display_query=="ABCA4":
            disease_info_default_text_3="""Morbus Stargardt gilt als häufigste Ursache für eine Makuladegeneration in der Kindheit. Üblicherweise beginnend zwischen dem siebten und zwölften Lebensjahr führt die Erkrankung durch den Zerfall der Zapfen in der Fovea centralis zu starken Seheinschränkungen bis hin zur Erblindung in der zweiten Lebensdekade. Ein späterer Beginn ist aber auch möglich, wenn gleich seltener. Spätmanifestierende Veränderungen sind mit einem langsameren Fortschreiten und einer länger erhaltenen Sehfunktion assoziiert. (Altschwager <i>et al</i>. 2017. PMID: 28941524 )<br><br> Ursächlich für einen Morbus Stargardt sind pathogene Varianten in dem Gen ABCA4. Diese werden autosomal rezessiv vererbt. Das bedeutet, dass homozygote (zwei gleich veränderte Allele) und compound heterozygote (zwei verschieden veränderte Allele) Anlageträger\*Innen die Erkrankung ausbilden. Heterozygote Anlageträger\*Innen zeigen in der Regel keine Zeichen der Erkrankung. Kinder von Eltern, die heterozygote Anlageträger\*Innen für eine autosomal rezessive Erkrankung sind, werden mit einer 25%igen Wahrscheinlichkeit beide pathogene Varianten von ihren Eltern erben und die Erkrankung ausbilden. Eine kausale Therapie ist bisher nicht bekannt. (Fahim <i>et al</i>. GeneReviews. 2017)."""
            recommendation_default_text_3="""Im weiteren Verlauf sollten mindestens jährliche augenärztliche Untersuchungen erfolgen. Es wird empfohlen auf hochdosiertes Vitamin A sowie auf Nikotinkonsum zu verzichten (Fahim <i>et al</i>. GeneReviews. 2017).  Weiteres Informationsmaterial zur Erkrankung und zu möglichen klinischen Studien sowie die Möglichkeit zur Eintragung in ein Patient\*Innenregister finden Sie unter https://www.pro-retina.de/."""

        elif display_query=="ABCC6":
            disease_info_default_text_3="""Das Pseudoxanthoma elasticum ist eine Erkrankung des elastischen Bindegewebes des Auges, der Haut, der Blutgefäße und des Gastrointestinaltrakts. Häufige Manifestationen sind Gefäßauffälligkeiten und Einblutungen der Netzhaut. Die Veränderungen der Netzhaut können zu Sehstörungen durch Neovaskularisationen und Makulaatrophie führen. Zudem treten Papeln oder Plaques der Haut auf; Prädilektionsstellen hierfür sind Ellenbeuge, Leisten, Achselhöhlen oder Kniekehlen. Weitere Symptome können Angina abdominalis, gastrointestinale Blutungen, Claudicatio intermittens, Schlaganfälle, arterielle Hypertonie und kardiovaskuläre Komplikationen sein. Die meisten Betroffenen haben eine normale Lebenserwartung.<br><br>Ursächlich für ein Pseudoxanthoma elasticum sind pathogene Varianten des <i>ABCC6</i>-Gens. Diese werden autosomal-rezessiv vererbt. Das bedeutet, dass homozygote (zwei gleich veränderte Allele) und compound heterozygote (zwei verschieden veränderte Allele) Anlageträger\*Innen die Erkrankung ausbilden. Heterozygote Anlageträger\*Innen zeigen in der Regel keine Zeichen der Erkrankung. Kinder von Eltern, die heterozygote Anlageträger:/Innen für eine autosomal rezessive Erkrankung sind, werden mit einer 25%igen Wahrscheinlichkeit beide pathogene Varianten von ihren Eltern erben und die Erkrankung ausbilden.<br><br> Eine kausale Therapie ist bislang nicht bekannt. Die Behandlung der Symptome erfolgt nach den therapeutischen Standards der jeweiligen Fachgebiete. Es wird empfohlen, die allgemeinen vaskulären Risikofaktoren zu reduzieren. Bei Neovaskularisationen im Makulabereich der Netzhaut ist eine intravitreale Injektionstherapie mittels Angiogenese-Inhibitoren von einem Retina-Spezialisten abzuwägen (GeneReviews: Terry <i>et al</i>., 2020)."""
            recommendation_default_text_3="""Nach Diagnosestellung sollten folgende Untersuchungen erfolgen (GeneReviews):<br> - Komplette Hautuntersuchung durch Dermatolog\*In zur Etablierung einer Baseline<br> - Komplette augenärztliche Untersuchung durch Netzhaut-Spezialist\*In zur Evaluation von choroidaler Neovaskularisierung, Makulaatrophie sowie angioid streaks. ggf. Einleitung einer antiangiogenetischen Medikation<br> - Im Falle gastrointestinaler Auffälligkeiten Überweisung an Gastroenterolog\*In<br> - Im Falle angiologischer Auffälligkeiten (Schlaganfall, Claudicatio, renovaskuläre Hypertonie) Überweisung an Angiolog\*In und Nephrolog*In<br> - Kardiologische Vorstellung mit Erhebung von RR, EKG und TTE. <br><br> Im Verlauf sollten folgende Untersuchungen erfolgen (GeneReviews):<br> - Regelmäßige dermatologische Vorstellung (Frequenz in Abhängigkeit der Befunde)<br> - Jährliche augenärztliche Vorstellung (Netzhautuntersuchung)<br> - Regelmäßige Selbstuntersuchung mit Amsler-Gitter als Monitoring für zentrale Sehstörung.<br><br> Aufgrund des erhöhten Risikos für Augen-/Kopfverletzungen und daraus resultierende Netzhautblutungen sollte Kontaktsport vermieden werden. Zur Reduktion gastrointestinaler Blutungen sollten nichtsteroidale antiinflammatorische Medikamente (NSAIDs) vermieden werden. Rauchen sollte vermieden werden.<br><br> Mit Nachweis der o.g. pathogenen Varianten im <i>ABCC6</i>-Gen besteht für Familienangehörige im Rahmen einer genetischen Beratung die Möglichkeit einer gezielten Diagnostik, dies gilt insbesondere für XX. Eine Terminvereinbarung ist unter der o.g. Telefonnummer möglich."""
            
        elif display_query=="Mikrodeletionssyndrom 16p11.2":
            disease_info_default_text_3="""Die 16p11.2-Mikrodeletion ist eine seltene strukturelle Chromosomenstörung. Es ist gekennzeichnet durch eine globale Entwicklungsverzögerung, im späteren Verlauf ist eine Intelligenzminderung beschrieben. Weiterhin sind psychiatrische Störungen und Verhaltensauffälligkeiten, typischerweise aus dem Bereich der Autismus-Spektrum-Störungen bekannt. Epileptische Anfälle können bei 25% der Betroffenen auftreten. Betroffene Kinder entwickeln häufig eine Adipositas. Auch Veränderungen der Wirbelsäule, der Kopfform, des Gehirns, des Herzens, der Blutgefäße oder eine Schwerhörigkeit können vorkommen.<br>Ursächlich ist eine Mikrodeletion der Region 16p11.2. Diese wird autosomal dominant vererbt. Das bedeutet, dass heterozygote Anlageträger\*Innen die Erkrankung ausbilden. Damit besteht für die Nachkommen von Anlageträger\*Innen eine 50%ige Wahrscheinlichkeit, diese zu erben und die Erkrankung ebenfalls auszubilden. Es ist eine variable Expressivität beschrieben. Das bedeutet, die Ausprägung der klinischen Symptomatik kann auch innerhalb einer Familie sehr unterschiedlich sein. Weiterhin ist eine unvollständige Penetranz beschrieben. Das bedeutet, nicht alle Anlageträger\*Innen bilden auch eine klinische Symptomatik aus. Eine kausale Therapie steht derzeit nicht zur Verfügung. (GeneReviews, 2021, 16p11.2 Recurrent Deletion)"""
            recommendation_default_text_3="""Nach Diagnosestellung des Mikrodeletionssyndroms 16p11.2 sollten folgende Untersuchungen erfolgen (GeneReviews, 2021, 16p11.2 Recurrent Deletion):

• Beurteilung des Entwicklungsstandes
• Neuropsychiatrische Evaluation
• Neurologische Evaluation
• Muskuloskelettale Beurteilung, inklusive Bildgebung der Wirbelsäule zur Beurteilung eventueller vertebraler Anomalien oder Skoliose)
• Endokrinologische Beurteilung, ggf. Bestimmung der Nüchternglukose und des HbA1c
• HNO-ärztliche Evaluation des Hörvermögens
• Kardiovaskuläre Beurteilung, insbesondere hinsichtlich Herzgeräuschen und Blutdruck


Im Verlauf sollten folgende Untersuchungen erfolgen (GeneReviews, 2021, 16p11.2 Recurrent Deletion):

• Regelmäßige Beurteilungen der intellektuellen Entwicklung und des Unterstützungsbedarfs
• Regelmäßige Beurteilung der Körpermaße zur frühzeitigen Detektion eines entstehenden Übergewichts
• Regelmäßige kinderpsychiatrische Beurteilung bezüglich Auffälligleiten des Verhaltens oder des Affekts
• Engmaschige neurologische Anbindung
• Regelmäßige körperliche Untersuchung, insbesondere hinsichtlich der skelettalen Reife und Skoliose
• Im Falle eines Übergewichts: Ernährungsmedizinische Beratung, aktiver Lebensstil
• Jährliche Bestimmung der Nüchternglukose und des HbA1c 
• Regelmäßige Messung des Blutdrucks (bei jedem Arztkontakt während der Kindheit)
• Bis zum 3. Lebensjahr jährliche HNO-ärztliche Evaluation des Hörvermögens

Wir empfehlen eine regelmäßige neuropädiatrische Betreuung, z.B. durch ein Sozialpädiatrisches Zentrum, sowie regelmäßige Fördermaßnahmen wie Frühförderung, Logopädie, Ergo- oder Physiotherapie. 

Wir empfehlen, auf Medikamente, die zu einer Gewichtszunahme führen (z.B. Clozapin, Olanzapin), wenn möglich zu verzichten.
Über die Familienselbsthilfe des Leona e.V. können Sie sich mit anderen betroffenen Familien vernetzen: https://www.leona-ev.de/start/

Wir empfehlen Ihnen bei Kinderwunsch oder spätestens im Falle einer Schwangerschaft in der 6. bis 9. Schwanger-schaftswoche eine genetische Beratung. Diese kann gern im Rahmen unserer Sprechstunde stattfinden. Eine Terminvereinbarung ist unter der o.g. Telefonnummer möglich.

Weiterhin besteht für ####  vor eigener Familienplanung die Möglichkeit einer erneuten genetischen Beratung hinsichtlich der Wiederholungswahrscheinlichkeit."""

        elif display_query=="Mikrodeletionssyndrom 16p12.2":
            disease_info_default_text_3="""Die 16p12.2-Mikrodeletion ist gekennzeichnet durch eine Reihe variabler Symptome wie u.a. Entwicklungsverzögerung, Intelligenzminderung, Wachstumsverzögerung, Mikrozephalie und Verhaltensauffälligkeiten (Girirajan et. al. 2018, GeneReviews, PMID: 25719193). Epileptische Anfälle können bei 40 % der Betroffenen auftreten. Auch Veränderungen des Gehirns, des Herzens oder eine Schwerhörigkeit sind beschrieben.
Ursächlich ist eine Mikrodeletion der Region 16p12.2. Diese wird autosomal dominant vererbt. Das bedeutet, dass heterozygote Anlageträger\*Innen die Erkrankung ausbilden. Damit besteht für die Nachkommen von Anlageträger\*Innen eine 50 %ige Wahrscheinlichkeit, diese zu erben und die Erkrankung ebenfalls auszubilden. Es ist eine variable Expressivität beschrieben. Das bedeutet, die Ausprägung der klinischen Symptomatik kann auch innerhalb einer Familie sehr unterschiedlich sein. Weiterhin ist eine unvollständige Penetranz beschrieben. Das bedeutet, nicht alle Anlageträger\*Innen bilden auch eine klinische Symptomatik aus. Eine kausale Therapie steht derzeit nicht zur Verfügung. Die Behandlung erfolgt symptomatisch durch entsprechende Spezialisten."""
            recommendation_default_text_3="""Beurteilung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Bei X wurde die o.g. heterozygote pathogene Deletion in der Region 16p12.2 und somit ein Mikrodeletionssyndrom 16p12.2 molekulargenetisch nachgewiesen. Eine sichere Vorhersage zu auftretenden Symptomen ist aufgrund der bekannt variablen Expressivität nicht möglich.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 Empfehlungen
Mit der Diagnosestellung des Mikrodeletionssyndroms 16p12.2 empfehlen wir regelmäßige neuropädiatrische Betreuung von X, z.B. durch ein Sozialpädiatrisches Zentrum, sowie ggfs. Fördermaßnahmen wie Frühförderung, Logopädie, Ergo- und / oder Physiotherapie.
Nach Diagnosestellung sollten folgende Untersuchungen stattfinden (16p12.2 Recurrent Deletion, GeneReviews. 2018):
• Bestimmung von Größe und Gewicht
• Beurteilung des Entwicklungsstandes 
• Neurologische Untersuchung insbesondere bei Krampfanfällen 
• Kardiologische Evaluation inkl. Echokardiographie
• Klinische Untersuchung hinsichtlich Fehlbildungen von weiteren Organsystemen
Im weiteren Verlauf empfehlen wir folgende Untersuchungen (16p12.2 Recurrent Deletion, GeneReviews. 2018):
• regelmäßige Evaluation des Entwicklungsstandes und Verhaltens hinsichtlich Entwicklungsverzögerungen, 
Intelligenzminderung, Autismus und andere entsprechende Auffälligkeiten
• regelmäßige kardiologische, nephrologische, urologische sowie dontologische Kontrolluntersuchungen insbesondere bei nachgewiesenen Auffälligkeiten
Weiterhin empfehlen wir Ihnen für den Austausch von Informationen den Selbsthilfeverein Leona e.V. für seltene Chromosomenerkrankungen  (https://www.leona-ev.de).
Mit Nachweis des Mikrodeletionssyndroms 16p12.2 bei X besteht für (leibliche) Familienangehörige die Möglichkeit einer gezielten Diagnostik bezüglich des Mikrodeletionssyndroms. Diese Untersuchung kann gern im Rahmen unserer Sprechstunde stattfinden. Eine Terminvereinbarung ist unter der o. g. Telefonnummer möglich. 
Weiterhin besteht für X vor eigener Familienplanung die Möglichkeit einer erneuten humangenetischen Beratung hinsichtlich des Wiederholungsrisikos."""

            

            
        disease_info_3 = st.text_area("Allgemeine Informationen zum Krankheitsbild", disease_info_default_text_3)
        recommendation_3 = st.text_area("Empfehlungen", recommendation_default_text_3)
        st.markdown("<div class='custom-paragraph'><b>Allgemeine Informationen zum Krankheitsbild:</b></div>",  unsafe_allow_html=True)
        st.markdown(disease_info_3, unsafe_allow_html=True)
        st.markdown("<div class='custom-paragraph'><b>Empfehlung</b></div>",  unsafe_allow_html=True)
        st.markdown(recommendation_3, unsafe_allow_html=True)

  
    
