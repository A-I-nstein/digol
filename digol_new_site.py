#####-----importing neccessary libraries-----#####

import imutils
import streamlit as st
from digol_backend import *

#####-----UI Elements-----#####

# configuring site

st.set_page_config(layout="wide", page_title="Digital Olfaction")

hide_streamlit_style = """
                   <style>
                   #MainMenu {visibility: hidden;}
                   footer {visibility: hidden;}
                   </style>
                   """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# title page

st.markdown('<h1 style = " font-size: 50px; text-align:center; font-weight:bold">Fragrance Recommendation System</h1>', unsafe_allow_html=True)
st.markdown('<h1 style = " font-size: 25px; text-align:center; font-weight:bold">A Tool for Digital Olfaction</h1>', unsafe_allow_html=True)
st.text("")

# configuring sidebar

method = st.sidebar.radio(
    "Suggest fragrances based on?",
    ("Fragrance", "Base notes")
)



# configuring main page

base_notes = load_base_notes()
fragrances = load_fragrances()

fragrance_page = st.container()
base_notes_page = st.container()

#####-----suggest fragrances based on a fragrance-----#####

if (method == "Fragrance"):

    with fragrance_page:
        st.markdown('<h1 style = " font-size: 40px; text-align:center; font-weight:bold">Find fragrances based on a fragrance</h1>', unsafe_allow_html=True)
        st.markdown("""---""")
        selected_fragrance = st.selectbox('Select your favourite fragrance', fragrances)
        st.write("")
        predict = st.button("Find similar Fragrances")
        st.write("")

        if predict:
            progress_bar = st.progress(0)

            st.markdown("""---""")
            st.markdown('<h1 style = " font-size: 40px; text-align:center; font-weight:bold">Similar Fragrances</h1>', unsafe_allow_html=True)
            st.markdown("""---""")
            suggested_fragrances = fragrance_to_fragrance(selected_fragrance)
            progress_bar.progress(50)

            fragrance_1 = st.container()
            st.markdown("""---""")
            fragrance_2 = st.container()
            st.markdown("""---""")
            fragrance_3 = st.container()

            progress_bar.progress(60)

            with fragrance_1:
                col1, col2, col3 = st.columns([2, 1, 3])
                title = col1.container()
                image = col2.container()
                details = col3.container()
                try:
                    with title:
                        st.subheader(suggested_fragrances[0][0])
                    with image:
                        st.image(imutils.url_to_image(suggested_fragrances[0][5]))
                    with details:
                        st.write("**BRAND:** " + suggested_fragrances[0][6])
                        st.write("**BASE NOTES:** " + suggested_fragrances[0][1])
                        st.write("**SECONDARY NOTES:** " + suggested_fragrances[0][2])
                        st.write("**GENDER:** " + suggested_fragrances[0][3])
                        st.write("**AGE:** " + suggested_fragrances[0][4])
                except Exception as e:
                    print(e)
                    st.error("Could not load fragrance")

            with fragrance_2:
                col1, col2, col3 = st.columns([2, 1, 3])
                title = col1.container()
                image = col2.container()
                details = col3.container()
                try:
                    with title:
                        st.subheader(suggested_fragrances[1][0])
                    with image:
                        st.image(imutils.url_to_image(suggested_fragrances[1][5]))
                    with details:
                        st.write("**BRAND:** " + suggested_fragrances[1][6])
                        st.write("**BASE NOTES:** " + suggested_fragrances[1][1])
                        st.write("**SECONDARY NOTES:** " + suggested_fragrances[1][2])
                        st.write("**GENDER:** " + suggested_fragrances[1][3])
                        st.write("**AGE:** " + suggested_fragrances[1][4])
                except Exception as e:
                    print(e)
                    st.error("Could not load fragrance")

            with fragrance_3:
                col1, col2, col3 = st.columns([2, 1, 3])
                title = col1.container()
                image = col2.container()
                details = col3.container()
                try:
                    with title:
                        st.subheader(suggested_fragrances[2][0])
                    with image:
                        st.image(imutils.url_to_image(suggested_fragrances[2][5]))
                    with details:
                        st.write("**BRAND:** " + suggested_fragrances[2][6])
                        st.write("**BASE NOTES:** " + suggested_fragrances[2][1])
                        st.write("**SECONDARY NOTES:** " + suggested_fragrances[2][2])
                        st.write("**GENDER:** " + suggested_fragrances[2][3])
                        st.write("**AGE:** " + suggested_fragrances[2][4])
                except Exception as e:
                    print(e)
                    st.error("Could not load fragrance")

            progress_bar.progress(100)

#####-----suggest fragrances based on base notes-----#####

else:

    with base_notes_page:
        st.markdown('<h1 style = " font-size: 40px; text-align:center; font-weight:bold">Find fragrances based on base notes</h1>', unsafe_allow_html=True)
        st.markdown("""---""")
        # configuring user data collection page

        col1, col2 = st.columns(2)
        gender_container = col1.container()
        age_container = col2.container()

        with gender_container:
            st.subheader("Gender")
            gender = st.radio(
                "Suggest fragrances for",
                ("Male", "Female", "Unisex")
            )

        with age_container:
            st.subheader("Age")
            age = st.radio(
                "Suggest fragrances for people",
                ("< 25", "> 25")
            )

        st.write("")
        st.subheader("Base Notes")
        selected_base_notes = st.multiselect('Select a minimum of 1 base note', base_notes)
        st.write("")
        predict = st.button("Find similar Fragrances")
        st.write("")

        if predict:
            if len(selected_base_notes)<1:
                st.error("Please select a minimum of 1 base note")
            else:
                progress_bar = st.progress(0)

                st.markdown("""---""")
                st.markdown('<h1 style = " font-size: 40px; text-align:center; font-weight:bold">Similar Fragrances</h1>', unsafe_allow_html=True)
                st.markdown("""---""")
                suggested_fragrances = base_notes_to_fragrance(selected_base_notes, gender, age)
                progress_bar.progress(50)

                fragrance_1 = st.container()
                st.markdown("""---""")
                fragrance_2 = st.container()
                st.markdown("""---""")
                fragrance_3 = st.container()

                progress_bar.progress(60)

                with fragrance_1:
                    col1, col2, col3 = st.columns([2, 1, 3])
                    title = col1.container()
                    image = col2.container()
                    details = col3.container()
                    try:
                        with title:
                            st.subheader(suggested_fragrances[0][0])
                        with image:
                            st.image(imutils.url_to_image(suggested_fragrances[0][5]))
                        with details:
                            st.write("**BRAND:** " + suggested_fragrances[0][6])
                            st.write("**BASE NOTES:** " + suggested_fragrances[0][1])
                            st.write("**SECONDARY NOTES:** " + suggested_fragrances[0][2])
                            st.write("**GENDER:** " + suggested_fragrances[0][3])
                            st.write("**AGE:** " + suggested_fragrances[0][4])
                    except Exception as e:
                        print(e)
                        st.error("Could not load fragrance")

                with fragrance_2:
                    col1, col2, col3 = st.columns([2, 1, 3])
                    title = col1.container()
                    image = col2.container()
                    details = col3.container()
                    try:
                        with title:
                            st.subheader(suggested_fragrances[1][0])
                        with image:
                            st.image(imutils.url_to_image(suggested_fragrances[1][5]))
                        with details:
                            st.write("**BRAND:** " + suggested_fragrances[1][6])
                            st.write("**BASE NOTES:** " + suggested_fragrances[1][1])
                            st.write("**SECONDARY NOTES:** " + suggested_fragrances[1][2])
                            st.write("**GENDER:** " + suggested_fragrances[1][3])
                            st.write("**AGE:** " + suggested_fragrances[1][4])
                    except Exception as e:
                        print(e)
                        st.error("Could not load fragrance")

                with fragrance_3:
                    col1, col2, col3 = st.columns([2, 1, 3])
                    title = col1.container()
                    image = col2.container()
                    details = col3.container()
                    try:
                        with title:
                            st.subheader(suggested_fragrances[2][0])
                        with image:
                            st.image(imutils.url_to_image(suggested_fragrances[2][5]))
                        with details:
                            st.write("**BRAND:** " + suggested_fragrances[2][6])
                            st.write("**BASE NOTES:** " + suggested_fragrances[2][1])
                            st.write("**SECONDARY NOTES:** " + suggested_fragrances[2][2])
                            st.write("**GENDER:** " + suggested_fragrances[2][3])
                            st.write("**AGE:** " + suggested_fragrances[2][4])
                    except Exception as e:
                        print(e)
                        st.error("Could not load fragrance")

                progress_bar.progress(100)
