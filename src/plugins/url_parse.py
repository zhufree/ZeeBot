from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from linkson import parse_url
from config import *
import json

url_matcher = on_regex(r'http|小程序|豆瓣', priority=1)
@url_matcher.handle()
async def handle_audio(bot: Bot, event: Event):
    msg = event.get_message()
    text = event.get_plaintext().strip()
    print(text)
    result = None
    url_type = ''
    if text.startswith('http'):
        url = text
        if 'weibo' in url:
            url_type = 'weibo'
            result = parse_url(url, weibo_cookies=weibo_cookies)
        elif 'douban' in url:
            url_type = 'douban'
            result = parse_url(url)
    else:
        for segment in msg:
            # 处理小程序
            if segment.type == 'json':
                data_str = segment.data['data']
                data_dict = json.loads(data_str.replace('\\', ''))
                if '热门微博' in data_str:
                    url = data_dict['meta']['detail_1']['qqdocurl'].replace('\/', '/')
                    result = parse_url(url, weibo_cookies=weibo_cookies)
                elif '豆瓣' in data_str:
                    url = data_dict['meta']['news']['jumpUrl'].replace('\/', '/')
                    result = parse_url(url)
    if result != None and result['success']:
        if url_type == 'douban':
            msg_segments = MessageSegment.text(f"{result['title']}\n")
        else:
            msg_segments = ''
        msg_segments += MessageSegment.text(f"{result['content']}\n")
        if len(result['pics']) > 0:
            for pic in result['pics']:
                pic_segment = MessageSegment(type='image', data={
                    'file': pic}
                )
                msg_segments += pic_segment
        msg_segments += MessageSegment.text(f"by {result['author']}")
        await url_matcher.finish(Message(msg_segments))