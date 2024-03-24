import pandas as pd
import streamlit as st
from urllib.parse import quote_plus

df = pd.read_csv("isegye_data.csv")


def search_songs(dataframe, search_query):
    search_query = search_query.lower()
    search_result = dataframe[
        dataframe['Artist'].str.lower().fillna("").str.contains(search_query) |
        dataframe['Artist2'].str.lower().fillna("").str.contains(search_query) |
        dataframe['Artist3'].str.lower().fillna("").str.contains(search_query) |
        dataframe['Title'].str.lower().str.contains(search_query)
        ]
    return search_result


def search_on_yt(keyword):
    base_url = "https://www.youtube.com/results?search_query="
    q = quote_plus(keyword)
    return base_url + q


st.title('ISEGYE Searchable Machine')

query = st.text_input("키워드를 입력하세요: ")

if query:
    result = search_songs(df, query)

    if not result.empty:
        result['YouTube'] = (result['Artist'].astype(str) + " " +
                             result['Title'].astype(str) + " " +
                             result['Artist2'].astype(str) + " " +
                             result['Artist3'].astype(str)).apply(
            lambda x: f"[지금 듣기]({search_on_yt(x)})")
        result['Title'] = result['Title'].apply(lambda x: x[:20] + "..." if len(x) > 40 else x)
        result['Artist2'] = result['Artist2'].fillna("")
        result['Artist3'] = result['Artist3'].fillna("")

        st.markdown(result[['Title', 'Artist', 'Artist2', 'Artist3', 'YouTube']].to_markdown(
            index=False), unsafe_allow_html=True)
    else:
        st.write("검색 결과가 없습니다.")
