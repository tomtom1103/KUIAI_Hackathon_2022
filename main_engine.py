from JL_utils import commercial_area, get_location_naver, subway_index_info, school_index_info, mart_index_info, get_nearest_com, get_comm_type


# input 부분 정의
def input_engine(address = "서울특별시 성북구 고려대로26길 45-4", sectors = "호프-간이주점"):
    while (True):  # ❶ 무한 반복
        # 데이터 입력
        address, sectors = str(input()), str(input())

        # 예외 처리: 주소가 잘못되었을시 다시 받음
        loc = get_location_naver(address)
        if loc == "ERROR":
            print('올바른 도로명 주소를 입력해주세요')
            continue  # ❷ while 문 본문의 시작 지점에서 다시 반복


        # 예외 처리: 업종명을 잘못 받았을 시 다시 받음
        if commercial_area(sectors) == "Error":
            print("업종을 바르게 입력하시오")
            continue  # ❷ while 문 본문의 시작 지점에서 다시 반복

        break  # ❸ 반복 중지

    return loc, sectors #WGS84(위도 경도)좌표와, 업종명을 Return



if __name__ == "__main__":
    position, sector= input_engine() #주소와 업종명 받아서 좌표와 업종명 보냄
    # 지하철, 학교, 마트 1,2,차 갯수 받아옴
    school_index_data = school_index_info(position,sector)
    subway_index_data = subway_index_info(position,sector)
    mart_index_data = mart_index_info(position,sector)

    sch1, sch2 = len(school_index_data[1]), len(school_index_data[2])
    sub1, sub2 = len(subway_index_data[1]), len(subway_index_data[2])
    mart1, mart2 = len(mart_index_data[1]), len(mart_index_data[2])

    # 근처 상권 지정
    com_zone = get_nearest_com(position)

    # 상권의 Type 지정
    com_type = get_comm_type(com_zone)

    #건축물 생애이력 데이터 (일반/집합), (용도)




    #이를 모델에 넣어줌
    #결과 plot