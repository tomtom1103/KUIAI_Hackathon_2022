import pandas as pd
import streamlit as st

areas = ['종로구 사직동', '종로구 삼청동', '종로구 부암동', '종로구 평창동', '종로구 교남동', '종로구 가회동',
       '종로구 종로1·2·3·4가동', '종로구 종로5·6가동', '종로구 이화동', '종로구 창신1동',
       '종로구 창신2동', '종로구 숭인1동', '종로구 숭인2동', '종로구 청운효자동', '종로구 혜화동',
       '중구 소공동', '중구 회현동', '중구 명동', '중구 필동', '중구 장충동', '중구 광희동',
       '중구 을지로동', '중구 신당5동', '중구 황학동', '중구 중림동', '중구 신당동', '중구 다산동',
       '중구 약수동', '중구 청구동', '중구 동화동', '용산구 후암동', '용산구 용산2가동', '용산구 남영동',
       '용산구 원효로2동', '용산구 효창동', '용산구 용문동', '용산구 이촌1동', '용산구 이촌2동',
       '용산구 이태원1동', '용산구 이태원2동', '용산구 서빙고동', '용산구 보광동', '용산구 청파동',
       '용산구 원효로1동', '용산구 한강로동', '용산구 한남동', '성동구 왕십리2동', '성동구 마장동',
       '성동구 사근동', '성동구 행당1동', '성동구 성수1가1동', '성동구 성수1가2동', '성동구 성수2가1동',
       '성동구 성수2가3동', '성동구 송정동', '성동구 용답동', '성동구 왕십리도선동', '성동구 금호2·3가동',
       '성동구 옥수동', '광진구 화양동', '광진구 군자동', '광진구 중곡1동', '광진구 중곡2동',
       '광진구 중곡3동', '광진구 중곡4동', '광진구 능동', '광진구 구의1동', '광진구 구의2동',
       '광진구 구의3동', '광진구 광장동', '광진구 자양1동', '광진구 자양2동', '광진구 자양3동',
       '광진구 자양4동', '동대문구 회기동', '동대문구 휘경1동', '동대문구 휘경2동', '동대문구 청량리동',
       '동대문구 용신동', '동대문구 제기동', '동대문구 전농1동', '동대문구 전농2동', '동대문구 답십리2동',
       '동대문구 장안1동', '동대문구 장안2동', '동대문구 이문1동', '동대문구 이문2동', '동대문구 답십리1동',
       '중랑구 면목2동', '중랑구 면목4동', '중랑구 면목7동', '중랑구 상봉1동', '중랑구 상봉2동',
       '중랑구 중화1동', '중랑구 중화2동', '중랑구 묵1동', '중랑구 묵2동', '중랑구 망우3동',
       '중랑구 신내1동', '중랑구 면목본동', '중랑구 면목3·8동', '중랑구 망우본동', '성북구 안암동',
       '성북구 보문동', '성북구 정릉2동', '성북구 정릉3동', '성북구 정릉4동', '성북구 길음1동',
       '성북구 길음2동', '성북구 월곡1동', '성북구 월곡2동', '성북구 장위1동', '성북구 장위2동',
       '성북구 장위3동', '성북구 성북동', '성북구 삼선동', '성북구 동선동', '성북구 종암동', '성북구 석관동',
       '강북구 삼양동', '강북구 미아동', '강북구 송중동', '강북구 송천동', '강북구 삼각산동', '강북구 우이동',
       '강북구 인수동', '도봉구 쌍문1동', '도봉구 쌍문2동', '도봉구 쌍문3동', '도봉구 방학1동',
       '도봉구 방학2동', '도봉구 방학3동', '도봉구 창1동', '도봉구 창2동', '도봉구 창3동', '도봉구 창4동',
       '도봉구 창5동', '도봉구 도봉1동', '도봉구 도봉2동', '노원구 월계1동', '노원구 하계1동',
       '노원구 중계4동', '노원구 상계1동', '노원구 상계2동', '노원구 상계5동', '노원구 상계3·4동',
       '노원구 상계6·7동', '노원구 중계2·3동', '노원구 공릉1동', '은평구 녹번동', '은평구 불광1동',
       '은평구 갈현1동', '은평구 갈현2동', '은평구 구산동', '은평구 대조동', '은평구 응암1동',
       '은평구 응암2동', '은평구 신사1동', '은평구 신사2동', '은평구 증산동', '은평구 수색동',
       '은평구 불광2동', '은평구 응암3동', '은평구 역촌동', '서대문구 천연동', '서대문구 홍제1동',
       '서대문구 홍제3동', '서대문구 홍제2동', '서대문구 홍은1동', '서대문구 홍은2동', '서대문구 남가좌1동',
       '서대문구 남가좌2동', '서대문구 북가좌1동', '서대문구 북가좌2동', '서대문구 충현동', '서대문구 북아현동',
       '서대문구 신촌동', '서대문구 연희동', '마포구 용강동', '마포구 대흥동', '마포구 염리동', '마포구 신수동',
       '마포구 서교동', '마포구 합정동', '마포구 망원1동', '마포구 망원2동', '마포구 연남동',
       '마포구 성산1동', '마포구 성산2동', '마포구 상암동', '마포구 도화동', '마포구 서강동', '마포구 공덕동',
       '마포구 아현동', '양천구 목1동', '양천구 목2동', '양천구 목3동', '양천구 목4동', '양천구 신월1동',
       '양천구 신월2동', '양천구 신월3동', '양천구 신월4동', '양천구 신월5동', '양천구 신월6동',
       '양천구 신월7동', '양천구 신정1동', '양천구 신정2동', '양천구 신정3동', '양천구 신정7동',
       '양천구 신정4동', '강서구 염창동', '강서구 등촌1동', '강서구 등촌2동', '강서구 등촌3동',
       '강서구 화곡본동', '강서구 화곡2동', '강서구 화곡3동', '강서구 화곡4동', '강서구 화곡6동',
       '강서구 화곡8동', '강서구 가양1동', '강서구 발산1동', '강서구 공항동', '강서구 방화1동',
       '강서구 방화2동', '강서구 화곡1동', '강서구 우장산동', '구로구 신도림동', '구로구 구로3동',
       '구로구 구로4동', '구로구 구로5동', '구로구 고척1동', '구로구 고척2동', '구로구 개봉2동',
       '구로구 개봉3동', '구로구 오류1동', '구로구 수궁동', '구로구 가리봉동', '구로구 구로2동',
       '구로구 개봉1동', '금천구 가산동', '금천구 독산1동', '금천구 독산2동', '금천구 독산3동',
       '금천구 독산4동', '금천구 시흥1동', '금천구 시흥3동', '금천구 시흥4동', '금천구 시흥5동',
       '영등포구 여의동', '영등포구 당산1동', '영등포구 당산2동', '영등포구 양평1동', '영등포구 양평2동',
       '영등포구 신길1동', '영등포구 신길3동', '영등포구 신길4동', '영등포구 신길5동', '영등포구 신길6동',
       '영등포구 신길7동', '영등포구 대림1동', '영등포구 대림2동', '영등포구 대림3동', '영등포구 영등포본동',
       '영등포구 영등포동', '영등포구 도림동', '영등포구 문래동', '동작구 노량진2동', '동작구 상도1동',
       '동작구 상도2동', '동작구 상도3동', '동작구 상도4동', '동작구 사당1동', '동작구 사당3동',
       '동작구 사당4동', '동작구 사당5동', '동작구 대방동', '동작구 신대방1동', '동작구 신대방2동',
       '동작구 흑석동', '동작구 노량진1동', '동작구 사당2동', '관악구 보라매동', '관악구 청림동',
       '관악구 행운동', '관악구 낙성대동', '관악구 중앙동', '관악구 인헌동', '관악구 남현동', '관악구 서원동',
       '관악구 신원동', '관악구 서림동', '관악구 신사동', '관악구 신림동', '관악구 난향동', '관악구 조원동',
       '관악구 대학동', '관악구 은천동', '관악구 성현동', '관악구 청룡동', '관악구 난곡동', '관악구 삼성동',
       '관악구 미성동', '서초구 서초1동', '서초구 서초2동', '서초구 서초3동', '서초구 서초4동',
       '서초구 잠원동', '서초구 반포1동', '서초구 반포4동', '서초구 방배본동', '서초구 방배1동',
       '서초구 방배2동', '서초구 방배3동', '서초구 방배4동', '서초구 양재1동', '서초구 양재2동',
       '강남구 신사동', '강남구 논현1동', '강남구 논현2동', '강남구 삼성1동', '강남구 삼성2동',
       '강남구 대치1동', '강남구 대치4동', '강남구 역삼1동', '강남구 역삼2동', '강남구 도곡1동',
       '강남구 도곡2동', '강남구 개포4동', '강남구 일원1동', '강남구 수서동', '강남구 압구정동',
       '강남구 청담동', '강남구 대치2동', '강남구 개포2동', '송파구 풍납1동', '송파구 마천2동',
       '송파구 방이1동', '송파구 방이2동', '송파구 오륜동', '송파구 오금동', '송파구 송파1동',
       '송파구 석촌동', '송파구 삼전동', '송파구 가락본동', '송파구 가락1동', '송파구 가락2동',
       '송파구 문정1동', '송파구 문정2동', '송파구 잠실본동', '송파구 잠실6동', '송파구 잠실3동',
       '강동구 상일동', '강동구 명일1동', '강동구 명일2동', '강동구 고덕1동', '강동구 고덕2동',
       '강동구 암사2동', '강동구 암사3동', '강동구 천호1동', '강동구 천호3동', '강동구 성내1동',
       '강동구 성내2동', '강동구 성내3동', '강동구 둔촌2동', '강동구 암사1동', '강동구 천호2동',
       '강동구 길동']

colnames = ['점포수', '분기당_매출_금액', '분기당_매출_건수', '주중_매출_비율', '주말_매출_비율',
       '월요일_매출_비율', '화요일_매출_비율', '수요일_매출_비율', '목요일_매출_비율', '금요일_매출_비율',
       '토요일_매출_비율', '일요일_매출_비율', '남성_매출_비율', '여성_매출_비율', '연령대_10_매출_비율',
       '연령대_20_매출_비율', '연령대_30_매출_비율', '연령대_40_매출_비율', '연령대_50_매출_비율',
       '연령대_60_이상_매출_비율', '주중_매출_금액', '주말_매출_금액', '월요일_매출_금액', '화요일_매출_금액',
       '수요일_매출_금액', '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액',
       '남성_매출_금액',
       '여성_매출_금액', '연령대_10_매출_금액', '연령대_20_매출_금액', '연령대_30_매출_금액',
       '연령대_40_매출_금액', '연령대_50_매출_금액', '연령대_60_이상_매출_금액', '주중_매출_건수',
       '주말_매출_건수', '월요일_매출_건수', '화요일_매출_건수', '수요일_매출_건수', '목요일_매출_건수',
       '금요일_매출_건수', '토요일_매출_건수', '일요일_매출_건수',
       '남성_매출_건수', '여성_매출_건수',
       '연령대_10_매출_건수', '연령대_20_매출_건수', '연령대_30_매출_건수', '연령대_40_매출_건수',
       '연령대_50_매출_건수', '연령대_60_이상_매출_건수', '점포수']

# 주간 매출 비율, 성별 매출 비율, 연령대별 매출 비율, 주간 매출 금액, 성별 매출 금액, 연령대별 매출 금액, 주간 매출 건수, 성별 매출 건수, 연령대별 매출 건수
# 주간/성별/연령대별
# 매출 비율, 매출 금액, 매출 건수
main_col = ['분기당_매출_금액','분기당_매출_건수','점포수']
week_ratio = ['주중_매출_비율', '주말_매출_비율',
       '월요일_매출_비율', '화요일_매출_비율', '수요일_매출_비율', '목요일_매출_비율', '금요일_매출_비율',
       '토요일_매출_비율', '일요일_매출_비율']

week_sale = ['주중_매출_금액', '주말_매출_금액', '월요일_매출_금액', '화요일_매출_금액',
       '수요일_매출_금액', '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액']

week_count = ['주중_매출_건수',
       '주말_매출_건수', '월요일_매출_건수', '화요일_매출_건수', '수요일_매출_건수', '목요일_매출_건수',
       '금요일_매출_건수', '토요일_매출_건수', '일요일_매출_건수']

sex_ratio = ['남성_매출_비율', '여성_매출_비율']
sex_sale = ['남성_매출_금액', '여성_매출_금액']
sex_count = ['남성_매출_건수', '여성_매출_건수']

age_ratio = ['연령대_10_매출_비율',
       '연령대_20_매출_비율', '연령대_30_매출_비율', '연령대_40_매출_비율', '연령대_50_매출_비율',
       '연령대_60_이상_매출_비율']
age_sale = ['연령대_10_매출_금액', '연령대_20_매출_금액', '연령대_30_매출_금액',
       '연령대_40_매출_금액', '연령대_50_매출_금액', '연령대_60_이상_매출_금액']
age_count = ['연령대_10_매출_건수', '연령대_20_매출_건수', '연령대_30_매출_건수', '연령대_40_매출_건수',
       '연령대_50_매출_건수', '연령대_60_이상_매출_건수']

'''
colnames = ['분기당_매출_금액', '분기당_매출_건수', '주중_매출_비율', '주말_매출_비율',
       '월요일_매출_비율', '화요일_매출_비율', '수요일_매출_비율', '목요일_매출_비율', '금요일_매출_비율',
       '토요일_매출_비율', '일요일_매출_비율', '시간대_00~06_매출_비율', '시간대_06~11_매출_비율',
       '시간대_11~14_매출_비율', '시간대_14~17_매출_비율', '시간대_17~21_매출_비율',
       '시간대_21~24_매출_비율', '남성_매출_비율', '여성_매출_비율', '연령대_10_매출_비율',
       '연령대_20_매출_비율', '연령대_30_매출_비율', '연령대_40_매출_비율', '연령대_50_매출_비율',
       '연령대_60_이상_매출_비율', '주중_매출_금액', '주말_매출_금액', '월요일_매출_금액', '화요일_매출_금액',
       '수요일_매출_금액', '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액',
       '시간대_00~06_매출_금액', '시간대_06~11_매출_금액', '시간대_11~14_매출_금액',
       '시간대_14~17_매출_금액', '시간대_17~21_매출_금액', '시간대_21~24_매출_금액', '남성_매출_금액',
       '여성_매출_금액', '연령대_10_매출_금액', '연령대_20_매출_금액', '연령대_30_매출_금액',
       '연령대_40_매출_금액', '연령대_50_매출_금액', '연령대_60_이상_매출_금액', '주중_매출_건수',
       '주말_매출_건수', '월요일_매출_건수', '화요일_매출_건수', '수요일_매출_건수', '목요일_매출_건수',
       '금요일_매출_건수', '토요일_매출_건수', '일요일_매출_건수', '시간대_건수~06_매출_건수',
       '시간대_건수~11_매출_건수', '시간대_건수~14_매출_건수', '시간대_건수~17_매출_건수',
       '시간대_건수~21_매출_건수', '시간대_건수~24_매출_건수', '남성_매출_건수', '여성_매출_건수',
       '연령대_10_매출_건수', '연령대_20_매출_건수', '연령대_30_매출_건수', '연령대_40_매출_건수',
       '연령대_50_매출_건수', '연령대_60_이상_매출_건수', '점포수']

'''

write1 = ('''
            해당 지도는 Polygon Map 으로, GeoJson 의 Multipolygon parsing 으로 구축되었습니다. 
            '''
            '''
            각 Polygon 은 서울시의 동을 나타내며, 색이 연할수록 선택한 변수값이 크다는 것을 의미합니다.
            '''
            '''
            변수의 종류는 주간/성별/연령대별 로 대분류되며, 매출 비율/매출 금액/매출 건수로 소분류됩니다.
            '''
            '''
            각 변수는 보다 정확한 비교를 위해 정규화 작업을 진행했습니다.
            ''')

code1 = ('''
       if '매출_금액' in colname:
              df_new[f'{colname}_new_per_payment'] = (df_new[f'{colname}_new'] / seoul['분기당_매출_건수_full']) / seoul['점포수_full']
              df_new[f'{colname}_정규화'] = df_new[f'{colname}_new_per_payment'] / df_new[f'{colname}_new_per_payment'].max()

       elif '매출_건수' in colname:
              df_new[f'{colname}_new_per_store'] = df_new[f'{colname}_new'] / seoul['점포수_full']
              df_new[f'{colname}_정규화'] = df_new[f'{colname}_new'] / df_new[f'{colname}_new'].max()

       else:
              df_new[f'{colname}_정규화'] = df_new[f'{colname}_new'] / df_new[f'{colname}_new'].max()

            ''')

md1 = ('''
            해당 지도는 Polygon Map 으로, GeoJson 의 Multipolygon parsing 으로 구축되었습니다. 
            '''
            '''
            각 Polygon 은 서울시의 동을 나타내며, 색이 연할수록 선택한 변수값이 크다는 것을 의미합니다.
            '''
            '''
            변수의 종류는 주간/성별/연령대별 로 대분류되며, 매출 비율/매출 금액/매출 건수로 소분류됩니다.
            '''
            '''
            각 변수는 보다 정확한 비교를 위해 정규화 작업을 진행했습니다.
            ''')

write2 = ('''
업종별 평균 건수당 매출액은 매출 금액 / 매출 건수로 정규화 한 수치입니다.
''')

main_md1 = (
       '''
       해당 지도는 Polygon Column Map 으로, 도로명주소와 업종을 Input 으로 받아
       '''
       '''
       실시간으로 Model 연산을 수행하며 해당 점포와 주변 입지들의 예상 분기당 매출액을 계산합니다.
       '''
       '''
       사용자가 입력한 주소는 빨간 기둥으로 표시되며, 반경 500m 기준 주변 상권은 흰색 기둥으로 표시됩니다.
       '''

)
