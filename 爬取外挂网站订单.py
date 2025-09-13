"""
示例：使用自定义请求头和随机延迟进行合规的网页请求示例。

警告与合规性：
- 在开始前确认目标网站允许抓取（优先使用官方 API 或取得授权）。
- 尊重 `robots.txt` 的规则；不要尝试绕过验证码或其他安全控制。
"""

import sys
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib import parse, request
import json




def build_default_headers() -> dict:
	# 模拟目标网站要求的请求头
	return {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Accept-Language": "zh-CN,zh;q=0.9",
		"X-Requested-With": "XMLHttpRequest",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Origin": "https://996.296k.my",
		"Referer": "https://996.296k.my/",
		"Sec-Ch-Ua": "\"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
		"Sec-Ch-Ua-Mobile": "?0",
		"Sec-Ch-Ua-Platform": "\"Windows\"",
		"Sec-Fetch-Site": "same-origin",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Dest": "empty",
		"Accept-Encoding": "gzip, deflate, br",
	}


def fetch_url(target_url: str, session: requests.Session = None, headers: dict = None) -> requests.Response:
	if session is None:
		session = requests.Session()
	if headers:
		session.headers.update(headers)

	# 简单的重试与延迟策略
	for attempt in range(1, 4):
		try:
			resp = session.get(target_url, timeout=15)
			return resp
		except requests.RequestException as e:
			wait = 1 + attempt * 2 + random.random()
			print(f"请求失败（尝试 {attempt}）：{e}，{wait:.1f}s 后重试")
			time.sleep(wait)
	raise RuntimeError("请求多次失败，放弃")


def main():
	keywords = input("请输入查询的 QQ 号码：").strip()
	url = "https://996.296k.my/ajax.php?act=query"  # 请替换为目标 URL

	data = {"type": "0", "qq": keywords, "page": "1"}

	data = parse.urlencode(data, encoding="utf-8")  # 编码转换

	headers = build_default_headers()
	session = requests.Session()
	# 设置 Cookie
	session.cookies.update({
		"_ok1_": "DrNOK/bDjhfsuOGQcESbBQWCB9uepCOZxydvbjOyjkXgOADweu589rpyVfUzYggV2yPi3bS99uEVZwiBfzMHJL9hfJ1qXPhd/rr1DQVOByfYCwTcGdTfSQhEilATCvqt",
		"PHPSESSID": "pdopbre2v6il7okq9h997igsh4",
		"mysid": "c928fe1b267cb5a453f027daa73e1d2c",
		"counter": "1"
	})

	# 随机短延迟，降低请求速率
	delay = random.uniform(1.0, 3.0)
	print(f"等待 {delay:.2f}s 后发起请求（遵守速率限制）...")
	time.sleep(delay)

	resp = session.post(url, data=data, headers=headers, cookies=session.cookies)
	if resp.ok:
		print("请求成功，状态码：", resp.status_code)
		json_data = resp.json()
		print("返回的 JSON 数据：", json.dumps(json_data['data'], ensure_ascii=False, indent=2))
		# print("所有 addtime 值：", [item['addtime'] for item in json_data['data']])
	else:
		print("请求失败，状态码：", resp.status_code)

	# 询问用户是否继续查询
	while True:
		choice = input("是否继续查询？(y/n): ").strip().lower()
		if choice == 'y':
			main()
			break
		elif choice == 'n':
			print("程序结束。")
			sys.exit()
		else:
			print("请输入 'y' 或 'n'。")


if __name__ == "__main__":
	main()