# -*- coding: utf-8 -*-
import sys, os.path, os, pysftp
from PyQt5.QtCore import QObject, QSize, Qt
from PyQt5.QtWidgets import *

class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUi()
        self.status = 0


    def setupUi(self):

        self.download_index = 0
        self.log_File_List = []

        self.resize(600, 800)
        self.setWindowTitle('Lotte Log Downloader')
        #self.setStyleSheet("QMainWindow{background-color:#ffffff};")
        #self.setWindowIcon(windowIcon)
        #self.centralwidget = QWidget(self)

        vBox_Central = QVBoxLayout()
        self.setLayout(vBox_Central)

        self.tw_Log_File_List = QTableWidget(0,1,self)
        self.tw_Log_File_List.setHorizontalHeaderItem(0, QTableWidgetItem('파일 리스트'))
        self.tw_Log_File_List.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_Log_File_List.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_Log_File_List.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tw_Log_File_List.horizontalHeader().setStretchLastSection(True)
        self.tw_Log_File_List.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_Log_File_List.setStyleSheet("""
                                        QWidget{background-color:#f8f9f9}
                                        QHeaderView::section{padding:5px;border:0px}
                                        QTableView{selection-color:white;selection-background-color:#566573}
                                        QTableView QTableCornerButton::section {background:#f8f9f9}
                                        """)

        vBox_Central.addWidget(self.tw_Log_File_List)

        self.btn_Reload = QPushButton("Reload")
        vBox_Central.addWidget(self.btn_Reload)

        hbox_File = QHBoxLayout()
        vBox_Central.addLayout(hbox_File)

        self.let_Folder_Dir = QLineEdit(self)
        hbox_File.addWidget(self.let_Folder_Dir)
        self.btn_Folder_Dir = QPushButton("저장위치",self)
        hbox_File.addWidget(self.btn_Folder_Dir)

        self.btn_Download = QPushButton("다운로드",self)
        vBox_Central.addWidget(self.btn_Download)

        self.lbl_Status = QLabel(self)
        vBox_Central.addWidget(self.lbl_Status)

        self.show()
        self.startSftp()

        self.btn_Folder_Dir.clicked.connect(self.addFolder)
        self.tw_Log_File_List.cellClicked.connect(self.select_loglist_row)
        self.btn_Download.clicked.connect(self.download_File)
        self.let_Folder_Dir.setText(os.getcwd())
        self.btn_Reload.clicked.connect(self.reload)

    def reload(self):
        if self.status == 1:
            fileList = self.s.listdir("/home/tdlotte/logfiles")
            self.log_File_List = fileList

            row = len(fileList)
            self.tw_Log_File_List.setRowCount(row)
           
            for i in range(row):
                self.tw_Log_File_List.setItem(i,0,QTableWidgetItem(self.log_File_List[i]))
            self.lbl_Status.setText("리로드 완료")
        else:
            self.startSftp()


    def addFolder(self):
        folder = QFileDialog.getExistingDirectory( None, 'Open working directory')
        self.let_Folder_Dir.setText(folder)

    def startSftp(self):
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            self.s = pysftp.Connection(host="172.28.242.40",username='tdlotte',password='P@ssw0rd',cnopts=cnopts)
            self.status = 1
            fileList = self.s.listdir("/home/tdlotte/logfiles")
            self.log_File_List = fileList

            row = len(fileList)
            self.tw_Log_File_List.setRowCount(row)
           
            for i in range(row):
                self.tw_Log_File_List.setItem(i,0,QTableWidgetItem(self.log_File_List[i]))

            self.lbl_Status.setText("로그서버에 접속 하였습니다.")
        except:
            self.lbl_Status.setText("로그서버에 접속 할 수 없습니다.")


    def select_loglist_row(self, row, colum):
        self.download_index = row

    def download_File(self):
        self.s.get('/home/tdlotte/logfiles/{}'.format(self.log_File_List[self.download_index]),
                    self.let_Folder_Dir.text()+'/{}'.format(self.log_File_List[self.download_index]))
        self.lbl_Status.setText('{} 파일을 다운로드 완료 하였습니다.'.format(self.log_File_List[self.download_index]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
