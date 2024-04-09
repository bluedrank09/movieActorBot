import streamlit as st

input = st.text_input("Input")
submit = st.button("submit")

if submit:
    if input == "":
        print("No input")
        message = st.text_area = "Please input a name"
        st.write(message)

#         txt = st.text_area(
#             "Text to analyze",
#             "It was the best of times, it was the worst of times, it was the age of "
#             "wisdom, it was the age of foolishness, it was the epoch of belief, it "
#             "was the epoch of incredulity, it was the season of Light, it was the "
#             "season of Darkness, it was the spring of hope, it was the winter of "
#             "despair, (...)",
#             )

#         st.write(f'You wrote {len(txt)} characters.')

# import streamlit as st

# txt = st.text_area("lol this is a text area")\\

import streamlit as st

