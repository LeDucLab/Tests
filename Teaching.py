import streamlit as st
import random
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError

import streamlit as st

# Set the title for the page
st.title("Personalisierte Medizin: Welche Informationen haben Sie mitgenommen")

# Define the questions
question_data_1 = [
    {
        'Question': 'Welche Informationen müssen berücksichtigt werden, um zu entscheiden, welche Therapie für ein Neugeborenes geeignet ist, bei dem im Rahmen des Neugeborenenscreenings eine spinale Muskelatrophie (SMA) diagnostiziert wurde?',
        'Answer': 'Kopienzahl vom SMN2-Gen',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/SMA_v1.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/SMA_v2.png',
        'QuestionType': 'fill_in',
    },
]

question_data_2 = [
    {
        'Question': 'Was ist das Hauptziel der personalisierten Medizin?',
        'Options': ['Eine "One-Size-Fits-All"-Ansatz für alle Patienten', 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen', 'Die ausschließliche Verwendung traditioneller Behandlungsansätze', 'Die Maximierung der Kosteneffizienz bei medizinischen Interventionen'],
        'Answer': 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/Personalisierte%20Medizin%20in%20der%20klinischen%20Genetik_v3.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/Personalisierte%20Medizin%20in%20der%20klinischen%20Genetik_v2.png',
        'QuestionType': 'multiple_choice',
    },
]

# Use session_state to store user's progress
session_state = st.session_state

if 'score' not in session_state:
    session_state.score = 0
if 'current_question' not in session_state:
    session_state.current_question = 0

# Iterate through each question
for question_data in question_data_1 + question_data_2[session_state.current_question:]:
    st.subheader(f"Frage {session_state.current_question + 1}:")
    st.write(question_data['Question'])

    if question_data['QuestionType'] == 'fill_in':
        user_answer = st.text_input("Ihre Antwort:")
        if st.button("Submit"):
            if any(word.lower() in question_data['Answer'].lower() for word in user_answer.split()):
                st.success("Korrekt!")
                st.markdown(f'<img src="{question_data["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
                session_state.score += 1
            else:
                st.warning("Falsch! Versuchen Sie nochmal.")
                st.markdown(f'<img src="{question_data["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
     
    elif question_data['QuestionType'] == 'multiple_choice':
        # Display multiple-choice options as radio buttons
        user_answer = st.radio("Ihre Antwort:", question_data['Options'])
        if user_answer == question_data['Answer']:
            st.success("Korrekt!")
            st.markdown(f'<img src="{question_data["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
            session_state.score += 1
        else:
            st.warning("Falsch! Versuchen Sie nochmal.")
            st.markdown(f'<img src="{question_data["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)

    if session_state.current_question < len(question_data_2) - 1:
        if st.button("Nächste Frage"):
            session_state.current_question += 1
   

# Display the final score
st.subheader("Ihr Endergebnis:")
st.write(f"Sie haben {session_state.score} von {len(question_data_1) + len(question_data_2)} Fragen korrekt beantwortet.")




   
#Display the final score
#st.subheader("Ergebnis")
#if score==2:
#     st.success("Damit ist die Übung abgeschlossen! Ausgezeichnet!:star:")
#     if st.button("Belohnung"):
#          st.balloons()





#from PIL import Image
#from pathlib import Path

#import settings

#def read_markdown_file(markdown_file):
 #   return Path(markdown_file).read_text()

#def print_hoc_part(show_answers):

 #   if show_answers:
#        answers = {
  #          "hboc_part_1_answer_0" : True,
   #         "hboc_part_2_answer_1" : True,
    #        "hboc_part_3_answer_1" : True,
    #        "hboc_part_3_reason" : "Keine ursächliche Variante identifiziert.",
     #       "hboc_part_4_answer_2" : True,
      #      "hboc_part_5_answer_0" : 3,
       #     "hboc_part_5_1_answer_1" : 2,
        #    "hboc_part_5_2_answer_0" : "Das Lebenszeitrisiko liegt unter 5%.",
        #    "hboc_part_7_answer_0" : 8.6,
        #    "hboc_part_7_answer_1" : True,
         #   "hboc_part_7_answer_3" : "Das Lebenszeitrisiko liegt jetzt über 5%."
      #  }
 #   else:
       # answers = {
         #   "hboc_part_1_answer_0" : False,
          #  "hboc_part_2_answer_1" : False,
         #   "hboc_part_3_answer_1" : False,
          #  "hboc_part_3_reason" : "",
          #  "hboc_part_4_answer_2" : False,
           # "hboc_part_5_answer_0" : 0,
           # "hboc_part_5_1_answer_1" : 0,
           # "hboc_part_5_2_answer_0" : "",
           # "hboc_part_7_answer_0" : 0.0,
            #"hboc_part_7_answer_1" : False,
          #  "hboc_part_7_answer_3" : ""
      #  }



    #st.markdown(read_markdown_file(settings.hboc_markdown + "hboc_part_1.md"))
   # with open('pages/hboc/pdfs/Mertens_et_al_2022.pdf', 'rb') as f:
       # st.download_button('Download', f, file_name='Mertens_et_al_2022.pdf')
    #st.markdown(read_markdown_file(settings.hboc_markdown + "hboc_part_1_2.md"))
    
   # hboc_family_tree = Image.open(settings.hboc_images + "hboc_part_1_family_tree.png")
   # st.image(hboc_family_tree)
    #with st.expander("**Infobox - Kriterien**"):
      #  hboc_infobox_1 = Image.open(settings.hboc_images + "hboc_part_1_infobox_1.png")
       # st.image(hboc_infobox_1, "aus Mertens et al., 2022")

   # st.markdown(":question: **Wann kann ein Tumorprädispositionssyndrom in der Familie vorliegen?**")

    
   # hboc_part_1_options= [
      #  "Frühes Erkrankungsalter, gehäuftes Auftreten von seltenen Tumorentitäten",
       # "Später Erkrankungsalter, gehäuftes Auftreten von seltenen Tumorentitäten",
       # "Es gibt keine besonderen Patientenmerkmale"
   # ]

   # hboc_part_1_answer_0 = st.checkbox(hboc_part_1_options[0], key="hboc_part_1_answer_0", value=answers["hboc_part_1_answer_0"])
   ## hboc_part_1_answer_1 = st.checkbox(hboc_part_1_options[1], key="hboc_part_1_answer_1")
    #hboc_part_1_answer_2 = st.checkbox(hboc_part_1_options[2], key="hboc_part_1_answer_2")

   # #if hboc_part_1_answer_0 and not hboc_part_1_answer_1 and not hboc_part_1_answer_2:
     #   st.success("Korrekt!")
     #   st.write(":sparkles: Ein frühes Erkrankungsalter und das gehäufte Auftreten von seltenen Tumorentitäten kann ein Hinweis auf das Vorliegen eines genetisch bedingten Tumorprädispositionssyndroms sein. In unserer Familie ist das Vorliegen eines Tumorprädipositionssyndroms möglich, da zwei Personen früh erkrankten.")

     #   st.markdown(read_markdown_file(settings.hboc_markdown + "hboc_part_2.md"))

     #   with st.expander("**Infobox - Methodik**"):
       #     hboc_infobox_2 = Image.open(settings.hboc_images + "hboc_part_2_methods.png")
     #       st.image(hboc_infobox_2, "aus Mertens et al., 2022")

     #   st.markdown("❓ Welche bevorzugte Möglichkeit der Testung wird der Patientin angeboten?")

     #   hboc_part_2_options = [
     #       "Sangersequenzierung",
     #       "Panelanalyse",
      #      "Genomsequenzierung"
      #  ]

       # hboc_part_2_answer_0 = st.checkbox(hboc_part_2_options[0], key="hboc_part_2_answer_0")
       # hboc_part_2_answer_1 = st.checkbox(hboc_part_2_options[1], key="hboc_part_2_answer_1", value=answers["hboc_part_2_answer_1"])
       # hboc_part_2_answer_2 = st.checkbox(hboc_part_2_options[2], key="hboc_part_2_answer_2")

      #  if hboc_part_2_answer_1 and not hboc_part_2_answer_0 and not hboc_part_2_answer_2:
       #     st.success("Korrekt!")
       #     st.markdown(":sparkles: Mittels einer **Panel-Analyse** werden alle Hauptgene für ein familiäres Tumorprädipositionssyndrom untersucht. Je nach Ergebnis der Analyse, ob positiv oder negativ können weitere Maßnahmen getroffen werden.")

      #      # st.markdown(read_markdown_file(settings.hboc_markdown + "hboc_part_3.md"))

       #     # hboc_part_3_answer_0 = st.checkbox("Ja", key="hboc_part_3_answer_0")
       #     # hboc_part_3_answer_1 = st.checkbox("Nein", key="hboc_part_3_answer_1", value=answers["hboc_part_3_answer_1"])

            # if hboc_part_3_answer_1 and not hboc_part_3_answer_0:

            #     hboc_part_3_reason = st.text_area("Begründe", value=answers["hboc_part_3_reason"])

            #     if hboc_part_3_reason != "":

            # Part 4
       #     st.markdown(read_markdown_file(settings.hboc_markdown + "hboc_part_4.md"))

      #      with st.expander("**Infobox - Entscheidungsbaum**"):
        #                hboc_dec_tree = Image.open(settings.hboc_images + "hboc_part_5_decision_tree.png")
            #            st.image(hboc_dec_tree)

     #       hboc_part_4_options = [
      #          "Risikominimierende Operation",
     #           "Einschluss in ein Vorsorgeprogramm (IFNP)", 
       #         "Berechnung des Risikos über das CanRisk-Tool",
     #           "keine weiteren Maßnahmen notwendig (Regelvorsorge)"
       #     ]

       #     hboc_part_4_answer_0 = st.checkbox(hboc_part_4_options[0], key="hboc_part_4_answer_0")
       #     hboc_part_4_answer_1 = st.checkbox(hboc_part_4_options[1], key="hboc_part_4_answer_1")
       #     hboc_part_4_answer_2 = st.checkbox(hboc_part_4_options[2], key="hboc_part_4_answer_2", value=answers["hboc_part_4_answer_2"])
        #    hboc_part_4_answer_3 = st.checkbox(hboc_part_4_options[3], key="hboc_part_4_answer_3")

       #     if hboc_part_4_answer_2 and not hboc_part_4_answer_0 and not hboc_part_4_answer_1 and not hboc_part_4_answer_3:
      #          st.success("Korrekt!")
      #          st.markdown(":sparkles: In unserem Fall haben wir eine **gesunde Ratsuchende getestet und ein negatives Ergebnis** mit der genetischen Diagnostik erzielt. Wir haben der Patientin eine **Risikoberechnung mittels CanRisk** angeboten und durchgeführt.")
                # Part 5
     #           st.markdown(read_markdown_file(settings.hboc_markdown + "hboc_part_5.md"))



       #         with open('pages/hboc/vcfs/pedigree.txt', 'rb') as f:
        #            st.download_button('Download pedigree.txt', f, file_name='pedigree.txt')
#
       #         st.markdown("❓ Wie hoch ist das 10-Jahres-Risiko der Patientin an Brustkrebs zu erkranken?")
       #         hboc_part_5_answer_0 = st.radio("Antwort", ["0-1%", "1-2%", "2-3%", "3-4%", "4-5%", ">5%"], horizontal=True, index=answers["hboc_part_5_answer_0"])

                


        #        if hboc_part_5_answer_0 == "3-4%":
         #           st.success("Korrekt!")
        #            st.markdown(read_markdown_file(settings.hboc_markdown + "hboc_part_5_1.md"))

        #            hboc_part_5_1_answer_0 = st.radio("Antwort", 
       #                                               [
          #                                              "Ja, da die Ratsuchende jünger als 50 Jahre alt ist.",
          #                                              "Ja, da die Ratsuchende zur Risikogruppe 3 gehört.",
          #                                              "Nein, da die CanRisk-Berechnung unter 5% liegt.",
          #                                              "Nein, da die Multigenpanel-Analyse unauffällig war."
           #                                           ],
          #                                            key="hboc_part_5_1_answer_0",
          #                                            index=answers["hboc_part_5_1_answer_1"])
                    
           #         if hboc_part_5_1_answer_0 == "Nein, da die CanRisk-Berechnung unter 5% liegt.":
                        
          #              st.markdown(":sparkles: Das 10-Jahresrisiko für Brustkrebs lag bei 3.4%. Daher sind die Einschlusskriterien für das intensivierte Früh- und Nachsorgeprogramm nicht erfüllt (10-Jahresrisiko mind. 5%).")

           #             st.success("Damit ist die Übung abgeschlossen! Ausgezeichnet! :star:")

           #            if st.button("Belohnung"):
           #                 st.balloons()
