import streamlit as st
import pandas as pd
from shareplum import Office365
from shareplum import Site
from shareplum.site import Version
from io import StringIO 

@st.cache_data
def get_authcookie():
    authcookie = Office365('https://wholesumbrands.sharepoint.com', username='yeri@wholesumbrands.com', password='2023June12/').GetCookies()
    return authcookie

@st.cache_data
def get_file_from_sharepoint(file_name):
    authcookie = get_authcookie()
    site = Site('https://wholesumbrands.sharepoint.com/sites/data_auto', version=Version.v365, authcookie=authcookie)
    folder = site.Folder('Shared Documents/Sales/DS Team/Raw/Archive')

    try:
        file_content = folder.get_file(file_name)
        return pd.read_csv(StringIO(file_content.decode('utf-8')), low_memory=False)
    except Exception as e:
        st.error(f"Error loading file {file_name}: {e}")
        return None

naver_df = get_file_from_sharepoint('naver_all_reviews.csv')
if naver_df is not None:
    naver_df = naver_df.drop(columns=['brand_e', 'review_id', 'date'])
    naver_df['product_code'] = naver_df['product_code'].astype(str)
    naver_df['review_date'] = pd.to_datetime(naver_df['review_date']).dt.strftime('%Y-%m-%d')
    naver_df = naver_df.rename(columns={
        'brand_k': '브랜드',
        'channel': '채널',
        'product_code': '상품코드',
        'review_date': '리뷰날짜',
        'user': '리뷰아이디',
        'product_name': '상품명',
        'product_option': '옵션명',
        'rating': '점수',
        'review_type': '리뷰타입',
        'repurchase': '재구매',
        'review_details': '상품평'
    })

#coupang_df = get_file_from_sharepoint(sales_folder, 'coupang_all_reviews.csv')
#if coupang_df is not None:
#    coupang_df = coupang_df.drop(columns=['brand_e', 'review_id', 'date'])
#    coupang_df['product_id'] = coupang_df['product_id'].astype(str)
#    coupang_df = coupang_df.rename(columns={
#        'brand_k': '브랜드',
#        'channel': '채널',
#        'seller': '판매자',
#        'product_id': '상품코드',
#        'review_date': '리뷰날짜',
#        'user': '리뷰아이디',
#        'review_title': '리뷰제목',
#        'product_details': '상품명',
#        'product_option': '옵션명',
#        'rating': '점수',
#        'review_type': '리뷰타입',
#        'repurchase': '재구매',
#        'review_details': '상품평'
#    })

st.title("🐔득근파티 리뷰 대시보드🐔")
st.write("")

st.subheader('')
#st.dataframe('')

tabs = st.tabs(["네이버 리뷰"]) #, "쿠팡 리뷰"
with tabs[0]:
    st.subheader('네이버 리뷰 데이터 미리보기')
    naver_brand_filter = st.selectbox("브랜드", options=naver_df["브랜드"].unique())
    naver_date_filter = st.date_input("리뷰 날짜", [])

    filtered_naver_df = naver_df.copy()
    if naver_brand_filter:
        filtered_naver_df = filtered_naver_df[filtered_naver_df["브랜드"] == naver_brand_filter]
    if naver_date_filter:
        filtered_naver_df = filtered_naver_df[
            pd.to_datetime(filtered_naver_df["리뷰날짜"], errors='coerce').dt.date == pd.to_datetime(naver_date_filter).date()
        ]
        #filtered_naver_df = filtered_naver_df[pd.to_datetime(filtered_naver_df["리뷰날짜"]).isin(pd.to_datetime(naver_date_filter))]

    # 네이버 리뷰 데이터 다운로드 버튼
    naver_csv = filtered_naver_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label=f"네이버 {naver_brand_filter} 리뷰 데이터 다운로드",
        data=naver_csv,
        file_name=f'naver_{naver_brand_filter}_reviews.csv',
        mime='text/csv'
    )
    st.subheader('미리보기 (처음 5줄)')
    st.dataframe(filtered_naver_df.head())
    
#with tabs[1]:
#    st.subheader('쿠팡 리뷰 데이터 미리보기')
#    coupang_brand_filter = st.selectbox("브랜드", options=coupang_df["브랜드"].unique())
#    coupang_date_filter = st.date_input("리뷰날짜", [])

    # 필터 적용
#    filtered_coupang_df = coupang_df.copy()
#    if coupang_brand_filter:
#        filtered_coupang_df = filtered_coupang_df[filtered_coupang_df["브랜드"] == coupang_brand_filter]
#    if coupang_date_filter:
#        filtered_coupang_df = filtered_coupang_df[pd.to_datetime(filtered_coupang_df["리뷰날짜"]).isin(pd.to_datetime(coupang_date_filter))]

    # 필터링된 쿠팡 데이터 출력
#    st.dataframe(filtered_coupang_df)

# 브랜드, 채널, 날짜 필터 옵션
#st.sidebar.header("필터 옵션")
#brand_filter = st.sidebar.multiselect("브랜드 선택", options=concat_df["브랜드"].unique())
#channel_filter = st.sidebar.multiselect("채널 선택", options=concat_df["채널"].unique())
#date_filter = st.sidebar.date_input("review_date", [])

# 필터 적용
#filtered_df = concat_df.copy()
#if brand_filter:
#    filtered_df = filtered_df[filtered_df["브랜드"].isin(brand_filter)]
#if channel_filter:
#    filtered_df = filtered_df[filtered_df["채널"].isin(channel_filter)]

#if date_filter:
#    filtered_df = filtered_df[pd.to_datetime(filtered_df["리뷰날짜"]).isin(pd.to_datetime(date_filter))]

# 필터링된 데이터 출력
#st.subheader('필터링된 데이터')

#st.subheader('미리보기 데이터')
#st.dataframe(coupang_df.head())
