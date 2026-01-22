import requests, re, time, os, random
from datetime import datetime

# ================= CẤU HÌNH NÂNG CAO =================
GIO_HOAT_DONG = (7, 22) # Từ 7h sáng đến 10h tối
DELAY_QUET = 45 # Phút chờ giữa mỗi chu kỳ
DANH_NGON = [
    "Hạnh phúc là hành trình, không phải đích đến.",
    "Mỗi ngày là một cơ hội mới.",
    "Sống tử tế, trời xanh tự an bài.",
    "Thành công đến từ sự kiên trì.",
    "Bình yên là tài sản vô giá."
]

class FB_Master_Tool:
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
            'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8',
            'referer': 'https://mbasic.facebook.com/'
        }
        self.base_url = "https://mbasic.facebook.com"

    def get_token(self, path):
        """Thuật toán GitHub trích xuất token bảo mật"""
        try:
            res = requests.get(self.base_url + path, headers=self.headers, timeout=15)
            fb_dtsg = re.search(r'name="fb_dtsg" value="(.*?)"', res.text).group(1)
            jazoest = re.search(r'name="jazoest" value="(.*?)"', res.text).group(1)
            action = re.search(r'action="(/.*?)"', res.text).group(1).replace('&amp;', '&')
            return {'fb_dtsg': fb_dtsg, 'jazoest': jazoest, 'action': action, 'text': res.text}
        except: return None

    def interact_newsfeed(self):
        """Tự động Like bài trên Newsfeed (Tăng Trust)"""
        print("[>] Đang tương tác Newsfeed...")
        try:
            res = requests.get(self.base_url, headers=self.headers)
            links = re.findall(r'/a/like.php\?.*?"', res.text)
            for link in links[:3]: # Like 3 bài đầu tiên
                requests.get(self.base_url + link.replace('"', '').replace('&amp;', '&'), headers=self.headers)
                print("   [✓] Đã thả like 1 bài viết.")
                time.sleep(random.randint(5, 10))
        except: pass

    def post_status(self):
        """Đăng bài tự động"""
        print("[>] Đang tiến hành đăng bài...")
        form = self.get_token("/composer/mbasic/")
        if form:
            data = {'fb_dtsg': form['fb_dtsg'], 'jazoest': form['jazoest'], 
                    'xc_message': random.choice(DANH_NGON), 'view_post': 'Đăng'}
            requests.post(self.base_url + form['action'], data=data, headers=self.headers)
            print("   [✓] Đăng bài hoàn tất.")

    def add_friends(self):
        """Kết bạn gợi ý"""
        print("[>] Đang tìm bạn mới...")
        try:
            res = requests.get(self.base_url + "/friends/center/suggestions/", headers=self.headers)
            links = re.findall(r'/a/mobile/friends/add_friend.php\?.*?"', res.text)
            if links:
                requests.get(self.base_url + links[0].replace('"', '').replace('&amp;', '&'), headers=self.headers)
                print("   [✓] Đã gửi lời mời kết bạn.")
        except: pass

def run_auto_pilot(bot):
    os.system('clear')
    print("="*40 + "\n   HỆ THỐNG NUÔI FB CHUYÊN NGHIỆP V10\n" + "="*40)
    last_post = ""
    while True:
        now = datetime.now()
        if GIO_HOAT_DONG[0] <= now.hour <= GIO_HOAT_DONG[1]:
            print(f"[{now.strftime('%H:%M:%S')}] Bắt đầu chu kỳ tương tác...")
            bot.interact_newsfeed()
            if now.strftime("%Y-%m-%d") != last_post:
                bot.post_status()
                last_post = now.strftime("%Y-%m-%d")
            bot.add_friends()
            print(f"--- Hoàn thành. Nghỉ {DELAY_QUET} phút ---")
        else:
            print(f"[{now.strftime('%H:%M:%S')}] Đang trong giờ nghỉ...")
        time.sleep(DELAY_QUET * 60)

if __name__ == "__main__":
    cookie = input("Nhập Cookie FB: ").strip()
    bot = FB_Master_Tool(cookie)
    run_auto_pilot(bot)
                               
