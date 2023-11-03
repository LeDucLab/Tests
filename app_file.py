import streamlit as st


# Create a Streamlit app
st.title("Button and Text Introduction with Options")

# Add a selectbox for choosing an option
option = st.selectbox("Select an option:", ["Option 1", "Option 2", "Option 3"])

# Create a button
if st.button("Click me!"):
    # Display text based on the selected option
    if option == "Option 1":
        st.write("You chose Option 1!")
    elif option == "Option 2":
        st.write("You chose Option 2!")
    elif option == "Option 3":
        st.write("You chose Option 3!")

# You can also add more text or content below the button
st.write("This is some additional text below the button and options.")
