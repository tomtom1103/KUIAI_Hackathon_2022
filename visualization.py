import pandas as pd
import geopandas as gpd
import json
from JL_utils2 import areas, colnames

#temp 가 무슨구 무슨동. pk로 사용
def refactor(colname):
    df = pd.read_pickle('data_upload/sales_eda_full.pkl')
    seoul = pd.read_pickle('data_upload/seoul_coord_data.pkl')
    #colname = '주중_매출_비율'
    adder = []
    for area in areas:
        adder.append(df.loc[df['temp'] == area, colname].sum()) #변수명을 기준으로 각 지역의 값을 합친다.

    df_new = pd.DataFrame()
    df_new['temp'] = areas
    df_new[colname + '_full'] = adder
    df_new = pd.merge(df_new, seoul, on='temp')
    df_new[f'{colname}_정규화'] = df_new[f'{colname}_full'] / df_new[f'{colname}_full'].max()

    return df_new

