# Streamlit 謝林隔離模型範例 (Schelling Segregation Model)

這是一個簡單的 Streamlit 應用程式範例，主要用來展示並實作 **謝林隔離模型 (Schelling Segregation Model)**，並將其部署到 **Streamlit Community Cloud** 上。

## 關於謝林隔離模型
謝林隔離模型是一個代理人基模型 (Agent-based model)，用來模擬和解釋多種族城市中的隔離現象。即使個體對鄰居的多樣性有很高的包容度，只要稍微偏好與自己相似的人為鄰，最終仍可能導致高度的社會隔離狀態。

在本專案中，你可以透過左側欄位調整以下參數，並即時觀察城市的隔離狀態變化：
- **人口總數 (Population Size)**
- **空屋比例 (Empty Houses Ratio)**
- **相似度門檻 (Similarity Threshold)**
- **模擬迭代次數 (Number of Iterations)**

## 參考來源
本專案的 Python 實作與 Streamlit 介面邏輯，主要參考自 Adil Moujahid 的優質教學文章：
👉 [An Implementation of Schelling Segregation Model using Python and Streamlit](https://adilmoujahid.com/posts/2020/05/streamlit-python-schelling/)

## 如何在本地執行
```bash
uv run streamlit run main.py
```
