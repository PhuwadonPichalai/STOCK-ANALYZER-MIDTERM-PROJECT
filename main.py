import csv
import time

def readRecordToList(filename):
    """
    ฟังก์ชันอ่านไฟล์ CSV คืนค่าเป็น List ของ List (2 มิติ) 
    ตามเนื้อหาบทเรียนที่อาจารย์สอน
    """
    infile = open(filename, 'r', encoding='utf-8')
    mylist = []
    heading = next(infile) # ข้ามบรรทัดหัวตาราง (Header)
    csv_obj = csv.reader(infile)
    for row in csv_obj:
        # ข้อมูลที่อ่านจาก csv จะเป็น String เสมอ ต้องแปลงเป็น float เพื่อใช้คำนวณ
        # โครงสร้าง: ["Ticker", "Score", "ROA", "Margin", "Debt_to_Equity"]
        # Index:      0         1        2        3         4
        ticker = row[0]
        score = float(row[1])
        roa = float(row[2])
        margin = float(row[3])
        debt = float(row[4])
        
        mylist.append([ticker, score, roa, margin, debt])
        
    infile.close()
    return mylist

def merge_sort_rec(arr, key_col):
    """
    อัลกอริทึม Merge Sort รับพารามิเตอร์คอลัมน์กุญแจ (key_col)
    เพื่อจัดเรียงข้อมูลแบบ Record โดยเรียงจาก มาก -> น้อย (Descending)
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort_rec(arr[:mid], key_col)
    right = merge_sort_rec(arr[mid:], key_col)

    return merge(left, right, key_col)

def merge(left, right, key_col):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        # เปรียบเทียบข้อมูลที่คอลัมน์ (key_col) ที่ระบุ
        # ใช้ >= เพื่อเรียงจาก มาก ไป น้อย
        if left[i][key_col] >= right[j][key_col]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def main():
    file_name = "sp500_fundamentals.csv"
    
    # 1. อ่านข้อมูลจากไฟล์ CSV มาเก็บในรูป List ซ้อน List
    try:
        data_list = readRecordToList(file_name)
    except FileNotFoundError:
        print(f"ไม่พบไฟล์ {file_name} กรุณารันไฟล์ download_data.py ก่อน")
        return
        
    print(f"อ่านข้อมูลเสร็จสิ้น จำนวน {len(data_list)} บริษัท\n")
    
    # 2. จัดเรียงข้อมูลโดยใช้ Merge Sort ตามคอลัมน์ Score (Index 1)
    key_column = 1 
    print(f"กำลังจัดเรียงข้อมูลด้วยกุญแจคอลัมน์ที่ {key_column} (Score)...")
    start_time_sort = time.time()
    
    sorted_stocks = merge_sort_rec(data_list, key_column)
    
    print(f"จัดเรียงเสร็จสิ้น ใช้เวลา: {time.time() - start_time_sort:.5f} วินาที\n")
    
    # 3. แสดงผล Top 5
    print("="*70)
    print(" " * 20 + "TOP 5 หุ้นน่าลงทุน (S&P 500)")
    print("="*70)
    print(f"{'อันดับ':<8}{'ชื่อหุ้น':<10}{'ROA (%)':<10}{'Margin (%)':<12}{'D/E Ratio':<12}{'คะแนนรวม':<12}")
    print("-" * 70)
    
    for i in range(min(5, len(sorted_stocks))):
        row = sorted_stocks[i]
        # การจัดรูปแบบการแสดงผล
        ticker = row[0]
        score = f"{row[1]:.4f}"
        roa = f"{row[2]*100:.2f}"
        margin = f"{row[3]*100:.2f}"
        de = f"{row[4]:.2f}"
        print(f"{i+1:<8}{ticker:<10}{roa:<10}{margin:<12}{de:<10}{score:<12}")
    print("="*70)

if __name__ == "__main__":
    main()