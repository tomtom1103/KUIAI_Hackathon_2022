import streamlit as st
import pandas as pd
import numpy as np
from JL_utils import *
from main_engine import main_engine

def main():
    df = pd.read_pickle('data_upload/sales_eda_full.pkl')
    seoul_df = pd.read_pickle('data_upload/seoul_coord_data.pkl')
    storetype_df = pd.read_pickle('data_upload/moneypertypeofservice.pkl')
    storetype = storetype_df['업종'].unique().tolist()

    with st.form("main1"):
        road = st.text_input("도로명주소를 입력하세요: ")
        store = st.selectbox("업종을 선택하세요: ", storetype)

        submitted = st.form_submit_button("Submit")

        if not submitted:
            st.stop()

    st.write('test')
    #main_engine(road, store)

    st.write(main_engine(road, store))


def mainpage():
    st.subheader("Main Engine")

    st.pydeck_chart(main())