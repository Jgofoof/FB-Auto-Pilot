# FB Auto-Pilot Tool cho Termux

Tool nuôi nick Facebook tự động chạy trên môi trường Termux.

## Tính năng
- Kiểm tra trạng thái Cookie.
- Tự động lấy danh ngôn từ Internet và đăng bài (1 lần/ngày).
- Tự động gửi lời mời kết bạn ngẫu nhiên.
- Chế độ Auto-Pilot thông minh tránh bị Facebook quét.

## Cách cài đặt
```bash
pkg update && pkg upgrade
pkg install python git
git clone [https://github.com/Tên_Của_Bạn/FB-Auto-Pilot](https://github.com/Tên_Của_Bạn/FB-Auto-Pilot)
cd FB-Auto-Pilot
pip install -r requirements.txt
python main.py
