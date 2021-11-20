import sys
import os

from PySide2 import *
from qt_material import *
from qtpy import QtCore
from qtpy import QtGui

from ui_mainGUI import *

import screen_brightness_control as sbc
import requests

URL = "https://im-fine-backend.herokuapp.com/api"
token = ""
user = {}
user_id = 0


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowIcon(QtGui.QIcon(":/User/User/home.png"))
        self.setWindowTitle("I Am Fine Notification System")

        #########################
        # STACK PAGES NAVIGATION#
        #########################
        self.ui.SignIn.clicked.connect(lambda: self.ui.switchSignInReg.setCurrentWidget(self.ui.SignIn_2))
        self.ui.Reg.clicked.connect(lambda: self.ui.switchSignInReg.setCurrentWidget(self.ui.Register))
        self.ui.LoginButton.clicked.connect(lambda: self.login_checker())
        self.ui.regButton.clicked.connect(lambda: [self.registration(),
                                                   self.ui.userPageSwitch.setCurrentWidget(self.ui.Homepage)])

        # User
        self.ui.mainBtn.clicked.connect(lambda: self.ui.userPageSwitch.setCurrentWidget(self.ui.Homepage))
        self.ui.Notification.clicked.connect(lambda: self.notification_control())
        self.ui.profileBtn.clicked.connect(lambda: self.ui.userPageSwitch.setCurrentWidget(self.ui.Profilepage))
        self.ui.friendBtn.clicked.connect(lambda: self.ui.userPageSwitch.setCurrentWidget(self.ui.Friendpage))
        self.ui.createPostBtn.clicked.connect(lambda: self.ui.userPageSwitch.setCurrentWidget(self.ui.CreatePostpage))
        self.ui.createButton.clicked.connect(lambda: self.ui.userPageSwitch.setCurrentWidget(self.ui.CreatePostpage2))
        self.ui.doneButton.clicked.connect(lambda: [self.ui.userPageSwitch.setCurrentWidget(self.ui.CreatePostpage),
                                                    self.ui.plainTextEdit.setPlainText("")])
        self.ui.meetScheduleBtn.clicked.connect(lambda: self.ui.userPageSwitch.setCurrentWidget(self.ui.meetingSchedule)
                                                )
        self.ui.nextBtn.clicked.connect(lambda: self.ui.time.setVisible(True))
        self.ui.editBtn_3.clicked.connect(lambda: self.ui.userPageSwitch.setCurrentWidget(self.ui.meetingSchedule2)
                                          )
        self.ui.nextBtn_2.clicked.connect(lambda: [self.ui.userPageSwitch.setCurrentWidget(self.ui.meetingSchedule),
                                                   self.ui.time.setVisible(False)
                                                   ])
        self.ui.HistoryBtn.clicked.connect(lambda: self.ui.userPageSwitch.setCurrentWidget(self.ui.history))
        self.ui.settingButton.clicked.connect(lambda: [self.ui.userPageSwitch.setCurrentWidget(self.ui.setting_user),
                                                       self.ui.brightnessSlider.setValue(sbc.get_brightness())
                                                       ])
        self.ui.brightnessSlider.sliderReleased.connect(lambda: sbc.set_brightness(self.ui.brightnessSlider.value()))
        self.ui.logoutBtn.clicked.connect(lambda: [self.ui.switchSignInReg.setCurrentWidget(self.ui.SignIn_2),
                                                   self.ui.mainSwitch.setCurrentWidget(self.ui.SignInRegPage),
                                                   self.ui.emailEnter.setPlaceholderText("Username"),
                                                   self.ui.PasswordEnter.setPlaceholderText("Password")
                                                   ])

        # Admin
        self.ui.mainBtn_admin.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Homepage_admin))
        self.ui.profileBtn_admin.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Profilepage_admin))
        self.ui.makeAnnocementBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.makeAnnoucementPage))
        self.ui.makeBtn.clicked.connect(lambda: self.ui.plainTextEdit_2.setPlainText(""))
        self.ui.manageUserBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.manageUserPage))
        self.ui.adminLogBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.adminLog))
        self.ui.settingButton_admin.clicked.connect(lambda: [self.ui.stackedWidget.setCurrentWidget(self.ui.settingpage_admin),
                                                             self.ui.brightnessSlider_2.setValue(sbc.get_brightness())
                                                             ])
        self.ui.brightnessSlider_2.sliderReleased.connect(lambda: sbc.set_brightness(self.ui.brightnessSlider_2.value()))
        self.ui.logoutBtn_2.clicked.connect(lambda: [self.ui.switchSignInReg.setCurrentWidget(self.ui.SignIn_2),
                                                   self.ui.mainSwitch.setCurrentWidget(self.ui.SignInRegPage),
                                                   self.ui.emailEnter.setPlaceholderText("Username"),
                                                   self.ui.PasswordEnter.setPlaceholderText("Password")
                                                   ])
        self.show()

    def login_checker(self):
        global token
        global user
        global user_id
        username = self.ui.emailEnter.text()
        password = self.ui.PasswordEnter.text()

        # request data
        data = {"username" : username,
                "password" : password}

        # Make request
        r = requests.post(url = URL + "/auth/login/", data = data)

        if r.status_code == 200:
            self.ui.error_2.setText("")
            token = r.json()["key"]
            user_id = r.json()["user_id"]

            headers = {"Authorization": f"Token {token}"}

            user = requests.get(url =f"{URL}/users/{user_id}", headers=headers).json()
            user_type = user["userType"]

            self.update_profile()

            if user_type == "ADMIN":
                self.ui.mainSwitch.setCurrentWidget(self.ui.AdminPage)
            elif user_type == "REGULAR":
                self.ui.mainSwitch.setCurrentWidget(self.ui.UserPage)
        else:
            error_msg = r.text[r.text.find("[") + 2:]
            self.ui.error_2.setWordWrap(True)
            self.ui.error_2.setFixedHeight(50)
            self.ui.error_2.setText(error_msg[:error_msg.find('"')])


    def update_profile(self):
        self.ui.name.setText(user["username"])
        self.ui.name_2.setText(user["username"])
        self.ui.name_3.setText(user["username"])
        self.ui.name_4.setText(user["username"])
        self.ui.name_5.setText(user["username"])
        self.ui.name_6.setText(user["username"])
        self.ui.name_7.setText(user["username"])
        self.ui.name_8.setText(user["username"])
        self.ui.mail_2.setText(user["email"])
        self.ui.mail.setText(user["email"])


    def notification_control(self):
        if self.ui.notification_Win.isVisible():
            self.ui.notification_Win.setVisible(False)
        else:
            self.ui.notification_Win.setVisible(True)

    def registration(self):
        global token
        global user
        global user_id
        username = self.ui.usenameEnter.text()
        password = self.ui.emailEnter_3.text()
        email = self.ui.PasswordEnter_2.text()

        # request data
        data = {"username" : username,
                "email" : email,
                "password1" : password,
                "password2" : password,
                "userType" : "REGULAR"}

        # Make request
        r = requests.post(url=URL + "/auth/register/", data=data)
        print(r.status_code)

        if r.status_code == 201:
            self.ui.error.setText("")
            token = r.json()["key"]
            user_id = r.json()["user_id"]
            self.ui.mainSwitch.setCurrentWidget(self.ui.UserPage)
        else:
            error_msg = r.text[r.text.find("[")+2:]
            self.ui.error.setWordWrap(True)
            self.ui.error.setFixedHeight(50)
            self.ui.error.setText(error_msg[:error_msg.find('"')])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

