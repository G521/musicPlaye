import os
import re
import threading
import time
from threading import *

import pyaudio
import wave
import numpy as np
# 定义数据流块
from com.tools.tools import mytime
CHUNK = 64
over = False
class MyThread(Thread):
    def init(self, filename):
        if not os.path.exists(filename):return
        self.current_music_rlc = ''
        self.t = mytime()
        if filename == None: return
        self.filename = filename
        global over
        over = False
        self.lrc=[]
        self.lrcT=[]
        self.wf = wave.open(filename, 'rb')  # (sys.argv[1], 'rb')
        self.p = pyaudio.PyAudio()  # 创建一个播放器
        self.wavedata = []
        self.maxData = self.getMax()
        self.chunk = CHUNK
        self.readLrc(filename[:-4]+'.lrc')
        # def init(self,filename):
        # 打开数据流
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True)
        # 读取数据
        self.data = self.wf.readframes(self.chunk)
        self.__flag = Event()  # 用于暂停线程的标识
        self.__flag.set()
        self.ifdo = True

    def isOver(self):
        return over
    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞
        self.t.stop()

    def resume(self):
        self.t.start()
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def getMax(self):
        return 32767
        # a = wave.open(self.filename)
        # nf = a.getnframes()
        # data = a.readframes(nf)
        # w = np.frombuffer(data, dtype=np.int16)
        # print(max(abs(w)))
        # return max(abs(w))

    def setChunk(self, chunk):
        self.chunk = chunk

    def getChunk(self):
        return self.chunk
    def readLrc(self,name):
        if not os.path.exists(name):
            self.lrc=[]
            return
        f = open(name)
        for i in f.readlines():
            m = re.match(r'(\[([^\[\]]*):([^\[\]]*)\])(.+)', i)
            if m:
                self.lrcT.append(int(int(m.group(2)) * 60 * 1000 + float(m.group(3)) * 1000))
                self.lrc.append(m.group(4))
    def updatelrc(self,):
        if len(self.lrcT)==0:
            return
        if self.t.getTime()>self.lrcT[0]:
            self.current_music_rlc=self.lrc[0]
            self.lrcT= self.lrcT[1:]
            self.lrc= self.lrc[1:]
    def stop(self):
        self.ifdo=False
    def run(self):
        try:
            self.t.init()
        except AttributeError:
            return
        while self.ifdo and self.data != '':
            self.__flag.wait()
            self.stream.write(self.data)
            self.updatelrc()
            self.data = self.wf.readframes(self.chunk)
            w = np.frombuffer(self.data, dtype=np.int16)
            global over
            if len(w) < self.chunk:
                over = True
            else:
                over = False

            self.wavedata = abs(w * 1.0) / self.maxData
