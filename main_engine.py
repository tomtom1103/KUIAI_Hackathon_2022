from JL_utils import commercial_area, get_location_naver


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
    a = input_engine()



