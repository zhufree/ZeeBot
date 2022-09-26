from nonebot import on_command, on_message
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import Arg, CommandArg, ArgPlainText
from config import *
import httpx, random
from hashlib import md5

url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

translate_matcher = on_command("translate", aliases={"翻译"}, priority=5) # rule=to_me(), 
en_to_cn_matcher = on_command("en2cn", aliases={"英翻中", 'encn', 'entocn'}, priority=5) # rule=to_me(), 

@translate_matcher.handle()
async def handle_cn_en_translate(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("query", args)

@en_to_cn_matcher.handle()
async def handle_en_cn_translate(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("query", args)


@translate_matcher.got("query", prompt="你想翻译什么？")
async def handle_query(query: Message = Arg(), query_str: str = ArgPlainText("query")):
    translated = await translate(query_str, 'en')
    await translate_matcher.finish(translated)

@en_to_cn_matcher.got("query", prompt="What do you want to translate?")
async def handle_en_query(query: Message = Arg(), query_str: str = ArgPlainText("query")):
    translated = await translate(query_str, 'zh')
    await translate_matcher.finish(translated)

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


async def translate(query, to):
    from_lang = 'zh'
    to_lang =  'en'
    if to == 'zh':
        from_lang = 'en'
        to_lang =  'zh'

    salt = random.randint(32768, 65536)
    sign = make_md5(baidu_appid + query + str(salt) + baidu_appkey)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': baidu_appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    r = httpx.post(url, params=payload, headers=headers)
    result = r.json()
    print(result)
    if 'from' in result.keys():
        msg = ''
        result_list = result['trans_result']
        for part in result_list:
            msg += part['dst']
        return msg
    else:
        return '翻译出错'

