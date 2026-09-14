# app.py
import streamlit as st
from pages import overview, driver_profile, drivers, constructors, circuits

st.set_page_config(
    page_title="F1 ETL Project",
    page_icon="🏎️",
    layout="wide"
)

st.sidebar.title("🏎️ F1 ETL Project")
page = st.sidebar.radio("Navigate", [
    "Overview",
    "Driver Analysis",
    "Constructor Analysis",
    "Circuit & Era Analysis",
    "Driver Profile"
])


if page == "Overview":
    overview.render()

elif page == "Driver Profile":
    driver_profile.render()

elif page == "Driver Analysis":
    drivers.render()

elif page == "Constructor Analysis":
    constructors.render()

elif page == "Circuit & Era Analysis":
    circuits.render()