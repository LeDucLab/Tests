import streamlit as st
import random

# Define a list of dictionaries with questions, correct answers, options, and images
questions_data = [
    {
        'Question': 'What is the capital of France?',
        'Answer': 'Paris',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/CorrectImage.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/IncorrectImage.png',
        'QuestionType': 'fill_in',
    },
    {
        'Question': 'Who wrote "Romeo and Juliet"?',
        'Answer': 'William Shakespeare',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/CorrectImage.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/IncorrectImage.png',
        'QuestionType': 'fill_in',
    },
    {
        'Question': 'What is the largest planet in our solar system?',
        'Options': ['Jupiter', 'Mars', 'Venus'],
        'Answer': 'Jupiter',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/CorrectImage.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/IncorrectImage.png',
        'QuestionType': 'multiple_choice',
    },
    {
        'Question': 'In which year did World War II end?',
        'Options': ['1943', '1945', '1950', '1960'],
        'Answer': '1945',
        'CorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/CorrectImage.png',
        'IncorrectImageURL': 'https://github.com/LeDucLab/Tests/raw/main/Images/IncorrectImage.png',
        'QuestionType': 'multiple_choice',
    },
    # Add more questions as needed
]

# Shuffle the questions
random.shuffle(questions_data)

# Set the title for the page
st.title("Interactive Knowledge Testing App")

# Initialize variables
score = 0
current_question = 0
user_answers = {}

# Display the current question
if current_question < len(questions_data):
    st.subheader(f"Question {current_question + 1}:")
    st.write(questions_data[current_question]['Question'])

    # Check the question type
    if questions_data[current_question]['QuestionType'] == 'fill_in':
        # Get user input for the answer
        user_answer = st.text_input("Your Answer:", key=f"input_{current_question}", value=user_answers.get(f"input_{current_question}", ""))

        # Store the user's answer in the dictionary
        user_answers[f"input_{current_question}"] = user_answer

    elif questions_data[current_question]['QuestionType'] == 'multiple_choice':
        # Create radio buttons for options without a default selection
        selected_option = st.radio("Select an option:", options=questions_data[current_question]['Options'], key=f"radio_{current_question}", index=user_answers.get(f"radio_{current_question}", 0))

        # Store the user's answer in the dictionary
        user_answers[f"radio_{current_question}"] = selected_option

    # Check if the user submitted an answer
    if st.button("Submit"):
        # Check if at least one word from the user's answer matches any word in the correct answer
        if questions_data[current_question]['QuestionType'] == 'fill_in':
            if any(word.lower() in questions_data[current_question]['Answer'].lower() for word in user_answer.split()):
                st.success("Correct!")
                st.markdown(f'<img src="{questions_data[current_question]["CorrectImageURL"]}" alt="Correct" width="100%">', unsafe_allow_html=True)
                score += 1
            else:
                st.warning("Incorrect! Try again.")
                st.markdown(f'<img src="{questions_data[current_question]["IncorrectImageURL"]}" alt="Incorrect" width="100%">', unsafe_allow_html=True)
        elif questions_data[current_question]['QuestionType'] == 'multiple_choice':
            if selected_option != '':
                # Check if the selected option is correct
                if selected_option == questions_data[current_question]['Answer']:
                    st.success("Correct!")
                    st.markdown(f'<img src="{questions_data[current_question]["CorrectImageURL"]}" alt="Correct" width="100%">', unsafe_allow_html=True)
                    score += 1
                else:
                    st.warning("Incorrect! Try again.")
                    st.markdown(f'<img src="{questions_data[current_question]["IncorrectImageURL"]}" alt="Incorrect" width="100%">', unsafe_allow_html=True)
            else:
                st.warning("Please select an option.")

# Button to go to the next question
if st.button("Next Question") and current_question < len(questions_data) - 1:
    current_question += 1
    st.experimental_rerun()

# Display the final score
st.subheader("Your Final Score:")
st.write(f"You got {score} out of {len(questions_data)} questions correct.")
