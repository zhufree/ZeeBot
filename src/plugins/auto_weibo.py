from config import *
import json, httpx, time, random
from pyquery import PyQuery as pq
from playwright.async_api import async_playwright
# from nonebot import require
# require("nonebot_plugin_apscheduler")
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler

@scheduler.scheduled_job("cron", hour='7-23', id="post_novel")
async def run_every_hour():
    logger.info('tick')
    await main()

async def main():
    # get novel list
    save_file = open('data/novel_data.json', 'r+', encoding='utf-8')
    content = save_file.read()
    save_file.close()
    data_list = []
    if content == '':
        data_list = init_data()
    else:
        data_list =  json.loads(content)
    # decide which novel which chapter
    selected_novel, select_chap = select_novel(data_list, 0)
    # grab content
    post_content = f'#{selected_novel["title"]}# by {selected_novel["author"]}\n'
    if select_chap != None:
        chapter_content = get_chapter_content(select_chap['url'])
        # in case content is too long
        if len(chapter_content) > 4500:
            post_content += chapter_content[:4500]
        else:
            post_content += chapter_content + '...'
    post_content += f'\n阅读原文：{selected_novel["url"]}'
    # post weibo
    if post_content != '':
        await post_weibo(post_content)
    # update novel data
    new_data = append_data(data_list)
    write_file = open('data/novel_data.json', 'w', encoding='utf-8')
    write_file.write(json.dumps(new_data, ensure_ascii=False))
    write_file.close()

def select_novel(data_list, retry):
    if retry > 5:
        return None
    selected_novel = random.choice(data_list)
    current_chap = selected_novel['current_chap']
    novel_detail = get_detail_page(selected_novel['url'])
    if current_chap >= novel_detail['chap_count']:
        retry += 1
        select_novel(data_list, retry)
    elif novel_detail['vip_chap_id'] != None and current_chap >= novel_detail['vip_chap_id'] - 1:
        data_list.remove(selected_novel)
        retry += 1
        select_novel(data_list, retry)
    else:
        # update chap count
        selected_novel['current_chap'] += 1
        return selected_novel, novel_detail['chap_list'][current_chap]


search_url = 'https://www.jjwxc.net/bookbase.php?xx3=3&sortType=3&isfinish=1&page={}'

def append_data(old_data):
    page = 0
    exist = False
    new_novel_list = []
    old_titles = [i['title'] for i in old_data]
    while not exist:
        res = httpx.get(search_url.format(page), headers={'Cookie': jjwxc_cookies})
        res.encoding = 'gb2312'
        doc = pq(res.text)
        trs = list(doc('table.cytable tr').items())
        for tr in trs[1:]:
            tds = list(tr('td').items())
            author = tds[0].text()
            title = tds[1].text()
            url = 'https://www.jjwxc.net/' + tds[1]('a').attr('href')
            wordcount = tds[5].text()
            publish_time = tds[7].text()
            # print(author, title, url, wordcount, publish_time)
            # novel_data = get_detail_page(url)
            if title in old_titles:
                exist = True
            new_novel_list.append({
                'title': title,
                'author': author,
                'url': url,
                'wordcount': wordcount,
                'publish_time': publish_time,
                'current_chap': 0
                # 'chap_count': novel_data['chap_count']
            })
    # with open('data/novel_data.json', 'w', encoding='utf-8') as save:
    #     save.write(json.dumps(new_novel_list, ensure_ascii=False))
    return old_data + new_novel_list


def init_data():
    page = 0
    delta_days = 0
    new_novel_list = []
    while delta_days < 20.0:
        res = httpx.get(search_url.format(page), headers={'Cookie': jjwxc_cookies})
        res.encoding = 'gb2312'
        doc = pq(res.text)
        trs = list(doc('table.cytable tr').items())
        for tr in trs[1:]:
            tds = list(tr('td').items())
            author = tds[0].text()
            title = tds[1].text()
            url = 'https://www.jjwxc.net/' + tds[1]('a').attr('href')
            wordcount = tds[5].text()
            publish_time = tds[7].text()
            # print(author, title, url, wordcount, publish_time)
            # novel_data = get_detail_page(url)
            new_novel_list.append({
                'title': title,
                'author': author,
                'url': url,
                'wordcount': wordcount,
                'publish_time': publish_time,
                'current_chap': 0
                # 'chap_count': novel_data['chap_count']
            })
            # 2022-12-20 08:58:15
            time_stamp = time.mktime(time.strptime(publish_time,"%Y-%m-%d %H:%M:%S"))
            delta_time = time.time() - time_stamp
            delta_days = delta_time // (24*3600)
        page += 1
    with open('data/novel_data.json', 'w', encoding='utf-8') as save:
        save.write(json.dumps(new_novel_list, ensure_ascii=False))
    return new_novel_list


def get_detail_page(url):
    detail_res = httpx.get(url)
    detail_res.encoding = 'gb2312'
    doc = pq(detail_res.text)
    chap_table = doc('#oneboolt')
    chapters = chap_table('tr[itemprop~=chapter]').items()
    chap_list = []
    for chap in chapters:
        chap_tds = list(chap('td').items())
        chap_id = chap_tds[0].text().strip()
        chap_title = chap_tds[1].text()
        if chap_title == '等待进入网审' or chap_title == '[屏蔽中]' or '[VIP]' in chap_title:
            continue
        chap_desc = chap_tds[2].text()
        chap_time = chap_tds[5]('span:first-child').text()
        chap_list.append({
            'id': chap_id,
            'title': chap_title,
            'url': chap_tds[1]('a').attr('href').replace('http://', 'https://'),
            'desc': chap_desc,
            'time': chap_time
        })
    return {
        'collection_count': doc('span[itemprop=collectedCount]').text(),
        'chap_count': len(chap_list),
        'vip_chap_id': None,
        'chap_list': chap_list
    }


def get_chapter_content(url):
    detail_res = httpx.get(url)
    detail_res.encoding = 'gb2312'
    doc = pq(detail_res.text)
    div = doc('.noveltext')
    div.remove('div:first-child')
    div.remove('div[align=right]')
    content = div.text()
    return content


async def post_weibo(content):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(storage_state='weibo_state.json')
        page = await context.new_page()
        await page.goto("https://weibo.com/")
        await page.get_by_placeholder("有什么新鲜事想分享给大家？").click()
        await page.get_by_placeholder("有什么新鲜事想分享给大家？").fill(content)
        # 粉见
        # page.get_by_text("公开").click()
        # page.get_by_role("button", name="粉丝").click()
        await page.get_by_role("button", name="发送").click()
        await page.get_by_text("发布成功").wait_for()
        await page.close()
        await context.storage_state(path='weibo_state.json')
        await context.close()
        await browser.close()
# scheduler.add_job(ru:n_every_day_from_program_start, "interval", days=1, id="xxx")
# main()