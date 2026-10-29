# FreshScan - web quét màu cảm biến thực phẩm

## Chạy trên máy tính
1. Cài Python 3.10 trở lên.
2. Mở Terminal/Command Prompt tại thư mục này.
3. Cài thư viện:
   `pip install -r requirements.txt`
4. Khởi chạy:
   `streamlit run app.py`
5. Trình duyệt sẽ mở trang web cục bộ.

## Cách dùng
- Ảnh cần là ảnh tem cảm biến có hai vùng màu đặt cạnh nhau.
- Zone A ở bên trái; Zone B ở bên phải.
- Chụp dưới ánh sáng trắng đều, tránh bóng và phản chiếu.
- Tải ảnh lên rồi bấm “Phân tích màu”.

## Giới hạn
Ứng dụng giữ ma trận màu và cách đối chiếu RGB từ code được cung cấp. Chỉ số FI và RSL là các giá trị trong bảng tham chiếu, chưa được xác thực bằng dữ liệu kiểm nghiệm thực tế. Không dùng để xác nhận thực phẩm an toàn.
