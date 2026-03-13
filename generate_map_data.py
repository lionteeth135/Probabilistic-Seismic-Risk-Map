import pandas as pd
import json
import os

# ================= 參數設定區 =================
EXCEL_FILE = "01_FINAL.xlsx"

# 將原本單一檔案改成一個列表 (List)，把 L, M, H 的檔案都寫進來
# 如果你有其他檔名，也可以直接加在這個中括號裡面
TARGET_CSVS = [
    "health_check_recordsC1L.csv",
    "health_check_recordsC1M.csv",
    "health_check_recordsC1H.csv"
]

# !!! 請根據你 Excel 實際的欄位名稱修改以下三個變數 !!!
EXCEL_ID_COL = "BUILD_ID"      # Excel 裡代表建築 ID 的欄位名稱
EXCEL_LAT_COL = "latitude"      # Excel 裡代表緯度的欄位名稱 (例如 23.xxx)
EXCEL_LNG_COL = "longitude"      # Excel 裡代表經度的欄位名稱 (例如 121.xxx)
# ==============================================

def create_js_data():
    print(f"正在讀取 {EXCEL_FILE} ...")
    try:
        # 1. 讀取包含所有座標的 Excel 檔案
        df_excel = pd.read_excel(EXCEL_FILE)
        
        # 2. 收集所有 CSV 檔案中的建築 ID
        all_target_buildings = set() # 使用集合 (set) 可以自動排除重複的 ID
        
        for csv_file in TARGET_CSVS:
            if os.path.exists(csv_file):
                print(f"正在讀取 {csv_file} ...")
                df_target = pd.read_csv(csv_file)
                # 將這個檔案裡的 b_id 加入集合中
                all_target_buildings.update(df_target['b_id'].unique())
            else:
                print(f"警告: 找不到檔案 {csv_file}，已略過。")
        
        print(f"\n共從 CSV 中找到 {len(all_target_buildings)} 棟不重複的建築。")
        
        # 3. 從 Excel 中篩選出這些目標建築的資料
        df_filtered = df_excel[df_excel[EXCEL_ID_COL].isin(all_target_buildings)]
        
        buildings_list = []
        
        # 4. 逐筆轉換為網頁需要的格式
        for index, row in df_filtered.iterrows():
            buildings_list.append({
                "id": str(row[EXCEL_ID_COL]),
                "lat": float(row[EXCEL_LAT_COL]),
                "lng": float(row[EXCEL_LNG_COL]),
                "name": f"建築 {row[EXCEL_ID_COL]}"
            })
            
        print(f"成功在 Excel 中配對到 {len(buildings_list)} 筆建築座標資料！\n")
        
        # 5. 將資料寫入成 JavaScript 檔案
        js_content = f"var buildings = {json.dumps(buildings_list, indent=4, ensure_ascii=False)};"
        
        with open("buildings_data.js", "w", encoding="utf-8") as f:
            f.write(js_content)
            
        print("🎉 已成功產出 buildings_data.js 檔案！現在可以打開 index.html 查看地圖了。")

    except Exception as e:
        print(f"發生錯誤: {e}")
        print("請確認檔案名稱與欄位名稱是否正確。")

if __name__ == "__main__":
    create_js_data()