#QT libraries
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

# system libraries
import sys

# youtube-dl for downloading the files
import youtube_dl


# Window 
ui,_ = loadUiType('mainwindow.ui')

class MyLogger(QtCore.QObject):
    messageSignal = QtCore.pyqtSignal(str)
    def debug(self, msg):
        self.messageSignal.emit(msg)

    def warning(self, msg):
        self.messageSignal.emit(msg)

    def error(self, msg):
        self.messageSignal.emit(msg)


class YoutubeDownload(QtCore.QThread):
    def __init__(self, url, ydl_opts, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)
        self.url = url
        self.ydl_opts = ydl_opts

    def run(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.load_buttons()
        

    def load_buttons(self):
        self.downloadButton.clicked.connect(self.download_audio)

    def download_audio(self):
        
        try:
            logger = MyLogger()
            logger.messageSignal.connect(self.loggerBox.appendPlainText)
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320'
                }],
                'logger':logger
            }
            self.thread = YoutubeDownload(self.urlVideo.text(), ydl_opts)
            self.thread.start()
            self.urlVideo.setText("")
        except:
            self.loggerBox.appendPlainText("Error downloading, verify the URL or try to download from other source")



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()