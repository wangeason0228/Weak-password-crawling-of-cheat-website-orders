
# 🔑 Weak-password-crawling-of-cheat-website-orders

## 📖 项目介绍 / Project Introduction

这是一个简单的爬虫工具，用于爬取外挂网站订单信息。  
This is a simple crawler tool for crawling orders from cheat websites.  


**绝对不是为了白嫖外挂网站订单**
这个小工具的灵感来自一些外挂网站的下单机制：  
在下单时会强制填写 QQ 号，有的人图省事，就用类似 `111` 这样的弱口令。  
本项目通过简单的 GUI + 爬虫逻辑，模拟用户查询订单。  

后续会加入：  
- 内置弱口令字典（用于演示弱口令风险，非实际攻击）  
- 自动排查最新订单的功能  

👉 **"千万不要用他来白嫖别人花钱买的外挂"**外挂本身就是违法的  
This project is for **research and learning only**. Do **not** use it to grab or exploit real orders. Cheating tools are illegal.

---

## ✨ 功能特性 / Features

- 🔗 自定义查询 URL / Custom query URLs  
- ⏳ 模拟人类行为（随机延迟） / Human-like random delays  
- 🛡️ 请求头伪装 / Simulated HTTP headers  
- 🖥️ 响应式 GUI / Responsive GUI interface  

---

## 📥 安装 / Installation

1. 克隆仓库 / Clone repository:
   ```bash
   git clone https://github.com/your-repo/Weak-password-crawling-of-cheat-website-orders.git
   cd Weak-password-crawling-of-cheat-website-orders

2. 安装依赖 / Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序 / Run:

   ```bash
   python 爬取外挂网站订单GUI.py
   ```

💡 懒得折腾？可以直接下载编译好的 **exe** 文件运行。

---

## 🚀 使用方法 / Usage

1. 输入要查询的 QQ 号码
2. （可选）输入页码和自定义 URL
3. 点击 **查询** 按钮
4. 在结果窗口查看订单信息

---

## ⚠️ 免责(甩锅)声明 / Disclaimer

* 本项目仅供 **学习、研究与演示弱口令风险** 之用。
* 请勿用于任何非法用途，否则后果自负。
* 作者不对任何滥用行为负责。

This project is for **educational purposes only**.
Do not misuse it. The author takes **no responsibility** for illegal uses.