# FaceID
## Hệ Thồng chấm công sử dụng công nghệ Face ID
Hệ thống chấm công Face ID là một giải pháp hiện đại để quản lý thời gian làm việc của nhân viên trong tổ chức. 

### Cách chạy
```
python display.py
```

### Tùy chọn dữ liệu
Cỏ thể thay thế thư mục data bằng data chuẩn bị trước.
Sau đó chạy 
```
python training.py
```
để cập nhật lại file encodings.pkl
Rồi chạy lại file 
```
python display.py
```
với data của bạn.
### Bản ghi log
Mọi thông tin về Tên đầy dủ, trạng thái, ngày, giờ sẽ được lưu trong file attention.csv trong folder csv.
