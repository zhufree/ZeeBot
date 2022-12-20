from nonebot import on_command, on_keyword, on_regex
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_message
import os, random


jailer_keywords = {
    'zoya': ['zoya', '卓娅'],
    'baiyi': ['白逸', '白1'],
    '72c': ['切尔西', '切尔西伯爵', '72c', '富婆'],
    'aien': ['艾恩'],
    'haila': ['海拉'],
    '99': ['九十九', '99'],
    'hekadi': ['赫卡蒂'],
    'lanli': ['兰利'],
    'heluo': ['赫罗'],
    'yilinna': ['伊琳娜', '10娜'],
    'hameier': ['哈梅尔', '水母'],
    'amypan': ['艾米潘', 'emp'],
    'fuluola': ['芙洛拉'],
    'guanxingzhe': ['占星者', '观星者'],
    'leibinisi': ['雷比尼斯'],
    'demoli': ['德莫莉'],
    'weiduoliya': ['维多利亚'],
    'kexi': ['科希', '科c'],
    'kaierwen': ['开尔文'],
    'yigeni': ['伊格尼'],
    'luliaika': ['露莉艾卡'],
    'qiong': ['琼'],
    'hujiao': ['胡椒'],
    'lisa': ['丽莎'],
    'puxila':['普希拉'],
    'taitela': ['泰特拉'],
    'peiji': ['佩姬'],
    'an': ['安'],
    'airuier': ['艾瑞尔'],
    'chensha': ['辰砂'],
    'duoli': ['多莉'],
    'jin':['堇'],
    'tan': ['昙'],
    'kamilian': ['卡米利安'],
    'koukou': ['蔻蔻'],
    'luweiyalei': ['露薇娅蕾'],
    'maqiduo': ['玛奇朵'],
    'nox': ['诺克斯', 'nox'],
    'pajiaxi': ['帕加茜'],
    'wendy': ['温蒂'],
    'xiayin': ['夏音'],
    'mess': ['莓丝'],
    'snake': ['娜恰', '小蛇'],
    'mcqueen': ['麦昆'],
    'enfer': ['恩菲尔'],
    'oak': ['oak', '橡木匣']
}
async def jailer_checker(event: Event) -> bool:
    all_keywords = []
    for i in jailer_keywords.values():
        all_keywords += i
    return event.get_plaintext() in all_keywords

jailer_rule = Rule(jailer_checker)
jailer_matcher = on_message(rule=jailer_rule)

@jailer_matcher.handle()
async def handle_jailer_audio(bot: Bot, event: Event):
    for jailer, keywords in jailer_keywords.items():
        if event.get_plaintext() in keywords:
            path = get_audio_path(jailer)
            audio_msg = Message(MessageSegment(type='record', data={
                'file':path}
            ))
            await jailer_matcher.finish(audio_msg)

def get_audio_path(audio_dir):
    audio_files = os.listdir(f'audios/{audio_dir}')
    random_audio = random.choice(audio_files)
    base_path = os.path.split(os.path.abspath(random_audio))[0]
    # return 'file:///' + base_path + f'\\audios\\{audio_dir}\\' + random_audio
    return 'file://' + base_path + f'/audios/{audio_dir}/' + random_audio

judy_matcher = on_regex(r"\s*((?:Judy|朱迪|朱)(?:叫|按钮))|(?:mea +button)\s*")
qywy_matcher = on_regex(r'温温温|绝绝绝|qywy|茜言万雨')
txl_matcher = on_regex(r'探虚陵')

@judy_matcher.handle()
async def handle_audio(bot: Bot, event: Event):
    path = get_audio_path('judy')
    audio_msg = Message(MessageSegment(type='record', data={
        'file':path}
    ))
    await judy_matcher.finish(audio_msg)

@qywy_matcher.handle()
async def handle_audio(bot: Bot, event: Event):
    path = get_audio_path('qywy')
    audio_msg = Message(MessageSegment(type='record', data={
        'file':path}
    ))
    await qywy_matcher.finish(audio_msg)

@txl_matcher.handle()
async def handle_audio(bot: Bot, event: Event):
    path = get_audio_path('txl')
    audio_msg = Message(MessageSegment(type='record', data={
        'file':path}
    ))
    await txl_matcher.finish(audio_msg)


keywords_dict = {
    '嘤': '嘤嘤嘤'
}
reaction = on_keyword(set(keywords_dict.keys()), priority=5)

@reaction.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    keyword = str(event.get_message())
    await reaction.finish(keywords_dict[keyword])

help_matcher = on_command('帮助')
@help_matcher.handle()
async def help_handler(bot: Bot, event: Event):
    msg = '''本bot目前支持以下功能：
    1.微博等平台的动态订阅（艾特我并发送“添加订阅”开始使用）
    2.点歌+歌名进行点歌
    3.发送关键词触发随机语音回复
    4.自定义群内自动回复
其他功能及详细说明请查看使用文档：
https://gj5i5wsqre.feishu.cn/docx/doxcnZ41X93jOqDb0qxB1afY9vh
广告位：https://baihehub.com
    '''
    await help_matcher.finish(msg)