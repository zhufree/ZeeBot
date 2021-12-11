from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

keywords_dict = {
    '嘤': '嘤嘤嘤'
}
reaction = on_keyword(set(keywords_dict.keys()), rule=to_me(), priority=5)


@reaction.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    keyword = str(event.get_message())
    await reaction.finish(keywords_dict[keyword])
