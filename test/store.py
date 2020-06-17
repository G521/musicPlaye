for i, h in enumerate(self.tr.wavedata):
    if (i % 2) == 0:
        d1 = (i * 1.0 / 64) * math.pi * 2
        d2 = (i + 0.5) * 1.0 / 64 * math.pi * 2
        qp.setBrush(QColor(200, (int)(abs(h) * 155), (int)((1 - abs(h)) * 155)))
        h = abs(300 * h)
        point1 = QPoint((len + h) * math.cos(d2) + loX, (len + h) * math.sin(d2) + loY)
        point2 = QPoint((len + h) * math.cos(d1) + loX, (len + h) * math.sin(d1) + loY)
        point3 = QPoint(len * math.cos(d2) + loX, len * math.sin(d2) + loY)
        point4 = QPoint(len * math.cos(d1) + loX, len * math.sin(d1) + loY)
        polygon = QPolygon([point1, point2, point4, point3])
        qp.drawPolygon(polygon)
    # else:
    #     d1 = (i * 1.0 / 64) * math.pi * 2
    #     d2 = (i + 0.5) * 1.0 / 64 * math.pi * 2
    #     qp.setBrush(QColor(200, (int)(abs(h)*d1 * 155), (int)((1 - abs(h))*d2 * 155)))
    #     h = (300 * h)
    #     point1 = QPoint((len + h) * math.cos(d2) + loX, (len + h) * math.sin(d2) + loY)
    #     point2 = QPoint((len + h) * math.cos(d1) + loX, (len + h) * math.sin(d1) + loY)
    #     point3 = QPoint(len * math.cos(d2) + loX, len * math.sin(d2) + loY)
    #     point4 = QPoint(len * math.cos(d1) + loX, len * math.sin(d1) + loY)
    #     polygon = QPolygon([point1, point2, point4, point3])
    #     qp.drawPolygon(polygon)


    #######################################
    # def paintEvent(self,e):
    #     qp = QPainter()
    #     qp.begin(self)
    #     qp.setBrush(Qt.blue)
    #     for i, h in enumerate(self.tr.wavedata):
    #         if (i % 2) == 0 :
    #             qp.setBrush(QColor(200, (int)(h * 155), (int)((1 - h) * 155)))
    #             qp.drawRect(i * 10, (int)(400 - abs(h) * 200), 7, int(abs(h) * 200))
    #         else:
    #             qp.setBrush(QColor(100, (int)(h * 155), (int)((1 - h) * 155)))
    #             qp.drawRect(i * 10, 400, 7, int(abs(h) * 200))
    #     for i, h in enumerate(self.preData):
    #         if (i % 2) == 0:
    #             qp.setBrush(QColor(200, (int)(h * 155), (int)((1 - h) * 155)))
    #             qp.drawRect(i * 10, (int)(400 - abs(h) * 200), 7, int(abs(h) * 200))
    #         else:
    #             qp.setBrush(QColor(100, (int)(h * 155), (int)((1 - h) * 155)))
    #             qp.drawRect(i * 10, 400, 7, int(abs(h) * 200))
    #     self.preData = self.data
    #     qp.end()