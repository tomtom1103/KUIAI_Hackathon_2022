import streamlit as st
from streamlit import cli as stcli
from JL_mainpage import mainpage
from JL_info import info
from JL_EDA import eda
import sys

def journeylee_app(): #웹앱 구동함수
    #st.set_page_config(layout="wide")
    st.markdown("""
        <style>
        .big-font {
            font-size:24px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.title("Journey Lee: KUIAI Hackathon🧑‍💻")
    st.sidebar.title("Journey Lee: KUIAI Hackathon")
    app_mode = st.sidebar.radio(
        "Go to", ("Main Page", "Explanatory Data Analysis", "About the Creators🚀")
    )

    st.sidebar.info(
        '''
        Journey Lee is a collaborative effort for the 2022 KUIAI Hackathon for Korea University.
        It was made from scratch by Thomas and John Lee between the course of 72 Hours. Enjoy!🐯 
        
        '''

    )
    # 웹앱 좌측 radio button 정의부분
    if app_mode == "Main Page": #웹앱 메인페이지
        mainpage()
    elif app_mode == "Explanatory Data Analysis": #웹앱 EDA 페이지
        eda()
    elif app_mode ==  "About the Creators🚀": #웹앱 Info 페이지
        info()

if __name__ == "__main__":
    if st._is_running_with_streamlit:
        journeylee_app()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0], "--server.port", "7001"]
        sys.exit(stcli.main())
