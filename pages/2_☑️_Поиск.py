import streamlit as st

st.set_page_config(page_title='Поиск', page_icon="☑️", layout="wide", initial_sidebar_state = 'collapsed')

hide_streamlit_style = """
<style>
footer {visibility: hidden;}
</style>
"""


def save_value(object_, name):
    st.session[name] = object_


try:
    db_object = st.session_state['DB_object']
    db_status = db_object.DB_connection_check()
    st.write('DB ok' if db_status else 'DB disconnected')

    legal_params = ['ИНН', "Короткое название", "Тип подразделения", 'HID', "Тип капитала", "Уставной капитал", "КПП", "ОГРН", "ОКАТО", "ОКОГУ", "ОКФС"]
    natural_params = ['ИНН', "Фамилия", "Имя", "Отчество", "HID"]


    remake_table = {
        'HID' : 'hid_party', 
        'ОГРН' : "ogrn",
        "ИНН" : "inn", 
        "КПП" : "kpp", 
        "ОКАТО" : "okato_code", 
        "Уставной капитал" : "capital_value", 
        "Тип капитала" : "capital_type", 
        "ОКОГУ" : "okogu_code",
        "Тип подразделения" : "branch_type", 
        "Короткое название" : "short_name", 
        "ОКФС" : "okfs_code",
        "Фамилия" : "surname", 
        "Имя" : "capital_value", 
        "Отчество" : "patronymic"
    }

    faces_column_1, faces_column_2 = st.columns(2)

    is_ok = True

    with faces_column_1:
        face_start = st.selectbox('Выберите тип лица, от которого начнется поиск', ['Юр. лицо', 'Физ. лицо'] if 'face_1' not in st.session_state else st.session_state.face_1, key = 'face_start')
        first_params_add = legal_params if face_start == 'Юр. лицо' else natural_params

        selector_start = st.multiselect('Параметры 2 лица', first_params_add, [] if 'params_1' not in st.session_state else st.session_state.params_1, key = 'params_start')
        
        try:
            temp_start = st.text_input(selector_start[-1], key = f'''{selector_start[-1]}_start_label''')
            st.session_state[f'''{selector_start[-1]}_start'''] = temp_start
            
        except IndexError:
            is_ok = True
            st.write('Параметры поиска не заданы')



    with faces_column_2:
        
        face_end = st.selectbox('Выберите тип лица, на котором закончится поиск', ['Юр. лицо', 'Физ. лицо'] if 'face_2' not in st.session_state else st.session_state.face_2, key = 'face_end')
        second_params_add = legal_params if face_end == 'Юр. лицо' else natural_params

        selector_end = st.multiselect('Параметры 2 лица', second_params_add, [] if 'params_2' not in st.session_state else st.session_state.params_2, key = 'params_end')
        
        try:
            temp_end = st.text_input(selector_end[-1], key = f'''{selector_end[-1]}_end_label''')
            st.session_state[f'''{selector_end[-1]}_end'''] = temp_end
            
        except IndexError:
            is_ok = True
            st.write('Параметры поиска не заданы')


    search_button = st.sidebar.button('Запрос', key = 'search_button', disabled = not is_ok)
    check_button = st.sidebar.button('Проверить', key = 'check_button', disabled = not is_ok)

    st.markdown('''
    <style>
        .css-z09lfk {width : 150px;}
    </style>
    ''', unsafe_allow_html=True)

    relation_type = st.text_input('Тип связи между субъектами', key = 'relation_input')

    param_column_1, param_column_2 = st.columns(2)

    with param_column_1:
        search_depth = st.number_input('Глубина поиска', value = 5, step = 1, min_value = 1, key = 'search_depth_input')
        shortest_path_switch = st.checkbox('Найти кратчайший путь', key = 'shortest_path_switch_input', value = False)
        bidirect_relation = st.checkbox('Учитывать обратные связи', key = 'relation_mode', value = True)

    with param_column_2:
        output_limit = st.number_input('Максимум записей', value = 5, step = 1, min_value = 1, key = 'search_limit_input')


    def query_prep():
        params_start_search = {}
        params_end_search = {}

        current_state = st.session_state

        for key in current_state:
            if '_start' in key:
                if key.split('_')[0] in current_state['params_start']:
                    params_start_search.update({ key.split('_')[0] : current_state[key]})

        for key in current_state:
            if '_end' in key:
                if key.split('_')[0] in current_state['params_end']:
                    params_end_search.update({ key.split('_')[0] : current_state[key]})

        first_face = str(face_start)
        first_params = dict(params_start_search)

        second_face = str(face_end)
        second_params = dict(params_end_search)

        shortest_path = shortest_path_switch


        first_params_append = '{' + f'''{', '.join([remake_table[key] + ' : ' + f'"{str(first_params[key])}"' for key in first_params])}''' + '}'
        second_params_append = '{' + f'''{', '.join([remake_table[key] + ' : ' + f'"{str(second_params[key])}"' for key in second_params])}''' + '}'

        
        if shortest_path:
            return(f'''match path = shortestPath( (first : {'Legal_Entity' if first_face == 'Юр. лицо' else 'Natural_Person'} {first_params_append}) - [{f'relation : `{relation_type}`' if relation_type != '' else ''}{f' *0..{search_depth}' if search_depth else ''} ] -{'>' if not bidirect_relation else ''} (second : {'Legal_Entity' if second_face == 'Юр. лицо' else 'Natural_Person'} {second_params_append}) ) return path limit {output_limit};''')
        
        else:
            return(f'''match (first : {'Legal_Entity' if first_face == 'Юр. лицо' else 'Natural_Person'} {first_params_append}) - [{f'relation : `{relation_type}`' if relation_type != '' else ''}{f' *0..{search_depth}' if search_depth else ''} ] -{'>' if not bidirect_relation else ''} (second : {'Legal_Entity' if second_face == 'Юр. лицо' else 'Natural_Person'} {second_params_append}) return first, second limit {output_limit};''')


    if check_button:
        st.write(query_prep())

    if search_button:
        session = st.session_state

        session.face_1 = ['Юр. лицо', "Физ. лицо"] if face_start == 'Юр. лицо' else ['Физ. лицо', "Юр. лицо"]
        session.face_2 = ['Юр. лицо', "Физ. лицо"] if face_end == 'Юр. лицо' else ['Физ. лицо', "Юр. лицо"]

        session.params_1 = selector_start
        session.params_2 = selector_end

        session.query_mode = bidirect_relation
        
        session.relation_type_ = relation_type
        

        with st.spinner(text='Ищем связи...'):
            st.markdown(hide_streamlit_style, unsafe_allow_html=True)
            response = db_object.DB_execute(query_prep())

            st.session_state['search_result'] = response            


except Exception as exception:
    print('[WARN] Client isn\'t connected to DB.', exception)
    st.write('Вы не подключены к базе данных. Подключитесь через соответствующее окно слева.')


# Сделать поле-монитор состояния подключения к базе данных. Можно использовать гипер-поточность

# st.write("Selected Decks:", selected_decks)


st.markdown(hide_streamlit_style, unsafe_allow_html=True)