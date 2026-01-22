import requests
import re
import time
import os
import random
from datetime import datetime

class FBAssistant:
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'accept-language': 'vi-VN,vi;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'referer': 'https://mbasic.facebook.com/',
        }
        self.base_url = "https://mbasic.facebook.com"
        self.quotes = [
            "Mọi thứ tốt đẹp đều cần thời gian. Cố gắng lên!",
            "Hãy sống là chính mình, bình thường nhưng không tầm thường.",
            "Nụ cười là khoảng cách ngắn nhất giữa hai tâm hồn.",
            "Lao động là vinh quang, nỗ lực là thành công.",
            "Hãy tận hưởng những điều nhỏ bé trong cuộc sống."
        ]

    def check_live(self):
        try:
            res = requests.get(f'{self.base_url}/profile.php', headers=self.headers, timeout=10)
            if 'logout.php' in res.text or 'mbasic_logout_button' in res.text:
                return True
            return False
        except: return False

    def auto_post_github_algo(self):
        """Thuật toán đăng bài chuyên sâu từ GitHub"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang trích xuất dữ liệu đăng bài...")
        try:
            # Bước 1: Lấy form và mã bảo mật
            res = requests.get(f"{self.base_url}/composer/mbasic/", headers=self.headers)
            
            # Thuật toán Regex lấy fb_dtsg và jazoest (Standard GitHub Algo)
            fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text).group(1)
            jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text).group(1)
            # Lấy URL hành động từ form
            action_raw = re.search(r'action="(/composer/mbasic/.*?)"', res.text).group(1)
            action_url = self.base_url + action_raw.replace('&amp;', '&')
            
            content = random.choice(self.quotes)
            data = {
                'fb_dtsg': fb_dtsg,
                'jazoest': jazoest,
                'xc_message': content,
                'view_post': 'Đăng'
            }
            
            # Bước 2: Gửi Request POST với full Header giả lập
            post_res = requests.post(action_url, data=data, headers=self.headers)
            
            # Kiểm tra xem có bị đá về trang login không
            if post_res.status_code == 200 and 'login.php' not in post_res.url:
                print(f"[✓] ĐĂNG BÀI THÀNH CÔNG: {content[:30]}...")
                return True
            else:
                print("[×] Đăng bài thất bại. Có thể do Token hết hạn hoặc bị chặn tính năng.")
                return False
        except Exception as e:
            print(f"[!] Lỗi trích xuất: {e}")
            return False

    def auto_add_friends_algo(self, limit=2):
        print("[...] Đang quét danh sách kết bạn...")
        try:
            res = requests.get(f'{self.base_url}/friends/center/suggestions/', headers=self.headers)
            # Thuật toán tìm link add friend ẩn
            add_links = re.findall(r'/a/mobile/friends/add_friend.php\?.*?"', res.text)
            count = 0
            for link in add_links:
                if count >= limit: break
                clean_link = self.base_url + link.replace('"', '').replace('&amp;', '&')
                requests.get(clean_link, headers=self.headers)
                print(f"[✓] Đã gửi lời mời thứ {count+1}")
                count += 1
                time.sleep(random.randint(10, 20))
        except: print("[×] Lỗi kết bạn.")

def auto_pilot_mode(bot):
    os.system('clear')
    print("="*40)
    print("   FB HYBRID BOT - AUTO PILOT V7.0")
    print("="*40)
    wait_min = int(input("[?] Nhập số phút chờ mỗi lần quét: "))
    
    last_post_date = ""
    while True:
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        # 1 lần đăng bài mỗi ngày
        if today != last_post_date:
            if bot.auto_post_github_algo():
                last_post_date = today
        
        # Kết bạn ngẫu nhiên
        if random.randint(1, 10) <= 3:
            bot.auto_add_friends_algo()
            
        print(f"[{now.strftime('%H:%M:%S')}] Chờ {wait_min} phút...")
        time.sleep(wait_min * 60)

def main():
    os.system('clear')
    print("="*35)
    print("  FB GITHUB HYBRID V7.0")
    print("="*35)
    cookie = input("[!] Nhập Cookie: ").strip()
    bot = FBAssistant(cookie)
    
    # Ép vào menu bất kể trạng thái check_live
    print("\n1. Test Đăng bài ngay (GitHub Algo)")
    print("2. Chạy Auto-Pilot (Hẹn giờ)")
    choice = input("Chọn: ")
    
    if choice == '1':
        bot.auto_post_github_algo()
    elif choice == '2':
        auto_pilot_mode(bot)

if __name__ == "__main__":
    main()
            
