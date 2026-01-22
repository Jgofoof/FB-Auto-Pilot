import requests
from bs4 import BeautifulSoup
import time
import os
import random
from datetime import datetime

# ================= CẤU HÌNH (BẠN CHỈNH Ở ĐÂY) =================
# Khung giờ được phép đăng bài (Ví dụ: từ 7h sáng đến 22h đêm)
GIO_BAT_DAU = 7
GIO_KET_THUC = 22

# Số lần kết bạn tối đa trong một ngày
MAX_ADD_FRIEND = 5

# Kho nội dung tiếng Việt (Bạn có thể thêm tùy ý)
DANH_NGON_VN = [
    "Không có gì quý hơn độc lập tự do.",
    "Muốn đi nhanh hãy đi một mình, muốn đi xa hãy đi cùng nhau.",
    "Hạnh phúc không phải là đích đến, mà là hành trình chúng ta đang đi.",
    "Đừng cúi đầu, vương miện sẽ rơi. Hãy ngẩng cao đầu và bước tiếp.",
    "Thất bại là mẹ thành công.",
    "Sống là phải biết cho đi, đâu chỉ nhận riêng mình.",
    "Cảm ơn đời mỗi sớm mai thức dậy, ta có thêm ngày nữa để yêu thương.",
    "Kiên nhẫn là cây đắng nhưng quả của nó lại rất ngọt.",
    "Hãy sống như một đóa hoa, vươn mình tỏa ngát hương thơm.",
    "Đừng đợi may mắn, hãy tự tạo ra cơ hội cho chính mình.",
    "Cười nhiều lên, may mắn tự nhiên sẽ đến!",
    "Chỉ cần bản thân cố gắng, trời xanh sẽ an bài.",
    "Bình yên là khi lòng không chứa chấp muộn phiền.",
]

# ================= CODE XỬ LÝ (KHÔNG CẦN SỬA) =================

class FBAssistant:
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.base_url = "https://mbasic.facebook.com"

    def check_live(self):
        if 'c_user' not in self.cookie: return False
        try:
            res = requests.get(f'{self.base_url}/home.php', headers=self.headers, allow_redirects=True)
            if 'login.php' in res.url or 'checkpoint' in res.url: return False
            return True
        except: return False

    def get_vietnamese_quote(self):
        # Lấy ngẫu nhiên 1 câu từ danh sách trên
        return random.choice(DANH_NGON_VN)

    def auto_post(self, content):
        print(f"[...] Đang tìm nơi đăng bài...")
        try:
            res = requests.get(self.base_url, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # --- THUẬT TOÁN TÌM FORM MỚI (FIX LỖI) ---
            # Cách 1: Tìm form có chứa input nhập liệu (xc_message)
            form = None
            target_input = soup.find('input', {'name': 'xc_message'})
            
            if target_input:
                form = target_input.find_parent('form')
            else:
                # Cách 2: Nếu không thấy input, tìm link "Đăng status" để click vào
                print("[!] Không thấy khung ở trang chủ, đang tìm nút chuyển hướng...")
                composer_link = soup.find('a', href=lambda x: x and '/composer/' in x)
                if composer_link:
                    # Vào trang soạn thảo riêng
                    res = requests.get(self.base_url + composer_link['href'], headers=self.headers)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    target_input = soup.find('input', {'name': 'xc_message'})
                    if target_input:
                        form = target_input.find_parent('form')

            if not form:
                print("[!] Bó tay: Không tìm thấy khung đăng bài (Có thể nick bị chặn đăng).")
                return

            # Lấy URL xử lý form
            action_url = self.base_url + form.get('action', '')
            
            # Lấy tất cả dữ liệu ẩn cần thiết (fb_dtsg, jazoest...)
            data = {}
            for inp in form.find_all('input'):
                if inp.get('name'):
                    data[inp.get('name')] = inp.get('value', '')
            
            # Chèn nội dung của mình vào
            data['xc_message'] = content
            data['view_post'] = 'Đăng'
            
            # Gửi bài
            post_req = requests.post(action_url, data=data, headers=self.headers)
            
            if post_req.status_code == 200:
                print(f"[✓] ĐĂNG BÀI THÀNH CÔNG: \"{content[:30]}...\"")
            else:
                print(f"[×] Đăng thất bại. Mã lỗi: {post_req.status_code}")

        except Exception as e:
            print(f"[×] Lỗi code đăng bài: {e}")

    def auto_add_friends(self, limit=3):
        print(f"[...] Đang quét gợi ý kết bạn...")
        try:
            res = requests.get(f'{self.base_url}/friends/center/suggestions/', headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a', href=lambda x: x and 'confirm=' in x) # Tìm link chứa 'confirm=' là nút kết bạn
            
            if not links:
                print("[!] Không có gợi ý kết bạn nào.")
                return

            count = 0
            for link in links:
                if count >= limit: break
                requests.get(self.base_url + link['href'], headers=self.headers)
                print(f"[✓] Đã gửi lời mời tới 1 người bạn mới.")
                count += 1
                time.sleep(random.randint(5, 10))
        except Exception as e:
            print(f"[×] Lỗi kết bạn: {e}")

def auto_pilot(bot):
    os.system('clear')
    print("="*40)
    print("   AUTO-PILOT: TREO MÁY NUÔI NICK VIỆT")
    print("="*40)
    print(f"[*] Cấu hình: Hoạt động từ {GIO_BAT_DAU}h - {GIO_KET_THUC}h")
    print("[*] Nhấn Ctrl + C để dừng.\n")
    
    last_posted_date = ""

    while True:
        try:
            now = datetime.now()
            today = now.strftime("%Y-%m-%d")
            h = now.hour

            # 1. KIỂM TRA GIỜ HOẠT ĐỘNG
            if GIO_BAT_DAU <= h <= GIO_KET_THUC:
                
                # --- NHIỆM VỤ ĐĂNG BÀI (1 ngày 1 lần) ---
                if today != last_posted_date:
                    # Chọn giờ đẹp ngẫu nhiên trong khoảng hoạt động
                    gio_vang = random.randint(GIO_BAT_DAU, GIO_KET_THUC)
                    
                    if h >= gio_vang:
                        print(f"\n[{now.strftime('%H:%M')}] >> Tới giờ đăng bài!")
                        content = bot.get_vietnamese_quote()
                        bot.auto_post(content)
                        last_posted_date = today
                    else:
                        print(f"[{now.strftime('%H:%M')}] Chưa tới giờ đăng bài (Dự kiến: {gio_vang}h).")
                else:
                    print(f"[{now.strftime('%H:%M')}] Hôm nay đã hoàn thành chỉ tiêu đăng bài.")

                # --- NHIỆM VỤ KẾT BẠN (Rải rác) ---
                # Random xác suất 20% mỗi lần thức dậy sẽ đi kết bạn
                if random.randint(1, 10) <= 2:
                    print(f"[{now.strftime('%H:%M')}] >> Rảnh rỗi, đi tìm bạn bè...")
                    bot.auto_add_friends(limit=random.randint(1, 2))

            else:
                print(f"[{now.strftime('%H:%M')}] Ngoài giờ hoạt động. Bot đang ngủ đông.")

            # --- NGHỈ NGƠI ---
            wait_min = random.randint(45, 90) # Nghỉ lâu hơn (45-90 phút) để an toàn
            print(f"[#] Nghỉ {wait_min} phút...")
            time.sleep(wait_min * 60)

        except KeyboardInterrupt:
            print("\n[!] Dừng Tool.")
            break
        except Exception as e:
            print(f"[×] Lỗi mạng/Hệ thống: {e}. Thử lại sau 10p.")
            time.sleep(600)

def main():
    os.system('clear')
    print("="*35)
    print("    TOOL NUÔI FB - PHIÊN BẢN 3.0")
    print("="*35)
    
    # Đoạn này để fix lỗi nhập cookie bị dính ký tự xuống dòng
    cookie_raw = input("[!] Nhập Cookie Facebook: ")
    cookie = cookie_raw.replace("\n", "").strip()
    
    bot = FBAssistant(cookie)

    print("\n[?] Đang kiểm tra Cookie...")
    if bot.check_live():
        print(f"[✓] Đăng nhập thành công! (Giờ hệ thống: {datetime.now().hour}h)")
        print("\n1. Treo máy tự động (Auto-Pilot)")
        print("2. Test đăng 1 status Tiếng Việt ngay")
        
        choice = input("[?] Chọn: ")
        if choice == '1':
            auto_pilot(bot)
        elif choice == '2':
            content = bot.get_vietnamese_quote()
            print(f"[i] Nội dung sẽ đăng: {content}")
            bot.auto_post(content)
    else:
        print("\n[×] Cookie lỗi! Hãy lấy lại cookie mới.")

if __name__ == "__main__":
    main()
            
