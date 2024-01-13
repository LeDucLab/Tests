import streamlit as st

# Set the title for the page
st.title("Student Quiz App")

# Define the questions
questions = [
    {
        'Question': 'What is the capital of France?',
        'Options': ['Berlin', 'Paris', 'London', 'Madrid'],
        'Answer': 'Paris',
    },
    {
        'Question': 'What is the largest planet in our solar system?',
        'Options': ['Earth', 'Jupiter', 'Mars', 'Saturn'],
        'Answer': 'Jupiter',
    },
    {
        'Question': 'Who wrote "Romeo and Juliet"?',
        'Options': ['Charles Dickens', 'Jane Austen', 'William Shakespeare', 'Mark Twain'],
        'Answer': 'William Shakespeare',
    },
]
# Use session_state to store user's progress
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

# Display the current question
st.subheader(f"Question {st.session_state.current_question + 1}:")
current_question = questions[st.session_state.current_question]
st.write(current_question['Question'])

# Display multiple-choice options
user_answer = st.radio("Your Answer:", current_question['Options'])

# Check if the answer is correct upon button click
if st.button("Submit"):
    if user_answer == current_question['Answer']:
        st.success("Correct!")
        st.session_state.score += 1
    else:
        st.warning("Incorrect! Try again.")

    st.session_state.current_question += 1

# Check if all questions have been answered
if st.session_state.current_question == len(questions):
    # Display the final score if all questions have been answered
    st.subheader("Your Final Score:")
    st.write(f"You scored {st.session_state.score} out of {len(questions)}")

    # Reset the session_state for a new quiz
    st.session_state.score = 0
    st.session_state.current_question = 0
