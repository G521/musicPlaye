#!bin/even/python3.6
# -*- encoding:utf-8 -*-
import os
import re

import requests
import json
from requests import RequestException

from com.tools import tools
from com.tools.tools import formatName


class Song:
    def __init__(song, name, id, time):
        song.name = name
        song.id = id
        song.down_addr = 'https://music.163.com/song/media/outer/url?id=' + str(id)
        song.time = time//1000
        song.singers=[]
    def addsinger(song, singer):
        song.singers.append(singer)
    class singer:
        def __init__(song, name, id):
            song.name = name
            song.url = 'https://music.163.com/#/artist?id=%d'%id
        def getname(self):
            return self.name

def searchSong(w, type, offset,limit):
    header_song = {
        'Referer': 'https://music.163.com/search/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'cookie': '_iuqxldmzr_=32; _ntes_nnid=7022e9820e509a6f110d17fdb2e736ec,1591249386502; _ntes_nuid=7022e9820e509a6f110d17fdb2e736ec; WM_TID=uq0pNrhrtZNBUQFRVFc%2BHG6iss2gVRbo; JSESSIONID-WYYY=fzNSgnCE980ASubEm5Yc44gFIWVfEhKp4G%2BZexw%2FwMp%2FFFBJ%5CPTpMBtSK1sXGXPAMS13sohEj1YUVykNSfThe7WiDJgUvC682MBK24YNv%2FuFf1az5KPYrq%2Bbl7IA%5CQE5XRK8%2FUbOjNGHmBqKgKE3PRkDX166jKulKvI9XaTf1Y8nA%2FyK%3A1591956135927; WM_NI=%2BCOlnUlwl4YzndpJ5ZvGHMhRKcYULIb5RHnHFKh9NghI3ypVIsP43ZBtEY%2FdeVQu6%2BSq7JnUzWJ4QOjYUdlkK2HRHRWuYu8a0jupComxrh%2Fu9ImW1gWE%2FjG79TF4AVcLdGE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee86fb3e8ca697bbc13bafe78ba6d44a969a9abab6608eefe5d5f134b4ec9baadc2af0fea7c3b92ae99d818ded5fb0a9a4d5dc72aebcc0abb852b69988aeeb5a89bd97b6cf43a2eb9ea9ed448695a8dacd6dac97fd9af35e8bada0d5b25282ac8bbaae70a78a9f96b52191aff9abed5fba8986d5d445aa879b85ef6189ee88b3cb5a95ab9796bb6bf4b6bb91c265afa8be89ae7ffb97a3b8b46d959be18bc63dfb8c8ad5c45ea194aca8c837e2a3'
    }
    base_url = 'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s={%s}&type=1&offset=0&total=true&limit=20' % w
    data = {
        'csrf_token': 'hlpretag=',
        'hlposttag': '',
        's': w,
        'type': type,
        'offset': offset,
        'total': 'true',
        'limit': limit
    }
    try:
        response = requests.get(base_url, params=data, headers=header_song)
        if response.status_code == 200:
            return parse_songs_info(response.text)
    except RequestException:
        print('Response songs list is wrong!')

def parse_songs_info(content):
    infos_ = json.loads(content)
    infos = infos_.get('result').get('songs')
    songs = []
    for info in infos:
        song_id = info.get('id')
        song_name = info.get('name')
        song_time = info.get('duration')
        song_ = Song(formatName(song_name), song_id, song_time)
        for i in info.get('artists'):
            song_.addsinger(song_.singer(formatName(i.get('name')),i.get('id')))
        songs.append(song_)
    return songs

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
    print(req.content)
    if not os.path.exists(path_store):
        with open(path_store, 'wb') as f:
            f.write(req.content)
            f.close()
    return True

#
# for song in searchSong("月光", 1, 1, 20):
#     print((song.down_addr, song.name))