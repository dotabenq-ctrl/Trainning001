import streamlit as st
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 視覺主題設定 (酒莊美學)
st.set_page_config(page_title="紅酒分類 2.0 - 酒莊專業版", layout="wide")

# 套用全域樣式：深酒紅強調色
st.markdown("""
    <style>
    .main {
        background-color: #FDFBFA;
    }
    .stButton>button {
        background-color: #800020;
        color: white;
        border-radius: 5px;
        border: none;
    }
    h1, h2, h3 {
        color: #4A0E0E;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 載入資料集
@st.cache_data
def load_data():
    wine = datasets.load_wine()
    df = pd.DataFrame(wine.data, columns=wine.feature_names)
    df['target'] = wine.target
    return wine, df

wine_data, df = load_data()

# 3. Sidebar 客製化
st.sidebar.markdown(f"<h1 style='color: #800020;'>🍷 酒莊實驗室</h1>", unsafe_allow_html=True)

model_name = st.sidebar.selectbox(
    "選擇預測模型",
    ("KNN", "Logistic Regression", "XGBoost", "Random Forest")
)

# 模型簡易說明 (Expander)
with st.sidebar.expander("什麼是這個模型？"):
    if model_name == "KNN":
        st.write("🔍 **KNN (最近鄰居法)**：找空間中最靠近的幾位鄰居，看誰的人數多就選哪一類。適合簡單、直觀的分類任務。")
    elif model_name == "Logistic Regression":
        st.write("📈 **羅吉斯迴歸**：利用數學公式畫出一條分界線，判斷資料屬於哪一邊。雖然名稱有迴歸，但它是分類利器！")
    elif model_name == "XGBoost":
        st.write("⚡ **XGBoost**：強大的『集成學習』模型。它會訓練一堆細小的機器人，並讓下一個機器人修正上一個的錯誤。")
    else:
        st.write("🌳 **隨機森林**：種植一整片決策樹，並透過投票決定結果。非常穩定且準確。")

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **資料集資訊**\n- 樣本數：{df.shape[0]}\n- 特徵數：{df.shape[1]-1}")

# 4. Main Area
st.title("🏆 紅酒品質與分類診斷系統 2.0")

tabs = st.tabs(["📋 資料探索", "🧪 互動實驗室 (推薦)", "📊 套用模型預測"])

with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🍷 樣本細節")
        st.dataframe(df.head(10), use_container_width=True)
    with col2:
        st.subheader("📈 統計指標")
        st.dataframe(df.describe().T[['mean', 'std', 'min', 'max']], use_container_width=True)

with tabs[1]:
    st.subheader("🔬 調整特性，自創一瓶酒！")
    st.write("拖動下方滑桿，看看你的設定會被模型分類為何種紅酒：")
    
    # 建立滑桿，範圍參考資料集的 min/max
    input_data = []
    cols = st.columns(3)
    for i, feature in enumerate(wine_data.feature_names):
        min_val = float(df[feature].min())
        max_val = float(df[feature].max())
        mean_val = float(df[feature].mean())
        val = cols[i % 3].slider(f"{feature}", min_val, max_val, mean_val)
        input_data.append(val)
    
    if st.button("進行即時實驗診斷", type="primary"):
        # 準備資料與訓練 (為了動態顯示，這裡簡化處理)
        X_train, X_test, y_train, y_test = train_test_split(wine_data.data, wine_data.target, test_size=0.2, random_state=42)
        
        if model_name == "KNN": model = KNeighborsClassifier()
        elif model_name == "Logistic Regression": model = LogisticRegression(max_iter=5000)
        elif model_name == "XGBoost": model = XGBClassifier()
        else: model = RandomForestClassifier()
        
        model.fit(X_train, y_train)
        pred = model.predict([input_data])
        
        st.markdown(f"### 🎯 診斷結果：這是一瓶 **{wine_data.target_names[pred[0]].upper()}** 級別的紅酒！")
        st.balloons()

with tabs[2]:
    if st.button("執行全樣本精準度測驗"):
        X_train, X_test, y_train, y_test = train_test_split(wine_data.data, wine_data.target, test_size=0.2, random_state=42)
        
        if model_name == "KNN": model = KNeighborsClassifier()
        elif model_name == "Logistic Regression": model = LogisticRegression(max_iter=5000)
        elif model_name == "XGBoost": model = XGBClassifier()
        else: model = RandomForestClassifier()
        
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("模型準確度 (Accuracy)", f"{acc*100:.2f}%")
        
        # 簡易特徵貢獻度圖表
        if hasattr(model, 'feature_importances_'):
            st.subheader("💡 特徵影響權重 Top 5")
            feat_importances = pd.Series(model.feature_importances_, index=wine_data.feature_names)
            st.bar_chart(feat_importances.sort_values(ascending=False).head(5))
        else:
            st.info("該模型暫不支援特徵貢驗度視覺化。")
