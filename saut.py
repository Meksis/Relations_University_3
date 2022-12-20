import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from datetime import date
import plotly.express as px
from PIL import Image
import sys
from py2neo import Graph
from neo4j import GraphDatabase
from streamlit import *



st.set_page_config(page_title='ПВВК',page_icon=":bar_chart",layout="wide")




class BD_interact():
    def __init__(self, protocol, ip_adress, port, bd_name, auth_name, auth_pass):
        self.protocol = protocol
        self.ip_adress = ip_adress
        self.port = port
        self.con_address = f'''{self.protocol}://{self.ip_adress}:{self.port}'''
        # print(self.con_address)

        self.bd_name = bd_name

        self.auth_name = auth_name
        self.auth_pass = auth_pass

        self.BD_connect()
    
    def BD_connect(self):
        self.graph = Graph(self.con_address, auth = (self.auth_name, self.auth_pass), name = self.bd_name)
        self.con_status = True

        print('[ERROR] Connection wasn\'t established! Try to use another port.' if not self.con_status else '[INFO] Connection established!')

        return(self.con_status)

    def BD_execute(self, query):
        self.response = list(self.graph.run(query).to_table())[0]

        return(self.response)

    def BD_conncetion_check(self):
        return()


bd_window = BD_interact('bolt', 'localhost', 7687, 'neo4j', 'neo4j', "12345")

class side_bar_after_connect:
    def facestart():
        face_start = sidebar.selectbox("Face start ",['Юр.лица', 'Физ.лица'],key=5,args=None)
        
    def paramstart():
        parameter_start = sidebar.multiselect("Parameter start ",['ИНН', 'ОГРН'],key=6,args=None)
               
    def linktype():
        type_link = sidebar.selectbox("Тип связи: ",['ТП1', 'ТП2'],key=7,args=None)
                  
    def faceend():
        face_end = sidebar.selectbox("Face end: ",['Юр.лица', 'Физ.лица'],key=8,args=None)
                     
    def paramend():
        parameter_end = sidebar.multiselect("Parameter end ",['ИНН', 'ОГРН'],key=9,args=None)
                          
    def depth():
        Search_Depth = sidebar.text_input("Глубина поиска",key=123)
        if(sidebar.button('Выполнить',key="complite")):
            result = Search_Depth.title()
            st.success(result)
                            
    def butonpoisk():
        if(sidebar.button("Поиcк",key="poiskbutton")):
           st.text("Poisk")
                                 
    def butonproverka():
        if(sidebar.button("Проверка",key="proverkabutton")):
            st.text("Proverka")


    first_face = str(facestart)
    second_face = str(faceend)

    first_params = {'inn' : '7452022281', 'ogrn' : '1027403774507'}
    second_params = {'inn' : '741500840011'}

    relation_type = 'Учреждено'

    search_depth = 1

    first_params_append = '{' + f'''{', '.join([key + ' : ' + f'"{str(first_params[key])}"' for key in first_params])}''' + '}'
    second_params_append = '{' + f'''{', '.join([key + ' : ' + f'"{str(second_params[key])}"' for key in second_params])}''' + '}'

    print(first_params_append, second_params_append)
    query = f'''match (first : {'Legal_Entity' if first_face == 'LEGAL' else 'Natural_Person'} {first_params_append}) - [{f'relation : `{relation_type}`' if relation_type != '' else ''}{f' *0..{search_depth}' if search_depth else ''} ] -> (second : {'Legal_Entity' if second_face == 'LEGAL' else 'Natural_Person'} {second_params_append}) return first, second'''
    #query
                                        




class side_bar_before_connect:
    def connect_bd1():
      
        protocol = st.sidebar.text_input("Please enter your used protocol",key=1,args=None)
        
        
    def connect_bd2():
    
        ip_adress = st.sidebar.text_input("Please enter your IP address",key=2,args=None)
        
    def connect_bd3():
      
        port = st.sidebar.text_input("Please enter your Port",key=3,args=None)
        
    def connect_bd4():
        
        connect_button = sidebar.button("Соединение с БД", on_click = side_bar_after_connect)
        
    
    connect_bd1()
    connect_bd2()
    connect_bd3()
    connect_bd4()




side_bar_after_connect.facestart()
side_bar_after_connect.paramstart()
side_bar_after_connect.linktype()
side_bar_after_connect.faceend()
side_bar_after_connect.paramend()
side_bar_after_connect.depth()
side_bar_after_connect.butonpoisk()
side_bar_after_connect.butonproverka()                         






img = Image.open(r"logo.png" )
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image(img)

with col3:
    st.write(' ')



main_bg = "sample.jpg"
main_bg_ext = "jpg"

side_bg = "sample.jpg"
side_bg_ext = "jpg"

st.markdown(
    """
    <style>
        background-attachment: fixed;
        .stApp {background-color: black;}
        .css-1avcm0n {background-color: black}
        .css-renyox {color : black}
        .css-6qob1r {background-color : black}
        .css-z09lfk {background-color: red}
        .css-1rs6os {color : red}
        .css-1i2wz1k {background-color : red}
        .css-ffhzg2{background-color : black}

    </style>
    """,


    unsafe_allow_html=True
)
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)