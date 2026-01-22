import requests
import re
import time
import os
import random
from datetime import datetime

# ================= CẤU HÌNH HỆ THỐNG =================
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 12; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
]

QUOTES_VN = [
    "Hành trình vạn dặm bắt đầu từ một bước chân.",
    "Thành công không phải là điểm dừng, thất bại không phải là kết thúc.",
    "Hãy sống tử tế với chính mình và mọi người xung quanh.",
    "Mỗi ngày mới là một cơ hội để làm tốt hơn ngày hôm qua.",
    "Kiên trì là chìa khóa mở mọi cánh cửa khó khăn."
]

class FB_Ultimate_Tool:
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'cookie': cookie,
            'user-agent': random.choice(USER_AGENTS),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
            'referer': 'https://mbasic.facebook.com/',
        }
        self.base_url = "https://mbasic.facebook.com"

    def get_form_data(self, url):
        """Thuật toán trích xuất form và token bảo mật từ GitHub"""
        try:
            res = requests.get(url, headers=self.headers, timeout=15)
            # Regex tìm mã bảo mật fb_dtsg và jazoest
            fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text)
            jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text)
            action = re.search(r'action="(/composer/mbasic/.*?)"', res.text) or \
                     re.search(r'action="(/a/mobile/friends/add_friend.php.*?)"', res.text)
            
            if fb_dtsg and jazoest and action:
                return {
                    'fb_dtsg': fb_dtsg.group(1),
                    'jazoest': jazoest.group(1),
                    'action': action.group(1).replace('&amp;', '&'),
                    'html': res.text
                }
            return None
        except: return None

    def auto_post(self):
        """Tính năng đăng bài tự động ngẫu nhiên"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang lấy dữ liệu đăng bài...")
        form = self.get_form_data(f"{self.base_url}/composer/mbasic/")
        if not form:
            print("[×] Không lấy được mã bảo mật đăng bài.")
            return False
        
        content = random.choice(QUOTES_VN)
        data = {
            'fb_dtsg': form['fb_dtsg'],
            'jazoest': form['jazoest'],
            'xc_message': content,
            'view_post': 'Đăng'
        }
        try:
            res = requests.post(self.base_url + form['action'], data=data, headers=self.headers)
            if res.status_code == 200 and 'login' not in res.url:
                print(f"[✓] ĐĂNG BÀI THÀNH CÔNG: {content[:30]}...")
                return True
            print("[×] Đăng bài thất bại.")
            return False
        except: return False

    def auto_add_friends(self, limit=2):
        """Tính năng kết bạn tự động từ gợi ý"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang quét gợi ý kết bạn...")
        try:
            res = requests.get(f"{self.base_url}/friends/center/suggestions/", headers=self.headers)
            links = re.findall(r'/a/mobile/friends/add_friend.php\?.*?"', res.text)
            count = 0
            for link in links:
                if count >= limit: break
                target = self.base_url + link.replace('"', '').replace('&amp;', '&')
                requests.get(target, headers=self.headers)
                print(f"[✓] Đã gửi lời mời kết bạn thứ {count+1}")
                count += 1
                time.sleep(random.randint(15, 30)) # Giãn cách an toàn
        except: print("[×] Lỗi khi kết bạn.")

def auto_pilot_mode(bot):
    os.system('clear')
    print("="*40 + "\n   CHẾ ĐỘ AUTO-PILOT ĐANG CHẠY\n" + "="*40)
    wait_min = int(input("[?] Nhập số phút chờ mỗi lần quét (30-60): "))
    last_post_date = ""
    
    while True:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        # 1. Đăng bài 1 lần mỗi ngày
        if today != last_post_date and 8 <= now.hour <= 20:
            if bot.auto_post():
                last_post_date = today
        
        # 2. Kết bạn ngẫu nhiên rải rác trong ngày
        if random.randint(1, 100) <= 25: # Xác suất 25% mỗi lần thức dậy
            bot.auto_add_friends(limit=random.randint(1, 2))
            
        print(f"[{now.strftime('%H:%M:%S')}] Chờ {wait_min} phút cho lần quét tiếp theo...")
        time.sleep(wait_min * 60)

def main():
    os.system('clear')
    print("="*40 + "\n     FB ULTIMATE INTEGRATED TOOL\n" + "="*40)
    cookie = input("[!] Nhập Cookie Facebook: ").strip()
    bot = FB_Ultimate_Tool(cookie)
    
    print("\n1. Chạy Auto-Pilot (Đăng bài + Kết bạn)")
    print("2. Chỉ Test đăng bài ngay")
    print("3. Chỉ Test kết bạn ngay")
    
    choice = input("\n[?] Lựa chọn của bạn: ")
    if choice == '1': auto_pilot_mode(bot)
    elif choice == '2': bot.auto_post()
    elif choice == '3': bot.auto_add_friends(limit=1)

if __name__ == "__main__":
    main()
        
