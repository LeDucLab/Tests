import streamlit as st
import random
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError



# Set the title for the page
st.title("Personalisierte Medizin: Welche Informationen haben Sie mitgenommen")
#github_image_url = 'https://cdn.pixabay.com/photo/2013/07/18/10/59/dna-163710_1280.jpg'
#st.image(github_image_url, use_column_width=True)

questions_data = [
    {
        'Question': 'Was ist das Hauptziel der personalisierten Medizin?',
        'Options': ['Eine "One-Size-Fits-All" -Ansatz für alle Patienten', 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen', 'Die ausschließliche Verwendung traditioneller Behandlungsansätze', 'Die Maximierung der Kosteneffizienz bei medizinischen Interventionen'],
        'Answer': 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen',
        'CorrectImageURL':'https://github.com/LeDucLab/Tests/raw/main/Images/Personalisierte%20Medizin%20in%20der%20klinischen%20Genetik_v3.png',
        'IncorrectImageURL':'https://github.com/LeDucLab/Tests/raw/main/Images/Personalisierte%20Medizin%20in%20der%20klinischen%20Genetik_v2.png',
        'QuestionType': 'multiple_choice',
    },
     {
        'Question':'Welche Informationen müssen berücksichtigt werden, um zu entscheiden, welche Therapie für ein Neugeborenes geeignet ist, bei dem im Rahmen des Neugeborenenscreenings eine spinale Muskelatrophie (SMA) diagnostiziert wurde?',
        'Answer': 'Kopienzahl vom SMN2-Gen',
        'CorrectImageURL':'https://github.com/LeDucLab/Tests/raw/main/Images/SMN2_v1.png',
        'IncorrectImageURL':'https://github.com/LeDucLab/Tests/raw/main/Images/SMN2_v2.png',
        'QuestionType': 'fill in',
    },
    # Add more questions as needed
]


# Initialize variables
score = 0
current_question = 0
user_answers = {}

# Display the current question
if current_question < len(questions_data):
    st.subheader(f"Frage {current_question + 1}:")
    st.write(questions_data[current_question]['Question'])

    # Check the question type
    if questions_data[current_question]['QuestionType'] == 'fill_in':
        # Get user input for the answer
        user_answer = st.text_input("Antwort:", key=f"input_{current_question}", value=user_answers.get(f"input_{current_question}", ""))

        # Store the user's answer in the dictionary
        user_answers[f"input_{current_question}"] = user_answer

    elif questions_data[current_question]['QuestionType'] == 'multiple_choice':
        # Create radio buttons for options without a default selection
        selected_option = st.radio("Wählen Sie eine Option:", options=['', *questions_data[current_question]['Options']], key=f"radio_{current_question}", index=user_answers.get(f"radio_{current_question}", 0))

        # Store the user's answer in the dictionary
        user_answers[f"radio_{current_question}"] = selected_option

    # Check if the user submitted an answer
    if st.button("Einreichen"):
        # Check if at least one word from the user's answer matches any word in the correct answer
        if questions_data[current_question]['QuestionType'] == 'fill_in':
            if any(word.lower() in questions_data[current_question]['Answer'].lower() for word in user_answer.split()):
                st.success("Korrekt!")
                st.markdown(f'<img src="{questions_data[current_question]["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
                score += 1
            else:
                st.warning("Falsch! Versuchen SIe nochmal.")
                st.markdown(f'<img src="{questions_data[current_question]["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
        elif questions_data[current_question]['QuestionType'] == 'multiple_choice':
            if selected_option != '':
                # Check if the selected option is correct
                if selected_option == questions_data[current_question]['Answer']:
                    st.success("Korrekt!")
                    st.markdown(f'<img src="{questions_data[current_question]["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
                    score += 1
                else:
                    st.warning("Falsch! Versuchen Sie nochmal!")
                    st.markdown(f'<img src="{questions_data[current_question]["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
            else:
                st.warning("Wählen Sie eine Option")

# Button to go to the next question
if st.button("Nächste Frage") and current_question < len(questions_data) - 1:
    current_question += 1
    st.experimental_rerun()

# Display the final score
st.subheader("Ergebnis")
st.write(f"Sie haben {score} von {len(questions_data)} Fragen korrekt beantwortet.")


# Initialize variables
#score = 0
#user_answers = {}

# Iterate through each question
#for i, question_data in enumerate(questions_data, start=1):
#    st.subheader(f"Frage {i}:")
 #   st.write(question_data['Question'])

 #   if question_data['QuestionType'] == 'fill_in':
   #     user_answer = st.text_input("Your Answer:", key=f"input_{i}", value=user_answers.get(f"input_{i}", ""))
   #     user_answers[f"input_{i}"] = user_answer
#
     #   if st.button("Submit"):
    #        if any(word.lower() in question_data['Answer'].lower() for word in user_answer.split()):
    #            st.success("Korrekt!")
    #            st.markdown(f'<img src="{question_data["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
    #            score += 1
     #       else:
   #             st.warning("Falsch! Versuchen Sie nochmal.")
    #            st.markdown(f'<img src="{question_data["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
            
  #  elif question_data['QuestionType'] == 'multiple_choice':
        # Create radio buttons for options without a default selection
  #      selected_option = st.radio("Select an option:", options=['', *question_data['Options']])

        # Check if an option is selected
  #      if selected_option != '':
            # Check if the selected option is correct
    #        if selected_option == question_data['Answer']:
      #          st.success("Correct!")
    #            st.markdown(f'<img src="{question_data["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
     #           score += 1
     #       else:
   #             st.warning("Falsch! Versuchen Sie nochmal.")
  #              st.markdown(f'<img src="{question_data["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
   #     else:
  #          st.warning("Wählen Sie eine Option.")

    # Create radio buttons for options without a default selection
    #selected_option = st.radio("Wählen Sie eine Option", options=['', *question_data['Options']])

    # Check if an option is selected
    #if selected_option != '':
        # Check if the selected option is correct
     #   if selected_option == question_data['Answer']:
      #      st.success("Korrekt!")
       # else:
        #    st.warning("Falsch! Versuchen Sie nochmal.")

        # Display the image directly from the URL using HTML
        #image_url = question_data['CorrectImageURL'] if selected_option == question_data['Answer'] else question_data['IncorrectImageURL']
        #st.markdown(f'<img src="{image_url}" alt="Image" width="100%">', unsafe_allow_html=True)

        #if selected_option == question_data['Answer']:
         #   score += 1
    #else:
     #   st.warning("Please select an option.")

# Display the final score
#st.subheader("Your Final Score:")
#st.write(f"You got {score} out of {len(questions_data)} questions correct.")






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
