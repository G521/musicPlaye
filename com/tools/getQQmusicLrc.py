import base64
import json
import requests
import re


def QQlrcGet(mid, name):
    heard = {
        'referer': 'https: // y.qq.com / portal / player.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?-=MusicJsonCallback_lrc&pcachetime=1592102808614&songmid=%s&g_tk_new_20200303=5381&g_tk=5381&loginUin=2997385765&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0' % mid
    req = requests.get(url, headers=heard)
    info = json.loads(req.text)
    info.get('lyric')
    result = base64.b64decode(info.get('lyric'))
    result = result.decode('utf-8').split('\n')
    return ('\n'.join(result[5:]))


#
print(QQlrcGet('003OTVXl3LeVF9', ''))

print('*' * 12)


# -*- coding:utf-8 -*-
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
    return '\n'.join(result)

print(NeteaseGet(1403858540, ''))