# 홈 탭

# 라이브러리 import
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

def run_title():
    # 서울시공공데이터에서 인증키를 받아 데이터를 받아옴
    # https://data.seoul.go.kr/dataList/OA-21276/S/1/datasetView.do
    # 인증키 : 4d42486779706d3034365957634870
    data = pd.read_csv('data/bds_data.csv', encoding='cp949')
    st.markdown("## 실거래 현황")
    st.write(data)

    # 컬럼을 두개 나눔
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("월세 실거래수 지역 순위")
        data_m = data[data['RENT_GBN']=='월세']
        cols = ['SGG_NM', 'BJDONG_NM']
        data_m['주소'] = data_m[cols].apply(lambda row:' '.join(row.values.astype(str)),axis=1)
        data_addr = data_m['주소'].value_counts().rename_axis('주소').reset_index(name='거래 수')
        data_addr = data_addr.reset_index(drop=True)
        data_addr.index = data_addr.index+1
        st.write(data_addr.head(10))
    with col2:
        st.subheader("전세 실거래수 지역 순위")
        data_m = data[data['RENT_GBN']=='전세']
        cols = ['SGG_NM', 'BJDONG_NM']
        data_m['주소'] = data_m[cols].apply(lambda row:' '.join(row.values.astype(str)),axis=1)
        data_addr = data_m['주소'].value_counts().rename_axis('주소').reset_index(name='거래 수')
        data_addr = data_addr.reset_index(drop=True)
        data_addr.index = data_addr.index+1
        st.write(data_addr.head(10))
