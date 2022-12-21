import streamlit as st
from streamlit import *

import py2neo
from py2neo import Graph

from typing import Union

st.set_page_config(page_title='Подключение', page_icon="⚙️", layout="wide", initial_sidebar_state = 'expanded')



class DB_interact():
    def __init__(self, protocol : str, ip_adress : str, port : Union[str, int], bd_name : str, auth_name : str, auth_pass : str) -> None:
        self.protocol = protocol
        self.ip_adress = ip_adress
        self.port = port
        self.con_address = f'''{self.protocol}://{self.ip_adress}:{self.port}'''

        self.db_name = bd_name

        self.auth_name = auth_name
        self.auth_pass = auth_pass

        self.DB_connect()
    
    def DB_connect(self):
        try:
            self.graph = Graph(self.con_address, auth = (self.auth_name, self.auth_pass), name = self.db_name)
            self.con_status = True
            self.error_text = ''
        
        except Exception as exception:
            self.error_text = str(exception)
            self.con_status = False

        if not self.con_status:
            if '[Security.Unauthorized]' in self.error_text or 'Connection has been closed' in self.error_text:
                self.error_text = '[ERROR] ' + self.error_text + '. Incorrect user data.'
                print('[ERROR] Connection wasn\'t established! Incorrect user data.' if not self.con_status else '[INFO] Connection established!')
            
            elif 'Cannot open connection to ConnectionProfile' in self.error_text:
                self.error_text = '[ERROR] ' + self.error_text + '. Incorrect connection data.'
                print('[ERROR] Connection wasn\'t established! Incorrect connection data.' if not self.con_status else '[INFO] Connection established!')
            
            elif 'neo4j_version' in self.error_text:
                self.error_text = '[ERROR] ' + self.error_text + '. Incorrect protocol.'
                print('[ERROR] Connection wasn\'t established! Incorrect protocol.' if not self.con_status else '[INFO] Connection established!')
            
            else:
                self.error_text = '[ERROR] ' + self.error_text + '. Unknown error.'
                print('[ERROR] Connection wasn\'t established! Unknown error.' if not self.con_status else '[INFO] Connection established!')
            
            self.con_status = False

        return(self.con_status)

    def DB_execute(self, query : str):
        self.response = list(self.graph.run(query).to_table())
        return(self.response)

        

    def DB_connection_check(self):
        if self.con_status:
            self.response = list(self.graph.run(f'''match (n) return n.inn limit 1;''').to_table())
            return(True)
        
        else:
            # st.write('[ERROR] Подключение к базе данных не выполнено!')
            return(False)
        

        # print(len(self.response))

        


hide_streamlit_style = """
<style>
footer {visibility: hidden;}
</style>
"""

auth_column_1, auth_column_2 = st.columns(2)

with auth_column_1:
    protocol_select = selectbox("Протокол подключения", ['bolt', 'http', 'https'])
    # print('localhost' if 'ip_select' not in st.session_state else st.session_state['ip_select'])
    ip_select = text_input("IP-адрес для подключения", value = 'localhost' if 'ip_select' not in st.session_state else st.session_state['ip_select'])
    port_select = number_input(label = "Порт для подключения", step = 1, value = 11003 if 'port_select' not in st.session_state else st.session_state['port_select'])

with auth_column_2:
    auth_db_name = text_input('Название базы данных', key = 'auth_db_name_1', value = 'TEST' if 'auth_db_name' not in st.session_state else st.session_state['auth_db_name'])
    auth_user_name = text_input('Имя пользователя', key = 'auth_user_name_1', value = 'neo4j' if 'auth_user_name' not in st.session_state else st.session_state['auth_user_name'])
    auth_user_pass = text_input('Пароль пользователя', key = 'auth_user_pass_1', type = 'password')




if st.sidebar.button("Подключиться"):
    with st.spinner(text='Подключаемся...'):
        st.session_state['protocol_select'] = str(protocol_select)
        st.session_state['ip_select'] = str(ip_select)
        st.session_state['port_select'] = port_select
        st.session_state['auth_db_name'] = str(auth_db_name)
        st.session_state['auth_user_name'] = str(auth_user_name)
        
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        db_object =  DB_interact(protocol_select, ip_select, port_select, auth_db_name, auth_user_name, str(auth_user_pass))
        error_text = ''

        try:
            con_status = db_object.DB_connection_check()
            
        
        except Exception as exception:
            con_status = False
            error_text = str(exception)
        
        if error_text != '':
            if '[Database.DatabaseNotFound]' in error_text:
                st.write(f'''[ERROR] {error_text} Incorrect database name.''')

            else:
                print(error_text)
                st.write(f'''[ERROR] {error_text}.''')

        if not con_status:
            st.write(f'''[ERROR] Connection with database wasn\'t established!''')
        
            

    
    st.session_state['DB_object'] = db_object
    st.write(db_object.error_text if not con_status else '[INFO] Соединение с базой данных установлено!')

    

st.markdown(hide_streamlit_style, unsafe_allow_html=True)