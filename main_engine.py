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
    #지하철, 학교, 마트 1,2,차 갯수 받아옴
    #근처 상권 지정
    #골목,전통,상권인지 나와야댐
    #건축물 생애이력 데이터 넣어줌
    #이를 모델에 넣어줌
    #결과 plot



for i in tqdm(range (len(df_comb_part_aug))):
    temp_up=com_list[i%63]
    df_comb_part_aug.loc[i,"업종"]=temp_up
    temp_school_info, temp_subway_info, temp_mart_info = school_index_info((df_comb_part_aug.loc[i]["위도"],df_comb_part_aug.loc[i]["경도"]),temp_up), subway_index_info((df_comb_part_aug.loc[i]["위도"],df_comb_part_aug.loc[i]["경도"]),temp_up), mart_index_info((df_comb_part_aug.loc[i]["위도"],df_comb_part_aug.loc[i]["경도"]),temp_up)
    df_comb_part_aug.loc[i,"1차_지하철_수"],df_comb_part_aug.loc[i,"2차_지하철_수"] = len(temp_subway_info[1]), len(temp_subway_info[2])
    df_comb_part_aug.loc[i,"1차_학교_수"], df_comb_part_aug.loc[i,"2차_학교_수"] = len(temp_school_info[1]), len(temp_school_info[2])
    df_comb_part_aug.loc[i,"1차_마트_수"], df_comb_part_aug.loc[i,"2차_마트_수"] = len(temp_mart_info[1]), len(temp_mart_info[2])