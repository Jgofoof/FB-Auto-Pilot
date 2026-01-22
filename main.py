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
            'user-agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'accept-language': 'vi-VN,vi;q=0.9',
            'referer': 'https://mbasic.facebook.com/',
        }
        self.base_url = "https://mbasic.facebook.com"
        self.quotes = ["Chúc mọi người một ngày tốt lành!", "Cố gắng mỗi ngày, thành công sẽ đến.", "Bình yên là ở trong tâm."]

    def get_token_securely(self):
        """Thuật toán tìm Token đa điểm (Fix lỗi NoneType)"""
        try:
            res = requests.get(f"{self.base_url}/composer/mbasic/", headers=self.headers, timeout=15)
            # Tìm fb_dtsg bằng nhiều mẫu Regex khác nhau
            fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text) or \
                      re.search(r'\"fb_dtsg\":\"(.*?)\"', res.text)
            
            jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text) or \
                      re.search(r'\"jazoest\":\"(.*?)\"', res.text)
            
            action = re.search(r'action="(/composer/mbasic/.*?)"', res.text)

            if fb_dtsg and jazoest and action:
                return {
                    'fb_dtsg': fb_dtsg.group(1),
                    'jazoest': jazoest.group(1),
                    'action': action.group(1).replace('&amp;', '&')
                }
            return None
        except: return None

    def auto_post(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang quét mã bảo mật...")
        token_data = self.get_token_securely()
        
        if not token_data:
            print("[×] Lỗi: Không thể lấy mã bảo mật. Hãy thử Like 1 bài trên trình duyệt rồi lấy lại Cookie.")
            return False

        try:
            content = random.choice(self.quotes)
            data = {
                'fb_dtsg': token_data['fb_dtsg'],
                'jazoest': token_data['jazoest'],
                'xc_message': content,
                'view_post': 'Đăng'
            }
            res = requests.post(self.base_url + token_data['action'], data=data, headers=self.headers)
            
            if res.status_code == 200 and 'login.php' not in res.url:
                print(f"[✓] ĐĂNG BÀI THÀNH CÔNG: {content}")
                return True
            else:
                print("[×] Đăng bài thất bại. Có thể do nick bị hạn chế.")
                return False
        except Exception as e:
            print(f"[!] Lỗi kết nối: {e}")
            return False

def main():
    os.system('clear')
    print("="*35 + "\n    FB AUTO TOOL V8.0 (FIX ERROR)\n" + "="*35)
    cookie = input("[!] Nhập Cookie: ").strip()
    bot = FBAssistant(cookie)
    
    print("\n1. Test Đăng bài ngay\n2. Chạy Auto-Pilot")
    choice = input("Chọn: ")
    if choice == '1': bot.auto_post()
    # (Tương tự cho các menu khác...)

if __name__ == "__main__":
    main()
    
