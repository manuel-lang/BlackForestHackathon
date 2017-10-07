import sys
import time
import datetime
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def __init__():
    pass

def createGui():
    gui = QWidget()
    gui.setWindowTitle("GUI test")
    gui.resize(QDesktopWidget().screenGeometry(-1).width(), QDesktopWidget().screenGeometry(-1).height())

    # warum funzt der scheiss nicht???
    # icon = QIcon(os.path.dirname(__file__) + "/icon_unicorn.jpg")
    # w.setWindowIcon(icon)

    gui.show()
    return gui

def updateLayout(persons):
    # persons ist eine Liste von erkannten Personen
    global gui
    layout = gui.layout()
    widget_width = (gui.width() / len(persons))
    # save old widgets
    widgets = {}
    if type(layout) is not type(None):
        for x in range(layout.count()):
            item = layout.itemAt(x)
            widgets[persons[x]] = item.widget()
            item.widget().setParent(None)
    else:
        layout = QHBoxLayout()

    for x in range(len(persons)):
        if persons[x] in widgets:
            # person wird bereits angezeigt
            # lade das widget aus widgets
            widgets[persons[x]].setMaximumSize(widget_width, gui.height())
            layout.addWidget(widgets[persons[x]])
        else:
            # person muss neu hinzugefuegt werden -> lade einstellung und zeige alles an

            if persons[x] == "Marius Bauer":
                # email
                mails = [["example1@example.com", "Example1",
                          "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."],
                         ["example2@example.com", "Example2",
                          "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."],
                         ["example3@example.com", "Example3",
                          "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."]]
                email_list = createList(mails, 'mails')
                email_list.setObjectName("Marius Bauer")
                email_list.setMaximumSize(widget_width, gui.height())
                layout.addWidget(email_list)
            elif persons[x] == "Manuel Lang":
                # news
                news = [["Headline1", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."],
                        ["Headline2", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."],
                        ["Headline3", "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."]]
                news_list = createList(news, 'news')
                news_list.setObjectName("Manuel Lang")
                news_list.setMaximumSize(widget_width, gui.height())
                layout.addWidget(news_list)
            elif persons[x] == "Tobias Oehler":
                # kalender
                current_timestamp = int(time.time())
                calendar = [[datetime.datetime.fromtimestamp(current_timestamp + 24 * 60 * 60 * 2).strftime('%Y-%m-%d %H:%M:%S'), " 1 Stunde", "Kaffepause1"],
                            [datetime.datetime.fromtimestamp(current_timestamp + 24 * 60 * 60 * 3).strftime('%Y-%m-%d %H:%M:%S'), " 30 Minuten", "Kaffepause2"],
                            [datetime.datetime.fromtimestamp(current_timestamp + 24 * 60 * 60 * 4).strftime('%Y-%m-%d %H:%M:%S'), " 1.5 Stunde", "Kaffepause3"]]
                calendar_list = createList(calendar, 'calendar')
                calendar_list.setObjectName("Tobias Oehler")
                calendar_list.setMaximumSize(widget_width, gui.height())
                layout.addWidget(calendar_list)
            elif persons[x] == "Jerome Klausmann":
                pass
                temp = QLabel("Temperatur: 15 Grad Celsius")
                wetterlage = QLabel("Wetterlage: Regen")
                widget = QWidget()
                lay_weather = QVBoxLayout()
                lay_weather.addWidget(temp)
                lay_weather.addWidget(wetterlage)
                widget.setLayout(lay_weather)

                layout.addWidget(widget)

    layout.update()
    gui.setLayout(layout)
    return layout

def createList(data, type):
    wList = QListWidget()
    wList.show()

    for x in range(len(data)):
        item = QListWidgetItem(wList)
        widget = QWidget()
        layout = QVBoxLayout()
        entry = QLabel()
        if (type == "mails"):
            entry.setText("Absender: " + data[x][0] + " \nBetreff:     " + data[x][1] + " \n" + " ".join(data[x][2].split(" ")[:20]))
        elif (type == "news"):
            entry.setText(data[x][0] + " \n" + " ".join(data[x][1].split(" ")[:20]))
        elif (type == "calendar"):
            entry.setText("Datum: " + str(data[x][0]) + " \nDauer: " + data[x][1]+ " \nBetreff: " + data[x][2])
        entry.setWordWrap(True)
        layout.addWidget(entry)
        layout.setSizeConstraint(QLayout.SetFixedSize)
        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        wList.setItemWidget(item, widget)
    return wList

def openMail(index):
    # Marius Bauer
    # QListWidget
    widget_marius = gui.layout().itemAt(0).widget()
    target_widget = widget_marius.itemAt(0, index)
    print "whatever"
app = QApplication(sys.argv)
gui = createGui()

#updateLayout(["Marius Bauer"])

updateLayout(["Marius Bauer", "Manuel Lang", "Tobias Oehler", "Jerome Klausmann"])
openMail(1)
# print(os.path.dirname(__file__) + "/icon_unicorn.jpg")
sys.exit(app.exec_())