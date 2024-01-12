import streamlit as st
import random
import requests
from PIL import Image
from io import BytesIO


# Set the title for the page
st.title("Personalisierte Medizin: Welche Informationen haben Sie mitgenommen")
#github_image_url = 'https://cdn.pixabay.com/photo/2013/07/18/10/59/dna-163710_1280.jpg'
#st.image(github_image_url, use_column_width=True)

questions_data = [
    {
        'Question': 'Was ist das Hauptziel der personalisierten Medizin?',
        'Options': ['Eine "One-Size-Fits-All" -Ansatz für alle Patienten', 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen', 'Die ausschließliche Verwendung traditioneller Behandlungsansätze', 'Die Maximierung der Kosteneffizienz bei medizinischen Interventionen'],
        'Answer': 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen',
        'CorrectImageURL':'https://raw.github.com/LeDucLab/main/Tests/raw/main/Images/Personalisierte%20Medizin%20in%20der%20klinischen%20Genetik_v3.png',
    },
    # Add more questions as needed
]


random.shuffle(questions_data)

# Set the title for the page


# Initialize variables
score = 0
question_number = 0

# Iterate through each question
for question_data in questions_data:
    question_number += 1

    st.subheader(f"Question {question_number}:")
    st.write(question_data['Question'])

    # Create radio buttons for options without a default selection
    selected_option = st.radio("Select an option:", options=['', *question_data['Options']])

    # Check if an option is selected
    if selected_option != '':
        # Check if the selected option is correct
        if selected_option == question_data['Answer']:
            st.success("Correct!")
            image_content = requests.get(question_data['CorrectImageURL']).content
            image = Image.open(BytesIO(image_content))
            st.image(image, caption='Correct!', use_column_width=True)
            score += 1
        else:
            st.warning("Incorrect! Try again.")
    else:
        st.warning("Please select an option.")

# Display the final score
st.subheader("Your Final Score:")
st.write(f"You got {score} out of {len(questions_data)} questions correct.")


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
