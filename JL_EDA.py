import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from JL_utils2 import *
import altair as alt

MAPBOX_API_KEY = st.secrets['map']  #Mapbox API Token

def sales_hexagon():

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
        )

    tooltip = {
        "html": "위도:<b>{lat}</b>, 경도:<b>{lng}</b>",
        "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    }


    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip = tooltip)
    return r


def polygon():

    df = pd.read_pickle('data_upload/sales_eda_full.pkl') #전체 매출 Data
    seoul = pd.read_pickle('data_upload/seoul_coord_data.pkl') #서울시 동별 Multipolygon GeoJson 정보
    colname = st.selectbox('보고싶은 Data 를 선택하세요:', colnames)

    adder = []
    for area in areas:
        adder.append(df.loc[df['temp'] == area, colname].sum())  # 변수명을 기준으로 각 지역의 값을 합친다.

    df_new = pd.DataFrame()
    df_new['temp'] = areas
    df_new[colname + '_new'] = adder
    df_new = pd.merge(df_new, seoul, on='temp')

    if '매출_금액' in colname:
        df_new[f'{colname}_new_per_payment'] = (df_new[f'{colname}_new'] / seoul['분기당_매출_건수_full']) / seoul['점포수_full'] #매출금액 데이터는 해당 동의 매출건수와 점포수로 나눠준다
        df_new[f'{colname}_정규화'] = df_new[f'{colname}_new_per_payment'] / df_new[f'{colname}_new_per_payment'].max() #그리고 정규화

    elif '매출_건수' in colname:
        df_new[f'{colname}_new_per_store'] = df_new[f'{colname}_new'] / seoul['점포수_full'] #매출건수 데이터는 해당 동의 점포수로 나눠준다
        df_new[f'{colname}_정규화'] = df_new[f'{colname}_new'] / df_new[f'{colname}_new'].max() #정규화

    else:
        df_new[f'{colname}_정규화'] = df_new[f'{colname}_new'] / df_new[f'{colname}_new'].max() #매출비율 데이터는 바로 정규화

    layer = pdk.Layer(
        'PolygonLayer',
        df_new,
        get_polygon='coordinates',
        get_fill_color=f'[0, 1000*{colname}_정규화 ,0]',
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

    tooltip = {
        "html": "<b>{temp}</b>, 분기당 매출 건수:<b>{분기당_매출_건수_full}</b>, 점포수: <b>{점포수_full}",
        "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    }


    r = pdk.Deck(layers=[layer],
                 map_provider='mapbox',
                 tooltip=tooltip,
                 initial_view_state=view_state)
    return r

def static():
    df = pd.read_pickle('data_upload/moneypertypeofservice.pkl')
    cols = df.columns.tolist()
    cols = cols[1:]

    data = st.selectbox('확인할 Data 를 선택하세요: ', cols)
    chart = (
        alt.Chart(
            df,
            title=f"{data}",
        )
            .mark_bar()
            .encode(
            x=alt.X(f"{data}", title="VALUES"),
            y=alt.Y("업종", sort=alt.EncodingSortField(field=f"{data}", order="descending")),
            tooltip=["업종", "업종별_분기당_매출_건수", "업종별_분기당_매출_금액(억원)","업종별_평균_건수당_매출액(만원)"],
        )
    )
    st.altair_chart(chart, use_container_width=True)

def eda():
    st.subheader("Explanatory Data Analysis")
    options = ['동별 Polygon 분석', '업종별 Altair 분석', '서울시 상권 분포 Hexagon Visualization']
    option = st.selectbox("Select EDA Type", options)

    if option == "동별 Polygon 분석":
        st.pydeck_chart(polygon())
        st.write(write1)

        st.markdown('##### Snippet')

        code = code1
        st.code(code,language='python')

    elif option == '업종별 Altair 분석':
        static()
        st.write(write2)

    elif option =='서울시 상권 분포 Hexagon Visualization':
        st.pydeck_chart(sales_hexagon())
