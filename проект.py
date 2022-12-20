from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1920, 800)

        self.style = '''color:white;'''
        self.faces_params = {'LEGAL' : ['Параметры', 'ИНН', "ОГРН", "ОКАТО_код", "ОКАТО_название", "ОКОПФ", "Исторический_ИД"], 'PHYSICAL' : ['Параметры', 'ИНН', "Имя", "Фамилия", "Отчество", "Исторический_ИД"]}


        self.setupUI()
    
    def setupUI(self):

        '''self.layout = QVBoxLayout(self)'''

        self.win_db_switch = QPushButton('Соединение с бд', self)
        self.win_graph_switch = QPushButton('графы', self)
        self.win_search_switch = QPushButton('поиск', self)

        self.win_glub_search_switch = QLineEdit('', self)
        self.win_glub_search_switch.setPlaceholderText('Глубина выборки')
        self.win_glub_search_switch.setInputMask('9999')




        self.win_search_1_switch = QPushButton('поиск', self)

        self.win_glub_search_switch.setGeometry(925,36,200,40)
        self.win_search_1_switch.setGeometry(1125,36,200,40)

    
        self.win_search_1_switch.clicked.connect(self.button_4_reaction)




        self.check_but = QPushButton('Проверка', self)
        self.check_but.setGeometry(1325,36,200,40)
        self.check_but.clicked.connect(self.button_5_reaction)




        self.win_db_switch.clicked.connect(self.button_reaction)
        self.win_graph_switch.clicked.connect(self.button_2_reaction)
        self.win_search_switch.clicked.connect(self.button_3_reaction)

        self.check_but.clicked.connect(self.check_but_react)

        #self.area.setGeometry(QtCore.QRect(X, Y, width, height))

        self.win_db_switch.setGeometry(0, 0, 205, 100)
        self.win_graph_switch.setGeometry(0, 74, 205, 100)
        self.win_search_switch.setGeometry(0, 148, 205, 100)

        self.label=QLabel('Текстовое поле',self)
        self.label.setStyleSheet(self.style)
        self.label.setGeometry(QtCore.QRect(250, 0, 1325, 40))

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Юр. лица")
        self.combo_box.addItem("Физ. лица")
        self.combo_box.setGeometry(205, 36, 120, 40)

        self.combo_box.currentIndexChanged.connect(self.face_1_changed)


        self.combo_box_1 = QComboBox(self)
        self.combo_box_1.setGeometry(325, 36, 120, 40)
        self.combo_box_1.addItems(self.faces_params['LEGAL'])

        self.combo_box_2 = QComboBox(self)
        self.combo_box_2.addItem('Тип связи')
        self.combo_box_2.addItem('Тип связи1')
        self.combo_box_2.setGeometry(445,36,120,40)

        self.combo_box_3 = QComboBox(self)
        self.combo_box_3.addItem('Юр. лица')
        self.combo_box_3.addItem('Физ. лица')
        self.combo_box_3.setGeometry(565,36,120,40)
        self.combo_box_3.currentIndexChanged.connect(self.face_2_changed)


        self.combo_box_4 = QComboBox(self)
        self.combo_box_4.setGeometry(685,36,120,40)
        self.combo_box_4.addItems(self.faces_params['LEGAL'])

        self.combo_box_5 = QComboBox(self)
        self.combo_box_5.addItem('Тип связи')
        self.combo_box_5.addItem('Тип связи1')
        self.combo_box_5.setGeometry(805,36,120,40)

        

        #self.combo_box.addItem("Физ.лица")
    

        '''self.layout.addWidget(self.button_2)
        self.layout.addWidget(self.label)'''

    
    def button_reaction(self):
        print('Button clicked')

    def button_2_reaction(self):
        print('Button clicked')

    def button_3_reaction(self):
        print('Button clicked')

    def button_4_reaction(self):
        print('Button clicked')
    
    
    def button_5_reaction(self):
        print('Button clicked')


    def check_but_react(self):
        self.label.setText('ЗДЕСБ ВАШ ТЕКСТ ПОЛУЧИВШЕГОСЯ ЗАПРОСА')
            

    

    def face_1_changed(self):
        self.combo_box_1.clear()
        self.combo_box_1.addItems(self.faces_params['LEGAL' if self.combo_box.currentText() == 'Юр. лица' else 'PHYSICAL'])            

        self.label.setText('Список 1 изменен')
        print()

    def face_2_changed(self):
        self.combo_box_4.clear()
        self.combo_box_4.addItems(self.faces_params['LEGAL' if self.combo_box_3.currentText() == 'Юр. лица' else 'PHYSICAL'])            

        self.label.setText('Список 4 изменен')
        print()


app = QApplication(sys.argv)
window = Test()
window.setStyleSheet('QMainWindow {background-image: url(лого.PNG); background-color : black; background-repeat : no-repeat; background-position : center center;}')
window.show()

sys.exit(app.exec())