from requests import Session
from time import time
start_time = time()


# 数据
like_url = 'https://tieba.baidu.com/mo/q/newmoindex?'
sign_url = 'http://tieba.baidu.com/sign/add'
tbs = '4fb45fea4498360d1547435295'
head = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    # 填入自己的cookie
    'Cookie': 'BAIDUID=xxxxxx:FG=1; compare_local_cookie=xxxxxx; BAIDU_WISE_UID=wpass_xxxxxx_642; logTraceID=xxxxxx; BDUSS=xxxxxxxxxx-xxxxx; STOKEN=xxxxxx; LASTLOGINTYPE=0; PTOKEN=xxxxxx; UBI=xxx%xxx-%xxx%xxx',
    'Host': 'tieba.baidu.com',
    'Referer': 'http://tieba.baidu.com/i/i/forum',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}
s = Session()


# 获取关注的贴吧
bars = []
dic = s.get(like_url, headers=head).json()['data']['like_forum']
for bar_info in dic:
    bars.append(bar_info['forum_name'])


# 签到
already_signed_message = '\u4eb2\uff0c\u4f60\u4e4b\u524d\u5df2\u7ecf\u7b7e\u8fc7\u4e86'
already_signed = 0
succees = 0
failed_bar = []
for bar in bars:
    data = {
        'ie': 'utf-8',
        'kw': bar,
        'tbs': tbs
    }
    try:
        r = s.post(sign_url, data=data, headers=head)
    except Exception as e:
        print(f'未能签到{bar}, 由于{e}。')
        failed_bar.append(bar)
        continue
    dic = r.json()
    if dic['error'] == already_signed_message: already_signed += 1
    print(f"{bar}：{dic['error']}")
    succees += 1
end_time = time()
t = end_time - start_time
l = len(bars)
failed = "\n失败列表："+'\n'.join(failed_bar) if len(failed_bar) else ''
input(f'''共{l}个吧，其中: {succees}个吧签到成功，{len(failed_bar)}个吧签到失败，{already_signed}个吧已经签到。{failed}
此次运行用时{t}s。''')
