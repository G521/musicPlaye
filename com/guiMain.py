'''
用画刷填充图形区域
'''
import math
import random
import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from com.music_Play import MyThread


class FillRect(QWidget):
    def __init__(self):
        super(FillRect, self).__init__()
        self.tr = MyThread()
        self.tr.init("/home/void/work/Python/musicPlayer/com/music/music.wav")
        self.resize(500, 500)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('Music')
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.data = []
        self.preData = []
        self.tr.start()
        self.playVisible()
        self.paintMethod = ['myPaint_circle_points', 'myPaint_circle_line', 'myPaint_circle_Rec',
                            'myPaint_line_Rec_one', 'myPaint_line_Rec_two']

    def playVisible(self):
        self.update()
        t = threading.Timer(0.1, self.playVisible)
        t.start()

    def myPaint_circle_points(self, qp):
        for i, h in enumerate(self.tr.wavedata):
            self.setBrush(self.brushid, qp, h)
            if (i % 2) == 0:
                d1 = (i * 1.0 / self.chunk) * math.pi * 2
                d2 = (i + self.roundWidth) / self.chunk * math.pi * 2
                qp.setBrush(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                qp.setPen(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                h = int(abs(self.recHeight * h))
                point1 = QPoint(int((self.circlelen + h) * math.cos(d2) + self.loX),
                                int((self.circlelen + h) * math.sin(d2) + self.loY))
                point2 = QPoint(int((self.circlelen + h) * math.cos(d1) + self.loX),
                                int((self.circlelen + h) * math.sin(d1) + self.loY))
                qp.drawLine(point1, point2)

    def myPaint_circle_line(self, qp):
        for i, h in enumerate(self.tr.wavedata):

            self.setBrush(self.brushid, qp, h)
            if (i % 2) == 0:
                d1 = (i * 1.0 / self.chunk) * math.pi * 2
                d2 = (i + self.roundWidth) / self.chunk * math.pi * 2
                qp.setBrush(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                qp.setPen(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                h = int(abs(self.recHeight * h))
                point1 = QPoint(int((self.circlelen + h) * math.cos(d2) + self.loX),
                                int((self.circlelen + h) * math.sin(d2) + self.loY))
                point2 = QPoint(int((self.circlelen) * math.cos(d1) + self.loX),
                                int((self.circlelen) * math.sin(d1) + self.loY))
                qp.drawLine(point1, point2)

    def myPaint_circle_Rec(self, qp):
        for i, h in enumerate(self.tr.wavedata):

            self.setBrush(self.brushid, qp, h)
            if (i % 2) == 0:
                d1 = (i * 1.0 / self.chunk) * math.pi * 2
                d2 = (i + self.roundWidth) / self.chunk * math.pi * 2
                qp.setBrush(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                qp.setPen(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                h = int(abs(self.recHeight * h))
                point1 = QPoint(int((self.circlelen + h) * math.cos(d2) + self.loX),
                                int((self.circlelen + h) * math.sin(d2) + self.loY))
                point2 = QPoint(int((self.circlelen + h) * math.cos(d1) + self.loX),
                                int((self.circlelen + h) * math.sin(d1) + self.loY))
                point3 = QPoint(int(self.circlelen * math.cos(d2) + self.loX),
                                int(self.circlelen * math.sin(d2) + self.loY))
                point4 = QPoint(int(self.circlelen * math.cos(d1) + self.loX),
                                int(self.circlelen * math.sin(d1) + self.loY))
                polygon = QPolygon([point1, point2, point4, point3])
                qp.drawPolygon(polygon)
            else:
                d1 = (i * 1.0 / self.chunk) * math.pi * 2
                d2 = (i + self.roundWidth) / self.chunk * math.pi * 2
                qp.setBrush(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                qp.setPen(QColor(255, (int)(d1 / math.pi / 2 * 255), (int)(random.random() * 255)))
                h = int(abs(self.recHeight * h))
                point1 = QPoint(int((self.circlelen - h) * math.cos(d2) + self.loX),
                                int((self.circlelen - h) * math.sin(d2) + self.loY))
                point2 = QPoint(int((self.circlelen - h) * math.cos(d1) + self.loX),
                                int((self.circlelen - h) * math.sin(d1) + self.loY))
                point3 = QPoint(int(self.circlelen * math.cos(d2) + self.loX),
                                int(self.circlelen * math.sin(d2) + self.loY))
                point4 = QPoint(int(self.circlelen * math.cos(d1) + self.loX),
                                int(self.circlelen * math.sin(d1) + self.loY))
                polygon = QPolygon([point4, point3, point1, point2])
                qp.drawPolygon(polygon)

    def setBrush(self, choice, qp, value):
        if self.brushfill_reverse == True:
            value = 1 - value
        if choice == 0:
            ##彩虹
            qp.setBrush(QColor(random.random() * 255, (int)(random.random() * 255), (int)(random.random() * 255)))
        elif choice == 1:
            ##红紫
            qp.setBrush(QColor(255, (int)(value * 255), (int)(random.random() * 255)))
        elif choice == 2:
            ##红橙黄
            qp.setBrush(QColor(255, (int)(random.random() * 255), (int)(value * 255)))
        elif choice == 3:
            ##绿黄
            qp.setBrush(QColor((int)(random.random() * 255), 255, (int)(value * 255)))
        elif choice == 4:
            ##白灰黑
            qp.setBrush(QColor((int)(value * 255), int(value * 255), (int)(value * 255)))
        elif choice == 5:
            ##浅蓝黄
            qp.setBrush(QColor((int)(value * 255), 255, (int)((1 - value) * 255)))
        elif choice == 6:
            ##浅紫黄
            qp.setBrush(QColor(255, (int)(value * 255), (int)((1 - value) * 255)))
        else:
            ##黑
            qp.setBrush(QColor(0, 0, 0))

    def myPaint_line_Rec_one(self, qp):
        qp.setPen(self.PenColor)
        for i, h in enumerate(self.tr.wavedata):
            self.setBrush(self.brushid, qp, h)
            qp.drawRect(i * self.recWidth+self.loX, (int)(self.loY- (1- abs(h)) * self.recHeight),
                        int(self.recWidth * self.gap), int(abs(h) * self.recHeight))

    def myPaint_line_Rec_two(self, qp):
        print('rec TWo')
        qp.setPen(self.PenColor)
        for i, h in enumerate(self.tr.wavedata):
            if (i % 2) == 0:
                self.setBrush(self.brushid, qp, h)
                qp.drawRect(i * self.recWidth + self.loX,
                            int(self.loY - abs(h) * self.recHeight) ,
                            int(self.recWidth * self.gap), int(abs(h) * self.recHeight))
            else:
                self.setBrush(self.brushid, qp, h)
                qp.drawRect(i * self.recWidth + self.loX,
                             self.loY,
                            int(self.recWidth * self.gap), int(abs(h) * self.recHeight))
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.chunk = self.tr.getChunk()
        self.gap = 0.5
        self.roundWidth = self.gap
        self.recHeight = 400
        self.recWidth = 5
        self.PenColor = QColor(255, 255, 255)
        self.brushid = 0
        self.brushfill_reverse = False
        self.loX = 200
        self.loY = 200
        self.circlelen = 50
        self.myPaint_circle_Rec(qp)
        qp.end()
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = FillRect()
#     main.show()
#     sys.exit(app.exec_())
