import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import math

#sales_eda_json_sparse 는 데이터 분포도 확인용.

def sales_hexagon(): #위도경도에 상권이 몇개있는지. 총 13만개

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
    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=8,
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


def normalized_polygon(): #각 동별 매출 정규화
    #df = pd.read_excel("상권 추정매출_2nd_eda.xlsx")
    df = ('https://raw.githubusercontent.com/tomtom1103/KUIAI_Hackathon_2022/main/data_upload/seouleda.json')
    #df = pd.read_pickle('seouldata.pickle')
    layer = pdk.Layer(
        'PolygonLayer',  # 사용할 Layer 타입
        df,  # 시각화에 쓰일 데이터프레임
        get_polygon='coordinates',  # geometry 정보를 담고있는 컬럼 이름
        get_fill_color='[0, 255*지역별매출정규화, 0]',  # 각 데이터 별 rgb 또는 rgba 값 (0~255)
        pickable=True,  # 지도와 interactive 한 동작 on
        auto_highlight=True  # 마우스 오버(hover) 시 박스 출력
    )

    # Set the viewport location
    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    return r

def sales_scatterplot():

    sales_eda_data = pd.read_pickle("data_upload/sales_eda_json_sparse.pkl")
    layer = pdk.Layer(
        'ScatterplotLayer',
        sales_eda_data,
        get_position='[lng, lat]',
        get_radius=50,
        get_fill_color='[255, 255, 255]',
        pickable=True,
        auto_highlight=True
    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10)

    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    return r

def sales_heatmap():
    sales_eda_data = pd.read_pickle("data_upload/sales_eda_json_sparse.pkl")

    layer = pdk.Layer(
        'HeatmapLayer',
        sales_eda_data,
        get_position='[lng, lat]',
        intensity = 0.5
    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10.5)

    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    return r

def sales_grid():
    sales_eda_data = pd.read_pickle("data_upload/sales_eda_json_sparse.pkl")

    layer = pdk.Layer(
        'CPUGridLayer',  # 대용량 데이터의 경우 'GPUGridLayer'
        sales_eda_data,
        get_position='[lng, lat]',
        pickable=True,
        auto_highlight=True,
        extruded=True,
        elevation_scale=3
    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10,
        bearing=-15,
        pitch=45
        )

    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    return r


def eda():
    st.title("Explanatory Data Analysis")
    options = ['Select Data',"Sales Data", "Polygon test", "Scatterplot test", "Heatmap test", "Gridmap test"]
    option = st.selectbox("Select EDA Type", options)

    if option == "Select Data":
        st.write("")

    elif option == 'Sales Data':
        st.header("Sales Data EDA")
        st.pydeck_chart(sales_hexagon())

    elif option == 'Polygon test':
        st.pydeck_chart(normalized_polygon())

    elif option == 'Scatterplot test':
        st.pydeck_chart(sales_scatterplot())

    elif option == "Heatmap test":
        st.pydeck_chart(sales_heatmap())

    elif option == "Gridmap test":
        st.pydeck_chart(sales_grid())