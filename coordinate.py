from pyproj import Proj, transform
import pandas as pd

#!pip install pyproj

#data인자: 파일명(경로, 확장자까지), str
#from_coord_type인자: 기존좌표계. (ex: epsg:2097 (인허가정보.csv), epsg:5181 (상권영역.csv), str
#to_cood_type인자: 변형희망좌표계. (ex: lat/long is epsg:4326), str
#original_coord_colname인자: 기존 데이터 좌표계의 column names, str

def coordinate_transformer(data, from_coord_type, to_coord_type, original_xcoord_colname, original_ycoord_colname):
    print("Check type of original coordinate data. ex: epsg:2097(인허가정보.csv), epsg:5181(상권영역.csv).")
    print("Check type of target coordinate data. ex: lat/long is epsg:4326")

    if 'csv' in data:
        data = pd.read_csv(data, encoding='cp949')
    else:
        data = pd.read_excel(data)

    proj_1 = Proj(from_coord_type)
    proj_2 = Proj(to_coord_type)

    x_list=[]
    y_list=[]

    for idx, row in data.iterrows():
        x,y= row[original_xcoord_colname], row[original_ycoord_colname]
        x_,y_ = transform(proj_1, proj_2, x, y)
        x_list.append(x_)
        y_list.append(y_)

    data['위도'] = x_list
    data['경도'] = y_list

    print('Saving excel as data_new.xlsx..')
    data.to_excel(f"data_new.xlsx")
    print('done!')

if __name__ == '__main__':
    #coordinate_transformer("data/서울시 대규모 점포 정보/서울특별시 대규모점포 인허가 정보.csv","epsg:2097","epsg:4326","좌표정보(X)","좌표정보(Y)")
    pass