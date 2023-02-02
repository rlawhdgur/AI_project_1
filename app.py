# 라이브러리 
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu

# 다른 파일의 함수를 불러온다
from title import run_title
from search import run_search
from predict import run_predict
from suggestions import run_suggestions


st.title('내 방, 어디?')

selected3 = option_menu(None, ["🏠Home", "🔎전월세 검색", "📊전세 예측?",
 '💬건의사항'], 
        # icons=['house', 'cloud-upload', "list-task", 'gear'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "gray", "font-size": "15px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#47C83E"},
    }
)


if selected3 == "🏠Home":
    run_title()

elif selected3 == "🔎전월세 검색":
    run_search()

elif selected3 == "📊전세 예측?":
    run_predict()

elif selected3 == "💬건의사항":
    run_suggestions()

else:
    selected3 == "🏠Home"