# NPM Proxy & Cloudflare DNS Update Service

Dự án này tự động hóa quá trình cập nhật các bản ghi DNS của Cloudflare dựa trên các thay đổi của proxy host từ NPM (Nginx Proxy Manager). Nó sử dụng một script Python để lấy thông tin proxy host từ NPM và sau đó tạo hoặc xóa các bản ghi CNAME của Cloudflare tương ứng. Script này được cài đặt dưới dạng dịch vụ systemd chạy mỗi 5 giây.

## Tính năng

- **Cập nhật tự động:**  
  Tự động kiểm tra các thay đổi trong proxy host của NPM và cập nhật các bản ghi DNS của Cloudflare.
- **Tích hợp Systemd:**  
  Chạy dưới dạng dịch vụ systemd với một bộ hẹn giờ thực thi script cập nhật mỗi 5 giây.
- **Cài đặt tương tác:**  
  Script cài đặt sẽ yêu cầu nhập tất cả các giá trị cấu hình cần thiết.
- **Gỡ cài đặt dễ dàng:**  
  Script gỡ cài đặt sẽ xóa tất cả các file được tạo ra và vô hiệu hóa các dịch vụ.

## Cấu trúc thư mục

```plaintext
npm-proxy-cloudflare/
├── listhostpython.py      # Script Python chính (đọc cấu hình từ config.py)
├── install.sh             # Script cài đặt để cấu hình và cài đặt dịch vụ
├── uninstall.sh           # Script gỡ cài đặt để xóa dịch vụ và cấu hình
└── README.md              # Tệp tài liệu này
```

## Yêu cầu
- **Ubuntu (hoặc một bản phân phối Linux hỗ trợ systemd khác)**
- **Python 3 và pip3**
- **Thư viện requests của Python (được cài đặt qua pip)**

## Cài đặt
Bạn có thể cài đặt dự án chỉ với một lệnh bằng cách sao chép kho lưu trữ và chạy script cài đặt. Ví dụ:
```bash
curl -sSL https://github.com/Hungdiec/autodns/archive/refs/heads/main.tar.gz | tar -xz && cd autodns-main && sudo bash ./install.sh
```

## Những gì Script Cài đặt Thực hiện
- **Cài đặt các phụ thuộc:**  
  Cập nhật danh sách gói và cài đặt Python3, pip3, và thư viện requests.
- **Yêu cầu cấu hình:**  
  Yêu cầu bạn nhập URL API NPM, tên người dùng, mật khẩu, token API Cloudflare, Zone ID, và địa chỉ IP/tên máy chủ.
- **Tạo tệp cấu hình:**  
  Ghi các giá trị cấu hình của bạn vào tệp config.py.
- **Thiết lập dịch vụ và bộ hẹn giờ của Systemd:**  
  Tạo và cài đặt các tệp dịch vụ systemd (npm_proxy_update.service) và bộ hẹn giờ (npm_proxy_update.timer). Dịch vụ sẽ chạy script cập nhật mỗi 5 giây.
- **Kích hoạt và khởi động bộ hẹn giờ:**  
  Tải lại daemon systemd, kích hoạt và khởi động bộ hẹn giờ để quá trình cập nhật bắt đầu tự động.

## Cấu hình
**Trong quá trình cài đặt, bạn sẽ được yêu cầu nhập các giá trị cấu hình sau:**

- **URL API NPM: [http://ipadress:81/api]**
- **Người dùng API NPM: [email đăng nhập npm]**
- **Mật khẩu API NPM: [mật khẩu đăng nhập]**
- **Token API Cloudflare:**
- **Zone ID Cloudflare:**
- **Địa chỉ IP hoặc Tên máy chủ:**
- **Các giá trị này được lưu trong tệp config.py (được tạo ra trong quá trình cài đặt) và được sử dụng bởi listhostpython.py.**

## Chạy Dịch vụ
Sau khi cài đặt, bộ hẹn giờ của systemd sẽ tự động kích hoạt dịch vụ mỗi 5 giây. Để kiểm tra trạng thái của bộ hẹn giờ hoặc dịch vụ, hãy sử dụng các lệnh sau:
```bash
# Kiểm tra trạng thái bộ hẹn giờ
sudo systemctl status npm_proxy_update.timer

# Kiểm tra trạng thái dịch vụ (sau khi chạy)
sudo systemctl status npm_proxy_update.service

# Xem nhật ký của dịch vụ
sudo journalctl -u npm_proxy_update.service -f
```

## Gỡ cài đặt
Để gỡ cài đặt dịch vụ và xóa tệp cấu hình được tạo ra, hãy chạy script gỡ cài đặt được cung cấp:
```bash
sudo bash uninstall.sh
```
Script gỡ cài đặt sẽ:
- Dừng và vô hiệu hóa bộ hẹn giờ và dịch vụ của systemd.
- Xóa các tệp đơn vị systemd khỏi `/etc/systemd/system/`.
- Tải lại daemon systemd.
- Xóa tệp `config.py` được tạo ra.

## Giấy phép
Bao gồm thông tin giấy phép của dự án của bạn ở đây.

## Đóng góp
Nếu bạn muốn đóng góp, hãy fork kho lưu trữ và tạo một pull request với các cải tiến của bạn.
