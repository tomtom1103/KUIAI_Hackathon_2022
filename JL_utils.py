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


#업종별 1,2,3차 상권 거리 구간 분류 함수
'''
※ 참고자료
성공창업에 이르는길
발행처 : 서울특별시
 '''
def commercial_area(com):
    com_dict = {'한식음식점': (500, 1000),
     '중식음식점': (500, 1000),
     '커피-음료': (500, 1000),
     '예술학원': (500, 1000),
     '미용실': (1000, 2000),
     '세탁소': (500, 1000),
     '슈퍼마켓': (500, 1000),
     '편의점': (500, 1000),
     '의료기기': (2000, 3000),
     '패스트푸드점': (1000, 2000),
     '분식전문점': (1000, 2000),
     '스포츠 강습': (2000, 3000),
     '일반의원': (2000, 3000),
     '치과의원': (2000, 3000),
     '네일숍': (1000, 2000),
     '가전제품수리': (2000, 3000),
     '노래방': (1000, 2000),
     '육류판매': (1000, 2000),
     '반찬가게': (500, 1000),
     '일반의류': (1000, 2000),
     '안경': (1000, 2000),
     '의약품': (2000, 3000),
     '애완동물': (1000, 2000),
     '가전제품': (1000, 2000),
     '철물점': (1000, 2000),
     '조명용품': (1000, 2000),
     '일식음식점': (1000, 2000),
     '양식음식점': (1000, 2000),
     '제과점': (1000, 2000),
     '치킨전문점': (500, 1000),
     '호프-간이주점': (500, 1000),
     '한의원': (2000, 3000),
     '당구장': (1000, 2000),
     'PC방': (1000, 2000),
     '스포츠클럽': (2000, 3000),
     '피부관리실': (2000, 3000),
     '여관': (1000, 2000),
     '청과상': (1000, 2000),
     '신발': (1000, 2000),
     '시계및귀금속': (1000, 2000),
     '문구': (500, 1000),
     '화장품': (1000, 2000),
     '운동/경기용품': (1000, 2000),
     '화초': (1000, 2000),
     '인테리어':(1000, 2000),
     '일반교습학원': (1000, 2000),
     '골프연습장': (2000, 3000),
     '가방': (1000, 2000),
     '가구': (1000, 2000),
     '고시원': (1000, 2000),
     '핸드폰': (1000, 2000),
     '컴퓨터및주변장치판매': (1000, 2000),
     '외국어학원': (1000, 2000),
     '섬유제품': (1000, 2000),
     '부동산중개업':(1000, 2000),
     '자동차미용': (2000, 3000),
     '수산물판매': (500, 1000),
     '전자상거래업': (1000, 2000),
     '자동차수리': (2000, 3000),
     '서적': (1000, 2000),
     '미곡판매': (1000, 2000),
     '완구': (500, 1000),
     '자전거 및 기타운송장비': (1000, 2000),
     '기타': (1000, 2000)}

    return com_dict.keys(com)
