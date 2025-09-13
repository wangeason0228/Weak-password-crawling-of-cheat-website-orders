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
import customtkinter as ctk
from tkinter import StringVar
from tkinter import scrolledtext




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


def fetch_data(keywords, page_number, custom_url=None, status_label=None, window=None):
	# 使用用户自定义URL或默认URL
	url = custom_url if custom_url and custom_url.strip() else "https://996.296k.my/ajax.php?act=query"
	data = {"type": "0", "qq": keywords, "page": page_number}
	data = parse.urlencode(data, encoding="utf-8")  # 编码转换

	# 更新状态栏显示
	if status_label and window:
		status_label.configure(text=f"正在搜索 QQ: {keywords}, 页码: {page_number}...")
		window.update()  # 强制更新UI

	headers = build_default_headers()
	session = requests.Session()
	session.cookies.update({
		"_ok1_": "DrNOK/bDjhfsuOGQcESbBQWCB9uepCOZxydvbjOyjkXgOADweu589rpyVfUzYggV2yPi3bS99uEVZwiBfzMHJL9hfJ1qXPhd/rr1DQVOByfYCwTcGdTfSQhEilATCvqt",
		"PHPSESSID": "pdopbre2v6il7okq9h997igsh4",
		"mysid": "c928fe1b267cb5a453f027daa73e1d2c",
		"counter": "1"
	})

	delay = random.uniform(1.0, 3.0)
	
	# 更新状态栏显示等待时间
	if status_label and window:
		status_label.configure(text=f"等待 {delay:.1f} 秒...(模拟你是人类)")
		window.update()
	
	time.sleep(delay)
	
	# 更新状态栏显示正在发送请求
	if status_label and window:
		status_label.configure(text="正在发送请求...")
		window.update()

	resp = session.post(url, data=data, headers=headers, cookies=session.cookies)
	
	# 更新状态栏显示请求结果
	if status_label and window:
		if resp.ok:
			status_label.configure(text="搜索完成")
		else:
			status_label.configure(text=f"请求失败，状态码：{resp.status_code}")
		window.update()
		
	if resp.ok:
		json_data = resp.json()
		return json.dumps(json_data['data'], ensure_ascii=False, indent=2)
	else:
		return f"请求失败，状态码：{resp.status_code}"

def main():
	# 设置外观模式和默认颜色主题
	ctk.set_appearance_mode("dark")  # 可选: "dark", "light", "system"
	ctk.set_default_color_theme("blue")  # 可选: "blue", "green", "dark-blue"
	
	def on_submit():
		keywords = entry.get().strip()
		if not keywords:
			result_text.insert("0.0", "请输入查询内容！\n")
			status_label.configure(text="错误：未输入查询内容")
			return
		page_number = page_entry.get().strip()  # 获取用户输入的页码值
		result_text.delete("0.0", "end")
		# 更新状态栏
		status_label.configure(text="准备查询...")
		window.update()
		
		# 禁用查询按钮，防止重复点击
		submit_button.configure(state="disabled")
		
		# 执行查询，传入状态栏标签和窗口对象
		# 获取用户自定义URL
		custom_url = url_entry.get().strip()
		
		# 执行查询，传入用户自定义URL、状态栏标签和窗口对象
		result = fetch_data(keywords, page_number, custom_url, status_label, window)
		
		# 重新启用查询按钮
		submit_button.configure(state="normal")
		result_text.insert("0.0", result)
		
		# 更新状态栏为完成状态
		status_label.configure(text="查询完成")

	# 创建主窗口
	window = ctk.CTk()
	window.title("数据查询工具")
	window.geometry("1000x700")
	
	# 创建主框架
	main_frame = ctk.CTkFrame(window)
	main_frame.pack(fill="both", expand=True, padx=20, pady=20)
	
	# 标题
	title_label = ctk.CTkLabel(main_frame, text="外挂网站订单查询工具", font=ctk.CTkFont(size=20, weight="bold"))
	title_label.pack(pady=10)

	# 输入框和标签 - 左右布局
	input_frame = ctk.CTkFrame(main_frame)
	input_frame.pack(fill="x", padx=20, pady=10)
	
	# 创建左侧和右侧框架
	left_frame = ctk.CTkFrame(input_frame)
	left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
	
	right_frame = ctk.CTkFrame(input_frame)
	right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
	
	# 左侧 - QQ号码输入
	label = ctk.CTkLabel(left_frame, text="请输入查询的 QQ 号码：")
	label.pack(anchor="w", pady=5, padx=10)
	entry = ctk.CTkEntry(left_frame, width=300, placeholder_text="输入QQ号码")
	entry.pack(fill="x", pady=8, padx=10)
	
	# 左侧 - 页码输入
	page_label = ctk.CTkLabel(left_frame, text="请输入页码：")
	page_label.pack(anchor="w", pady=5, padx=10)
	page_entry = ctk.CTkEntry(left_frame, width=300, placeholder_text="默认为1")
	page_entry.pack(fill="x", pady=8, padx=10)
	page_entry.insert(0, "1")  # 默认页码为1
	
	# 右侧 - URL输入框
	url_label = ctk.CTkLabel(right_frame, text="请输入查询URL（可选）：")
	url_label.pack(anchor="w", pady=5, padx=10)
	url_entry = ctk.CTkEntry(right_frame, width=300, placeholder_text="默认为https://996.296k.my/ajax.php?act=query")
	url_entry.pack(fill="x", pady=8, padx=10)
	url_entry.insert(0, "https://996.296k.my/ajax.php?act=query")  # 默认URL
	
	# 右侧 - 查询按钮
	submit_button = ctk.CTkButton(right_frame, text="查询", command=on_submit)
	submit_button.pack(pady=15, padx=10, fill="x")

	# 结果显示框
	result_frame = ctk.CTkFrame(main_frame)
	result_frame.pack(fill="both", expand=True, padx=20, pady=10)
	
	result_label = ctk.CTkLabel(result_frame, text="查询结果：")
	result_label.pack(anchor="w", padx=5, pady=5)
	
	result_text = ctk.CTkTextbox(result_frame, width=600, height=250)
	result_text.pack(fill="both", expand=True, padx=5, pady=5)

	# 状态栏
	status_frame = ctk.CTkFrame(main_frame, height=30)
	status_frame.pack(fill="x", padx=20, pady=5)
	status_label = ctk.CTkLabel(status_frame, text="就绪")
	status_label.pack(side="left", padx=10)

	window.mainloop()


if __name__ == "__main__":
	main()