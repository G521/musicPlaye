'''
用画刷填充图形区域
'''
import math
import random
import sys
import threading

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from com.music_Play import MyThread


class musicGraphy(QWidget):
    def __init__(self):
        super(musicGraphy, self).__init__()
        self.musicPlay = MyThread()
        self.resize(500, 500)
        self.setWindowTitle('Music')
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.preData = []
        self.speed=1
        self.penWidth=1
        self.isPlay=False
        self.rotate = 0
    def setMusicName(self,path):
        self.musicPlay.init(path)
    def initValue(self,data):
        self.Lrcfont=data.get('Lrcfont',QFont('SimSun',15))
        self.showPic = data.get('showPic',True)
        self.musicID=eval(data.get('musicID','{}'))
        self.gap = data.get('gap', 0.5)
        self.recHeight = data.get("recHeight", 400)
        self.recWidth = data.get("recWidht", 400)
        self.PenColor = data.get('penColor', QColor(255, 255, 255))
        self.brushid = data.get('brushid', 6)
        self.type = data.get('type', 0)
        self.brushfill_reverse = data.get("reverse", 'False')
        self.loX = data.get('loX', 200)
        self.loY = data.get('loY', 200)
        self.circleR = data.get('circleR', 100)
        self.paintMethod = [self.myPaint_circle_points, self.myPaint_circle_line, self.myPaint_circle_Rec,
                            self.myPaint_line_Rec_one, self.myPaint_line_Rec_two]
        self.chunk = 64
        self.win_Width =data.get('win_Width',500)
        self.win_Height = data.get('win_Height',500)
        self.setFixedSize(self.win_Width,self.win_Height)
        self.win_loX = data.get('win_lox',200)
        self.win_loY = data.get('win_loy',200)
        self.penWidth =data.get('penWidht',1)
        self.move(self.win_loX,self.win_loY)
    def setWinAdapt(self):
        self.setFixedSize(self.win_Width,self.win_Height)
        self.move(self.win_loX,self.win_loY)
    def setWin_Width(self,width):
        self.win_Width = width
        self.setWinAdapt()
    def setWin_Height(self, height):
        self.win_Height = height
        self.setWinAdapt()
    def setWin_X(self,x):
        self.win_loX = x
        self.setWinAdapt()
    def setWin_Y(self,y):
        self.win_loY =y
        self.setWinAdapt()
    def setSpeed(self,s):
        self.speed=s
    def setShowPic(self, showPic):
        self.showPic = showPic
    def setLrcfont(self,qfont):
        self.Lrcfont = qfont
    def setReverse(self, bool):
        self.brushfill_reverse = bool
    def playVisible(self):
        self.update()
        t = threading.Timer(0.1, self.playVisible)
        t.start()
    def myPaint_circle_points(self, qp):
        if self.showPic:
            qp.drawImage(QRect(self.loX - self.circleR, self.loY - self.circleR, 2 * self.circleR, 2 * self.circleR),
                     self.image)
        for i, h in enumerate(self.musicPlay.wavedata):
            self.setBrush(self.brushid, qp, h)
            if (i % 2) == 0:
                d1 = (i * 1.0 / self.chunk) * math.pi * 2
                d2 = (i + self.gap) / self.chunk * math.pi * 2
                h = int(abs(self.recHeight * h))
                point1 = QPoint(int((self.circleR + h) * math.cos(d2) + self.loX),
                                int((self.circleR + h) * math.sin(d2) + self.loY))
                point2 = QPoint(int((self.circleR + h) * math.cos(d1) + self.loX),
                                int((self.circleR + h) * math.sin(d1) + self.loY))

                qp.drawPoints(point1)
                qp.drawPoints(point2)

    def setPenwidth(self,w):
        self.penWidth = w
    def setRecHeight(self, h):
        self.recHeight = h
    def setRecWidth(self, w):
        self.recWidth = w
    def setGap(self, gap):
        self.gap = gap
    def setBrushid(self, id):
        self.brushid = id
    def setChunk(self, chunk):
        self.musicPlay.setChunk(chunk)
        self.chunk = chunk

    def setQColor(self, color):
        self.PenColor = color

    def setloX(self, x):
        self.loX = x

    def setloY(self, y):
        self.loY = y

    def setR(self, r):
        self.circleR = r

    def setType(self, type):
        self.type = type

    def myPaint_circle_line(self, qp):
        if self.showPic:
            qp.drawImage(QRect(self.loX - self.circleR, self.loY - self.circleR, 2 * self.circleR, 2 * self.circleR),
                         self.image)

        for i, h in enumerate(self.musicPlay.wavedata):
            # image.save('/home/void/work/Python/musicPlayer/com/img/circle.png')## 防止格式不行,转换一下

                d1 = (i * 1.0 / self.chunk) * math.pi * 2
                d2 = (i + self.gap) / self.chunk * math.pi * 2
                h = int(abs(self.recHeight * h))
                point1 = QPoint(int((self.circleR + h) * math.cos(d2) + self.loX),
                                int((self.circleR + h) * math.sin(d2) + self.loY))
                point2 = QPoint(int((self.circleR) * math.cos(d1) + self.loX),
                                int((self.circleR) * math.sin(d1) + self.loY))
                qp.drawLine(point1, point2)

    def myPaint_circle_Rec(self, qp):
        if self.showPic:
            qp.drawImage(QRect(self.loX - self.circleR, self.loY - self.circleR, 2 * self.circleR, 2 * self.circleR),
                         self.image)

        for i, h in enumerate(self.musicPlay.wavedata):
            # self.setBrush(self.brushid, qp, h)
            if (i % 2) == 0:
                d1 = (i * 1.0 / self.chunk) * math.pi * 2
                d2 = (i + self.gap) / self.chunk * math.pi * 2
                # qp.setBrush(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                # qp.setPen(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))

                h = int(abs(self.circleR * h))
                point1 = QPoint(int((self.circleR + h) * math.cos(d2) + self.loX),
                                int((self.circleR + h) * math.sin(d2) + self.loY))
                point2 = QPoint(int((self.circleR + h) * math.cos(d1) + self.loX),
                                int((self.circleR + h) * math.sin(d1) + self.loY))
                point3 = QPoint(int(self.circleR * math.cos(d2) + self.loX),
                                int(self.circleR * math.sin(d2) + self.loY))
                point4 = QPoint(int(self.circleR * math.cos(d1) + self.loX),
                                int(self.circleR * math.sin(d1) + self.loY))
                polygon = QPolygon([point1, point2, point4, point3])
                qp.drawPolygon(polygon)
            else:
                d1 = (i * 1.0 / self.chunk) * math.pi * 2
                d2 = (i + self.gap) / self.chunk * math.pi * 2
                # qp.setBrush(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                # qp.setPen(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                h = int(abs(self.recHeight * h))
                point1 = QPoint(int((self.circleR - h) * math.cos(d2) + self.loX),
                                int((self.circleR - h) * math.sin(d2) + self.loY))
                point2 = QPoint(int((self.circleR - h) * math.cos(d1) + self.loX),
                                int((self.circleR - h) * math.sin(d1) + self.loY))
                point3 = QPoint(int(self.circleR * math.cos(d2) + self.loX),
                                int(self.circleR * math.sin(d2) + self.loY))
                point4 = QPoint(int(self.circleR * math.cos(d1) + self.loX),
                                int(self.circleR * math.sin(d1) + self.loY))
                polygon = QPolygon([point4, point3, point1, point2])
                qp.drawPolygon(polygon)


    def setBrush(self, choice, qp, value):
        if self.brushfill_reverse == 'True':
            value = 1 - value
        if choice == 0:
            ##彩虹
            qp.setBrush(QColor((int)(random.random() * 255), random.random() * 255, (int)(random.random() * 255)))
            return
        elif choice == 1:
            ##红紫
            qp.setBrush(QColor(255, (int)(value * 255), (int)(random.random() * 255)))
            return
        elif choice == 2:
            ##红橙黄
            qp.setBrush(QColor(255, (int)(random.random() * 255), (int)(value * 255)))
            return
        elif choice == 3:
            ##绿黄
            qp.setBrush(QColor((int)(random.random() * 255), 255, (int)(value * 255)))
            return
        elif choice == 4:
            ##白灰黑
            qp.setBrush(QColor((int)(value * 255), int(value * 255), (int)(value * 255)))
            return
        elif choice == 5:
            ##浅蓝黄
            qp.setBrush(QColor((int)(value * 255), 255, (int)((1 - value) * 255)))
            return
        elif choice == 6:
            ##浅紫黄
            qp.setBrush(QColor(255, (int)(value * 255), (int)((1 - value) * 255)))
            return
        else:
            ##黑
            qp.setBrush(QColor(0, 0, 0))
            return

    def myPaint_line_Rec_one(self, qp):
        qp.setPen(self.PenColor)
        for i, h in enumerate(self.musicPlay.wavedata):
            self.setBrush(self.brushid, qp, h)
            qp.drawRect(i * self.recWidth + self.loX, (int)((self.loY - abs(h) * self.recHeight)),
                        int(self.recWidth * (1 - self.gap)), int(abs(h) * self.recHeight))

    def myPaint_line_Rec_two(self, qp):
        qp.setPen(self.PenColor)
        for i, h in enumerate(self.musicPlay.wavedata):
            if (i % 2) == 0:
                self.setBrush(self.brushid, qp, h)
                qp.drawRect(i * 10 + self.loX, (int)(self.loY - abs(h) * self.recHeight),
                            int(self.recWidth * (1 - self.gap)),
                            int(abs(h) * self.recHeight))
            else:
                self.setBrush(self.brushid, qp, h)
                qp.drawRect(i * 10 + self.loX, self.loY, int(self.recWidth * (1 - self.gap)),
                            int(abs(h) * self.recHeight))

    def paintEvent(self, e):
        if self.isPlay == False : return
        qp = QPainter(self)
        qp.begin(self)
        image = QImage('img/circle.png')
        transform = QTransform()  # PyQt5
        #        martix.speed(90)        # PyQt4,PyQt5中已废弃

        transform.rotate(self.rotate)  # PyQt5
        self.rotate += self.speed
        self.image = image.transformed(transform)  # 相应的matrix改为transform
        pen = QPen(self.PenColor)
        pen.setWidth(self.penWidth)
        qp.setPen(pen)
        self.paintMethod[self.type](qp)
        qp.setFont(self.Lrcfont)

        qp.drawText(QRect(20,self.win_Height-100, self.win_Width, 80), Qt.AlignCenter, self.musicPlay.current_music_rlc)
        qp.end()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = musicGraphy()
#     main.setMusicName('/home/void/work/Python/musicPlayer/com/music/music3.wav')
#     ##需要制定存储文件才能使用
#     # main.initValue()
#     main.musicPlay.start()
#     main.playVisible()
#     main.show()
#     sys.exit(app.exec_())
