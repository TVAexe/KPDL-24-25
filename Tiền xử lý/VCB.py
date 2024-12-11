import pandas as pd
import re

# Đọc dữ liệu từ file CSV
file_path = ""
df = pd.read_csv("file_path")

# 1. Loại bỏ các cột không cần thiết
columns_to_drop = ["Số tiền ghi nợ/ Debit", "Số dư/ Balance"]
df = df.drop(columns=columns_to_drop, errors="ignore")

# Loại bỏ các cột không có dữ liệu 
df = df.dropna(axis=1, how="all")

# 2. Chỉnh sửa tên các cột
df = df.rename(columns={
    "Ngày GD/TNX Date Số CT/Doc No": "Ngày GD",
    "Số tiền ghi có/ Credit": "Số tiền",
    "Nội dung chi tiết/ Transaction in detail": "Nội dung chi tiết"
})

# 3. Định dạng lại cột Ngày GD
df["Ngày GD"] = pd.to_datetime(df["Ngày GD"], errors="coerce").dt.strftime("%d/%m/%Y")

# 4. Chuyển cột Số tiền sang kiểu dữ liệu số
df["Số tiền"] = (
    df["Số tiền"]
    .str.replace(r"[^\d.]", "", regex=True)  # Loại bỏ ký tự không phải số hoặc dấu chấm
    .astype(float, errors="ignore")          # Chuyển đổi sang kiểu float
)

# 5. Xóa các hàng có giá trị trống trong cột Số tiền
df = df.dropna(subset=["Số tiền"])

# 6. Làm sạch và trích xuất thông tin từ cột "Nội dung chi tiết"
def clean_and_extract_transaction_info(value):
    value = str(value)
    
    # Loại bỏ dấu chấm, khoảng trắng không cần thiết và các cụm không mong muốn
    value = re.sub(r'\.', ' ', value)  # Thay dấu chấm bằng khoảng trắng
    value = re.sub(
        r'toi MAT TRAN TO QUOC VN - BAN CUU TRO TW|CT tu|VCB|MBVCB|Vietcombank'
        r':0011001932418:|PARTNER DIRECT_DEBITS_[A-Z]+|CTDK|MSE|ZLP|IBFT|Vietcombank|'
        r'toi Uy Ban Trung uong Mat tran To quoc Viet Nam',
        '',
        value,
        flags=re.IGNORECASE
    )
    value = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{1,2}:\d{2}(:\d{2})?\b', '', value)  # Xóa ngày, giờ
    value = re.sub(r'-|02009704[^\s]*|[A-Z]*\d+[A-Z]*|\b\d+_[^\s]*', '', value)  # Loại bỏ chuỗi không cần thiết
    value = value.replace('***', '').strip()
    
    # Tách tên người gửi
    name_match = re.search(r'[A-Z\s]+', value)
    name = name_match.group(0).strip() if name_match else None
    
    # Trả về dữ liệu đã tách
    return pd.Series({
        'Nội dung chi tiết': value.strip(),
        'Người gửi': name
    })

# Áp dụng hàm cho cột "Nội dung chi tiết"
df[["Nội dung chi tiết", "Người gửi"]] = df["Nội dung chi tiết"].apply(clean_and_extract_transaction_info)

result_df = df[['Ngày GD', 'Số tiền', 'Nội dung chi tiết', 'Người gửi']]

# Xuất dữ liệu sau xử lý ra file mới
result_df.to_csv("cleaned_data.csv", index=False, encoding="utf-8-sig")
