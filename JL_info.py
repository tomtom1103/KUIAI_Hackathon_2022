import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

def info():
    st.subheader("About the Creators🚀")
    df = pd.read_pickle("data_upload/jl.pickle")

    st.markdown('##### Journey Lee?')

    st.markdown('*전의 이씨는 옛 전의군 지역(소정면, 전의면, 전동면)을 본관으로 하는 대한민국의 한국의 성씨. 시조는 고려 초 개국 공신인 이도(李棹)인데, 초명은 치(齒)이며, 시호는 성절(聖節) 이다.*')
    st.dataframe(df)

    st.markdown('##### Thomas Lee🐱')
    st.markdown('*전의이가 전서공파 30대손*')
    st.markdown('[Github](https://github.com/tomtom1103)')
    st.markdown('[Mail](tomtom1103@korea.ac.kr)')

    st.markdown('##### John Lee‍🧑‍🚀')
    st.markdown('*전의이가 전서공파 31대손*')
    st.markdown('[Github](https://github.com/johnbuzz98)')
    st.markdown('[Mail](johnbuzz98@korea.ac.kr)')