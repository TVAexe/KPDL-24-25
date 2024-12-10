import pandas as pd

# Đọc dữ liệu từ file CSV
file_path = ""
df = pd.read_csv("file_path")

# Tính toán các chỉ số thống kê
tong_so_tien = df["Số tiền"].sum()
so_tien_trung_binh = df["Số tiền"].mean()
so_tien_trung_vi = df["Số tiền"].median()
so_tien_mode = df["Số tiền"].mode()[0]
so_luong_mode = df["Số tiền"].value_counts()[so_tien_mode]
so_tien_lon_nhat = df["Số tiền"].max()
so_tien_nho_nhat = df["Số tiền"].min()

# Tổng hợp kết quả vào DataFrame
summary_data = {
    "Chỉ số": [
        "Tổng số tiền ủng hộ",
        "Số tiền ủng hộ trung bình",
        "Số tiền trung vị",
        "Số tiền ủng hộ phổ biến nhất",
        "Số lần xuất hiện của giá trị phổ biến nhất",
        "Số tiền ủng hộ lớn nhất",
        "Số tiền ủng hộ nhỏ nhất"
    ],
    "Giá trị": [
        tong_so_tien,
        so_tien_trung_binh,
        so_tien_trung_vi,
        so_tien_mode,
        so_luong_mode,
        so_tien_lon_nhat,
        so_tien_nho_nhat
    ]
}

summary_df = pd.DataFrame(summary_data)

# Xuất kết quả ra file Excel
with pd.ExcelWriter("analysis_results.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Cleaned Data", index=False, encoding='utf-8-sig')
    summary_df.to_excel(writer, sheet_name="Summary", index=False, encoding='utf-8-sig')

print("Kết quả đã được lưu vào file 'analysis_results.xlsx'.")
