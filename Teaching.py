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
        'Options': ['','Eine One-Size-Fits-All-Ansatz für alle Patienten', 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen', 'Die ausschließliche Verwendung traditioneller Behandlungsansätze', 'Die Maximierung der Kosteneffizienz bei medizinischen Interventionen'],
        'Answer': 'Eine individualisierte Behandlung basierend auf genetischen, molekularen und anderen individuellen Merkmalen',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/Personalisierte%20Medizin%20in%20der%20klinischen%20Genetik_v3.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/Personalisierte%20Medizin%20in%20der%20klinischen%20Genetik_v2.png',
        'QuestionType': 'multiple_choice',
    },
]


# Display the first question
for question_data in question_data_1:
    st.subheader(f"Frage 1:")
    st.write(question_data['Question'])
    user_answer_1 = st.text_input("Ihre Antwort:", key="user_answer_1")
    if st.button("Einreichen Frage 1", key="A1"):
        if any(word.lower() in question_data['Answer'].lower() for word in st.session_state.user_answer_1.split()):
            st.success("Korrekt!")
            st.markdown(f'<img src="{question_data["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
            for question_data_2 in question_data_2:
                st.subheader(f"Frage 2:")
                st.write(question_data_2['Question'])
                user_answer_2 = st.radio("Ihre Antwort:", options=question_data_2['Options'], key="user_answer_2")
                #if st.button("Einreichen Frage 2", key="A2"):
                if user_answer_2 !='':
                    if user_answer_2 == question_data_2['Answer']:
                        st.success("Korrekt!")
                        st.markdown(f'<img src="{question_data_2["CorrectImageURL"]}" alt="Korrekt" width="100%">', unsafe_allow_html=True)
                    else:
                        st.warning("Falsch! Versuchen Sie nochmal.")
                        st.markdown(f'<img src="{question_data_2["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
        else:
            st.warning("Falsch! Versuchen Sie nochmal.")
            st.markdown(f'<img src="{question_data["IncorrectImageURL"]}" alt="Falsch" width="100%">', unsafe_allow_html=True)
       






   
