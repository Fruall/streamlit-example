import streamlit as st
import numpy as np
import pandas as pd
from requests_html import HTMLSession
import json

st.title('HTTP Status Observer')

url = st.text_input('Enter your URL-address')
check = st.button('Check!')

pd.set_option("display.max_colwidth", None)

if url or (url and check):
    session = HTMLSession()
    r = session.get(url, allow_redirects=False)

    if r.status_code == (301 or 302 or 303):
        r_full = session.get(url, allow_redirects=True)
        st.write(r_full.status_code)
        st.subheader('Headers')
        headers = dict(r_full.headers)
        df = pd.DataFrame(headers, index=['Header Value']).transpose()
        st.dataframe(df, height=768)
        st.subheader('Redirect Chains')
        nb_redirects = len(r_full.history)
        st.write('First Status Code :', r_full.history[0])
        st.write('Number Of Redirects :', nb_redirects)

        st.write(url)

        for resp in r.history:
            st.write(resp.status_code, resp.url)

        st.write(r.status_code, r.url)
    else:
        st.write(r.status_code)
        st.subheader('Headers')
        headers = dict(r.headers)
        st.write(headers)
        df = pd.DataFrame(headers, index=['Header Value']).transpose()
        df['Header Value'] = df['Header Value'].str.wrap(10)
        st.dataframe(df, width=1024, height=768)
else:
    st.write('No url added')
