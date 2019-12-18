# login 창

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget,  QDialog
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from roomlist import *
import session


class LoginWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.show()


    def initUi(self):
        main_vbox = QVBoxLayout()

        id_label = QLabel("ID: ")
        self.idEdit = QLineEdit()
        self.idEdit.setStyleSheet("width: 150px;height: 25px;")
        h1_box = QHBoxLayout()
        h1_box.addStretch(1)
        h1_box.addWidget(id_label)
        h1_box.addWidget(self.idEdit)

        pw_label = QLabel("PW: ")
        self.pwEdit = QLineEdit()
        self.pwEdit.setStyleSheet("width: 150px;height: 25px;")
        self.pwEdit.setEchoMode(QLineEdit.Password)
        h2_box = QHBoxLayout()
        h2_box.addStretch(1)
        h2_box.addWidget(pw_label)
        h2_box.addWidget(self.pwEdit)

        v1_box = QVBoxLayout()
        v1_box.addLayout(h1_box)
        v1_box.addLayout(h2_box)

        self.loginButton = QPushButton("로그인")
        self.loginButton.setStyleSheet("font-size: 20px;width: 120px;height: 60px;")
        self.loginButton.clicked.connect(self.loginButtonClicked)
        h3_box = QHBoxLayout()
        h3_box.addLayout(v1_box)
        h3_box.addStretch(1)
        h3_box.addWidget(self.loginButton)

        self.joinButton = QPushButton("회원가입")
        self.joinButton.setStyleSheet("width: 120px;height: 30px;background-color: #DAC7FF")
        self.joinButton.clicked.connect(self.joinButtonClicked)
        h4_box = QHBoxLayout()
        h4_box.addWidget(self.joinButton)

        main_vbox.addLayout(h3_box)
        main_vbox.addLayout(h4_box)

        self.setLayout(main_vbox)
        self.setWindowTitle("Login")
        self.setGeometry(600, 350, 400, 200)


    # Enter Event > 로그인으로 연결
    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.loginButtonClicked()



    def loginButtonClicked(self):
        sender = self.sender()

        if len(self.idEdit.text()) == 0 or len(self.pwEdit.text()) == 0:
            QMessageBox.about(self, "warning", "ID/PW 제대로 입력해주세요!")
            return


        # 회원인지 check
        id = self.idEdit.text()
        pw = self.pwEdit.text()

        if not self.isMember(id, pw):
            QMessageBox.about(self, "warning", "등록된 회원이 아닙니다!")
            return


        session.id = id
        session.passwd = pw

        self.room = RoomWindow()
        self.room.show()

        self.close()


    # 등록된 회원인지 아닌지 Check
    def isMember(self, id, pw):
        command = "select * from member where id=\'{}\' and  passwd=\'{}\'" .format(id, pw)
        rs = session.sql.select(command)

        if len(rs) == 0:
            return False

        return True


    def joinButtonClicked(self):
        self.joinWindow = JoinMemberWindow()
        self.joinWindow.exec_()




# 새로운 방만들기 창
class JoinMemberWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.show()

    def initUi(self):
        # print(login_info.id, login_info.passwd)

        main_vbox = QVBoxLayout()


        idLabel = QLabel("ID: ")
        self.idEdit = QLineEdit()
        self.idEdit .setMaxLength(20)
        self.idEdit .setStyleSheet("width: 200px;height: 25px;")
        h1_box = QHBoxLayout()
        h1_box.addWidget(idLabel)
        h1_box.addWidget(self.idEdit)


        pwLabel = QLabel("PW: ")
        self.pwEdit = QLineEdit()
        self.pwEdit.setMaxLength(20)
        self.pwEdit.setEchoMode(QLineEdit.Password)
        self.pwEdit.setStyleSheet("width: 200px;height: 25px;")
        h2_box = QHBoxLayout()
        h2_box.addWidget(pwLabel)
        h2_box.addWidget(self.pwEdit)

        nicknameLabel = QLabel("별명: ")
        self.nicknameEdit = QLineEdit()
        self.nicknameEdit.setMaxLength(20)
        self.nicknameEdit.setStyleSheet("width: 200px;height: 25px;")
        h3_box = QHBoxLayout()
        h3_box.addWidget(nicknameLabel)
        h3_box.addWidget(self.nicknameEdit)



        self.createButton = QPushButton("생성")
        self.createButton.setStyleSheet("width: 100px;height: 30px;")
        self.createButton.clicked.connect(self.createButtonClicked)
        h4_box = QHBoxLayout()
        h4_box.addStretch(1)
        h4_box.addWidget(self.createButton)


        main_vbox.addLayout(h1_box)
        main_vbox.addLayout(h2_box)
        main_vbox.addLayout(h3_box)
        main_vbox.addLayout(h4_box)



        self.setLayout(main_vbox)
        self.setWindowTitle("Room")
        self.setGeometry(600, 250, 250, 150)


    # Enter Event > 회원가입으로 연결
    def keyPressEvent(self, e):
        if e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.createButtonClicked()


    def createButtonClicked(self):
        id, pw, nickname = "", "", ""

        if len(self.idEdit.text()) == 0 or len(self.pwEdit.text()) == 0:
            QMessageBox.about(self, "warning", "ID/PW 제대로 입력해주세요!")
            return

        id = self.idEdit.text()
        pw = self.pwEdit.text()
        if len(self.nicknameEdit.text()) == 0:
            nickname = "default"




        # 등록된 ID가 있는지 Check
        if self.isinMember(id):
            QMessageBox.about(self, "warning", "이미 등록된 ID 입니다!")
            return

        # 회원가입(insert)
        self.joinMember(id, pw, nickname)
        QMessageBox.about(self, "Pass", "회원가입되었습니다!")
        self.close()




    # 등록된 아이디가 있는지 Check
    def isinMember(self, id):
        command = "select * from member where id=\'{}\'".format(id)
        rs = session.sql.select(command)

        if len(rs) == 0:
            return False

        return True


    def joinMember(self, id, pw, nickname):
        command = "insert into member(id, passwd, nickname, join_date)" \
                  "values(\'{}\', \'{}\', \'{}\', now())" .format(id, pw, nickname)
        session.sql.insert(command)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())