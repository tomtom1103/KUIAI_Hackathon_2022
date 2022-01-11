import pandas as pd
import requests
from haversine import haversine
from config import kakao_api, naver_client_id, naver_client_secert
from urllib import parse

school_data = pd.read_csv(
    ".\전처리완료 파일\school_data_loc.csv", encoding="cp949", index_col=0)
subway_data = pd.read_csv(
    ".\전처리완료 파일\subway_data_loc.csv", encoding="cp949", index_col=0)


#KAKAO API 이용하여, 도로명 주소를 EPSG:4326 (aka WGS84, 위도 경도)로 변환
def get_location(address):
    result = ""
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    header = {'Authorization': 'KakaoAK ' + kakao_api}
    #api는 configure파일에 숨겨놓기!
    r = requests.get(url, headers=header)

    if r.status_code == 200: #정상 리턴만 반응
        result_address = r.json()["documents"][0]["address"]

        result = float(result_address["y"]), float(result_address["x"])
    else:
        result = "ERROR"
    return result

#판다스 데이터 프레임을 input으로 받아 위도와 경도를 get_location 함수를 이용하여 채워주는 함수
def get_location_v2(df):
    for i in range(len(df)):
        try:
            temp_loc = get_location(df.loc[i]["도로명주소"])
            df.loc[i, "위도"], df.loc[i, "경도"] = temp_loc
        except:
            print(f"error in {i}th row")
    return df


def get_location_naver(address):
    url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=' + parse.quote(
        address)
    header = {
        'X-NCP-APIGW-API-KEY-ID': naver_client_id,
        'X-NCP-APIGW-API-KEY': naver_client_secert
    }
    r = requests.get(url, headers=header)

    if r.status_code == 200:  # 정상 리턴만 반응
        if r.json()['addresses'][0] == []:
            latitude = None
            longitude = None
        else:
            latitude = r.json()['addresses'][0]['y']
            longitude = r.json()['addresses'][0]['x']

        result = (float(latitude), float(longitude))
    else:
        result = "ERROR"
    return result



#하버사인 공식을 이용하여 WGS84(위도 경도)를 바탕으로 거리를 구하는 함, 단위는 m
#좌표로도, 주소로도 둘다 받을 수 있게 정의
def get_distance(start, goal):
    if type(start) == str:
        type(start)
        print(start)
        #start = get_location(start)
    if type(goal) == str:
        type(goal)
        print(goal)
        #goal = get_location(goal)
    return haversine(start, goal, unit='m')