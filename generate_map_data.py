import pandas as pd
import json
import os

# ================= 參數設定區 =================
EXCEL_FILE = "01_FINAL.xlsx"
TARGET_CSVS = [
    "health_check_recordsC1L.csv",
    "health_check_recordsC1M.csv",
    "health_check_recordsC1H.csv"
]
EXCEL_ID_COL = "BUILD_ID"      
EXCEL_LAT_COL = "latitude"      
EXCEL_LNG_COL = "longitude"     
# ==============================================

def create_js_data():
    print(f"正在讀取 {EXCEL_FILE} ...")
    try:
        df_excel = pd.read_excel(EXCEL_FILE)
        all_target_buildings = set() 
        
        for csv_file in TARGET_CSVS:
            if os.path.exists(csv_file):
                print(f"正在讀取 {csv_file} ...")
                df_target = pd.read_csv(csv_file)
                all_target_buildings.update(df_target['b_id'].astype(str).unique())
            else:
                print(f"警告: 找不到檔案 {csv_file}，已略過。")
        
        print(f"\n共從 CSV 中找到 {len(all_target_buildings)} 棟不重複的已分析建築。")
        
        buildings_list = []
        
        # 【修改處】改成遍歷 Excel 中的所有建築，而不是 df_filtered
        for index, row in df_excel.iterrows():
            b_id = str(row[EXCEL_ID_COL])
            # 判斷這棟建築的 ID 是否在我們收集到的 CSV ID 集合中
            has_data = b_id in all_target_buildings
            
            buildings_list.append({
                "id": b_id,
                "lat": float(row[EXCEL_LAT_COL]),
                "lng": float(row[EXCEL_LNG_COL]),
                "has_data": has_data  # 新增這個屬性供前端分類
            })
            
        print(f"成功處理總計 {len(buildings_list)} 筆建築座標資料！\n")
        
        js_content = f"var buildings = {json.dumps(buildings_list, indent=4, ensure_ascii=False)};"
        with open("buildings_data.js", "w", encoding="utf-8") as f:
            f.write(js_content)
            
        print("🎉 已成功產出 buildings_data.js 檔案！")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    create_js_data()