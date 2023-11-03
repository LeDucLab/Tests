import streamlit as st

# Create a Streamlit app
st.title("Button and Text Introduction App")

# Create a button
if st.button("Click me!"):
    # Display text when the button is clicked
    st.write("You clicked the button!")

# You can also add more text or content below the button
st.write("This is some additional text below the button.")

