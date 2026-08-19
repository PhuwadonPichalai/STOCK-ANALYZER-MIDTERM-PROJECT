import yfinance as yf
import pandas as pd
import csv
import time
import requests
import io

def get_sp500_tickers():
    print("กำลังดึงรายชื่อหุ้น S&P 500 จาก Wikipedia...")
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    # เพิ่ม User-Agent เพื่อป้องกัน HTTP 403 Forbidden
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    
    # ใช้ io.StringIO ครอบ response.text เพื่อแก้ปัญหา pandas deprecation
    tables = pd.read_html(io.StringIO(response.text))
    df = tables[0]
    tickers = df['Symbol'].tolist()
    # หุ้นบางตัวใน Wiki จะมี . แทน - เช่น BRK.B แต่ yfinance ใช้ BRK-B
    tickers = [t.replace('.', '-') for t in tickers]
    return tickers

def main():
    tickers = get_sp500_tickers()
    print(f"พบรายชื่อหุ้นทั้งหมด {len(tickers)} ตัว")
    
    filename = "sp500_fundamentals.csv"
    
    # เปิดไฟล์เขียนแบบ CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # เขียน Heading หรือ Header
        writer.writerow(["Ticker", "Score", "ROA", "Margin", "Debt_to_Equity"])
        
        count = 0
        print("เริ่มดึงข้อมูล (ขั้นตอนนี้อาจใช้เวลาหลายนาที)...")
        start_time = time.time()
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                roa = info.get("returnOnAssets", 0)
                margin = info.get("profitMargins", 0)
                
                raw_debt = info.get("debtToEquity")
                debt_to_equity = (raw_debt / 100.0) if raw_debt is not None else 0.0
                
                # หากข้อมูลขาดหาย ให้ข้ามไป
                if roa is None or margin is None or debt_to_equity is None:
                    continue

                # สูตรคำนวณคะแนนใหม่ ใช้ ROA แทน
                score = (roa * 0.4) + (margin * 0.4) - (debt_to_equity * 0.2)
                
                # เขียนลงไฟล์ CSV ทีละบรรทัด (แบบ Record)
                writer.writerow([ticker, score, roa, margin, debt_to_equity])
                count += 1
                
                # พิมพ์อัปเดตสถานะทุกๆ 50 ตัว
                if count % 50 == 0:
                    print(f"ดึงข้อมูลและบันทึกลง CSV แล้ว {count} บริษัท...")
                    
            except Exception as e:
                # ข้ามตัวที่มีปัญหาเงียบๆ
                continue
                
    end_time = time.time()
    print(f"\nดาวน์โหลดและบันทึกข้อมูลเสร็จสิ้นทั้งหมด {count} บริษัท!")
    print(f"บันทึกไฟล์เป็น {filename} (ใช้เวลา {end_time - start_time:.2f} วินาที)")

if __name__ == '__main__':
    main()
