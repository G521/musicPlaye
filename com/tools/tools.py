import base64
import json
import os
import re
import time

import requests

#os.environ['path'] = os.environ.get('path')+';{}\\bin'.format(os.getcwd())

PATH = '~/.myMusicPlayer/'
def time_format(time):
    m = time // 60
    s = time % 60
    return "{}:{}".format(m, s)


class mytime:
    def __init__(self):
        self.startTime = int(time.time()*1000)
        self.layTime = 0
        self.currentTime = 0
        self.stoptime = 0
        self.isStop = False
    def getTime(self):
        if self.isStop:
            return (self.currentTime )
        self.currentTime = (int(time.time()*1000) - self.startTime - self.layTime)
        return (self.currentTime)
    def init(self):
        self.startTime = int(time.time()*1000)
    def reset(self):
        self.startTime = int(time.time()*1000)
        self.currentTime = 0
        self.layTime = 0

    def stop(self):
        if self.isStop:
            return
        self.isStop = True
        self.stoptime = int(time.time()*1000)

    def start(self):
        if not self.isStop: return
        self.layTime = int(time.time()*1000) - self.stoptime
        self.isStop = False
def transTowav(from_name,to_name):
    os.system(r'ffmpeg -i {} {}'.format(from_name,to_name))
    print('finished')
def initMymusics():
    class struct:
        def __init__(self, name, music_path, music_lrc_path):
            self.name = name
            self.music_path = music_path
            self.lrc_path = music_lrc_path

    result = []
    if not os.path.exists(PATH):
        return {}
    for dir in os.listdir(PATH):
        if dir.endswith('.dat'):continue
        music_path = PATH + '/' + dir +'/'+ 'music.wav'
        music_lrc_path = PATH + '/'+dir+'/' + 'music.lrc'
        result.append(struct(dir,music_path ,music_lrc_path ))
    return result
def formatName(name):
    pattern = re.compile(r'[/\\*/?《》\s:\(\) <>\"]')
    name,_ = re.subn(pattern,'_',name)
    return name

def QQlrcGet(mid, name):
    heard = {
        'referer': 'https: // y.qq.com / portal / player.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?-=MusicJsonCallback_lrc&pcachetime=1592102808614&songmid=%s&g_tk_new_20200303=5381&g_tk=5381&loginUin=2997385765&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0' % mid
    req = requests.get(url, headers=heard)
    info = json.loads(req.text)
    info.get('lyric')
    if info==None:
        return False
    result = base64.b64decode(info.get('lyric'))
    result = result.decode('utf-8').split('\n')
    f = open(PATH+name, 'w')
    f.writelines('\n'.join(result[5:]))
    f.close()
    return True

def NeteaseGet(id, name):
    lrc_url = 'https://api.imjad.cn/cloudmusic/?type=lyric&id=' + str(id)
    lyric = requests.get(lrc_url)
    info = json.loads(lyric.text)
    content = info.get('lrc').get('lyric')
    result = []
    contentArray = content.split('\n')
    for i in contentArray:
        m =re.match(r'(\[[^\[\]]*\])(\[[^\[\]]*\])(.*)', i)
        if m:
            result.append(m.group(1)+m.group(3))
            result.append(m.group(2)+m.group(3))
        else:
            result.append(i)
    result.sort(key=lambda a: a[1:5])
    f = open(PATH+ name,'w')
    f.writelines('\n'.join(result))
    f.close()
    return True

def downMusic(downaddr,path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    if os.path.exists(path)==True:return False
    req = requests.get(downaddr, headers=headers)
    if req.ok==False:return  False
    content = req.content
    if not os.path.exists(path[:-9]):
        os.mkdir(path[:-9])
    f = open(path, 'wb')
    f.write(content)
    f.close()
    transTowav(path,path[:-4]+'.wav')
    del downaddr
    del path
    print('finished !')
    return True
# t = downMusic()
# t.init('https://music.163.com/song/media/outer/url?id=1403858440',r'D:/.myMusicPlayer/test/music.m4a')
# t.start()
