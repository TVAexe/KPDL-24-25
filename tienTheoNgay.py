import pandas as pd

# Cài đặt định dạng hiển thị cho số thực
pd.options.display.float_format = '{:,.2f}'.format

# Đọc file CSV với các cột tương ứng (thay đổi file tương ứng)
file_path = 'Viettin_16-29.csv'
df = pd.read_csv(file_path, usecols=['Thời gian chuyển khoản', 'Số tiền ghi có (VND)', 'Nội dung chi tiết'])

# Xử lý cột 'Thời gian chuyển khoản' với định dạng ngày/tháng/năm giờ:phút:giây
df['Thời gian chuyển khoản'] = pd.to_datetime(df['Thời gian chuyển khoản'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

# Loại bỏ các hàng có giá trị NaT trong cột 'Thời gian chuyển khoản'
df = df.dropna(subset=['Thời gian chuyển khoản'])

# Trích xuất ngày từ cột 'Thời gian chuyển khoản'
df['Ngày'] = df['Thời gian chuyển khoản'].dt.date

# Xử lý cột 'Số tiền ghi có (VND)': loại bỏ dấu phẩy và chuyển đổi sang kiểu số
df['Số tiền ghi có (VND)'] = df['Số tiền ghi có (VND)'].str.replace(',', '').astype(float)

# Loại bỏ các hàng có giá trị NaN trong cột 'Số tiền ghi có (VND)'
df = df.dropna(subset=['Số tiền ghi có (VND)'])

# Loại bỏ các hàng trùng lặp
df = df.drop_duplicates()

# Tính tổng số tiền và số lượng giao dịch cho từng ngày
df_daily_summary = df.groupby('Ngày').agg(
    Tổng_số_tiền=('Số tiền ghi có (VND)', 'sum'),
    Số_lượng_giao_dịch=('Số tiền ghi có (VND)', 'count')
).reset_index()

# Đổi tên các cột cho dễ đọc
df_daily_summary.columns = ['Ngày', 'Tổng số tiền (VND)', 'Số lượng giao dịch']

# Hiển thị kết quả
print(df_daily_summary)
