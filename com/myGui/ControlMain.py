import os
import random
import shelve
import shutil
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QMessageBox, QFontDialog, QFileDialog

from com.music_Play import MyThread
from com.myGui.callSearchMusic import *

from com.myGui.callSearchMusic import SearchMusic
from com.myGui.Control import *
from com.myGui.musicPlayer import musicGraphy
from com.tools import tools


class ControlMainWindow(QMainWindow, Ui_Control):
    def __init__(self):
        super(ControlMainWindow, self).__init__()
        self.setupUi(self)
        self.myAddmusic = SearchMusic()
        self.setWindowTitle('张 ---music Player')
        self.musicsPlayer = None
        self.setType.currentIndexChanged.connect(self.chooseType)
        self.setChunk.valueChanged.connect(self.chooseChunk)
        self.setReverse.currentIndexChanged.connect(self.chooseReverse)
        self.setGap.valueChanged.connect(self.chooseGap)
        self.fillTheme.currentIndexChanged.connect(self.chooseBrushTheme)
        self.setBorderColor.clicked.connect(self.chooseColor)  ## 设置边框颜色
        self.setReverse.currentIndexChanged.connect(self.chooseReverse)  ## 设置 是否高低颜色反转
        ##########
        self.setH.valueChanged.connect(self.chooseH)  ## 设置图形高度
        self.setW.valueChanged.connect(self.chooseW)  ##设置图形宽度
        self.setX.valueChanged.connect(self.chooseX)  ## 设置图形在窗口的X坐标
        self.setY.valueChanged.connect(self.chooseY)  ## 设置图形在窗口的Y坐标
        self.setR.valueChanged.connect(self.chooseR)  ## 设置图形为 圆时的半径
        self.setpenWidth.valueChanged.connect(self.choosePenWidth)
        self.speed.valueChanged.connect(self.chooseSpeed)
        self.showPic.clicked.connect(self.chooseshowPic)
        self.save.clicked.connect(self.saveData)  ## 设置保存按钮
        self.delete_2.clicked.connect(self.deleteMusic)
        self.musiclist.clicked.connect(self.chooseMusic)
        self.addmusic.clicked.connect(self.addMusics)
        self.open.clicked.connect(self.openPath)
        if os.path.exists(r'D:\.myMusicPlayer\info.dat')==False:os.mkdir('D:\.myMusicPlayer\info.dat')
        ###
        self.initValue()  ## 控件 赋初值
        self.setX_2.valueChanged.connect(self.setWin_X)  ## 设置主窗口X坐标
        self.setY_2.valueChanged.connect(self.setWin_y)
        self.setH_2.valueChanged.connect(self.setWin_height)
        self.setW_2.valueChanged.connect(self.setWin_width)
        self.play.clicked.connect(self.playMusic)
        self.setfont.clicked.connect(self.chooseLrcFont)
        self.upMove.clicked.connect(self.upmove)
        ## 当前播放音乐序号
        self.PlayStop = False
        self.currentMusicId = 0
        self.initMusicinfo()

    def startPlaye(self):
        print('startPlay !!!!!!!!!!!')
        '''初始化图形播放器并开始播放音乐'''
        self.musicsPlayer = musicGraphy()
        self.musicsPlayer.setMusicName(self.musics.get(self.musicNameList[self.currentMusicId]).music_path)
        self.musicsPlayer.initValue(self.data)
        self.musicsPlayer.musicPlay.setDaemon(True)
        self.musicsPlayer.musicPlay.start()
        self.musicsPlayer.isPlay = True
        self.musicsPlayer.playVisible()
        self.musicsPlayer.show()
        self.checkmusicisOver()

    def openPath(self):
        QFileDialog.getOpenFileName(self, '打开文件', directory=tools.PATH)

    def addMusics(self):
        self.myAddmusic.show()
    def choosePenWidth(self):
        if self.musicsPlayer == None:return
        self.musicsPlayer.setPenwidth(self.setpenWidth.value())
    def chooseLrcFont(self):
        if self.musicsPlayer == None:return
        font, ok = QFontDialog.getFont()
        if ok:
            self.musicsPlayer.setLrcfont(font)
    def deleteMusic(self):
        reply = QMessageBox.information(self, 'Really?', '确定删除吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        ###  modify
        if reply == QMessageBox.Yes:
            self.chooseMusic()
            if len(self.musiclist.selectedItems())==0:return
            shutil.rmtree(os.path.dirname(self.musics[self.musicNameList[self.currentMusicId]].music_path))
            self.musicID.pop(self.musics[self.musicNameList[self.currentMusicId]].name)
            self.musicNameList.remove(self.musics[self.musicNameList[self.currentMusicId]].name)
            if len(self.musiclist.selectedIndexes())==0:return
            self.musiclist.takeItem(self.currentMusicId)

    def chooseshowPic(self):

        if self.musicsPlayer == None:return
        self.musicsPlayer.setShowPic(self.showPic.isChecked())

    def chooseSpeed(self):

        if self.musicsPlayer == None:return
        self.musicsPlayer.setSpeed(self.speed.value())

    def getmusicId(self, name):
        '''根据名字获取歌曲的排序id ,如果没有 则..'''
        if self.musicID.get(name) == None:
            self.musicID[name] = len(self.musicID) + 1
        return self.musicID.get(name)

    def initMusicinfo(self):
        '''初始化歌曲信息'''
        ## 歌曲名字 ,用来排序的 中间载体 根据这个名字列表排序,所以要先将这个列表排序
        self.musicNameList = [music.name for music in tools.initMymusics()]
        ## 存储 所有歌曲本体
        self.musics = dict(zip(self.musicNameList, tools.initMymusics()))
        self.musicNameList.sort(key=self.getmusicId)
        for i in range(len(tools.initMymusics())):
            self.musiclist.addItem(self.musicNameList[i])
        if len(self.musicNameList) > 0:
            self.startPlaye()
    def updateMusic(self):
        print("start updateMusic")
        if self.musicsPlayer == None:return
        self.musicsPlayer.isPlay=False
        self.musicsPlayer.musicPlay.stop()
        self.musicsPlayer.musicPlay = MyThread()
        self.musicsPlayer.setMusicName(self.musics[self.musicNameList[0]].music_path)
        self.showcurrentMusic.setText(self.musics[self.musicNameList[0]].name)
        self.musicsPlayer.musicPlay.start()
        self.musicsPlayer.isPlay=True
        print("update finished!")

    def initValue(self):
        self.data = shelve.open('musicPlayer.dat')
        self.setH.setValue(self.data.get("recHeight", 400))
        self.setW.setValue(self.data.get("recWidth", 400))
        self.setX.setValue(self.data.get('loX', 200))
        self.setY.setValue(self.data.get('loY', 200))
        self.setR.setValue(self.data.get("circleR",100))
        self.setReverse.setCurrentText(self.data.get("reverse", 'False'))
        self.setGap.setValue(self.data.get('gap', 0.5))
        self.setChunk.setValue(self.data.get('chunk', 20))
        self.fillTheme.setCurrentIndex(self.data.get('brushid', 6))
        self.setType.setCurrentIndex(self.data.get('type', 0))
        self.speed.setValue(self.data.get("speed",5))
        self.showPic.setChecked(self.data.get("showPic",True))
        ##########
        self.setH_2.setValue(self.data.get('win_Height', 500))
        self.setW_2.setValue(self.data.get('win_Width', 500))
        self.setX_2.setValue(self.data.get('win_lox', 200))
        self.setY_2.setValue(self.data.get('win_loy', 200))
        self.musicID = self.data.get('musicID', {})

    def saveData(self):
        self.data['speed'] = self.speed.value()
        self.data["recHeight"] = self.setH.value()
        self.data['recWidth'] = self.setW.value()
        if self.musicsPlayer!=None:
            self.data['penColor'] = self.musicsPlayer.PenColor
        self.data['brushid'] = self.fillTheme.currentIndex()
        self.data['type'] = self.setType.currentIndex()
        self.data['reverse'] = self.setReverse.currentText()
        self.data['loX'] = self.setX.value()
        self.data['loY'] = self.setY.value()
        self.data['circleR'] = self.setR.value()
        self.data['gap'] = self.setGap.value()
        self.data['win_Width'] = self.setW_2.value()
        self.data['win_Height'] = self.setH_2.value()
        self.data['win_lox'] = self.setX_2.value()
        self.data['win_loy'] = self.setH_2.value()
        self.data['musicID'] = str(self.musicID)
        self.data['showPic'] = self.showPic.isChecked()
        self.statusbar.showMessage("保存成功")
        return True

    def playMusic(self):
        if self.musicsPlayer ==None:
            if len(self.musicNameList) > 0:
                self.startPlaye()
            else:
                self.play.setText('没有音乐')
            return
        if not self.PlayStop:
            self.PlayStop = True
            self.musicsPlayer.musicPlay.pause()
            self.musicsPlayer.isPlay=False
            self.play.setText("暂停")
        else:
            self.PlayStop = False
            self.musicsPlayer.isPlay=True
            self.musicsPlayer.musicPlay.resume()
            self.play.setText("播放")

    def checkmusicisOver(self):
        if self.musicsPlayer ==None or self.musicsPlayer.isPlay==False :return
        if self.musicsPlayer.musicPlay.isOver()==True and self.autoPlay.isChecked():
            self.currentMusicId += 1
            if len(self.musicNameList) <= self.currentMusicId:
                self.currentMusicId = 0
            self.musicsPlayer.setMusicName(self.musics.get(self.musicNameList[self.currentMusicId]).music_path)
        t = threading.Timer(1, self.checkmusicisOver)
        t.start()

    def chooseMusic(self):
        if len(self.musiclist.selectedIndexes()) == 0: return
        self.currentMusicId = self.musiclist.selectedIndexes()[0].row()

    def upmove(self):
        if self.musicsPlayer ==None :return
        if self.currentMusicId == 0: return
        self.chooseMusic()
        if len(self.musiclist.selectedItems())==0:return
        self.musicID[self.musicNameList[self.currentMusicId]] = self.currentMusicId - 1
        self.musicID[self.musicNameList[self.currentMusicId - 1]] = self.currentMusicId
        print("change finished")
        self.musiclist.clear()
        self.musicNameList.sort(key=lambda name: self.musicID.get(name, random.randint(1, 9)))
        for i in range(len(self.musicNameList)):
            self.musiclist.addItem(self.musicNameList[i])
        if self.currentMusicId == 1: self.updateMusic()
        print("upmove Over")

    def setWin_width(self):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setWin_Width(self.setW_2.value())

    def setWin_height(self):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setWin_Height(self.setH_2.value())

    def setWin_X(self):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setWin_X(self.setX_2.value())

    def setWin_y(self):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setWin_Y(self.setY_2.value())

    def chooseColor(self):
        if self.musicsPlayer ==None :return
        color = QColorDialog.getColor()
        self.showColor.setAutoFillBackground(True)
        p = QPalette()
        p.setColor(QPalette.Window, color)
        self.showColor.setPalette(p)
        self.musicsPlayer.setQColor(color)

    def chooseBrushTheme(self, index):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setBrushid(index)

    def chooseH(self):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setRecHeight(self.setH.value())

    def chooseW(self):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setRecWidth(self.setW.value())

    def chooseX(self):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setloX(self.setX.value())

    def chooseY(self):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setloY(self.setY.value())

    def chooseR(self):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setR(self.setR.value())

    def chooseGap(self):
        '''选择间隙'''
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setGap(self.setGap.value())

    def chooseType(self, index):
        '''选择图形'''
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setType(index)

    def chooseChunk(self):
        '''选择分频'''
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setChunk(self.setChunk.value())

    def chooseReverse(self,index):
        if self.musicsPlayer ==None :return
        self.musicsPlayer.setReverse(self.setReverse.currentText())
    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        myWin = ControlMainWindow()
        myWin.show()
        sys.exit(app.exec_())
    except BaseException as e:
        raise e
        myWin.musicsPlayer.musicsPlayer.stop()
        QMessageBox.information(None,'error',"请删除D:\\.myMusicPlayer\\info.dat 后重新启动",QMessageBox.Yes)