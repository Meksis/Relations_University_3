import streamlit as st

st.set_page_config(page_title='Просмотр', page_icon="∴", layout="wide", initial_sidebar_state = 'expanded')

if 'search_result' in st.session_state:
    result = st.session_state['search_result']

    res_0 = []
    res_1 = []
    
    #st.write(list(result))
    #st.write(list(result)[0][0])
    
    for counter in range(len(result)):
        res_0.append(dict(result[counter][0]))
        res_1.append(dict(result[counter][1]))
        # res_1.append(list(result[counter])[1])

    result_column_1, result_column_2 = st.columns(2)

    with result_column_1:
        st.write('''### I группа подходящих лиц''')
        st.write(res_0)

    with result_column_2:
        st.write('''### II группа подходящих лиц''')
        st.write(res_1)

else:
    '''# Здесь пока ничего нет\nПоищите что-нибудь и мы вам это покажем.'''



hide_streamlit_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)