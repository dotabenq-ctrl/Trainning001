@echo off
TITLE 🍷 紅酒 App 一鍵啟動神器 - 自動偵測版
echo 正在準備啟動 2.0 版紅酒分類系統...

:: 1. 切換到腳本所在目錄
cd /d "%~dp0"

:: 2. 自動偵測虛擬環境位置 (優先找同層，再找上一層)
set VENV_PATH=
if exist ".venv\Scripts\activate.bat" (
    set VENV_PATH=".venv\Scripts\activate.bat"
) else if exist "..\.venv\Scripts\activate.bat" (
    set VENV_PATH="..\.venv\Scripts\activate.bat"
)

if defined VENV_PATH (
    echo [成功] 找到虛擬環境於: %VENV_PATH%
    call %VENV_PATH%
) else (
    echo [警告] 找不到虛擬環境 (.venv)，將嘗試使用系統環境啟動...
)

:: 3. 執行 Streamlit
echo 伺服器啟動中，請稍候...
:: 使用 python -m streamlit 啟動更穩健
python -m streamlit run app_v2.py --server.port 8502

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [錯誤] 啟動失敗！請確認是否已安裝 requirements.txt 中的套件。
    pause
)

pause
