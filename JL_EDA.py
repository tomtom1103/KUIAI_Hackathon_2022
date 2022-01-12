import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import math
from config import map
from JL_utils2 import colnames, areas
from visualization import refactor

#sales_eda_json_sparse 는 데이터 분포도 확인용.

MAPBOX_API_KEY = map

def sales_hexagon(): #위도경도에 상권이 몇개있는지. 총 13만개

    sales_eda_data = pd.read_pickle("data_upload/sales_eda_json_sparse.pkl")
    layer = pdk.Layer(
        'HexagonLayer',
        sales_eda_data,
        get_position='[lng,lat]',
        auto_highlight=True,
        elevation_scale=20,
        pickable=True,
        elevation_range=[0, 3000],

        coverage=1
        )

    # Set the viewport location
    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10
        #pitch=40.5,
        #bearing=-27.36
        )

    r = pdk.Deck(layers=[layer], initial_view_state=view_state)
    return r


def normalized_polygon(): #각 동별 매출 정규화
    df = pd.read_pickle('data_upload/sales_eda_3rd.pkl')

    layer = pdk.Layer(
        'PolygonLayer',
        df,
        get_polygon='coordinates',
        get_fill_color='[0, 800*지역별매출정규화,0]',
        pickable=True,
        auto_highlight=True,
        extruded=True,


    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10

        )


    r = pdk.Deck(layers=[layer],
                 #map_style='mapbox://styles/mapbox/outdoors-v11',
                 #mapbox_key=MAPBOX_API_KEY,
                 map_provider='mapbox',
                 initial_view_state=view_state)
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

    r = pdk.Deck(layers=[layer],
                 initial_view_state=view_state,
                 )
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

def full():
    df = pd.read_pickle('data_upload/sales_eda_full.pkl')
    seoul = pd.read_pickle('data_upload/seoul_coord_data.pkl')
    colname = st.selectbox('보고싶은 정보를 선택하세요:', colnames)

    adder = []
    for area in areas:
        adder.append(df.loc[df['temp'] == area, colname].sum())  # 변수명을 기준으로 각 지역의 값을 합친다.

    df_new = pd.DataFrame()
    df_new['temp'] = areas
    df_new[colname + '_full'] = adder
    df_new = pd.merge(df_new, seoul, on='temp')
    df_new[f'{colname}_정규화'] = df_new[f'{colname}_full'] / df_new[f'{colname}_full'].max()

    layer = pdk.Layer(
        'PolygonLayer',
        df_new,
        get_polygon='coordinates',
        get_fill_color=f'[0, 800*{colname}_정규화 ,0]',
        pickable=True,
        auto_highlight=True,
        extruded=True,


    )

    center = [126.986, 37.565]
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=10

        )

    r = pdk.Deck(layers=[layer],
                 #map_style='mapbox://styles/mapbox/outdoors-v11',
                 #mapbox_key=MAPBOX_API_KEY,
                 map_provider='mapbox',
                 initial_view_state=view_state)
    return r




def eda():
    st.title("Explanatory Data Analysis")
    options = ['Select Data',"전체 상권의 분포도", "동별 매출 비율", "Scatterplot test", "Heatmap test", "Gridmap test",'full']
    option = st.selectbox("Select EDA Type", options)

    if option == "Select Data":
        st.write("")

    elif option == '전체 상권의 분포도':
        st.header("전체 상권의 분포도")
        st.pydeck_chart(sales_hexagon())
        st.write(
            '''
            이 Hexagon Map 은 약 13만개의 판매시설, 제 1종 근린시설, 제 2종 근린시설의 서울 분포도를 나타냅니다.
            '''

        )

    elif option == '동별 매출 비율':
        st.header("동별 매출 비율")
        st.pydeck_chart(normalized_polygon())
        st.write(
            '''
            이 Polygon Map은 서울의 동별 상권의 매출을 정규화한 비율을 나타냅니다.
            '''
            '''
            색이 짙을수록 분기당 더 높은 매출을 보였습니다.
            '''

        )

    elif option == 'Scatterplot test':
        st.pydeck_chart(sales_scatterplot())

    elif option == "Heatmap test":
        st.pydeck_chart(sales_heatmap())

    elif option == "Gridmap test":
        st.pydeck_chart(sales_grid())

    elif option == 'full':
        st.pydeck_chart(full())