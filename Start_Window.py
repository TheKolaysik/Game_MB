import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui


# Основное окно
class Component(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui\MainWindow.ui", self)
        self.show()
        self.con = sqlite3.connect("results.sqlite")

        self.start.clicked.connect(self.username)
        self.result.clicked.connect(self.res_window)
        # self.setings.clicked.connect(self.getsql)

    def username(self):
        self.name1 = ''
        self.name2 = ''
        name, ok_pressed = QInputDialog.getText(self, "Добро пожалуйста 1-ый игрок",
                                                "Введите своё имя")
        if ok_pressed:
            self.name1 = name

        name, ok_pressed = QInputDialog.getText(self, "Добро пожалуйста 2-ый игрок",
                                                "Введите своё имя")
        if ok_pressed:
            self.name2 = name



    # Открытие окна результатов
    def res_window(self):
        self.wns = Results(self.con)
        self.wns.show()

    # Передача параметров из окна добавления элементов
    def adder_item(self, data, data1):
        self.cur.execute("INSERT INTO Track{} VALUES{} ".format(data1, data))
        self.con.commit()
        self.update_result()


class Results(QMainWindow):
    def __init__(self, con):
        super().__init__()
        uic.loadUi("gui\ResWindow.ui", self)
        self.show()

        self.cur = con.cursor()
        result = self.cur.execute("SELECT * FROM track").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]) - 1)
        self.tableWidget.setHorizontalHeaderLabels(
            tuple([description[0] for description in self.cur.description][1:]))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem[1:]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Component()
    sys.exit(app.exec_())
