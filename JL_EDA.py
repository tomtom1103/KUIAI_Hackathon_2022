import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from JL_utils2 import *
import altair as alt
from visualization import refactor

#sales_eda_json_sparse 는 데이터 분포도 확인용.

MAPBOX_API_KEY = st.secrets['map']

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

# 주간/성별/연령대별
# 매출 비율, 매출 금액, 매출 건수


def polygon():

    df = pd.read_pickle('data_upload/sales_eda_full.pkl')
    seoul = pd.read_pickle('data_upload/seoul_coord_data.pkl')
    ch_1 = ['Select', '주간', '성별', '연령대별']
    ch_2 = ['Select', '매출 비율', '매출 금액', '매출 건수']

    '''
    with st.form('form'):

        o1 = st.selectbox('보고싶은 Data 대분류:', ch_1)
        o2 = st.selectbox('보고싶은 Data 중분류:', ch_2)

        option1 = o1+' '+o2
        submitted = st.form_submit_button("Submit")

        if submitted:

            if '주간 매출 비율' in option1:
                cl = st.selectbox('보고싶은 Data 를 선택하세요:', week_ratio)

            elif '주간 매출 금액' in option1:
                cl = st.selectbox('보고싶은 Data 를 선택하세요:', week_sale)

            elif '주간 매출 건수' in option1:
                cl = st.selectbox('보고싶은 Data 를 선택하세요:', week_count)

            elif '성별 매출 비율' in option1:
                cl = st.selectbox('보고싶은 Data 를 선택하세요:', sex_ratio)

            elif '성별 매출 금액' in option1:
                cl = st.selectbox('보고싶은 Data 를 선택하세요:', sex_sale)

            elif '성별 매출 건수' in option1:
                cl = st.selectbox('보고싶은 Data 를 선택하세요:', sex_count)

            elif '연령대별 매출 비율' in option1:
                cl = st.selectbox('보고싶은 Data 를 선택하세요:', age_ratio)

            elif '연령대별 매출 금액' in option1:
                cl = st.selectbox('보고싶은 Data 를 선택하세요:', age_sale)

            elif '연령대별 매출 건수' in option1:
                cl = st.selectbox('보고싶은 Data 를 선택하세요:', age_count)


            colname = cl
            submitted = st.form_submit_button("Run")

            if submitted:
    '''

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

    r = pdk.Deck(layers=[layer],
                 #map_style='mapbox://styles/mapbox/outdoors-v11',
                 #mapbox_key=MAPBOX_API_KEY,
                 map_provider='mapbox',
                 initial_view_state=view_state)
    return r

def static():
    df = pd.read_pickle('data_upload/moneypertypeofservice.pkl')
    storetype = df['업종'].unique().tolist()
    cols = df.columns.tolist()
    cols = cols[1:]

    data = st.selectbox('확인할 Data 를 선택하세요: ', cols)

    stores = st.multiselect(
        "서울시 주요 업종들", options=storetype, default=storetype
    )
    #df['업종'] = df['업종'].isin(stores)
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
    options = ['Select Data','동별 Polygon 분석','업종별 Altair 분석','hextest']
    option = st.selectbox("Select EDA Type", options)

    if option == "동별 Polygon 분석":
        st.pydeck_chart(polygon())
        st.write(write1)

        st.markdown('##### Snippet')

        code = code1
        st.code(code,language='python')

        st.markdown(md1)

    elif option == '업종별 Altair 분석':
        static()
        st.write(write2)

    elif option =='hextest':
        st.pydeck_chart(sales_hexagon())


# 주간/성별/연령대별
# 매출 비율, 매출 금액, 매출 건수
