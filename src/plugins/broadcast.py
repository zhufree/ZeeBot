from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, PrivateMessageEvent
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
import asyncio

broadcast = on_command("广播", aliases={"bc"}, permission=SUPERUSER)
banned_group = [] # 不发广播的群

@broadcast.handle()
async def _(bot: Bot, event: PrivateMessageEvent, arg: Message = CommandArg()) -> None:
    msg = arg.extract_plain_text().strip()
    if not msg:
        await bot.send_private_msg(user_id=event.user_id, message="请在指令后接需要广播的消息")
    group_list = await bot.get_group_list()
    for group in group_list:
        group_id = group["group_id"]
        if group_id not in banned_group:
            await bot.send_group_msg(group_id=group["group_id"], message=msg)
            await asyncio.sleep(0.5)