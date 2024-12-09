import pdfplumber
import csv
import os
import re

# file convert
pdf_paths = [

]

def format_currency(value):
    value = re.sub(r'[^\d,]', '', value)
    
    if ' ' in value:
        value = value.split()[-1]

    parts = value.split(',')
    formatted_value = parts[0]
    
    if len(parts) > 1:
        for part in parts[1:]:
            formatted_value += f'.{part}'
    
    return formatted_value

def process_column_five(value):
    return value.replace(',', '.')

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
                for row in table[1:]:
                    # fix column 3,4
                    row[2] = format_currency(row[2])  
                    row[3] = format_currency(row[3])  

                    # column 5
                    row[4] = process_column_five(row[4])

                    # insert column 7,8
                    row.append('AGRIBANK') 
                    row.append('MTTQ') 

                    csv_writer.writerow(row)
            else:
                print(f"Không tìm thấy bảng trên trang {page_number + 1}/{total_pages}")

    print(f"Dữ liệu đã được xuất ra {csv_output_path}")

for pdf_path in pdf_paths:
    extract_table_from_pdf(pdf_path)
