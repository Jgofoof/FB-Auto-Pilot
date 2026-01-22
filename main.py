import requests
from bs4 import BeautifulSoup
import time
import os
import random
from datetime import datetime

class FBAssistant:
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
        }
        self.base_url = "https://mbasic.facebook.com"

    def check_live(self):
        try:
            res = requests.get(f'{self.base_url}/profile.php', headers=self.headers)
            return 'logout.php' in res.text
        except: return False

    def get_random_quote(self):
        try:
            response = requests.get("https://zenquotes.io/api/quotes")
            data = response.json()
            quote_data = random.choice(data)
            return f"{quote_data['q']} — {quote_data['a']}"
        except:
            return "Sống là phải mạnh mẽ! #motivation"

    def auto_post(self, content):
        try:
            res = requests.get(self.base_url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            form = soup.find('form', action=lambda x: x and '/composer/mbasic/' in x)
            action_url = self.base_url + form['action']
            data = {inp.get('name'): inp.get('value', '') for inp in form.find_all('input') if inp.get('name')}
            data['xc_message'] = content
            data['view_post'] = 'Đăng'
            requests.post(action_url, data=data, headers=self.headers)
            print(f"[✓] Đã đăng bài: {content[:30]}...")
        except Exception as e: print(f"[×] Lỗi đăng bài: {e}")

    def auto_add_friends(self, limit=5):
        try:
            res = requests.get(f'{self.base_url}/friends/center/suggestions/', headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a', text='Thêm bạn bè')
            for i, link in enumerate(links[:limit]):
                requests.get(self.base_url + link['href'], headers=self.headers)
                print(f"[✓] Đã gửi lời mời thứ {i+1}")
                time.sleep(random.randint(5, 15))
        except Exception as e: print(f"[×] Lỗi kết bạn: {e}")

def auto_pilot(bot):
    last_posted_date = ""
    print("[!] Kích hoạt Auto-Pilot thành công. Đang treo máy...")
    while True:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        # Đăng bài 1 lần/ngày vào giờ ngẫu nhiên (8h-20h)
        if today != last_posted_date and 8 <= now.hour <= 20:
            bot.auto_post(bot.get_random_quote())
            last_posted_date = today
            
        # Kết bạn rải rác ban ngày
        if 7 <= now.hour <= 22:
            bot.auto_add_friends(limit=random.randint(1, 3))
            
        wait_time = random.randint(30, 90)
        print(f"[{now.strftime('%H:%M:%S')}] Nghỉ {wait_time} phút...")
        time.sleep(wait_time * 60)

def main():
    os.system('clear')
    print("="*35 + "\n    FB AUTO-PILOT TOOL\n" + "="*35)
    cookie = input("[!] Nhập Cookie Facebook: ")
    bot = FBAssistant(cookie)
    if bot.check_live():
        print("1. Chạy thủ công (Đăng bài ngay)\n2. Chạy Auto-Pilot (Treo máy)")
        if input("[?] Chọn: ") == '2': auto_pilot(bot)
        else: bot.auto_post(bot.get_random_quote())
    else: print("[×] Cookie Die!")

if __name__ == "__main__":
    main()

