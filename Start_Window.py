import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from Game_window import Board


# Основное окно
class Component(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui\MainWindow.ui", self)
        self.show()
        self.con = sqlite3.connect("results.sqlite")
        self.start.clicked.connect(self.username)
        self.result.clicked.connect(self.res_window)

    def username(self):
        global ex
        name, ok_pressed = QInputDialog.getText(self, "Добро пожалуйста 1-ый игрок",
                                                "Введите своё имя")
        if ok_pressed:
            if name == '':
                name = "FIRST"
            self.name1 = name
            win1 = Board(10, 10, 1, ex)
            win1.set_view(0, 0, 40)
            win1.set_name(name)
            win1.start_screen()
            win2 = Board(10, 10, 2, ex)
            win2.set_view(0, 0, 40)
            win2.set_name2(name)
            win1.strun(win1, win2)
            win1.running_game()
            win1.set_mode()

        name, ok_pressed = QInputDialog.getText(self, "Добро пожалуйста 2-ый игрок",
                                                "Введите своё имя")
        if ok_pressed:
            if name == "":
                name = "SECOND"
            self.name2 = name
            win2.strun(win2, win1)
            win2.set_name(name)
            win1.set_name2(name)
            win2.start_screen()
            win2.running_game()
            win2.set_mode()
            win1.start_screen()
            win1.running_game()

    # Открытие окна результатов
    def res_window(self):
        self.wns = Results(self.con)
        self.wns.show()

    # Запись побед и поражений
    def adder_item(self, data, data1=None, data2=None):
        self.cur = self.con.cursor()
        res = self.cur.execute("SELECT Name FROM track").fetchall()
        res = [i[0] for i in res]
        if data not in res:
            if data1:
                self.cur.execute("INSERT INTO Track(name, victories, defeats) VALUES{}".format((data, data1, 0)))
                self.con.commit()
            if data2:
                self.cur.execute("INSERT INTO Track(name, victories, defeats) VALUES{}".format((data, 0, data2)))
                self.con.commit()
        else:
            if data1:
                self.cur.execute("UPDATE track SET victories=victories+1 WHERE Name={}".format(data))
                self.con.commit()
            if data2:
                self.cur.execute("UPDATE track SET defeats=defeats+1 WHERE Name={}".format(data))
                self.con.commit()

    # Применить значение поля 1
    def set_board1(self, board):
        self.board1 = board

    # Применить значение поля 2
    def set_board2(self, board):
        self.board2 = board

    # Получение координат поля 1
    def get_coords1(self, x, y):
        return self.board1[x][y]

    # Получение координат поля 2
    def get_coords2(self, x, y):
        return self.board2[x][y]


# Окно результатов
class Results(QMainWindow):
    def __init__(self, con):
        super().__init__()
        uic.loadUi("gui\ResWindow.ui", self)
        self.show()
        self.cur = con.cursor()
        result = self.cur.execute("SELECT * FROM track").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            tuple([description[0] for description in self.cur.description]))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Component()
    sys.exit(app.exec_())
