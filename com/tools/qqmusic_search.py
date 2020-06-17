#!bin/even/python3.6
# -*- encoding:utf-8 -*-
# author:pzq
import requests
import os
import re
import json
from requests import RequestException
from multiprocessing import Pool

from com.tools import tools


class Song:
    class singer:
        def __init__(self, name, mid):
            self.name = name
            self.mid = mid
            self.url = 'https://y.qq.com/n/yqq/singer/'+mid+'.html'

    def __init__(self, name, down_addr,mid, time):
        self.name = name
        self.id = mid
        self.time = time
        self.down_addr = down_addr
        self.singers = []

    def addSinger(self, singer):
        self.singers.append(singer)


class QQMusic:
    def __init__(self):

        header_song = {
            'Referer': 'https://y.qq.com/portal/player.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        header_download = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }
        download_url = 'http://isure.stream.qqmusic.qq.com/'
        song_info_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?'
        self.song_info_url = song_info_url
        self.header_song = header_song
        self.download_url = download_url
        self.header_download = header_download

    def searchSong(self, w):
        """
        get play menu's id and get songs information
        :param id: everyone play menu of id can gain every songs information
        :return:
        """
        header_song_list = {
            'Referer': 'https://y.qq.com/portal/search.html',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        }
        base_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=58148780555861704&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w=%s&g_tk_new_20200303=5381&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0' % w
        data = {
            'ct': 24,
            'qqmusic_ver': 1298,
            'new_json': 1,
            'remoteplace': 'txt.yqq.song',
            'searchid': '58148780555861704',
            't': 0,
            'aggr': 1,
            ' cr': 1,
            'catZhida': 1,
            'lossless': 0,
            'flag_qc': 0,
            'p': 1,
            'n': 10,
            'w': w,
            'g_tk_new_20200303': 5381,
            'g_tk': 5381,
            'loginUin': 0,
            'hostUin': 0,
            'format': 'json',
            'inCharset': ' utf8',
            'outCharset': 'utf - 8',
            'notice': 0,
            'platform': 'yqq.json',
            'needNewCode': 0,
        }
        try:
            response = requests.get(base_url, params=data, headers=header_song_list)
            if response.status_code == 200:
                return self.parse_songs_info(response.text)
        except RequestException:
            print('Response songs list is wrong!')

    def parse_songs_info(self, content):
        """
        get menu's of information parse every html get songmid: in order to get vkey and get start download songs
        :param content: every html information and get id start
        :return:
        """
        infos_ = json.loads(content)
        infos = infos_.get('data').get('song').get('list')
        songs = []
        for info in infos:
            song_mid = info.get('mid')
            song_name = info.get('title')
            song_down_addr = self.parse_song((song_mid, song_name))
            if song_down_addr == None: continue
            song_subTitle = info.get('subtitle')
            song_time = info.get('interval')
            song = Song(tools.formatName(song_name+song_subTitle), song_down_addr,song_mid, song_time)
            for songer in info.get('singer'):
                song.addSinger(singer=Song.singer(songer.get('title'), songer.get('mid')))
            songs.append(song)
        return songs

    def parse_song(self, song_info):
        """
        song_info is list id is the first param
        :param song_info: including sond_mid and song_name to get songs content and start download
        :return:
        """
        data = {
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf - 8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0',
            'data': '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"8874756349","songmid":["' +
                    song_info[
                        0] + '"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}',
        }
        try:
            response = requests.get(self.song_info_url, params=data, headers=self.header_song)
            if response.status_code == 200:
                return self.parse_play_id(response.text, song_info)
        except RequestException:
            print('Song response is wrong!')

    def parse_play_id(self, content, song_info):

        info = json.loads(content)
        part_url = info.get('req_0').get('data').get('midurlinfo')[0].get('purl')
        if part_url == '': return None
        return self.download_url + part_url

