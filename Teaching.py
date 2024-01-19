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
        'Question': 'Was ist das Hauptziel der personalisierten Medizin?',
        'Options': ['','Eine One-Size-Fits-All-Ansatz für alle Patienten', 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen', 'Die ausschließliche Verwendung traditioneller Behandlungsansätze', 'Die Maximierung der Kosteneffizienz bei medizinischen Interventionen'],
        'Answer': 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/Personalisierte%20Medizin%20in%20der%20klinischen%20Genetik_v3.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/Personalisierte%20Medizin%20in%20der%20klinischen%20Genetik_v2.png',
        'QuestionType': 'multiple_choice',
    },
]
question_data_2 = [
    {
        'Question': 'Welche Methode wird voraussichtlich eine Schlüsselrolle in der Zukunft der genetischen Therapie in der personalisierten Medizin spielen?',
        'Options': ['','Gentechnisch veränderte Organismen', 'Bioprinting von Organen', 'Gezielte Genom-Editierung', 'Stammzelltransplantation'],
        'Answer': 'Gezielte Genom-Editierung',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/Therapie_v1.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/Therapie_v2.png',
        'QuestionType': 'multiple_choice',
    },
]



question_data_3 = [
    {
        'Question': 'Welche Informationen müssen berücksichtigt werden, um zu entscheiden, welche Therapie für ein Neugeborenes geeignet ist, bei dem im Rahmen des Neugeborenenscreenings eine spinale Muskelatrophie (SMA) diagnostiziert wurde?',
        'Answer': 'Kopienzahl vom SMN2-Gen',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/SMA_v1.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/SMA_v2.png',
        'QuestionType': 'fill_in',
    },
]




# Initialize session state
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0


# Display the current question
if st.session_state.question_index == 0:
    current_question = question_data_1[0]
    st.subheader(f"Frage 1:")
    st.write(current_question['Question'])
    user_answer_1 = st.radio("Ihre Antwort:", options=current_question['Options'], key="user_answer_1")
    if user_answer_1 != '':
        if user_answer_1 == current_question['Answer']:
            st.success("Korrekt!")
            st.markdown(f'<img src="{current_question["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
            st.session_state.question_index += 1
            st.write(st.session_state.question_index)
            st.button("Nächste Frage", key="Q2")
        else:
            st.warning("Falsch! Versuchen Sie nochmal.")
            st.markdown(f'<img src="{current_question["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)


# Display the next question
elif st.session_state.question_index == 1:
    current_question = question_data_2[0]
    st.subheader(f"Frage 2:")
    st.write(current_question['Question'])
    user_answer_2 = st.radio("Ihre Antwort:", options=current_question['Options'], key="user_answer_2")
    if user_answer_2 != '':
        if user_answer_2 == current_question['Answer']:
            st.success("Korrekt!")
            st.markdown(f'<img src="{current_question["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
            st.session_state.question_index += 1
            st.write(st.session_state.question_index)
            st.button("Nächste Frage", key="Q3")
        else:
            st.warning("Falsch! Versuchen Sie nochmal.")
            st.markdown(f'<img src="{current_question["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
   
elif st.session_state.question_index == 2:
    current_question = question_data_3[0]
    st.subheader(f"Frage 3:")
    st.write(current_question['Question'])
    user_answer_3 = st.text_input("Ihre Antwort:", key="user_answer_1")
    if st.button("Antwort einreichen", key="A3"):
        if any(word.lower() in current_question['Answer'].lower() for word in user_answer_3.split()):
            st.success("Korrekt!")
            st.markdown(f'<img src="{current_question["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
            st.session_state.question_index += 1
            st.write(st.session_state.question_index)
            #button_placeholder.button.on_event('on_click', lambda x: x.js('document.querySelector("button[data-baseweb-id=1]").click()'))
            st.button("Belohnung", key="Q4")
        else:
            st.warning("Falsch! Versuchen Sie nochmal.")
            st.markdown(f'<img src="{current_question["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)

elif st.session_state.question_index == 3:
    st.success("Sie haben die Übung erfolgreich abgeschlossen. Viel Spaß beim Lernen! Liebe Grüße, Diana Le Duc")
    st.balloons()
# Display the first question
#for question_data_1_item in question_data_1:
#    st.subheader(f"Frage 1:")
#    st.write(question_data_1_item['Question'])
#    user_answer_1 = st.text_input("Ihre Antwort:", key="user_answer_1")
#    if st.button("Einreichen Frage 1", key="A1"):
#        if any(word.lower() in question_data_1_item['Answer'].lower() for word in st.session_state.user_answer_1.split()):
#            st.success("Korrekt!")
#            st.markdown(f'<img src="{question_data_1_item["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
#            for question_data_2_item in question_data_2:
#                st.subheader(f"Frage 2:")
#                st.write(question_data_2_item['Question'])
#                user_answer_2 = st.radio("Ihre Antwort:", options=question_data_2_item['Options'], key="user_answer_2")
                #if st.button("Einreichen Frage 2", key="A2"):
#                if user_answer_2 !='':
#                    if user_answer_2 == question_data_2_item['Answer']:
#                        st.success("Korrekt!")
#                        st.markdown(f'<img src="{question_data_2_item["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
#                    else:
#                        st.warning("Falsch! Versuchen Sie nochmal.")
#                        st.markdown(f'<img src="{question_data_2_item["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
#        else:
#            st.warning("Falsch! Versuchen Sie nochmal.")
#           st.markdown(f'<img src="{question_data_1_item["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
       






   
