from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Message, PrivateMessageEvent
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
import httpx
url = "https://api.notion.com/v1/blocks/{}/children"
diary = on_message(permission=SUPERUSER)
banned_group = [] # 不发广播的群

@diary.handle()
async def _(bot: Bot, event: PrivateMessageEvent) -> None:
    msg = event.get_plaintext().strip()
    print(msg)
    if len(msg) >= 10:
        if sync(msg):
            await bot.send_private_msg(user_id=event.user_id, message='√')
        else:
            await bot.send_private_msg(user_id=event.user_id, message='error')

def sync(msg: str):
    from config import notion_secret, page_id
    print('sync')
    headers = {
        "Authorization":"Bearer " + notion_secret,
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }
    data = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text","text": { "content": msg,}}]
                }
            }
	    ]
    }
    res = httpx.patch(url.format(page_id), headers=headers, json=data)
    print(res.content)
    if res.status_code == 200:
        return True
    else:
        return False


