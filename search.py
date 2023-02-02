# 전월세 검색 탭

import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import math

def run_search():
    st.markdown("## 전월세 검색결과")
    data = pd.read_csv('data/bds_data.csv', encoding='cp949')

    # 해당 구 선택
    gu = data['SGG_NM'].unique()
    gu_select = st.sidebar.selectbox('구를 선택해주세요', gu)
    
    # 해당 동 선택
    dong = data['BJDONG_NM'][data['SGG_NM'] == gu_select].unique()
    dong_selcet = st.sidebar.selectbox('동을 선택해주세요', dong)

    # 전월세 선택
    rent_type = data['RENT_GBN'].unique()
    type_select = st.sidebar.selectbox('전세/월세', rent_type)

    # 보증금 범위 설정
    rent_gtn_list = data['RENT_GTN'].values.tolist()
    rent_gtn_select = st.sidebar.select_slider('보증금(만단위)', 
    options = np.arange(min(rent_gtn_list), max(rent_gtn_list)+1),
    value = (min(rent_gtn_list), max(rent_gtn_list)))

    # 월세 범위 설정
    rent_fee_list = data['RENT_FEE'].values.tolist()
    rent_fee_select = st.sidebar.select_slider('월세(만단위)', 
    options = np.arange(0, max(rent_fee_list)+1),
    value = (0, max(rent_fee_list)))

    # 임대면적(평) 
    rent_area_list = data['RENT_AREA'].values.tolist()
    min_rent_list = min(rent_area_list)
    max_rent_list = max(rent_area_list)
    # 제곱미터 => 평 전환
    min_pyeong = math.floor(min_rent_list / 3.3058)
    max_pyeong = math.ceil(max_rent_list / 3.3058)
    rent_area_select = st.sidebar.select_slider('면적(평)', 
        options = np.arange(min_pyeong, max_pyeong +1),
        value = (min_pyeong, max_pyeong))
    rent_area_min = rent_area_select[0] * 3.3058
    rent_area_max = rent_area_select[1] * 3.3058

    # 버튼 생성
    if st.sidebar.button('조회'):
        gu_search = (data['SGG_NM'] == gu_select)
        dong_search = (data['BJDONG_NM'] == dong_selcet)
        type_search = (data['RENT_GBN'] == type_select)
        rent_gtn_search = (rent_gtn_select[0] <= data['RENT_GTN']) & (data['RENT_GTN'] <= rent_gtn_select[1])
        rent_fee_search = (rent_fee_select[0] <= data['RENT_FEE']) & (data['RENT_FEE'] <= rent_fee_select[1])
        rent_area_search = (rent_area_select[0]<= data['RENT_AREA']) & (data['RENT_AREA'] <= rent_area_select[1])

        # data_search에 검색한 값들만 데이터 추출
        data_search = data[gu_search & dong_search & type_search & rent_gtn_search & rent_fee_search & rent_area_search]

        # FLR_NO 컬럼 데이터에 층이란 문자열 추가
        data_search['FLR_NO'] = data_search['FLR_NO'].astype(str) + '층'
        
        # 필요없는 컬럼 삭제
        data_search = data_search.drop(['SGG_CD', 'BJDONG_CD'], axis=1)

        # 번지라는 컬럼을 만들고 'BOBN', 'BUBN' 컬럼 합치기
        # 뒤에 번지수가 0 이면 앞 번지수만 들어가게 한다
        cols = ['BOBN', 'BUBN']
        data_search['번지'] = data_search[cols].apply(lambda row: '-'.join(row.values.astype(str)) 
                                            if row['BUBN'] != 0
                                            else row['BOBN'], axis=1)

        # BLDG_NM 컬럼 데이터에 아파트, 오피스텔 있는 글자를 없애기 
        data_search['BLDG_NM'] = data_search['BLDG_NM'].str.replace("아파트", "")
        data_search['BLDG_NM'] = data_search['BLDG_NM'].str.replace("오피스텔", "")

        # 주소라는 컬럼을 만들고 그 안에 
        cols1 = ['SGG_NM', 'BJDONG_NM', '번지', 'BLDG_NM', 'HOUSE_GBN_NM', 'FLR_NO']
        data_search['주소'] = data_search[cols1].apply(lambda row:' '.join(row.values.astype(str)),axis=1)
        
        # 필요 없는 컬럼 삭제
        data_search = data_search.drop(['SGG_NM', 'BJDONG_NM', 'BOBN', 
    'BUBN', 'FLR_NO', 'BLDG_NM', '번지', 'HOUSE_GBN_NM'], axis=1)

        data_search['RENT_AREA'] = data_search['RENT_AREA'].apply(lambda x: math.trunc(x / 3.3058))
        data_search.columns = ['계약일', '전월세 구분', '임대면적(평)',
     '보증금(만원)', '임대료(만원)', '건축년도', '주소']

        data_search = data_search[['계약일', '주소', '보증금(만원)', 
     '임대료(만원)', '임대면적(평)', '건축년도', '전월세 구분']]

        data_search = data_search.reset_index(drop=True)
        data_search.index = data_search.index+1

        st.write(data_search)