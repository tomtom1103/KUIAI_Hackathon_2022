import pandas as pd
import requests
from haversine import haversine
from config import kakao_api, naver_client_id, naver_client_secert
from urllib import parse
from numpy import cos, sin, arcsin, sqrt
from math import radians

'''school_data = pd.read_csv(
    ".\전처리완료 파일\school_data_loc.csv", encoding="cp949", index_col=0)
subway_data = pd.read_csv(
    ".\전처리완료 파일\subway_data_loc.csv", encoding="cp949", index_col=0)
mart_data = pd.read_csv(
    ".\전처리완료 파일\mart_data_loc.csv", encoding="cp949", index_col=0)
com_area_data = pd.read_csv(".\전처리완료 파일\상권좌표.csv",
                          encoding="cp949",
                          usecols=["상권_코드_명","위도","경도"])'''


# KAKAO API 이용하여, 도로명 주소를 EPSG:4326 (aka WGS84, 위도 경도)로 변환
def get_location(address):
    result = ""
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    header = {'Authorization': 'KakaoAK ' + kakao_api}
    # api는 configure파일에 숨겨놓기!
    r = requests.get(url, headers=header)

    if r.status_code == 200:  # 정상 리턴만 반응
        result_address = r.json()["documents"][0]["address"]

        result = float(result_address["y"]), float(result_address["x"])
    else:
        result = "ERROR"
    return result


# 판다스 데이터 프레임을 input으로 받아 위도와 경도를 get_location 함수를 이용하여 채워주는 함수
def get_location_v2(df):
    for i in range(len(df)):
        try:
            temp_loc = get_location(df.loc[i]["도로명주소"])
            df.loc[i, "위도"], df.loc[i, "경도"] = temp_loc
        except:
            print(f"error in {i}th row")
    return df


def get_location_naver(address):  # 네이버 지도 api 를 이용하여 geocode를 받아오는 함수
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


# 하버사인 공식을 이용하여 WGS84(위도 경도)를 바탕으로 거리를 구하는 함, 단위는 m
# 좌표로도, 주소로도 둘다 받을 수 있게 정의
def get_distance(start, goal):
    if type(start) == str:
        type(start)
        print(start)
        # start = get_location(start)
    if type(goal) == str:
        type(goal)
        print(goal)
        # goal = get_location(goal)
    return haversine(start, goal, unit='m')


# 벡터방식의 거리구하기
def get_distance_vect(row, lon, lat):
    lon1 = lon
    lat1 = lat
    lon2 = row['위도']
    lat2 = row['경도']
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * arcsin(sqrt(a))
    m = 6.367 * c
    return m


# 업종별 1,2,3차 상권 거리 구간 분류 함수
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
                '인테리어': (1000, 2000),
                '일반교습학원': (1000, 2000),
                '골프연습장': (2000, 3000),
                '가방': (1000, 2000),
                '가구': (1000, 2000),
                '고시원': (1000, 2000),
                '핸드폰': (1000, 2000),
                '컴퓨터및주변장치판매': (1000, 2000),
                '외국어학원': (1000, 2000),
                '섬유제품': (1000, 2000),
                '부동산중개업': (1000, 2000),
                '자동차미용': (2000, 3000),
                '수산물판매': (500, 1000),
                '전자상거래업': (1000, 2000),
                '자동차수리': (2000, 3000),
                '서적': (1000, 2000),
                '미곡판매': (1000, 2000),
                '완구': (500, 1000),
                '자전거 및 기타운송장비': (1000, 2000),
                }

    if com_dict.get(com) == None:
        return "ERROR"
    else:
        return com_dict[com]


# 주변 학교 정보를 출력하는 함수
def school_index_info(address_input, sectors):
    school_data = pd.read_csv(
        ".\전처리완료 파일\school_data_loc.csv", encoding="cp949", usecols=["위도", "경도"])
    division = commercial_area(sectors)  # 1 2차 상권 기준
    if address_input is str:
        address_input_loc = get_location_naver(address_input)  # 입력 주소를 WGS84로 변환
    else:
        address_input_loc = address_input
    school_data["temp_dist"] = ""  # 임시로 입력주소와 각 학교간의 거리를 기록할 행 추가
    for i in range(len(school_data)):  # 각 학교와 입력주소간의 거리 계산 후 temp_dist에 등록
        school_data.loc[i, "temp_dist"] = get_distance(
            (school_data.loc[i, "위도"], school_data.loc[i, "경도"]),
            address_input_loc)
    school_data["temp_dist"] = pd.to_numeric(
        school_data["temp_dist"])  # temp dist column을 숫자형으로 바꿔줌
    min_dist_list = [school_data["temp_dist"].idxmin()
                     ]  # 가장 가까운 학교의 인덱스 리스트를 받음
    primary_zone_list = school_data[
        school_data["temp_dist"] <= division[0]].index.tolist(
    )  # 1차 상권에 포함되는 학교 인덱스 리스트
    secondary_zone_list = school_data[
        (school_data["temp_dist"] < division[1])  # 2차 상권에 포함되는 학교 인덱스 리스트
        & (school_data["temp_dist"] >= division[0])].index.tolist()
    '''tertiary_zone_list = school_data[
        school_data["temp_dist"] > division[1]].index.tolist(
        )'''  # 3차 상권에 포함되는 학교 인덱스 리스트
    return [
        min_dist_list, primary_zone_list, secondary_zone_list,
    ]  # 이를 모두 이중 리스트로 묶어 내보냄


# 주변 지하철 정보를 출력하는 함수
def subway_index_info(address_input, sectors):
    subway_data = pd.read_csv(
        ".\전처리완료 파일\subway_data_loc.csv", encoding="cp949", usecols=["위도", "경도"])
    division = commercial_area(sectors)  # 1 2차 상권 기준
    if address_input is str:
        address_input_loc = get_location_naver(address_input)  # 입력 주소를 WGS84로 변환
    else:
        address_input_loc = address_input
    subway_data["temp_dist"] = ""  # 임시로 입력주소와 각 지하철역 간의 거리를 기록할 행 추가
    for i in range(len(subway_data)):  # 각 지하철 역과 입력주소간의 거리 계산 후 temp_dist에 등록
        subway_data.loc[i, "temp_dist"] = get_distance(
            (subway_data.loc[i, "위도"], subway_data.loc[i, "경도"]),
            address_input_loc)
    subway_data["temp_dist"] = pd.to_numeric(
        subway_data["temp_dist"])  # temp dist column을 숫자형으로 바꿔줌
    min_dist_list = [subway_data["temp_dist"].idxmin()
                     ]  # 가장 가까운 지하철 역의 인덱스 리스트를 받음
    primary_zone_list = subway_data[
        subway_data["temp_dist"] <= division[0]].index.tolist(
    )  # 1차 상권에 포함되는 지하철 인덱스 리스트
    secondary_zone_list = subway_data[
        (subway_data["temp_dist"] < division[1])  # 2차 상권에 포함되는 지하철 인덱스 리스트
        & (subway_data["temp_dist"] >= division[0])].index.tolist()
    '''tertiary_zone_list = subway_data[
        subway_data["temp_dist"] > division[1]].index.tolist(
        ) '''  # 3차 상권에 포함되는 지하철 인덱스 리스트
    return [
        min_dist_list, primary_zone_list, secondary_zone_list
    ]  # 이를 모두 이중 리스트로 묶어 내보냄


# 주변 마트 정보를 출력하는 함수
def mart_index_info(address_input, sectors):
    mart_data = pd.read_csv(
        ".\전처리완료 파일\mart_data_loc.csv", encoding="cp949", usecols=["위도", "경도"])
    division = commercial_area(sectors)  # 1 2차 상권 기준
    if address_input is str:
        address_input_loc = get_location_naver(address_input)  # 입력 주소를 WGS84로 변환
    else:
        address_input_loc = address_input
    mart_data["temp_dist"] = ""  # 임시로 입력주소와 각 마트 간의 거리를 기록할 행 추가
    for i in range(len(mart_data)):  # 각 마트 역과 입력주소간의 거리 계산 후 temp_dist에 등록
        mart_data.loc[i, "temp_dist"] = get_distance(
            (mart_data.loc[i, "위도"], mart_data.loc[i, "경도"]),
            address_input_loc)
    mart_data["temp_dist"] = pd.to_numeric(
        mart_data["temp_dist"])  # temp dist column을 숫자형으로 바꿔줌
    min_dist_list = [mart_data["temp_dist"].idxmin()
                     ]  # 가장 가까운 마트 역의 인덱스 리스트를 받음
    primary_zone_list = mart_data[
        mart_data["temp_dist"] <= division[0]].index.tolist(
    )  # 1차 상권에 포함되는 마트 인덱스 리스트
    secondary_zone_list = mart_data[
        (mart_data["temp_dist"] < division[1])  # 2차 상권에 포함되는 마트 인덱스 리스트
        & (mart_data["temp_dist"] >= division[0])].index.tolist()
    '''tertiary_zone_list = mart_data[
        mart_data["temp_dist"] > division[1]].index.tolist(
        )'''  # 3차 상권에 포함되는 마트 인덱스 리스트
    return [
        min_dist_list, primary_zone_list, secondary_zone_list
    ]  # 이를 모두 이중 리스트로 묶어 내보냄


# 학교 데이터 보내주는 함수
def school_info(index_list=[], *args):
    '''['학교종류명', '설립구분', '표준학교코드', '학교명', '영문학교명', '관할조직명', '도로명우편번호', '도로명주소',
       '도로명상세주소', '전화번호', '홈페이지주소', '팩스번호', '남녀공학구분명', '고등학교구분명',
       '산업체특별학급존재여부', '고등학교일반실업구분명', '특수목적고등학교계열명', '입시전후기구분명', '주야구분명',
       '설립일자', '개교기념일', '시도교육청코드', '시도교육청명', '소재지명', '주야과정', '계열명', '학과명',
       '적재일시', '위도', '경도', 'temp_dist']'''

    school_data = pd.read_csv(
        ".\전처리완료 파일\school_data_loc.csv", encoding="cp949", index_col=0)

    return school_data.loc[index_list][list(args)]

    # 예시 school_info([1,2,3],'학교종류명', '학교명','도로명주소')


# 지하철역 데이터 보내주는 함수
def subway_info(index_list=[], *args):
    '''['역번호', '호선', '역명', '역전화번호', '도로명주소', '위도', '경도']'''
    subway_data = pd.read_csv(
        ".\전처리완료 파일\subway_data_loc.csv", encoding="cp949", index_col=0)

    return subway_data.loc[index_list][list(args)]

    # 예시 subway_info([1,2,3],'호선', '역명','도로명주소')


# 마트 데이터 보내주는 함수
def mart_info(index_list=[], *args):
    '''['개방자치단체코드', '관리번호', '인허가일자', '인허가취소일자', '영업상태코드', '영업상태명', '상세영업상태코드',
       '상세영업상태명', '전화번호', '소재지면적', '소재지우편번호', '지번주소', '도로명주소', '도로명우편번호',
       '사업장명', '최종수정일자', '데이터갱신구분', '데이터갱신일자', '업태구분명', '좌표정보(X)', '좌표정보(Y)',
       '점포구분명', '위도', '경도']'''
    mart_data = pd.read_csv(
        ".\전처리완료 파일\mart_data_loc.csv", encoding="cp949", index_col=0)
    return mart_data.loc[index_list][list(args)]

    # 예시 mart_info([1,2,3],'사업장명','전화번호','도로명주소')


# 가까운 상권을 return 하는 함수
def get_nearest_com(address_input):
    com_area_data = pd.read_csv(".\전처리완료 파일\상권좌표.csv",
                                encoding="cp949",
                                usecols=["상권_코드_명", "위도", "경도"])
    com_area_data["temp_dist"] = ""  # 임시로 상권과 입력위치간의 거리를 기록하는 column을 만듬
    for i in range(len(com_area_data)):
        com_area_data.loc[i, "temp_dist"] = get_distance(
            address_input,
            (com_area_data.loc[i, "위도"], com_area_data.loc[i, "경도"]))  # 각 상권마다의 거리를 계산해서 기록
    com_area_data["temp_dist"] = pd.to_numeric(com_area_data["temp_dist"])
    return com_area_data.loc[com_area_data["temp_dist"].idxmin(), "상권_코드_명"]  # 가장 가까운 상권명을 return


# 상권 구분 결과 return 하는 함수
def get_comm_type(comm):
    com_area_data = pd.read_csv(".\전처리완료 파일\상권좌표.csv",
                                encoding="cp949",
                                usecols=["상권_코드_명", "상권_구분_코드_명"])

    return com_area_data[com_area_data["상권_코드_명"] == comm]["상권_구분_코드_명"]


# 건축물 생애이력 데이터 (일반/집합), (용도) return 하는 함수

def get_building_info(address):
    building_data = pd.read_csv(".\전처리완료 파일\df_concat.csv",
                                encoding="cp949",
                                usecols=["도로명주소","일반/집합 구분", "용도"])

    return building_data[building_data["도로명주소"]=="서울특별시 마포구 양화로 164"][["일반/집합 구분","용도"]].values.tolist()[0]
