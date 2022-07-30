from nonebot import on_command, on_keyword, on_regex
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_message
import os, random

judy_matcher = on_regex(r"\s*((?:Judy|朱迪|朱)(?:叫|按钮))|(?:mea +button)\s*")
qywy_matcher = on_regex(r'温温温|绝绝绝')
txl_matcher = on_regex(r'探虚陵|txl|探')

def get_audio_path(audio_dir):
    audio_files = os.listdir(f'audios/{audio_dir}')
    random_audio = random.choice(audio_files)
    base_path = os.path.split(os.path.abspath(random_audio))[0]
    # return 'file:///' + base_path + f'\\audios\\{audio_dir}\\' + random_audio
    return 'file://' + base_path + f'/audios/{audio_dir}/' + random_audio

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
