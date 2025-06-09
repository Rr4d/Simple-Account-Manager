from PyQt6.QtWidgets import (
    QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QLabel, QFrame, QDialog
)
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import Qt
import ppa
from tkinter import messagebox

class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adding an account")
        self.setFixedSize(320, 240)
        self.setWindowIcon(QIcon('add.png'))
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        titleLabel = QLabel("Add Account")
        titleLabel.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titleLabel)

        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Username")
        self.usernameInput.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #EEB917;
            }
        """)
        layout.addWidget(self.usernameInput)

        self.passwordInput = QLineEdit()
        self.passwordInput.setPlaceholderText("Password")
        self.passwordInput.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #EEB917;
            }
        """)
        layout.addWidget(self.passwordInput)

        self.siteInput = QLineEdit()
        self.siteInput.setPlaceholderText("Site")
        self.siteInput.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #EEB917;
            }
        """)
        layout.addWidget(self.siteInput)

        self.enterButton = QPushButton("Add")
        self.enterButton.setStyleSheet("""
            QPushButton {
                background-color: #EEB917;
                color: #090E16;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D4A017;
            }
        """)
        self.enterButton.clicked.connect(self.accept)
        layout.addWidget(self.enterButton)

        self.setLayout(layout)

    def getData(self):
        return self.usernameInput.text().strip(), self.passwordInput.text().strip(), self.siteInput.text().strip()

class EditAccountDialog(QDialog):
    def __init__(self, user_id, username, password, site, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.original_username = username
        self.original_password = password
        self.original_site = site
        self.setWindowTitle("Editing an account")
        self.setFixedSize(320, 280)
        self.setWindowIcon(QIcon('edit.png'))
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        titleLabel = QLabel("Edit Account")
        titleLabel.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titleLabel)

        self.usernameInput = QLineEdit()
        self.usernameInput.setText(self.original_username)
        self.usernameInput.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #EEB917;
            }
        """)
        layout.addWidget(self.usernameInput)

        self.passwordInput = QLineEdit()
        self.passwordInput.setText(self.original_password)
        self.passwordInput.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #EEB917;
            }
        """)
        layout.addWidget(self.passwordInput)

        self.siteInput = QLineEdit()
        self.siteInput.setText(self.original_site)
        self.siteInput.setReadOnly(True)
        self.siteInput.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f0f0f0;
            }
        """)
        

        btnLayout = QHBoxLayout()
        self.editButton = QPushButton("Edit")
        self.editButton.setStyleSheet("""
            QPushButton {
                background-color: #EEB917;
                color: #090E16;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D4A017;
            }
        """)
        self.cancelButton = QPushButton("Close")
        self.cancelButton.setStyleSheet("""
            QPushButton {
                background-color: #ccc;
                color: #090E16;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
        """)
        self.editButton.clicked.connect(self.editData)
        self.cancelButton.clicked.connect(self.reject)
        btnLayout.addWidget(self.editButton)
        btnLayout.addWidget(self.cancelButton)
        layout.addLayout(btnLayout)

        self.setLayout(layout)

    def editData(self):
        new_username = self.usernameInput.text().strip()
        new_password = self.passwordInput.text().strip()
        if not (new_username and new_password):
            messagebox.showerror('Error', 'Please fill all fields.')
            return
        if (new_username == self.original_username and new_password == self.original_password):
            messagebox.showerror('Error', 'No changes detected in the data.')
            return
        if ppa.check_duplicate_edit(self.user_id, new_username, new_password, self.original_site):
            messagebox.showerror('Error', 'Duplicate entry: This username and password combination already exists.')
            return
        ppa.update_data(self.user_id, new_username, new_password)
        self.accept()

    def getData(self):
        return self.user_id, self.usernameInput.text().strip(), self.passwordInput.text().strip()

class kecewa(QWidget):
    def __init__(self):
        super().__init__()
        self.original_username = ""
        self.original_password = ""
        self.original_site = ""
        self.setWindowTitle("Simple Account Manager")
        self.setWindowIcon(QIcon('icon.png'))
        self.setFixedSize(900, 600)
        self.setupUI()
        self.loadData()

    def setupUI(self):
        mainLayout = QHBoxLayout(self)
        self.usernameInput = QLineEdit()
        self.usernameInput.setText(self.original_username)
        self.passwordInput = QLineEdit()
        self.passwordInput.setText(self.original_password)
        self.siteInput = QLineEdit()
        self.siteInput.setText(self.original_site)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #1e1e1e; color: white;")
        sidebarLayout = QVBoxLayout(sidebar)
        sidebarLayout.setContentsMargins(10, 10, 10, 10)
        sidebarLayout.setSpacing(20)

        # User info
        userPic = QLabel()
        pixmap = QPixmap('pp.webp').scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        userPic.setPixmap(pixmap)
        sidebarLayout.addWidget(userPic, alignment=Qt.AlignmentFlag.AlignLeft)

        userNameLabel = QLabel("Hi, I am The User")
        userNameLabel.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        sidebarLayout.addWidget(userNameLabel, alignment=Qt.AlignmentFlag.AlignLeft)

        userBasicLabel = QLabel("These are my accounts from different sites")
        userBasicLabel.setFont(QFont("Arial", 8))
        sidebarLayout.addWidget(userBasicLabel, alignment=Qt.AlignmentFlag.AlignLeft)

        # Editing guide
        editingLabel = QLabel("To edit an account, just simply select the ID of\nthe account that you wanna edit")
        editingLabel.setFont(QFont("OldEnglish", 8))
        editingLabel.setStyleSheet("color: #EEB917;")
        sidebarLayout.addWidget(editingLabel, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add Account Button
        self.addAccountButton = QPushButton("Add Account")
        self.addAccountButton.setStyleSheet("""
            QPushButton {
                background-color: #FCFBF4;
                color: #4A5462;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #EEB917;
                color: #090E16;
            }
        """)
        self.addAccountButton.clicked.connect(self.addOrEditAccount)
        sidebarLayout.addWidget(self.addAccountButton)

        # Cancel Edit Button
        self.cancelEditButton = QPushButton("Cancel Edit")
        self.cancelEditButton.setStyleSheet("""
            QPushButton {
                background-color: #FFF2D7;
                color: #704F15;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #EEDEC5;
                color: #42240C;
            }
        """)
        self.cancelEditButton.clicked.connect(self.cancelEdit)
        self.cancelEditButton.hide()
        sidebarLayout.addWidget(self.cancelEditButton)

        # Recent Change/Update Section
        recentChangeLabel = QLabel("Recent Change")
        recentChangeLabel.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        sidebarLayout.addWidget(recentChangeLabel)

        # Recently used items - dynamically fetched last 3 entries
        udus = ppa.get_data()
        # Sort by created_at descending and take top 3
        from datetime import datetime
        def parse_date(item):
            try:
                return datetime.strptime(item[4], "%Y-%m-%d %H:%M:%S")
            except Exception:
                return datetime.min
        sorted_udus = sorted(udus, key=parse_date, reverse=True)[:3]
        for user_id, name, password, site, created_at in sorted_udus:
            label = QLabel(f"{site} : {name} : {password}")
            label.setFont(QFont("Arial", 8))
            sidebarLayout.addWidget(label)

        # Footer
        footerPic = QLabel()
        pixi=QPixmap('pic.png').scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        footerPic.setPixmap(pixi)
        sidebarLayout.addStretch()
        sidebarLayout.addWidget(footerPic, alignment=Qt.AlignmentFlag.AlignLeft)
        # Main content area
        contentArea = QFrame()
        contentArea.setStyleSheet("background-color: #2e2e2e; color: white;")
        contentLayout = QVBoxLayout(contentArea)
        contentLayout.setContentsMargins(20, 20, 20, 20)
        contentLayout.setSpacing(15)

        # Greeting and search bar (Doesn't work lol; just a decoration)
        greetingLayout = QHBoxLayout()
        greetingLabel = QLabel("Hello, there! \u270B")
        greetingLabel.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        greetingLayout.addWidget(greetingLabel)

        self.searchInput = QLineEdit()
        self.searchInput.setPlaceholderText("Search for an account or website")
        self.searchInput.setFixedWidth(300)
        greetingLayout.addWidget(self.searchInput)

        contentLayout.addLayout(greetingLayout)

        # Categories section
        categoriesLayout = QHBoxLayout()
        categories = [
            ("Socials", "#16c5e4"),
            ("Utilities", "#e01010"),
            ("Games", "#0fe20f"),
        ]
        for name, color in categories:
            catFrame = QFrame()
            catFrame.setFixedSize(100, 60)
            catFrame.setStyleSheet(f"background-color: {color}; border-radius: 10px;")
            catLabel = QLabel(name)
            catLabel.setStyleSheet("color: white; font-weight: bold;")
            catLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            catLayout = QVBoxLayout(catFrame)
            catLayout.addWidget(catLabel)
            categoriesLayout.addWidget(catFrame)
        contentLayout.addLayout(categoriesLayout)

        # Accounts table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Account", "Site", "Created/Updated"])
        self.table.setRowCount(0)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.cell_was_clicked)
        self.table.cellDoubleClicked.connect(self.cell_was_clicked)
        self.table.setColumnWidth(4, 125)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: black;
                color: white;
            }
            QTableWidget QHeaderView::section {
                background-color: #444444;
                color: white;
            }
        """)
        contentLayout.addWidget(self.table)

        # Delete section
        deleteLayout = QHBoxLayout()
        self.idInput = QLineEdit()
        self.idInput.setPlaceholderText("Enter the ID you want to delete")
        deleteLayout.addWidget(self.idInput)

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.removeData)
        deleteLayout.addWidget(self.deleteButton)

        contentLayout.addLayout(deleteLayout)

        mainLayout.addWidget(sidebar)
        mainLayout.addWidget(contentArea)

        self.setLayout(mainLayout)

    def addOrEditAccount(self):
        if hasattr(self, 'selected_id'):
            # Edit mode
            dialog = EditAccountDialog(self.selected_id,
                                       self.original_username,
                                       self.original_password,
                                       self.original_site,
                                       self)
            if dialog.exec():
                user_id, new_username, new_password = dialog.getData()
                if not (new_username and new_password):
                    messagebox.showerror('Error', 'Please fill all fields.')
                    return
                if (new_username == self.original_username and new_password == self.original_password):
                    messagebox.showerror('Error', 'No changes detected in the data.')
                    return
                if ppa.check_duplicate_edit(user_id, new_username, new_password, self.original_site):
                    messagebox.showerror('Error', 'Duplicate entry: This username and password combination already exists.')
                    return
                ppa.update_data(user_id, new_username, new_password)
                self.loadData()
                self.cancelEdit()
        else:
            # Add mode
            dialog = AddAccountDialog(self)
            if dialog.exec():
                username, password, site = dialog.getData()
                if not (username and password and site):
                    messagebox.showerror('Error', 'Please fill all fields.')
                    return
                if ppa.check_duplicate(username, password, site):
                    messagebox.showerror('Error', 'Duplicate entry: This username, password, and site combination already exists.')
                    return
                ppa.insert_data(username, password, site)
                self.loadData()

    def cell_was_clicked(self, row, column):
        if column == 0:
            self.selected_id = self.table.item(row, 0).text()
            self.original_username = self.table.item(row, 1).text()
            self.original_password = self.table.item(row, 2).text()
            self.original_site = self.table.item(row, 3).text()
            self.usernameInput.setText(self.original_username)
            self.passwordInput.setText(self.original_password)
            self.siteInput.setText(self.original_site)
            self.addAccountButton.setText("Edit Account")
            self.cancelEditButton.show()

    def cancelEdit(self):
        if hasattr(self, 'selected_id'):
            del self.selected_id
        self.usernameInput.clear()
        self.passwordInput.clear()
        self.siteInput.clear()
        self.addAccountButton.setText("Add Account")
        self.cancelEditButton.hide()

    def removeData(self):
        user_id = self.idInput.text().strip()
        if user_id.isdigit():
            ppa.delete_data_by_id(int(user_id))
            self.idInput.clear()
            self.loadData()
        else:
            messagebox.showerror('Cihuy', 'Mana ID-nya?')

    def loadData(self):
        from datetime import datetime, timedelta
        udus = ppa.get_data()
        self.table.setRowCount(0)
        for row_num, (user_id, name, password, site, created_at) in enumerate(udus):
            self.table.insertRow(row_num)
            self.table.setItem(row_num, 0, QTableWidgetItem(str(user_id)))
            self.table.setItem(row_num, 1, QTableWidgetItem(name))
            self.table.setItem(row_num, 2, QTableWidgetItem(password))
            self.table.setItem(row_num, 3, QTableWidgetItem(site))
            item = QTableWidgetItem(created_at)
            font = item.font()
            try:
                created_dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                if now - created_dt > timedelta(minutes=1):
                    font.setBold(True)
            except Exception:
                pass
            item.setFont(font)
            self.table.setItem(row_num, 4, item)