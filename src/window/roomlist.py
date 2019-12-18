
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QDialog
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QMessageBox, QComboBox, QListWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

import src.session as session
from src.window.filelist import *

class RoomWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.show()

    def initUi(self):
        #print(session.id, session.passwd)

        main_vbox = QVBoxLayout()


        sortLabel = QLabel("정렬: ")
        self.keyCombo = QComboBox()
        self.keyCombo.addItem("생성날짜")
        self.keyCombo.addItem("방 제목")
        self.keyCombo.addItem("파일 수")
        self.keyCombo.currentIndexChanged.connect(self.changeCombobox)
        h0_box = QHBoxLayout()
        h0_box.addStretch(1)
        h0_box.addWidget(sortLabel)
        h0_box.addWidget(self.keyCombo)

        # database Query
        session.room_data = self.getRoomList(self.keyCombo.currentText())

        self.listwidget = QListWidget()
        self.listwidget.verticalScrollBar().setStyleSheet("width: 10px;")
        for room_id, title, cnt, date, host in session.room_data:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextTitle(title)
            myQCustomQWidget.setCntTitle(cnt)
            myQCustomQWidget.setDateTitle(date)
            myQCustomQWidget.setHostTitle(host)

            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.listwidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

            # Add QListWidgetItem into QListWidget
            self.listwidget.addItem(myQListWidgetItem)
            self.listwidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            #print(myQCustomQWidget.getTextTitle())

        h1_box = QHBoxLayout()
        h1_box.addWidget(self.listwidget)
        self.listwidget.doubleClicked.connect(self.listClicked)
        self.listwidget.setStyleSheet("font-size: 15px; width: 150px")


        self.deleteRoomButton = QPushButton("방 삭제")
        self.deleteRoomButton.setStyleSheet("color: red;width: 150px;height: 40px;")
        self.deleteRoomButton.clicked.connect(self.deleteRoomButtonClicked)
        self.makeRoomButton = QPushButton("방 만들기")
        self.makeRoomButton.setStyleSheet("width: 150px;height: 40px;")
        self.makeRoomButton.clicked.connect(self.makeRoomButtonClicked)
        h2_box = QHBoxLayout()
        #h2_box.addStretch(1)
        h2_box.addWidget(self.deleteRoomButton)
        h2_box.addWidget(self.makeRoomButton)

        main_vbox.addLayout(h0_box)
        main_vbox.addLayout(h1_box)
        main_vbox.addLayout(h2_box)

        self.setLayout(main_vbox)
        self.setWindowTitle("Room")
        self.setGeometry(600, 250, 400, 500)


    def refreshList(self):
        self.listwidget.clear()

        for room_id, title, cnt, date, host in session.room_data:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextTitle(title)
            myQCustomQWidget.setCntTitle(cnt)
            myQCustomQWidget.setDateTitle(date)
            myQCustomQWidget.setHostTitle(host)

            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.listwidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

            # Add QListWidgetItem into QListWidget
            self.listwidget.addItem(myQListWidgetItem)
            self.listwidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)


    # DoubleClicked Event
    def listClicked(self):
        # 현재 선택된 row index 리턴
        idx = self.listwidget.currentRow()

        it = self.listwidget.currentItem()
        widget = self.listwidget.itemWidget(it)


        session.room_id = session.room_data[idx][0]
        session.title = session.room_data[idx][1]

        self.file = FileWindow()
        self.file.show()



    def makeRoomButtonClicked(self):
        # CreateRoomWindow에서 insert문을 날린다.
        self.createRoom = CreateRoomWindow()
        self.createRoom.exec_()


        command = "insert into room(title, host_id, create_date) \
                    values(\'{}\', \'{}\', now());" .format(session.create_title, session.id)
        session.sql.insert(command)
        session.room_data = self.getRoomList(self.keyCombo.currentText())
        self.refreshList()


    def deleteRoomButtonClicked(self):
        idx = self.listwidget.currentRow()

        # 방 주인과 로그인한 id가 같은지 판별
        host_id = session.room_data[idx][4]

        if host_id != session.id:
            QMessageBox.about(self, "warning", "당신은 방 주인이 아닙니다!")
            return



        room_id = session.room_data[idx][0]
        command = """
            delete room, file
            from room left outer join file
	        on room.room_id = file.room_id
            where room.room_id = \'{}\'
        """ .format(room_id)
        session.sql.delete(command)
        session.room_data = self.getRoomList(self.keyCombo.currentText())

        self.refreshList()


    # Combobox 변경되었을 때
    def changeCombobox(self):
        session.room_data = self.getRoomList(self.keyCombo.currentText())
        self.refreshList()


    def getRoomList(self, key="생성날짜"):
        sort_key = "생성날짜"

        if key == "생성날짜":
            sort_key = "room.create_date"
        elif key == "방 제목":
            sort_key = "room.title"
        elif key == "파일 수":
            sort_key = "count(*)"

        command = "select room.room_id, room.title, if(file.room_id is null, 0, count(*)), DATE_FORMAT(room.create_date, '%Y/%m/%d'), room.host_id \
                    from room left outer join file \
                        ON room.room_id = file.room_id \
                    group by room.room_id, file.room_id \
                    order by {}" .format(sort_key)

        rs = session.sql.select(command)
        data = []

        for i in range(len(rs)):
            tmp = []
            for j in range(len(rs[i])):
                if j == 2:  # 파일수는 (n) 처리
                    tmp.append("(" + str(rs[i][j]) +")")
                else:
                    tmp.append(str(rs[i][j]))
            data.append(tmp)

        return data






# 새로운 방만들기 창
class CreateRoomWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.show()

    def initUi(self):
        # print(login_info.id, login_info.passwd)

        main_vbox = QVBoxLayout()


        titleLabel = QLabel("title: ")
        self.titleEdit = QLineEdit()
        self.titleEdit.setMaxLength(30)
        self.titleEdit.setStyleSheet("width: 200px;height: 25px;")
        h1_box = QHBoxLayout()
        h1_box.addWidget(titleLabel)
        h1_box.addWidget(self.titleEdit)

        self.createButton = QPushButton("생성")
        self.createButton.setStyleSheet("width: 100px;height: 30px;")
        self.createButton.clicked.connect(self.createButtonClicked)
        h2_box = QHBoxLayout()
        h2_box.addStretch(1)
        h2_box.addWidget(self.createButton)


        main_vbox.addLayout(h1_box)
        main_vbox.addLayout(h2_box)



        self.setLayout(main_vbox)
        self.setWindowTitle("Room")
        self.setGeometry(600, 250, 250, 150)


    def createButtonClicked(self):
        if len(self.titleEdit.text()) == 0:
            QMessageBox.about(self, "warning", "Title을 제대로 입력해주세요!")
            return


        session.create_title = self.titleEdit.text()
        print(session.create_title)

        # db에 해당 title이 이미 있는지 Check하고 할당
        room_titles = []
        for item in session.room_data:
            room_titles.append(item[1])

        if session.create_title in room_titles:
            QMessageBox.about(self, "warning", "이미 있는 방입니다!")
            return

        self.close()


# 방목록
class QCustomQWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)

        self.titleLabel = QLabel()
        self.titleLabel.setStyleSheet("font-size: 13pt; font-weight: bold;")

        self.cntLabel = QLabel()
        self.cntLabel.setStyleSheet("color: red")

        self.dateLabel = QLabel()

        self.hostLabel = QLabel()
        self.hostLabel.setStyleSheet("font-weight: bold;")

        self.allQHBoxLayout = QHBoxLayout()
        self.allQHBoxLayout.addWidget(self.titleLabel)
        self.allQHBoxLayout.addWidget(self.cntLabel)
        self.allQHBoxLayout.addWidget(self.dateLabel)
        self.allQHBoxLayout.addWidget(self.hostLabel)

        self.setLayout(self.allQHBoxLayout)


    def setTextTitle (self, text):
        self.titleLabel.setText(text)

    def getTextTitle(self):
        return self.titleLabel.text()

    def setCntTitle (self, text):
        self.cntLabel.setText(text)

    def getCntTitle(self):
        return self.cntLabel.text()

    def setDateTitle (self, text):
        self.dateLabel.setText(text)

    def getDateTitle(self):
        return self.dateLabel.text()

    def setHostTitle (self, text):
        self.hostLabel.setText(text)

    def getHostTitle(self):
        return self.hostLabel.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoomWindow()
    sys.exit(app.exec_())