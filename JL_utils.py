
import requests
from haversine import haversine
from config import kakao_api

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
            df.loc[i, "위도"] = temp_loc[0]
            df.loc[i, "경도"] = temp_loc[1]
        except:
            print(f"error in {i}th row")
    return df


#하버사인 공식을 이용하여 WGS84(위도 경도)를 바탕으로 거리를 구하는 함, 단위는 m
def get_distance(start, goal):
    return haversine(get_location(start), get_location(goal),unit = 'm')