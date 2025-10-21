import os
import glob
from PIL import Image


# --- 範例使用方式 ---
# 設定您切割後的 JPG 檔案所在的目錄
input_folder = "Temp_Pages"
# 設定輸出的 PDF 檔案名稱
output_file = "merged_book.pdf"


def merge_images_to_pdf(folder_path, output_pdf_path):
    """
    依據檔名由小到大排序，將資料夾內所有 JPG 檔案合併成一個 PDF 檔案。

    Args:
        folder_path (str): 包含 JPG 檔案的資料夾路徑 (例如: 'Temp_Pages')。
        output_pdf_path (str): 輸出 PDF 檔案的路徑和名稱 (例如: 'merged_book.pdf')。
    """
    # 1. 取得所有 JPG 檔案路徑
    # 使用 glob 模組來查找所有符合 '.jpg' 或 '.jpeg' 結尾的檔案
    search_pattern = os.path.join(folder_path, "*.jpg")
    jpg_files = glob.glob(search_pattern)

    # 2. 依據檔名排序
    # 檔名是 '001.jpg', '002.jpg', ... Python 的 sort() 會自動進行正確的數字排序
    jpg_files.sort()

    if not jpg_files:
        print(f"在資料夾 '{folder_path}' 中找不到任何 JPG 檔案。")
        return
    
    print(f'在資料夾 "{folder_path}" 中, 共找到 ({len(jpg_files)}) 個 JPG 檔案。')
    print("開始 Merge, Merge 中 ....")

    # 3. 開啟所有圖像
    images_list = []
    
    # 開啟第一張圖像作為 PDF 的主體
    try:
        # 載入第一張圖像，並將其轉換為 'RGB' 模式，以確保與 PDF 格式兼容
        first_image = Image.open(jpg_files[0]).convert('RGB')
        
        # 載入其餘圖像
        for file_path in jpg_files[1:]:
            # 將圖像轉換為 'RGB' 模式以避免 PDF 儲存時出現顏色模式不兼容問題
            img = Image.open(file_path).convert('RGB')
            images_list.append(img)
            
    except Exception as e:
        print(f"載入圖像時發生錯誤: {e}")
        return

    # 4. 合併並儲存為 PDF
    try:
        # 使用第一張圖像的 .save() 方法，將其餘圖像作為附加頁面 (append_images)
        first_image.save(
            output_pdf_path,
            "PDF",
            resolution=100.0,  # 設置 PDF 解析度
            save_all=True,     # 必須設置為 True 才能保存多頁
            append_images=images_list # 附加其餘圖像
        )
        print(f'成功將 {len(jpg_files)} 張圖像合併並保存為: "{output_pdf_path}"')
    except Exception as e:
        print(f"保存 PDF 檔案時發生錯誤: {e}")


# 執行函式
merge_images_to_pdf(input_folder, output_file)