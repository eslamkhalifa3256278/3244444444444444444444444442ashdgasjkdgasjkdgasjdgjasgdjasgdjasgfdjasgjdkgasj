import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QListWidget, QTextEdit, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("LEO.AI")
        self.setFixedSize(400, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 30px;
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #4285F4;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #3367D6;
            }
            QLabel#divider {
                text-align: center;
                color: #777;
                margin: 15px 0;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)

        # العنوان
        title = QLabel("# LEO.AI")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # حقل البريد الإلكتروني
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("البريد الالكتروني")
        layout.addWidget(self.email_input)

        # حقل كلمة المرور
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # زر تسجيل الدخول
        login_btn = QPushButton("تسجيل الدخول")
        layout.addWidget(login_btn)

        # فاصل
        divider = QLabel("أو")
        divider.setObjectName("divider")
        divider.setAlignment(Qt.AlignCenter)
        layout.addWidget(divider)

        # أزرار تسجيل الدخول الخارجية
        btn_layout = QHBoxLayout()
        google_btn = QPushButton("Google")
        microsoft_btn = QPushButton("Microsoft")
        btn_layout.addWidget(google_btn)
        btn_layout.addWidget(microsoft_btn)
        layout.addLayout(btn_layout)

        # فاصل
        divider2 = QLabel("أو")
        divider2.setObjectName("divider")
        divider2.setAlignment(Qt.AlignCenter)
        layout.addWidget(divider2)

        # زر إنشاء حساب
        create_account_btn = QPushButton("قم بإنشاء حساب جديد")
        layout.addWidget(create_account_btn)

        self.setLayout(layout)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("LEOAI")
        self.setFixedSize(1000, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            }
            QListWidget {
                background-color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e0e0e0;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #4285F4;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: #3367D6;
            }
            QFrame#sidebar {
                background-color: white;
                border-right: 1px solid #ddd;
            }
            QFrame#chat_area {
                background-color: #f5f5f5;
            }
        """)

        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # الشريط الجانبي
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)

        sidebar_title = QLabel("# LEOAI")
        sidebar_title.setObjectName("title")
        sidebar_title.setAlignment(Qt.AlignRight)
        sidebar_layout.addWidget(sidebar_title)

        new_chat_btn = QPushButton("محادثة جديدة")
        sidebar_layout.addWidget(new_chat_btn)

        sidebar_layout.addSpacing(20)

        old_chats_label = QLabel("المحادثات القديمة")
        old_chats_label.setAlignment(Qt.AlignRight)
        sidebar_layout.addWidget(old_chats_label)

        self.chats_list = QListWidget()
        self.chats_list.addItems(["محادثة واحد", "محادثة اثنين", "محادثة ثلاثة"])
        sidebar_layout.addWidget(self.chats_list)

        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)

        # منطقة المحادثة
        chat_area = QFrame()
        chat_area.setObjectName("chat_area")
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(20, 20, 20, 20)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("مرحبًا بك...")
        chat_layout.addWidget(self.chat_display)

        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(100)
        self.message_input.setPlaceholderText("اكتب رسالتك هنا...")
        chat_layout.addWidget(self.message_input)

        send_btn = QPushButton("إرسال")
        chat_layout.addWidget(send_btn)

        chat_area.setLayout(chat_layout)
        main_layout.addWidget(chat_area)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # لتطبيق RTL
    app.setLayoutDirection(Qt.RightToLeft)
    
    # اختر أي نافذة تريد عرضها للتجربة
    window = LoginWindow()  # أو ChatWindow() لرؤية واجهة المحادثة
    window.show()
    
    sys.exit(app.exec_())
