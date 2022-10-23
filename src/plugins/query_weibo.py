from nonebot import on_command
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message, MessageSegment
import json

query_matcher = on_command('MBCC查询', aliases={'厕所查询', '微博查询', 'mbcc查询', 'MBCC检索'}, priority=5)

@query_matcher.handle()
async def handle_query(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("query", args)


@query_matcher.got("query", prompt="请输入编号或查询关键字")
async def query_weibo(query: Message = Arg(), query_str: str = ArgPlainText("query")):
    with open('6601575845.json', 'r', encoding='utf-8') as f:
        lines =f.readlines()
        weibo_list = []
        for l in lines:
            weibo_list.append(json.loads(l))
    query_result = []
    if query_str.isdigit():
        for weibo in weibo_list:
            if f'【{query_str}】' in weibo['content'] or weibo['content'].startswith(query_str+'\n'):
                query_result.append(weibo)
    else:
        for weibo in weibo_list:
            if query_str in weibo['content']:
                query_result.append(weibo)
    ellipse, weibo_msg = (await send_weibo(query_result))
    if ellipse:
        await query_matcher.reject(weibo_msg)
    else:
        await query_matcher.finish(weibo_msg)

async def send_weibo(weibo_list):
    ellipse = False
    if len(weibo_list) > 10:
        ellipse = True
        msg_segments = MessageSegment.text("检索结果超过10条，建议使用更精确的关键词，回复编号查看详情\n")
    elif len(weibo_list) > 1:
        ellipse = True
        msg_segments = MessageSegment.text("回复编号查看详情\n")
    else:
        ellipse = False
        msg_segments = MessageSegment.text("检索结果：\n")
    for weibo in weibo_list[:10]:
        if ellipse and len(weibo['content']) > 100:
            msg_segments += MessageSegment.text(f"{weibo['content'][:100]}...\n")
        else:
            msg_segments += MessageSegment.text(f"{weibo['content']}\n")
        if 'pics' in weibo.keys():
            for pic in weibo['pics']:
                if ellipse:
                    msg_segments += f'[ {pic} ]\n'
                else:
                    pic_segment = MessageSegment(type='image', data={
                        'file': pic}
                    )
                    msg_segments += pic_segment
        if 'video' in weibo.keys():
            msg_segments += f'视频[ {weibo["video"]} ]\n'
        msg_segments += f"at {weibo['time']}\n"
    msg_segments += 'Powered by FreeStudio, 数据非实时更新，全部微博存档: https://fun.zhufree.fun/5732/weibo/'
    return (ellipse, msg_segments)
