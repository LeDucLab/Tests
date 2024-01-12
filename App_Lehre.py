import random
import streamlit as st
from PIL import Image

from pages.wbs import wbs
from pages.hboc import hboc

st.set_page_config(
    page_title='HUG - UaK',
    page_icon=':dna:',
    initial_sidebar_state='collapsed'
)

with st.sidebar:
    answer_mode_pw = st.text_input("Passwort", type="password")
    if answer_mode_pw == "schlaukopf":
        show_answers = True
    else:
        show_answers = False

st.title(":dna: UaK-WebApp der Humangenetik")

"---"
"Welcher Fall wird bearbeitet?"

tabs = st.tabs([":woman_in_lotus_position: FBREK", ":brain: ID"])

# FBREK case
with tabs[0]:
    hboc.print_hoc_part(show_answers)


# ID case
with tabs[1]:
    wbs.print_wbs_part(show_answers)