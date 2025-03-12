import threading
import requests
import time
import concurrent.futures


# รายการเว็บไซต์ที่จะทำการดาวน์โหลด
WEBSITES = [
    "https://www.python.org/",
    "https://www.google.com/",
    "https://www.github.com/",
    "https://www.stackoverflow.com/",
    "https://www.wikipedia.org/"
]

def download_site(url):
    """
    ฟังก์ชันสำหรับดาวน์โหลดเนื้อหาจากเว็บไซต์
    """
    print(f"เริ่มดาวน์โหลด: {url}")
    response = requests.get(url)
    print(f"ดาวน์โหลดเสร็จสิ้น: {url}, ขนาด: {len(response.content)} ไบต์")
    return len(response.content)


def download_sequential():
    """
    ดาวน์โหลดเว็บไซต์แบบลำดับ (ทีละเว็บไซต์)
    """
    print("\n--- เริ่มการดาวน์โหลดแบบลำดับ ---\n")
    start_time = time.time()
    
    total_size = 0
    for url in WEBSITES:
        size = download_site(url)
        total_size += size
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\n--- การดาวน์โหลดแบบลำดับเสร็จสิ้น ---")
    print(f"ขนาดที่ดาวน์โหลดทั้งหมด: {total_size} ไบต์")
    print(f"เวลาที่ใช้ทั้งหมด: {execution_time:.2f} วินาที\n")
    
    return execution_time


def download_threaded():
    """
    ดาวน์โหลดเว็บไซต์แบบขนานโดยใช้เธรด
    """
    print("\n--- เริ่มการดาวน์โหลดแบบใช้เธรด ---\n")
    start_time = time.time()
    
    # สร้างเธรดสำหรับแต่ละเว็บไซต์
    threads = []
    for url in WEBSITES:
        thread = threading.Thread(target=download_site, args=(url,))
        threads.append(thread)
        thread.start()
    
    # รอให้เธรดทั้งหมดทำงานเสร็จ
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\n--- การดาวน์โหลดแบบใช้เธรดเสร็จสิ้น ---")
    print(f"เวลาที่ใช้ทั้งหมด: {execution_time:.2f} วินาที\n")
    
    return execution_time


def download_with_threadpool():
    """
    ดาวน์โหลดเว็บไซต์โดยใช้ ThreadPoolExecutor
    """
    print("\n--- เริ่มการดาวน์โหลดด้วย ThreadPoolExecutor ---\n")
    start_time = time.time()
    
    total_size = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(download_site, url): url for url in WEBSITES}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                size = future.result()
                total_size += size
            except Exception as e:
                print(f"เกิดข้อผิดพลาดในการดาวน์โหลด: {e}")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\n--- การดาวน์โหลดด้วย ThreadPoolExecutor เสร็จสิ้น ---")
    print(f"ขนาดที่ดาวน์โหลดทั้งหมด: {total_size} ไบต์")
    print(f"เวลาที่ใช้ทั้งหมด: {execution_time:.2f} วินาที\n")
    
    return execution_time


if __name__ == "__main__":
    print("=== เปรียบเทียบวิธีการดาวน์โหลด ===")
    
    seq_time = download_sequential()
    th_time = download_threaded()
    pool_time = download_with_threadpool()
    
    print("=== ผลการเปรียบเทียบประสิทธิภาพ ===")
    print(f"เวลาดาวน์โหลดแบบลำดับ: {seq_time:.2f} วินาที")
    print(f"เวลาดาวน์โหลดแบบใช้เธรดพื้นฐาน: {th_time:.2f} วินาที")
    print(f"เวลาดาวน์โหลดแบบใช้ ThreadPoolExecutor: {pool_time:.2f} วินาที")
    
    seq_vs_thread = (seq_time / th_time) if th_time > 0 else 0
    seq_vs_pool = (seq_time / pool_time) if pool_time > 0 else 0
    
    print(f"\nการใช้เธรดเร็วกว่าแบบลำดับ {seq_vs_thread:.2f} เท่า")
    print(f"การใช้ ThreadPoolExecutor เร็วกว่าแบบลำดับ {seq_vs_pool:.2f} เท่า") 