import requests
from bs4 import BeautifulSoup
import time
import os
import random
from datetime import datetime

# ================= CẤU HÌNH NỘI DUNG =================
DANH_NGON_VN = [
    "Hạnh phúc là một hành trình, không phải là đích đến.",
    "Chỉ cần bạn không dừng lại, việc bạn đi chậm thế nào không quan trọng.",
    "Mọi khó khăn rồi sẽ qua đi, giống như cơn mưa ngoài cửa sổ.",
    "Hãy sống như một đóa hoa, tự tin tỏa hương dù thế nào đi nữa.",
    "Thành công là tên gọi khác của sự nỗ lực.",
    "Ngày mới tốt lành và tràn đầy năng lượng nhé cả nhà!",
    "Bình yên nằm ở tâm hồn, không phải ở thế giới bên ngoài.",
    "Cố gắng thêm một chút, thành công sẽ ở ngay trước mắt.",
    "Đừng để ngày hôm qua chiếm dụng quá nhiều thời gian của ngày hôm nay."
]

class FBAssistant:
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.base_url = "https://mbasic.facebook.com"

    def check_live(self):
        try:
            res = requests.get(f'{self.base_url}/home.php', headers=self.headers, allow_redirects=True)
            if 'login.php' in res.url or 'checkpoint' in res.url: return False
            return True
        except: return False

    def auto_post(self, content):
        print(f"[...] Đang truy cập trình soạn thảo bài viết...")
        try:
            # Truy cập thẳng vào URL soạn thảo để tránh lỗi không tìm thấy khung ở trang chủ
            res = requests.get(f"{self.base_url}/composer/mbasic/", headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Tìm form đăng bài
            form = soup.find('form', action=lambda x: x and '/composer/mbasic/' in x)
            if not form:
                print("[!] LỖI: Vẫn không tìm thấy form đăng bài. Nick có thể bị chặn tính năng hoặc giao diện bị đổi.")
                return False

            action_url = self.base_url + form['action']
            data = {}
            # Lấy tất cả input hidden (fb_dtsg, jazoest, ...)
            for inp in form.find_all('input'):
                name = inp.get('name')
                value = inp.get('value', '')
                if name:
                    data[name] = value
            
            # Ghi đè nội dung bài viết
            data['xc_message'] = content
            data['view_post'] = 'Đăng'
            
            # Gửi bài
            response = requests.post(action_url, data=data, headers=self.headers)
            
            if response.status_code == 200 and 'composer/mbasic' not in response.url:
                print(f"[✓] ĐĂNG BÀI THÀNH CÔNG: {content[:30]}...")
                return True
            else:
                print("[×] Đăng bài thất bại. Có thể do nội dung trùng lặp hoặc bị chặn.")
                return False
        except Exception as e:
            print(f"[×] Lỗi kết nối: {e}")
            return False

    def auto_add_friends(self, limit=2):
        print(f"[...] Đang tìm kiếm bạn bè...")
        try:
            res = requests.get(f'{self.base_url}/friends/center/suggestions/', headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a', href=lambda x: x and 'confirm=' in x)
            
            count = 0
            for link in links:
                if count >= limit: break
                requests.get(self.base_url + link['href'], headers=self.headers)
                print(f"[✓] Đã gửi 1 lời mời kết bạn.")
                count += 1
                time.sleep(random.randint(10, 20))
        except:
            print("[×] Không thể kết bạn lúc này.")

def auto_pilot(bot, wait_min, start_h, end_h):
    os.system('clear')
    print("="*40)
    print("   FB AUTO-PILOT V4.0 (SUPER FIX)")
    print("="*40)
    print(f"[*] Hoạt động: {start_h}h - {end_h}h")
    print(f"[*] Chờ giữa các lần quét: {wait_min} phút")
    
    last_posted_date = ""

    while True:
        now = datetime.now()
        h = now.hour
        today = now.strftime("%Y-%m-%d")

        if start_h <= h <= end_h:
            # Đăng bài 1 lần/ngày
            if today != last_posted_date:
                content = random.choice(DANH_NGON_VN)
                success = bot.auto_post(content)
                if success:
                    last_posted_date = today
            
            # Kết bạn (xác suất 30%)
            if random.randint(1, 100) <= 30:
                bot.auto_add_friends(limit=random.randint(1, 2))
        else:
            print(f"[{now.strftime('%H:%M')}] Đang ngoài giờ hoạt động. Bot nghỉ ngơi...")

        print(f"[{now.strftime('%H:%M')}] Chờ {wait_min} phút cho lần quét tới...")
        time.sleep(wait_min * 60)

def main():
    os.system('clear')
    print("="*35)
    print("   TOOL FB - PHIÊN BẢN V4.0")
    print("="*35)
    
    cookie = input("[!] Nhập Cookie Facebook: ").strip()
    bot = FBAssistant(cookie)

    if bot.check_live():
        print(f"[✓] Login thành công!")
        print("\n1. Chạy Auto-Pilot (Hẹn giờ)")
        print("2. Test đăng bài ngay lập tức")
        
        choice = input("[?] Chọn: ")
        
        if choice == '1':
            wait_min = int(input("[?] Số phút chờ giữa mỗi lần quét (nên để 30-60): "))
            start_h = int(input("[?] Giờ bắt đầu (0-23): "))
            end_h = int(input("[?] Giờ kết thúc (0-23): "))
            auto_pilot(bot, wait_min, start_h, end_h)
        elif choice == '2':
            bot.auto_post(random.choice(DANH_NGON_VN))
    else:
        print("[×] Cookie Die hoặc sai định dạng.")

if __name__ == "__main__":
    main()
            
