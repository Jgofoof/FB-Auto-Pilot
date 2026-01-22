import requests
from bs4 import BeautifulSoup
import time
import random
import os
import xml.etree.ElementTree as ET

# --- MÀU SẮC ---
R = '\033[1;91m' # Đỏ
G = '\033[1;92m' # Xanh lá
Y = '\033[1;93m' # Vàng
C = '\033[1;96m' # Xanh dương
W = '\033[1;97m' # Trắng

class FBProTool:
    def __init__(self):
        self.base_url = "https://mbasic.facebook.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Nokia 2.4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'upgrade-insecure-requests': '1'
        }
        self.session = requests.Session()
        self.cookie = ""

    def clear(self):
        os.system('clear')

    def logo(self):
        print(f"""{C}
    ╔══════════════════════════════════════╗
    ║      TOOL FB PRO - CRAWL & SHARE     ║
    ║      Chức năng: Lấy tin mạng & Share ║
    ╚══════════════════════════════════════╝
        {W}""")

    def login(self):
        self.clear()
        self.logo()
        # Kiểm tra file cookie cũ
        if os.path.exists("cookie.txt"):
            use_old = input(f"{Y}Tìm thấy cookie cũ, dùng lại không? (y/n): {W}")
            if use_old.lower() == 'y':
                with open("cookie.txt", "r") as f:
                    self.cookie = f.read().strip()
            else:
                self.cookie = input(f"{G}Nhập Cookie FB mới: {W}")
        else:
            self.cookie = input(f"{G}Nhập Cookie FB: {W}")
        
        # Lưu cookie
        with open("cookie.txt", "w") as f:
            f.write(self.cookie)

        self.headers.update({'Cookie': self.cookie})
        
        try:
            resp = self.session.get(self.base_url + "/me", headers=self.headers)
            if "mbasic_logout_button" in resp.text:
                soup = BeautifulSoup(resp.text, 'html.parser')
                name = soup.title.string if soup.title else "Unknown"
                print(f"{G}[SUCCESS] Login thành công: {name}{W}")
                time.sleep(1)
                return True
            else:
                print(f"{R}[DIE] Cookie hỏng! Hãy lấy cookie mới.{W}")
                os.remove("cookie.txt")
                return False
        except Exception as e:
            print(f"{R}[ERROR] Lỗi mạng: {e}{W}")
            return False

    def get_fb_dtsg(self):
        try:
            resp = self.session.get(self.base_url, headers=self.headers)
            soup = BeautifulSoup(resp.text, 'html.parser')
            fb_dtsg = soup.find('input', {'name': 'fb_dtsg'})['value']
            jazoest = soup.find('input', {'name': 'jazoest'})['value']
            return fb_dtsg, jazoest
        except:
            return None, None

    # --- CHỨC NĂNG 1: LẤY NỘI DUNG TỪ MẠNG ---
    def crawl_content(self):
        """Lấy tiêu đề tin tức từ VnExpress RSS hoặc Quote"""
        sources = [
            "https://vnexpress.net/rss/tin-moi-nhat.rss",
            "https://vnexpress.net/rss/tam-su.rss",
            "https://vnexpress.net/rss/cuoi.rss"
        ]
        
        print(f"{Y}[INFO] Đang tìm kiếm nội dung hay trên mạng...{W}")
        news_list = []
        
        try:
            # Chọn random 1 nguồn
            src = random.choice(sources)
            resp = requests.get(src)
            # Parse XML RSS
            root = ET.fromstring(resp.content)
            
            for item in root.findall('./channel/item'):
                title = item.find('title').text
                desc = item.find('description').text
                # Làm sạch description (thường chứa HTML)
                clean_desc = BeautifulSoup(desc, "html.parser").text
                
                # Tạo nội dung post
                full_post = f"{title}\n\n{clean_desc}\n(Nguồn: VnExpress)"
                news_list.append(full_post)
            
            if len(news_list) > 0:
                return random.choice(news_list)
            return "Hôm nay trời đẹp quá! Chúc mọi người vui vẻ."
            
        except Exception as e:
            print(f"{R}Lỗi lấy tin: {e}. Dùng caption mặc định.{W}")
            return "Cuộc sống thật thú vị! #HelloFacebook"

    def auto_crawl_and_post(self):
        so_luong = int(input(f"{C}Số lượng bài muốn đăng: {W}"))
        delay = int(input(f"{C}Thời gian nghỉ (giây): {W}"))

        for i in range(so_luong):
            # 1. Tự động lấy nội dung
            content = self.crawl_content()
            print(f"{C}--> Nội dung tìm được: {content[:30]}...{W}")

            # 2. Đăng bài
            try:
                fb_dtsg, jazoest = self.get_fb_dtsg()
                if not fb_dtsg: break

                resp_home = self.session.get(self.base_url, headers=self.headers)
                soup = BeautifulSoup(resp_home.text, 'html.parser')
                form = soup.find('form', {'action': lambda x: x and '/composer/mbasic/' in x})

                if form:
                    action_url = self.base_url + form['action']
                    data = {
                        'fb_dtsg': fb_dtsg,
                        'jazoest': jazoest,
                        'xc_message': content,
                        'view_post': 'Đăng'
                    }
                    p = self.session.post(action_url, headers=self.headers, data=data)
                    if p.status_code == 200:
                        print(f"{G}[{i+1}] Đăng thành công!{W}")
                    else:
                        print(f"{R}Lỗi đăng bài.{W}")
                
                time.sleep(delay)
            except Exception as e:
                print(f"{R}Lỗi: {e}{W}")

    # --- CHỨC NĂNG 2: AUTO SHARE ---
    def auto_share(self):
        """Tìm bài trên newsfeed và share về tường"""
        print(f"{Y}[WARN] Tính năng Share dễ bị Checkpoint. Để delay cao!{W}")
        so_luong = int(input(f"{C}Số lượng bài muốn share: {W}"))
        delay = int(input(f"{C}Thời gian nghỉ (giây): {W}"))

        count = 0
        while count < so_luong:
            try:
                # 1. Lướt newfeed
                resp = self.session.get(self.base_url, headers=self.headers)
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # 2. Tìm các link "Chia sẻ" (Share)
                # Trên mbasic nút share thường có dạng: /composer/mbasic/?c_src=share&...
                links = soup.find_all('a', href=True)
                share_links = [l['href'] for l in links if 'c_src=share' in l['href'] or 'sharer.php' in l['href']]

                if not share_links:
                    print(f"{Y}Không thấy nút share nào, đang tải lại feed...{W}")
                    time.sleep(2)
                    continue

                # 3. Thực hiện share
                for link in share_links:
                    if count >= so_luong: break
                    
                    # Vào trang xác nhận share
                    full_url = link if "http" in link else self.base_url + link
                    resp_share = self.session.get(full_url, headers=self.headers)
                    soup_share = BeautifulSoup(resp_share.text, 'html.parser')
                    
                    # Tìm form submit share
                    form = soup_share.find('form')
                    if form:
                        action = self.base_url + form['action']
                        inputs = form.find_all('input')
                        data = {}
                        for inp in inputs:
                            data[inp.get('name')] = inp.get('value')
                        
                        # Thêm caption cho bài share (tùy chọn)
                        data['view_post'] = 'Chia sẻ' 
                        
                        self.session.post(action, headers=self.headers, data=data)
                        count += 1
                        print(f"{G}[{count}] Đã chia sẻ 1 bài viết về tường!{W}")
                        time.sleep(delay)
                    else:
                        print(f"{R}Không share được bài này.{W}")

            except Exception as e:
                print(f"{R}Lỗi khi share: {e}{W}")
                time.sleep(5)

    def main(self):
        if self.login():
            while True:
                self.clear()
                self.logo()
                print(f"{Y}1. Auto Tìm tin trên mạng & Đăng bài")
                print(f"{Y}2. Auto Share bài viết trên Newsfeed")
                print(f"{Y}0. Thoát")
                choice = input(f"{C}Chọn: {W}")

                if choice == '1':
                    self.auto_crawl_and_post()
                elif choice == '2':
                    self.auto_share()
                elif choice == '0':
                    break
                else:
                    print("Sai lựa chọn.")
                
                input(f"\n{Y}Enter để quay lại...{W}")

if __name__ == "__main__":
    try:
        app = FBProTool()
        app.main()
    except KeyboardInterrupt:
        pass
                
