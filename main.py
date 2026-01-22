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
            'user-agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://mbasic.facebook.com',
            'referer': 'https://mbasic.facebook.com/',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin'
        }
        self.base_url = "https://mbasic.facebook.com"
        self.quotes = [
            "Cuộc sống không phải là chờ đợi cơn bão đi qua, mà là học cách khiêu vũ trong mưa.",
            "Mỗi ngày là một cơ hội mới để viết nên câu chuyện của riêng mình.",
            "Đừng so sánh mình với người khác, hãy so sánh mình với ngày hôm qua.",
            "Thành công không phải là chìa khóa của hạnh phúc, hạnh phúc mới là chìa khóa của thành công.",
            "Cứ hướng về phía mặt trời, bóng tối sẽ ngả về sau bạn.",
            "Sự kiên trì là con đường ngắn nhất dẫn đến thành công.",
            "Hãy sống tử tế, vì ai bạn gặp cũng đang chiến đấu một trận chiến khó khăn."
        ]

    def check_live(self):
        try:
            res = requests.get(f'{self.base_url}/profile.php', headers=self.headers, timeout=10)
            return 'logout.php' in res.text or 'mbasic_logout_button' in res.text
        except: return False

    def auto_post(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang lấy mã bảo mật để đăng bài...")
        try:
            # 1. Truy cập trang soạn thảo
            res = requests.get(f"{self.base_url}/composer/mbasic/", headers=self.headers)
            
            # 2. Sử dụng REGEX để lấy các giá trị ẩn (Thuật toán từ các tool GitHub xịn)
            fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text).group(1)
            jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text).group(1)
            target = re.search(r'action="(/composer/mbasic/.*?)"', res.text).group(1)
            
            content = random.choice(self.quotes)
            
            data = {
                'fb_dtsg': fb_dtsg,
                'jazoest': jazoest,
                'xc_message': content,
                'view_post': 'Đăng'
            }
            
            # 3. Thực hiện POST bài
            post_res = requests.post(self.base_url + target, data=data, headers=self.headers)
            
            if post_res.status_code == 200:
                print(f"[✓] ĐĂNG BÀI THÀNH CÔNG: {content[:30]}...")
                return True
            else:
                print("[×] Lỗi phản hồi từ Facebook.")
                return False
        except Exception as e:
            print(f"[!] Không lấy được form. Có thể do Token bảo mật đã bị ẩn sâu hơn. Lỗi: {e}")
            return False

    def auto_add_friends(self):
        print("[...] Đang kết bạn tự động...")
        try:
            res = requests.get(f'{self.base_url}/friends/center/suggestions/', headers=self.headers)
            # Tìm link kết bạn bằng regex
            links = re.findall(r'/a/mobile/friends/add_friend.php\?.*?"', res.text)
            if links:
                target = links[0].replace('"', '').replace('&amp;', '&')
                requests.get(self.base_url + target, headers=self.headers)
                print("[✓] Đã gửi 1 lời mời kết bạn.")
        except: pass

def auto_pilot(bot, wait_min, start_h, end_h):
    os.system('clear')
    print("="*40)
    print("   FB ULTIMATE BOT V5.0 (GITHUB HYBRID)")
    print("="*40)
    last_date = ""
    while True:
        now = datetime.now()
        if start_h <= now.hour <= end_h:
            if now.strftime("%Y-%m-%d") != last_date:
                if bot.auto_post(): last_date = now.strftime("%Y-%m-%d")
            if random.randint(1, 10) <= 3: bot.auto_add_friends()
        else:
            print(f"[{now.strftime('%H:%M')}] Đang ngoài giờ làm việc...")
        
        print(f"--- Chờ {wait_min} phút cho lần quét tới ---")
        time.sleep(wait_min * 60)

def main():
    os.system('clear')
    print("="*35)
    print("   FB AUTO TOOL V5.0 - ULTIMATE")
    print("="*35)
    cookie = input("[!] Nhập Cookie: ").strip()
    bot = FBAssistant(cookie)
    if bot.check_live():
        print("[✓] Tài khoản LIVE.")
        print("1. Chạy Auto-Pilot (Cấu hình thời gian)\n2. Test đăng bài ngay")
        choice = input("Chọn: ")
        if choice == '1':
            wait = int(input("Số phút nghỉ giữa mỗi lần: "))
            start = int(input("Giờ bắt đầu (VD: 8): "))
            end = int(input("Giờ kết thúc (VD: 22): "))
            auto_pilot(bot, wait, start, end)
        else:
            bot.auto_post()
    else:
        print("[×] Cookie DIE!")

if __name__ == "__main__":
    main()
        
