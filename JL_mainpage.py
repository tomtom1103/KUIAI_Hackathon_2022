import streamlit as st
import pandas as pd
import numpy as np
from JL_utils import *
from JL_utils2 import main_md1
from main_engine import main_engine
import pydeck as pdk

MAPBOX_API_KEY = st.secrets['map']

def main():

    storetype_df = pd.read_pickle('data_upload/moneypertypeofservice.pkl') #업종별 분기당 매출 Data
    storetype = storetype_df['업종'].unique().tolist()

    with st.form("main1"):
        road = st.text_input("도로명주소를 입력하세요 (실험용으로 고려대로 26길 45-4 를 입력해보세요! 고대생들의 마음의 고향 춘자입니다🍺): ")
        store = st.selectbox("업종을 선택하세요: ", storetype)

        submitted = st.form_submit_button("Submit")

        if not submitted:
            st.stop()


    coords = main_engine(road,store) #main engine 구동함수. 인자는 웹앱상 사용자에게서 받은 str 로 입력

    heat = pd.DataFrame(columns=(['lat','lng','eval_val'])) #시각화에 사용할 dataframe 정의.
    for i in range(len(coords)):
        heat.loc[i,["lat","lng","eval_val"]] = coords[i][0][0], coords[i][0][1], coords[i][1] #main engine 구동함수에서 받은 해당 점포의 예상매출값과 반경 500미터 점포들의 예상매출값 indexing

    heat['eval_norm'] = heat['eval_val']/heat['eval_val'].max() #시각화용 예상매출액 정규화

    #사용자가 입력한 도로명주소 반경 500미터 흰색 column
    layer1 = pdk.Layer(
        'ColumnLayer',
        data=heat,
        get_position='[lng, lat]',
        get_elevation='eval_norm',
        elevation_scale=1000,
        radius=15,
        get_fill_color=[255,255,255,140],
        pickable=True,
        auto_highlight=True
    )

    #사용자가 입력한 도로명주소 붉은 column
    layer2 = pdk.Layer(
        'ColumnLayer',
        data=heat.iloc[:1],
        get_position='[lng, lat]',
        get_elevation='eval_norm',
        elevation_scale=1000,
        radius=15,
        get_fill_color=[189,27,33,255],
        pickable=True,
        auto_highlight=True
    )

    center = [heat.loc[0][1], heat.loc[0][0]] #시각화 지도의 시작점을 사용자의 도로명주소로 initialize
    view_state = pdk.ViewState(
        longitude=center[0],
        latitude=center[1],
        zoom=14,
        pitch=10
        )

    #시각화용 tooltip. column 위 cursor 위치시 정보표기
    tooltip = {
        "html": "위도:<b>{lat}</b>, 경도:<b>{lng}</b>, 해당 주소의 예상 매출은 <b>{eval_val}</b> 원, 주위 상권 대비 예상매출액 비율은 <b>{eval_norm}</b>.",
        "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    }

    r = pdk.Deck(layers=[layer1,layer2],
                 map_provider='mapbox',
                 tooltip=tooltip,
                 initial_view_state=view_state)

    return r



def mainpage():
    st.subheader("Main Engine")
    #st.write('Main Engine 은 사용자가 해당 도로명주소에 해당 업종으로 창업을 한다면 분기당 예상 매출액,')
    #st.write('그리고 반경 500미터의 동종업종의 예상 매출액을 동적으로 계산하여 Interactive Map 에 시각화 하는 Tool 입니다.')
    #st.write('표시되는 모든 점포들은 서울시 우리마을가게 상권분석 Data 와 판매/제1종근린시설/제2종근린시설 건축물 생애이력 Data 를 기반으로 합니다.')
    st.code(
        '''
        Main Engine 은 사용자가 해당 도로명주소에 해당
        업종으로 창업을 한다면 분기당 예상 매출액,
        그리고 반경 500미터의 동종업종의 예상 매출액을
        동적으로 계산하여 Interactive Map 에 시각화 하는 Tool 입니다.
        표시되는 모든 점포들은 서울시 우리마을가게 상권분석 Data 와
        판매/제1종근린시설/제2종근린시설 건축물 생애이력 Data 를 기반으로 합니다!
        '''
    )

    st.pydeck_chart(main())
    st.markdown(main_md1)