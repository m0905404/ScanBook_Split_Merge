import fitz  # PyMuPDF
from PIL import Image
import os
import shutil # 需要導入 shutil 模組來刪除目錄及其內容
from io import BytesIO

# --- 範例使用方式 ---
# 請將 'your_input_file.pdf' 替換為您的 PDF 檔案路徑
pdf_file_path = "a.pdf"
output_folder_name = "Temp_Pages"

def split_and_reorder_pdf_pages(pdf_path, output_dir="Temp_Pages", dpi=300):
    """
    將掃描的 PDF 檔案 (每頁包含書本的兩頁) 轉換並切分成單頁 JPG 檔案。

    - 每一 PDF 頁面會被轉換成一個圖像。
    - 圖像會被切分成右半部 (先) 和左半部 (後)。
    - 切分後的圖像會以 001, 002, 003... 依序命名為 JPG 檔案。

    Args:
        pdf_path (str): 輸入的 PDF 檔案路徑。
        output_dir (str): 輸出 JPG 檔案的資料夾。
        dpi (int): 渲染 PDF 時的解析度 (每英吋點數)。更高的 DPI 產生更清晰的圖像，但也佔用更多空間和時間。
    """
    if os.path.exists(output_dir):
        # 如果目錄存在，則刪除它及其所有內容
        shutil.rmtree(output_dir)
        print(f"已刪除舊的輸出資料夾: {output_dir}")
        
    # 創建新的輸出資料夾
    os.makedirs(output_dir)
    print(f"已創建新的輸出資料夾: {output_dir}")

    doc = None
    try:
        # 嘗試打開 PDF 檔案
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        output_counter = 1  # 輸出檔案的計數器，從 1 開始

        print('開始處理檔案，切割，并且存成 jpg 檔...')
        for page_num in range(total_pages):
            page = doc.load_page(page_num)

            # 1. 將 PDF 頁面渲染成 Pixmap (像素圖)
            # 使用 Matrix 設置 DPI 來控制渲染質量
            zoom = dpi / 72.0
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix, alpha=False)

            # 2. 將 Pixmap 轉換為 PIL Image
            # 必須使用 BytesIO 才能在不存儲到磁碟的情況下傳遞數據給 PIL
            img_data = pix.tobytes("ppm")
            img = Image.open(BytesIO(img_data))

            # 3. 計算切分點
            width, height = img.size
            mid_width = width // 2

            # 定義右半部和左半部的裁剪區域
            # 裁剪區域的格式是 (left, upper, right, lower)
            # 右半部 (書本的偶數頁)
            right_box = (mid_width, 0, width, height)
            # 左半部 (書本的奇數頁)
            left_box = (0, 0, mid_width, height)

            # 4. 裁剪圖像並按照 "右半部在前, 左半部在後" 的順序處理

            # a) 處理右半部
            page_right = img.crop(right_box)
            # 命名格式: 001, 002, ...
            filename_right = os.path.join(output_dir, f"{output_counter:03d}.jpg")
            page_right.save(filename_right, "JPEG", quality=95)
            #print(f"已保存: {filename_right}")
            output_counter += 1

            # b) 處理左半部
            page_left = img.crop(left_box)
            filename_left = os.path.join(output_dir, f"{output_counter:03d}.jpg")
            page_left.save(filename_left, "JPEG", quality=95)
            #print(f"已保存: {filename_left}")
            output_counter += 1

    except Exception as e:
        print(f"處理過程中發生錯誤: {e}")
    finally:
        print(f'處理完成！共切出 {output_counter-1} 個 jpg 檔...')
        if doc:
            doc.close()
        

# 執行函式
# 注意：請確保您的 'your_input_file.pdf' 檔案存在於程式碼執行的目錄中，或者使用完整的路徑。
split_and_reorder_pdf_pages(pdf_file_path, output_folder_name)