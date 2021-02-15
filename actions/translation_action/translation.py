# -*- coding: utf-8 -*-
# Time    : 2021/2/15 17:35
# Author  : LiaoKong
import hashlib
import requests
import random
from secret_config import baidu_appid, translation_secret_key


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def translation(query):
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    if is_contain_chinese(query):
        from_lang = 'zh'
        to_lang = 'en'
    else:
        from_lang = 'en'
        to_lang = 'zh'
    salt = random.randint(32768, 65536)

    sign = baidu_appid + query + str(salt) + translation_secret_key
    sign = sign.encode('utf-8')
    m1 = hashlib.md5()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = u'{}?appid={}&q={}&from={}&to={}&salt={}&sign={}'.format(
        myurl, baidu_appid, query, from_lang, to_lang, salt, sign)

    try:
        response = requests.get(myurl)
        data = response.json()
        return [x['dst'] for x in data['trans_result']]
    except Exception, e:
        import traceback
        traceback.print_exc()
        return []


if __name__ == '__main__':
    print translation(u'apple random')
