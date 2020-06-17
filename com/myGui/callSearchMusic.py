import string
import sys
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from com.tools import neteaseMusic, tools
from com.tools.qqmusic_search import QQMusic
from com.myGui.searchMusic import Ui_MainWindow

import os
import requests
def download_song(down_addr, file):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    req = requests.get(down_addr, headers=headers)
    if 'DOCTYPE' in req.text:
        return False
    path_store = file.replace('\"',"")
    path_store = path_store.replace('/','_')
    path_store = path_store.replace('?','_')
    path_store = path_store.replace('<','_')
    path_store = path_store.replace('>','_')
    path_store = path_store.replace('\\','_')
    path_store = path_store.replace(':','_')
    path_store = path_store.replace('*','_')
    path_store = path_store.replace('|','_')
    path_store = tools.PATH+os.sep+path_store
    print(path_store)
    if not os.path.exists(path_store):
        os.mkdir(path_store)
    with open(path_store+os.sep+'music.mp3', 'wb') as f:
        f.write(req.content)
        f.close()
    return True
class SearchMusic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(SearchMusic, self).__init__()
        self.setupUi(self)
        self.initAction()
        self.QQmusic = QQMusic()
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.result = {}
        self.musics = {"QQ音乐": 0, "网易云音乐": 1}
        self.currentMusic = 0
        self.chooseMusic.currentIndexChanged.connect(self.Musicchoose)

    def Musicchoose(self):
        self.currentMusic = self.musics.get(self.chooseMusic.currentText())

    def initAction(self):
        self.Search.clicked.connect(self.searchMusic)
        self.download.clicked.connect(self.downloadSong)

    def searchMusic(self):
        self.searchResult.clear()
        if self.searchEnter.text() == "": return

        if self.currentMusic==0:
            self.result = self.QQmusic.searchSong(self.searchEnter.text())
        else:
            self.result = neteaseMusic.searchSong(self.searchEnter.text(),1,1,20)
        for single in self.result:
                self.searchResult.addItem(single.name+'     '+single.singers[0].name+'       time:  '+tools.time_format(single.time))

    def downloadSong(self):
        if self.searchEnter.text() == ""or len(self.searchResult.selectedIndexes())==0: return
        self.download_progress.setValue(0)
        song = self.result[self.searchResult.selectedIndexes()[0].row()]
        if self.currentMusic == 0:
            if tools.downMusic(song.down_addr,
                            tools.PATH + song.name + '_' + self.chooseMusic.currentText()  + '/music.m4a')==False:
                self.statusbar.showMessage("下载失败")
                return
            # kwargs={}
            self.download_progress.setValue(30)
            tools.QQlrcGet(song.id, song.name + '_' + self.chooseMusic.currentText()+ '/music.lrc')
            self.download_progress.setValue(100)
            self.statusBar().showMessage("下载完成!")
        else:
            if tools.downMusic(song.down_addr,tools.PATH + song.name + '_' + self.chooseMusic.currentText()  + '/music.mp3')==False:
                self.statusbar.showMessage("下载失败")
                return
            #kwargs={}
            self.download_progress.setValue(30)
            tools.NeteaseGet(song.id,song.name + '_' + self.chooseMusic.currentText()+'/music.lrc')
            self.download_progress.setValue(100)
            self.statusBar().showMessage("下载完成!")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myWin = SearchMusic()
#     myWin.show()
#     sys.exit(app.exec_())
