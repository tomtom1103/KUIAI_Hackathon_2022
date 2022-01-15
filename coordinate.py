from pyproj import Proj, transform
import pandas as pd

#!pip install pyproj

#Check type of original coordinate data. ex: epsg:2097, epsg:5181
#Check type of target coordinate data. ex: lat/long is epsg:4326

def coordinate_transformer(data, from_coord_type, to_coord_type, original_xcoord_colname, original_ycoord_colname):

    if 'csv' in data:
        data = pd.read_csv(data, encoding='cp949')
    elif 'xlsx' in data:
        data = pd.read_excel(data)

    elif 'pkl' in data:
        data = pd.read_pickle(data)

    proj_1 = Proj(from_coord_type)
    proj_2 = Proj(to_coord_type)

    x_list=[]
    y_list=[]

    for idx, row in data.iterrows():
        x,y= row[original_xcoord_colname], row[original_ycoord_colname]
        x_,y_ = transform(proj_1, proj_2, x, y)
        x_list.append(x_)
        y_list.append(y_)

    data['lat'] = x_list
    data['lng'] = y_list

    print('Saving excel as data_new.pkl..')
    data.to_pickle(f"data_new.pkl")
    print('done!')
