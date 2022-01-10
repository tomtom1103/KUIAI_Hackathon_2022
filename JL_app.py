import streamlit as st
from streamlit import cli as stcli
from JL_mainpage import mainpage
from JL_info import info
import sys

def journeylee_app():
    #st.set_page_config(layout="wide")
    st.markdown("""
        <style>
        .big-font {
            font-size:24px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.title("Journey Lee: KUIAI Hackathon")
    st.sidebar.title("Journey Lee: KUIAI Hackathon")
    app_mode = st.sidebar.radio(
        "Go to", ("Main Page", "Journey Lee Info")
    )

    st.sidebar.info(
        "Journey Lee: KUIAI Hackathon"
        ""
        "Jong Hyun Lee"
        ""
        "Woo Jun Lee"

    )

    if app_mode == "Gillajab-i!":
        mainpage()
    elif app_mode == "Gillajab-i Info":
        info()

if __name__ == "__main__":
    if st._is_running_with_streamlit:
        journeylee_app()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0], "--server.port", "7001"]
        sys.exit(stcli.main())
