import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

class Structure:
    def data_display(df):
        st.write(df)

if "uploaded_data" not in st.session_state:
    file = st.file_uploader("Choose your file", type=['csv'])
    if file is not None:
        st.session_state.uploaded_data = pd.read_csv(file)
        st.rerun()

if "uploaded_data" in st.session_state:
    df=pd.DataFrame(st.session_state.uploaded_data)
    key=st.sidebar.selectbox("select The Unic key",df.columns)
    remove_duplicates= df.drop_duplicates(subset=key, keep='first')
    col1,col2,col3=st.columns(3)
    with col1:
        columns=df.columns
        st.sidebar._checkbox(columns[0],value=True)
        st.write('Number of rows when you enter ',len(df))
        st.write(df.tail())
        city=df['City'].value_counts()
        city_selected=st.sidebar.selectbox('select city',city.index)
        if city_selected in city.index:
            st.sidebar.write("Number of customer in the",city_selected," ",city[city_selected])
    df=remove_duplicates
    with col2:
        st.write('Number of rows after procceing ',len(df))
        st.dataframe(df.tail())
    fig,ax=plt.subplots()
    ax.set_title("City")
    ax.set_ylabel("City")
    city.plot(kind='pie',ax=ax)
    st.pyplot(fig)
    if st.sidebar.button("Upload a different file"):
        del st.session_state.uploaded_data
        st.rerun()