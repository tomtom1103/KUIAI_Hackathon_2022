import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

def info():
    st.subheader("About the Creatorsπ")
    df = pd.read_pickle("data_upload/jl.pickle")

    st.markdown('##### Journey Lee?')

    st.markdown('*μ μ μ΄μ¨λ μ μ μκ΅° μ§μ­(μμ λ©΄, μ μλ©΄, μ λλ©΄)μ λ³Έκ΄μΌλ‘ νλ λνλ―Όκ΅­μ νκ΅­μ μ±μ¨. μμ‘°λ κ³ λ € μ΄ κ°κ΅­ κ³΅μ μΈ μ΄λ(ζζ£Ή)μΈλ°, μ΄λͺμ μΉ(ι½)μ΄λ©°, μνΈλ μ±μ (θη―) μ΄λ€.*')
    st.dataframe(df)

    image = Image.open('data_upload/journey.jpg')
    st.image(image, caption='No sleep')

    st.markdown('##### Thomas Leeπ± (right)')
    st.markdown('*μ μμ΄κ° μ μκ³΅ν 30λμ*')
    st.markdown('[Github](https://github.com/tomtom1103)')
    st.markdown('[Mail](tomtom1103@korea.ac.kr)')

    st.markdown('##### John Leeβπ§βπ (Left)')
    st.markdown('*μ μμ΄κ° μ μκ³΅ν 31λμ*')
    st.markdown('[Github](https://github.com/johnbuzz98)')
    st.markdown('[Mail](johnbuzz98@korea.ac.kr)')