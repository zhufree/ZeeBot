from nonebot import on_command, on_keyword, on_regex
from nonebot.rule import to_me, Rule
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
    'lanli': ['兰利']
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
qywy_matcher = on_regex(r'温温温|绝绝绝')
txl_matcher = on_regex(r'探虚陵|txl|探')

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
reaction = on_keyword(set(keywords_dict.keys()), rule=to_me(), priority=5)

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
其他功能及详细说明请查看使用文档：
https://gj5i5wsqre.feishu.cn/docx/doxcnZ41X93jOqDb0qxB1afY9vh
广告位：https://baihehub.com
    '''
    await help_matcher.finish(msg)