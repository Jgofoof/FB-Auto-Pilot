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
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5'
        }
        self.base_url = "https://mbasic.facebook.com"

    # --- HÀM CHECK LIVE MỚI (CHÍNH XÁC HƠN) ---
    def check_live(self):
        # Bước 1: Kiểm tra nhanh trong chuỗi cookie có ID người dùng chưa
        if 'c_user' not in self.cookie:
            return False
            
        try:
            # Bước 2: Truy cập trang chủ
            res = requests.get(f'{self.base_url}/home.php', headers=self.headers, allow_redirects=True)
            
            # Bước 3: Nếu bị chuyển hướng sang trang Login hoặc Checkpoint -> DIE
            if 'login.php' in res.url or 'checkpoint' in res.url:
                return False
            
            # Bước 4: Kiểm tra xem có khung đăng bài hoặc nút đăng xuất không -> LIVE
            if 'composer/mbasic' in res.text or 'mbasic_logout_button' in res.text:
                return True
            
            # Nếu URL vẫn là home.php hoặc profile thì coi như Live
            return True
        except:
            return False

    def get_random_quote(self):
        try:
            # Lấy câu nói từ API miễn phí
            response = requests.get("https://zenquotes.io/api/quotes")
            data = response.json()
            quote_data = random.choice(data)
            return f"{quote_data['q']} — {quote_data['a']}"
        except:
            # Dự phòng nếu mất mạng hoặc lỗi API
            return "Hôm nay là một ngày tuyệt vời để bắt đầu! #motivation"

    def auto_post(self, content):
        print(f"[...] Đang chuẩn bị đăng bài: {content[:30]}...")
        try:
            res = requests.get(self.base_url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Tìm form đăng bài
            form = soup.find('form', action=lambda x: x and '/composer/mbasic/' in x)
            if not form:
                print("[!] Không tìm thấy khung đăng bài. Có thể nick bị chặn đăng.")
                return

            action_url = self.base_url + form['action']
            data = {}
            for inp in form.find_all('input'):
                if inp.get('name'):
                    data[inp.get('name')] = inp.get('value', '')
            
            data['xc_message'] = content
            data['view_post'] = 'Đăng'
            
            requests.post(action_url, data=data, headers=self.headers)
            print(f"[✓] Đã đăng bài thành công lúc {datetime.now().strftime('%H:%M:%S')}!")
        except Exception as e:
            print(f"[×] Lỗi đăng bài: {e}")

    def auto_add_friends(self, limit=5):
        print(f"[...] Đang tìm kiếm bạn bè (Limit: {limit})...")
        try:
            res = requests.get(f'{self.base_url}/friends/center/suggestions/', headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a', text='Thêm bạn bè')
            
            if not links:
                print("[!] Không tìm thấy gợi ý kết bạn nào.")
                return

            for i, link in enumerate(links[:limit]):
                requests.get(self.base_url + link['href'], headers=self.headers)
                print(f"[✓] Đã gửi lời mời kết bạn thứ {i+1}")
                # Nghỉ ngẫu nhiên 5-10 giây giữa mỗi lần bấm
                time.sleep(random.randint(5, 10))
        except Exception as e:
            print(f"[×] Lỗi kết bạn: {e}")

def auto_pilot(bot):
    os.system('clear')
    print("="*40)
    print("   AUTO-PILOT MODE: TREO MÁY 24/7")
    print("="*40)
    print("[*] Bot sẽ tự động đăng bài 1 lần/ngày và kết bạn dạo.")
    print("[*] Nhấn Ctrl + C để dừng.\n")
    
    last_posted_date = ""

    while True:
        try:
            now = datetime.now()
            today = now.strftime("%Y-%m-%d")
            current_hour = now.hour

            # --- TÁC VỤ 1: ĐĂNG BÀI (1 lần/ngày vào 8h-20h) ---
            if today != last_posted_date:
                # Random giờ đăng bài để không bị lộ
                target_hour = random.randint(8, 20)
                
                # Nếu giờ hiện tại >= giờ mục tiêu thì đăng
                if current_hour >= target_hour:
                    quote = bot.get_random_quote()
                    bot.auto_post(quote)
                    last_posted_date = today # Đánh dấu xong nhiệm vụ hôm nay
                else:
                    print(f"[{now.strftime('%H:%M')}] Chưa tới giờ đăng bài (Dự kiến: {target_hour}h).")
            else:
                print(f"[{now.strftime('%H:%M')}] Hôm nay đã đăng bài rồi.")

            # --- TÁC VỤ 2: KẾT BẠN (Hoạt động từ 7h-22h) ---
            if 7 <= current_hour <= 22:
                # Tỷ lệ 30% sẽ đi kết bạn trong mỗi lần thức dậy
                if random.choice([True, False, False]): 
                    bot.auto_add_friends(limit=random.randint(1, 2))
                else:
                    print(f"[{now.strftime('%H:%M')}] Lần này bỏ qua kết bạn cho giống người thật.")

            # --- TÁC VỤ 3: NGỦ ĐÔNG ---
            # Ngủ ngẫu nhiên từ 30 đến 60 phút
            wait_minutes = random.randint(30, 60)
            print(f"[#] Bot đi ngủ {wait_minutes} phút...")
            time.sleep(wait_minutes * 60)
            
        except KeyboardInterrupt:
            print("\n[!] Đã dừng bot.")
            break
        except Exception as e:
            print(f"[×] Lỗi hệ thống: {e}. Thử lại sau 10 phút.")
            time.sleep(600)

def main():
    os.system('clear')
    print("="*35)
    print("    FB AUTO TOOL (FIXED LOGIN)")
    print("="*35)
    cookie = input("[!] Nhập Cookie Facebook: ")
    bot = FBAssistant(cookie)

    print("\n[?] Đang kiểm tra trạng thái Cookie...")
    if bot.check_live():
        print("[✓] Cookie LIVE! Đăng nhập thành công.")
        time.sleep(1)
        print("\n--- MENU ---")
        print("1. Chạy Auto-Pilot (Treo máy tự động)")
        print("2. Test đăng 1 bài ngay lập tức")
        print("3. Test kết bạn ngay lập tức")
        choice = input("[?] Nhập lựa chọn: ")

        if choice == '1':
            auto_pilot(bot)
        elif choice == '2':
            bot.auto_post(bot.get_random_quote())
        elif choice == '3':
            bot.auto_add_friends(limit=3)
    else:
        print("\n[×] Cookie DIE hoặc Sai định dạng!")
        print("Lưu ý: Hãy copy đầy đủ chuỗi cookie bao gồm 'c_user=...; xs=...'")

if __name__ == "__main__":
    main()
            
