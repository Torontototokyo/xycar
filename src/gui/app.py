from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
    QGroupBox, QSpinBox,QTabWidget, QMessageBox,QTextEdit
)
from pymysql.err import OperationalError
from PyQt6.QtCore import Qt
import sys
import gui.console as console
import gui.translator as t
import pandas as pd
import work_card.db as db
from work_card.sms import Sample
import os
from work_card.utils import get_resource_path
from dotenv import load_dotenv

# 获取打包在内部的 .env 文件的路径
dotenv_path = get_resource_path('.env')

# 明确告诉 load_dotenv 从这个路径加载
load_dotenv(dotenv_path=dotenv_path)

translator = t.YAMLTranslator()


translator.set_language('zh')



class DatabaseConnectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(translator.get("myapp"))
        self.setMinimumSize(600, 400)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Main layout for the first tab
       
        self.create_log_processor_tab()

        self.create_sms_tab()


     
    def create_log_processor_tab(self):
        self.main_tab = QWidget()
        self.tabs.addTab(self.main_tab, translator.get("main_tab"))
        
        main_layout = QVBoxLayout(self.main_tab)
         # Create the database connection group
        db_group = QGroupBox(translator.get("db_connection_settings"))

        db_layout = QGridLayout()
        # db_layout = QVBoxLayout()


        
        # Database fields
        # Row 0: Username
        db_layout.addWidget(QLabel(translator.get("user")), 0, 0)
        self.db_username = QLineEdit()
        self.db_username.setPlaceholderText(translator.get("enter_username"))
        # self.db_username.setText('root')  # Default username
        db_layout.addWidget(self.db_username, 0, 1)
        
        # Row 1: Password
        db_layout.addWidget(QLabel(translator.get("password")), 1, 0)
        self.db_password = QLineEdit()
        self.db_password.setPlaceholderText(translator.get("enter_password"))
        self.db_password.setEchoMode(QLineEdit.EchoMode.Password)
        # self.db_password.setText('root')  # Default password
        db_layout.addWidget(self.db_password, 1, 1)
        
        # Row 2: Address
        db_layout.addWidget(QLabel(translator.get("address")), 2, 0)
        self.db_address = QLineEdit()
        self.db_address.setPlaceholderText(translator.get("enter_address"))
        self.db_address.setText('localhost')
        db_layout.addWidget(self.db_address, 2, 1)
        
        # Row 3: Port
        db_layout.addWidget(QLabel(translator.get("db_port")), 3, 0)
        self.db_port = QSpinBox()
        self.db_port.setRange(1, 65535)
        self.db_port.setValue(3306)  # Default MySQL port
        db_layout.addWidget(self.db_port, 3, 1)
        
        # Row 4: Database Name
        db_layout.addWidget(QLabel(translator.get("db_name")), 4, 0)
        self.db_name = QLineEdit()
        self.db_name.setPlaceholderText(translator.get("enter_db_name"))
        # self.db_name.setText('cars_db')  # Default database name
        db_layout.addWidget(self.db_name, 4, 1)
        
        db_group.setLayout(db_layout)
        main_layout.addWidget(db_group)

        # Add console widget
        
        # Create the file selectors group
        file_group = QGroupBox(translator.get("file_selectors"))
        file_layout = QVBoxLayout()
        
        # File Selector 1
        file1_layout = QHBoxLayout()
        file1_layout.addWidget(QLabel(translator.get("enter_card_file")))
        self.file1_path = QLineEdit()
        self.file1_path.setPlaceholderText(translator.get("select_card_file"))
        file1_layout.addWidget(self.file1_path)
        self.file1_button = QPushButton(translator.get("select_file"))
        self.file1_button.clicked.connect(lambda: self.browse_file(self.file1_path))
        file1_layout.addWidget(self.file1_button)
        file_layout.addLayout(file1_layout)

        
        
        # File Selector 2
        file2_layout = QHBoxLayout()
        file2_layout.addWidget(QLabel(translator.get("enter_logs_file")))
        self.file2_path = QLineEdit()
        self.file2_path.setPlaceholderText(translator.get("select_logs_file"))
        file2_layout.addWidget(self.file2_path)
        self.file2_button = QPushButton(translator.get("select_file"))
        self.file2_button.clicked.connect(lambda: self.browse_file(self.file2_path))
        file2_layout.addWidget(self.file2_button)
        file_layout.addLayout(file2_layout)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        
        self.console = console.ConsoleOutput(namespace={'app': self})
        main_layout.addWidget(self.console)
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.connect_button = QPushButton(translator.get("run"))
        self.connect_button.clicked.connect(self.run)
        button_layout.addWidget(self.connect_button)
        
        self.clear_button = QPushButton(translator.get("clear_all"))
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        self.exit_button = QPushButton(translator.get("exit"))
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)
        
        main_layout.addLayout(button_layout)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()

     
    def create_sms_tab(self):
        """Create a tab with file selector, run, clear, and exit buttons"""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        self.tabs.addTab(tab, translator.get("sms_tab"))  # You can use translator.get("send_sms") if you have a translation for it
        
        
        # === FILE SELECTOR SECTION ===
        file_group = QGroupBox(translator.get("file_selectors"))

        file_layout = QVBoxLayout(file_group)
        
        # File path with browse button
        file_row = QHBoxLayout()
        
        self.sms_file_path = QLineEdit()
        self.sms_file_path.setPlaceholderText(translator.get("select_file"))

        file_row.addWidget(self.sms_file_path)
        
        browse_btn = QPushButton(translator.get("select_file"))

        browse_btn.clicked.connect(lambda: self.browse_file(self.sms_file_path))

        file_row.addWidget(browse_btn)
        
        file_layout.addLayout(file_row)
        

        tab_layout.addWidget(file_group)
        
        # === Console DISPLAY ===
        self.sms_console = console.ConsoleOutput(namespace={'app': self})
        tab_layout.addWidget(self.sms_console)
        
        
        # === BUTTON SECTION ===


        button_layout = QHBoxLayout()

        
        # Run button
        self.run_btn = QPushButton(translator.get("run"))
        self.run_btn.clicked.connect(self.run_sms_processor)

        button_layout.addWidget(self.run_btn)
        
        # Clear button
        self.clear_btn = QPushButton(translator.get("clear_all"))
        self.clear_btn.clicked.connect(self.clear_sms_content)

        button_layout.addWidget(self.clear_btn)
        
        # Exit button
        self.exit_btn = QPushButton(translator.get("exit"))
        self.exit_btn.clicked.connect(self.close)

        button_layout.addWidget(self.exit_btn)
        
        # Status label
       
        tab_layout.addLayout(button_layout)
        
        # Add stretch to push everything up
        tab_layout.addStretch()
        

    def run_sms_processor(self):
        sms_file = self.sms_file_path.text()
        if not sms_file:
            self.sms_console.print_output("⚠️  Please select a file to process.")
            return

        df = pd.read_excel(sms_file)
    
        for _,row in df.iterrows():
            car_no = row['车牌号码']
            phone_number = row['手机号码']
            hour = row['超时小时']
            # print(phone_number,car_no,hour)
            try:
                Sample.sms(car_no=car_no,hour=hour,phone_numer=phone_number)
                now = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                self.sms_console.print_output(f"✅ {translator.get('sms_success')} {car_no} - {phone_number} {translator.get('time')} : {now}")
            except Exception as e:
                self.sms_console.print_output(f"❌ {translator.get('sms_failed')} {car_no} - {phone_number} {translator.get('time')} : {now}")
            pass
    def clear_sms_content(self):
        self.sms_file_path.clear()
        self.sms_console.clear()

    def browse_file(self, line_edit):
        """Open file dialog and set the selected file path"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Files (*.*);;Text Files (*.txt);;CSV Files (*.csv);;JSON Files (*.json)"
        )
        if file_path:
            line_edit.setText(file_path)
    
    def run(self):
        """Collect all values and display them (placeholder for actual connection)"""
        username = self.db_username.text()
        password = self.db_password.text()
        address = self.db_address.text()
        port = self.db_port.value()
        db_name = self.db_name.text()
        card_excel = self.file1_path.text()
        logs_excel = self.file2_path.text()

        if not username:
            return self.console.print_output('⚠️ 请输入数据库用户名')
        if not password:
            return self.console.print_output('⚠️ 请输入数据库密码')
        if not db_name:
            return self.console.print_output('⚠️ 请输入数据库名称')
        if not address:
            return self.console.print_output('⚠️ 请输入数据库主机')
        if not port:
            return self.console.print_output('⚠️ 请输入数据库连接端口')
        
            
        
        print("=" * 50)
        print("Database Connection Details:")
        print(f"Username: {username}")
        print(f"Password: {'*' * len(password)}")
        print(f"Address: {address}")
        print(f"Port: {port}")
        print(f"Database: {db_name}")
        print(f"Card File: {card_excel}")
        print(f"Log File: {logs_excel}")
        print("=" * 50)

      
        
        # Here you would add your actual database connection logic
        # e.g., using psycopg2, sqlite3, mysql-connector-python, etc.
        
        # Simple validation
        
        self.console.print_output("✅ All fields filled. Ready to connect!")

        conf = db.DbConf(user=username,password=password,address=address,port=port,db_name=db_name)

        res = db.test_connection_with_context(conf)

        if not res:
            return self.console.print_output(translator.get('esdbconn_failed'))
            
        engine = db.init_engine(conf)

        
        if card_excel:
            df = pd.read_excel(card_excel)
    
            db.import_car_cards(df,engine)
    
        if logs_excel:
    
            df = pd.read_excel(logs_excel)
            
            db.import_logs(df,engine)

        if logs_excel or card_excel:

            self.console.print_output('----------运行中----------')
            
            result = db.update_card_parking_time_db(engine=engine)

            if result:
                self.console.print_output(f"✅ 超时转临停车辆已导出到: {result}")
            else:
                self.console.print_output("⚠️ 没有超时转临停车辆需要导出")


            
            
    
    def clear_all(self):
        """Clear all input fields"""
        self.db_username.clear()
        self.db_password.clear()
        self.db_address.clear()
        self.db_port.setValue(3306)
        self.db_name.clear()
        self.file1_path.clear()
        self.file2_path.clear()
        self.console.print_output("All fields cleared")

    def add_tab(self, title, content):
        """Add a tab with simple content"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        label = QLabel(content)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.tabs.addTab(tab, title)


def main():
    app = QApplication(sys.argv)
    
    # Set application style for better appearance
    app.setStyle('Fusion')
    
    window = DatabaseConnectionWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()