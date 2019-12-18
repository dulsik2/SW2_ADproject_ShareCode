
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QDialog, QFileDialog
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QMessageBox, QComboBox, QListWidgetItem, QPlainTextEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

import src.session as session
import syntax
from fileView import *

class FileWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.show()

    def initUI(self):
        #print(session.id, session.passwd)

        main_vbox = QVBoxLayout()


        sortLabel = QLabel("정렬: ")
        self.keyCombo = QComboBox()
        self.keyCombo.addItem("생성날짜")
        self.keyCombo.addItem("파일명")
        self.keyCombo.addItem("좋아요 수")
        self.keyCombo.currentIndexChanged.connect(self.changeCombobox)
        h0_box = QHBoxLayout()
        h0_box.addStretch(1)
        h0_box.addWidget(sortLabel)
        h0_box.addWidget(self.keyCombo)

        # database Query
        session.file_data = self.getFileList(self.keyCombo.currentText())

        self.listwidget = QListWidget()
        self.listwidget.verticalScrollBar().setStyleSheet("width: 10px;")
        for file_name, host, contents, date, like, file_id in session.file_data:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextTitle(file_name)
            myQCustomQWidget.setCntTitle(like)
            myQCustomQWidget.setDateTitle(date)
            myQCustomQWidget.setHostTitle(host)

            # Create QListWidgetItem
            myQListWidgetItem = QListWidgetItem(self.listwidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

            # Add QListWidgetItem into QListWidget
            self.listwidget.addItem(myQListWidgetItem)
            self.listwidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

        h1_box = QHBoxLayout()
        h1_box.addWidget(self.listwidget)
        self.listwidget.doubleClicked.connect(self.listClicked)
        self.listwidget.setStyleSheet("font-size: 15px; width: 150px")


        self.deleteFileButton = QPushButton("파일 삭제")
        self.deleteFileButton.setStyleSheet("color: red;width: 150px;height: 40px;")
        self.deleteFileButton.clicked.connect(self.deleteFileButtonClicked)
        self.uploadFileButton = QPushButton("Upload")
        self.uploadFileButton.setStyleSheet("width: 150px;height: 40px;")
        self.uploadFileButton.clicked.connect(self.uploadFileButtonClicked)
        h2_box = QHBoxLayout()
        h2_box.addWidget(self.deleteFileButton)
        h2_box.addWidget(self.uploadFileButton)

        main_vbox.addLayout(h0_box)
        main_vbox.addLayout(h1_box)
        main_vbox.addLayout(h2_box)

        self.setLayout(main_vbox)
        self.setWindowTitle("File")
        self.setGeometry(600, 250, 600, 500)



    def refreshList(self):
        self.listwidget.clear()

        for file_name, host, contents, date, like, file_id in session.file_data:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextTitle(file_name)
            myQCustomQWidget.setCntTitle(like)
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

        session.contents = session.file_data[idx][2]

        self.fileview = FileViewWindow()
        self.fileview.show()



    # uploadFileButton
    def uploadFileButtonClicked(self):
        filePath =  QFileDialog.getOpenFileName(self)[0]
        fileName = filePath.split('/')[-1]

        if len(fileName) == 0:
            print("파일이 선택되지 않았음!")
            return

        # Update
        # 기존 파일이름 == 업로드 파일이름 && 업로드id == 로그인id
        if self.existFile(fileName):
            command = """
                update file
                set contents = %s,
                    upload_time = now()
                where upload_id = %s and file_name = %s
            """
            insert_data = (self.convertToBinaryData(filePath), session.id, fileName)
            session.sql.update_b(command, insert_data)


        else:
            command = """
                    insert into file(file_name, upload_id, contents, upload_time, room_id, like1)
                    values(%s, %s, %s, now(), %s, 0)
            """
            # command = "insert into file(file_name, upload_id, contents, upload_time, room_id, like1) \
            #                     values(\'{}\', \'{}\', {}, now(), \'{}\', 0);" \
            #           .format(fileName, session.id, self.convertToBinaryData(filePath), session.room_id)
            insert_data = (fileName, session.id, self.convertToBinaryData(filePath), session.room_id)
            session.sql.insert_b(command, insert_data)

        session.file_data = self.getFileList(self.keyCombo.currentText())

        self.refreshList()



    # deleteFileButton
    def deleteFileButtonClicked(self):
        idx = self.listwidget.currentRow()

        # 방 주인과 로그인한 id가 같은지 판별
        host_id = session.file_data[idx][1]

        if host_id != session.id:
            QMessageBox.about(self, "warning", "당신은 파일 주인이 아닙니다!")
            return

        file_id = session.file_data[idx][5]
        command = "delete from file where file_id = \'{}\' and room_id = \'{}\'".format(file_id, session.room_id)
        session.sql.delete(command)
        session.file_data = self.getFileList(self.keyCombo.currentText())

        self.refreshList()


    # Combobox 변경되었을 때
    def changeCombobox(self):
        session.file_data = self.getFileList(self.keyCombo.currentText())
        self.refreshList()



    def getFileList(self, key="생성날짜"):
        sort_key = "upload_time"

        if key == "생성날짜":
            sort_key = "upload_time"
        elif key == "파일명":
            sort_key = "file_name"
        elif key == "좋아요 수":
            sort_key = "like1"

        command = "select file_name, upload_id, CONVERT(contents using utf8), upload_time, like1, file_id \
                    from file \
                    where room_id = \'{}\' \
                    order by {}".format(session.room_id, sort_key)

        rs = session.sql.select(command)
        data = []

        for i in range(len(rs)):
            tmp = []
            for j in range(len(rs[i])):
                if j == 4:  # 파일수는 (n) 처리
                    tmp.append("(" + str(rs[i][j]) +")")
                else:
                    tmp.append(str(rs[i][j]))
            data.append(tmp)

        return data


    def existFile(self, fileName):
        for file_name, host, contents, date, like, file_id in session.file_data:
            if host == session.id and file_name == fileName:
                return True

        return False

    def convertToBinaryData(self, fileName):
        binaryData = None
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()

        return binaryData






# 파일목록
class QCustomQWidget (QWidget):
    def __init__ (self, parent=None):
        super(QCustomQWidget, self).__init__(parent)

        self.titleLabel = QLabel()
        self.titleLabel.setStyleSheet("font-size: 11pt; font-weight: bold;")

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
    window = FileWindow()
    sys.exit(app.exec_())