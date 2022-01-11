import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import math

def sales():

    # 2014 locations of car accidents in the UK

    sales_eda_data = pd.read_pickle("data_upload/sales_eda_json_sparse.pkl")
    # Define a layer to display on a map
    layer = pdk.Layer(
        'HexagonLayer',
        sales_eda_data,
        #get_position=["lng", "lat"],
        get_position='[lng,lat]',
        auto_highlight=True,
        elevation_scale=50,
        pickable=True,
        elevation_range=[0, 3000],
        extruded=True,
        coverage=1
        )

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=126.5924,
        latitude=37.3336,
        zoom=10,
        min_zoom=5,
        max_zoom=15,
        pitch=40.5,
        bearing=-27.36
        )

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    #r.to_html('demo.html')
    #r.show()
    return r


def eda():
    st.title("Explanatory Data Analysis")
    options = ["Sales Data", "Test"]
    option = st.selectbox("Select EDA Type", options)
    if option == 'Sales Data':
        st.header("Sales Data EDA")
        st.pydeck_chart(sales())

    elif option == 'Test':
        st.write("TEST")


