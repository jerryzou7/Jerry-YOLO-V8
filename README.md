# Demo - 智慧電池管理 YOLOv8 物體偵測

## 概述

這是一個具有智慧電池管理功能的 YOLOv8 物體偵測程式。該程式會根據模擬的電池電量自動切換使用不同大小的 YOLOv8 模型，以平衡效能和電池續航力。當電池電量充足時使用較準確的重型模型，電量不足時切換到較輕量的快速模型。

## 功能特色

- **智慧模型切換**：根據電池電量自動選擇合適的 YOLOv8 模型
- **電池模擬**：模擬電池消耗和充電過程
- **即時物體偵測**：使用攝影機進行即時影像處理
- **動態效能調整**：在準確度和效率之間動態平衡
- **視覺化資訊**：即時顯示電池電量和當前使用的模型

## 系統需求

### 必要套件
```bash
pip install ultralytics opencv-python torch
```

### 硬體需求
- 攝影機（內建或外接）
- 支援 CUDA 的 GPU（可選，用於加速推論）

## 程式碼說明

### 主要組件

1. **模型初始化**
   ```python
   model_heavy = YOLO('yolov8s.pt')  # 較慢但準確
   model_light = YOLO('yolov8n.pt')  # 快速但較不準確
   ```
   - 載入兩個不同大小的 YOLOv8 模型
   - `yolov8s.pt`：較大模型，準確度更高
   - `yolov8n.pt`：較小模型，速度更快

2. **電池模擬系統**
   ```python
   battery_level = 100
   # 模擬電池消耗
   battery_level -= random.uniform(0.5, 1.0)
   if battery_level < 20:
       battery_level = 100  # 模擬充電
   ```
   - 初始電池電量設為 100%
   - 每幀隨機消耗 0.5-1.0% 電量
   - 電量低於 20% 時自動充電至 100%

3. **智慧模型選擇**
   ```python
   if battery_level > 50:
       model = model_heavy
       model_name = "YOLOv8s (Heavy)"
   else:
       model = model_light
       model_name = "YOLOv8n (Light)"
   ```
   - 電池電量 > 50%：使用重型模型（YOLOv8s）
   - 電池電量 ≤ 50%：使用輕型模型（YOLOv8n）

4. **即時資訊顯示**
   ```python
   cv2.putText(annotated_frame, f"Battery: {int(battery_level)}%", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
   cv2.putText(annotated_frame, f"Model: {model_name}", (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
   ```
   - 在影像上疊加電池電量資訊
   - 顯示當前使用的模型名稱

## 使用方法

1. **執行程式**
   ```bash
   python demo.py
   ```

2. **操作說明**
   - 程式會開啟攝影機並顯示偵測視窗
   - 觀察電池電量的變化（綠色文字顯示）
   - 注意模型切換時的效能變化
   - 按 `Q` 鍵退出程式

## 模型比較

### YOLOv8s (Heavy Model)
- **檔案大小**：約 22 MB
- **速度**：較慢
- **準確度**：高
- **適用場景**：電池電量充足時

### YOLOv8n (Light Model)
- **檔案大小**：約 6.2 MB
- **速度**：快速
- **準確度**：中等
- **適用場景**：電池電量不足時

## 電池管理策略

### 電量閾值設定
- **高電量模式**（> 50%）：使用重型模型
- **低電量模式**（≤ 50%）：使用輕型模型
- **充電觸發**：電量 < 20% 時自動充電

### 自訂電池參數
```python
# 修改電池消耗速度
battery_level -= random.uniform(0.1, 0.5)  # 降低消耗速度

# 修改切換閾值
if battery_level > 70:  # 提高切換閾值
    model = model_heavy

# 修改充電觸發點
if battery_level < 10:  # 降低充電觸發點
    battery_level = 100
```

## 效能監控

### 觀察指標
1. **電池電量變化**：觀察電量消耗速度
2. **模型切換**：注意切換時的效能變化
3. **偵測準確度**：比較不同模型的偵測效果
4. **處理速度**：觀察 FPS 變化

### 效能優化建議
1. **調整電池消耗速度**：根據實際需求調整
2. **優化切換閾值**：找到最佳的電量切換點
3. **添加更多模型選項**：實現更細緻的效能分級

## 擴展功能

### 可能的改進
1. **多級模型切換**
   ```python
   if battery_level > 80:
       model = YOLOv8m  # 中型模型
   elif battery_level > 50:
       model = YOLOv8s  # 小型模型
   elif battery_level > 20:
       model = YOLOv8n  # 納米模型
   else:
       model = YOLOv8n  # 最低功耗模式
   ```

2. **實際電池監控**
   - 整合系統電池 API
   - 實時監控實際電池電量

3. **效能統計**
   - 記錄不同模型的 FPS
   - 統計電池使用效率

4. **使用者設定**
   - 允許使用者自訂切換策略
   - 添加手動模式切換

## 應用場景

### 適合的使用情境
- **行動裝置**：手機、平板電腦的 AI 應用
- **邊緣運算**：IoT 裝置的智慧監控
- **無人機**：需要平衡效能和續航力的場景
- **嵌入式系統**：資源受限的智慧裝置

### 實際應用範例
- 智慧監控攝影機
- 行動機器人視覺系統
- 穿戴式智慧裝置
- 車載 AI 系統

## 故障排除

### 常見問題

1. **模型切換延遲**
   - 檢查模型載入時間
   - 考慮預載入所有模型

2. **電池消耗過快**
   - 調整消耗參數
   - 優化模型推論效率

3. **偵測準確度下降**
   - 檢查模型切換邏輯
   - 調整切換閾值

## 授權資訊

本程式使用以下開源專案：
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [PyTorch](https://pytorch.org/)

## 聯絡資訊

如有問題或建議，請聯繫開發者。
