import pdfplumber
import csv
import os

# file convert
pdf_paths = [

]

def extract_table_from_pdf(pdf_path):
     # create file csv
    csv_output_path = os.path.splitext(pdf_path)[0] + '.csv'

    with pdfplumber.open(pdf_path) as pdf, open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:
        total_pages = len(pdf.pages)
        csv_writer = csv.writer(csvfile)
        print(f"Bắt đầu xử lý tệp {pdf_path}, Tổng số trang: {total_pages}")
        
        for page_number, page in enumerate(pdf.pages):

            table = page.extract_table()

            if table:
                # insert 2 column
                for row in table:
                    row.append('VIETIN') 
                    row.append('BVDCTTU')  
                    csv_writer.writerow(row)
            else:
                print(f"Không tìm thấy bảng trên trang {page_number + 1}/{total_pages}")

    print(f"Dữ liệu đã được xuất ra {csv_output_path}")

for pdf_path in pdf_paths:
    extract_table_from_pdf(pdf_path)
