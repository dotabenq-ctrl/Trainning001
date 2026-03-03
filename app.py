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

# 設定網頁標題
st.set_page_config(page_title="紅酒分類機器學習專題", layout="wide")

# 1. 載入資料集
@st.cache_data
def load_data():
    wine = datasets.load_wine()
    df = pd.DataFrame(wine.data, columns=wine.feature_names)
    df['target'] = wine.target
    return wine, df

wine_data, df = load_data()

# 2. 左側 Sidebar
st.sidebar.header("模型設定")
model_name = st.sidebar.selectbox(
    "選擇機器學習模型",
    ("KNN", "Logistic Regression", "XGBoost", "Random Forest")
)

st.sidebar.markdown("---")
st.sidebar.header("資料集資訊")
st.sidebar.write(f"**資料集名稱:** Wine Dataset")
st.sidebar.write(f"**樣本總數:** {df.shape[0]}")
st.sidebar.write(f"**特徵數量:** {df.shape[1]-1}")
st.sidebar.write(f"**類別數量:** {len(np.unique(wine_data.target))}")
st.sidebar.write("**類別名稱:** " + ", ".join(wine_data.target_names))

# 3. 右側 Main 區
st.title("🍷 紅酒資料集分類預測")

col1, col2 = st.columns(2)

with col1:
    st.subheader("資料預覽 (前 5 筆)")
    st.dataframe(df.head())

with col2:
    st.subheader("特徵統計值")
    st.dataframe(df.describe().T)

st.markdown("---")

# 4. 預測與訓練
st.subheader(f"當前選擇模型: {model_name}")

if st.button("開始執行預測"):
    # 分割資料
    X = wine_data.data
    y = wine_data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 模型初始化
    if model_name == "KNN":
        model = KNeighborsClassifier(n_neighbors=5)
    elif model_name == "Logistic Regression":
        model = LogisticRegression(max_iter=5000)
    elif model_name == "XGBoost":
        model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    else: # Random Forest
        model = RandomForestClassifier(n_estimators=100)

    # 訓練模型
    with st.spinner(f"正在訓練 {model_name} 模型..."):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

    # 顯示結果
    st.success("預測完成！")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label="模型準確度 (Accuracy)", value=f"{acc*100:.2f}%")
    
    with res_col2:
        # 顯示前 10 筆測試樣本的預測與真實值對比
        comparison_df = pd.DataFrame({
            '真實類別': [wine_data.target_names[i] for i in y_test[:10]],
            '預測類別': [wine_data.target_names[i] for i in y_pred[:10]]
        })
        st.write("測試集前 10 筆預測對比：")
        st.table(comparison_df)
