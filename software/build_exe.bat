@echo off
chcp 65001 >nul
echo === Blog Manager 打包工具 ===
echo.
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo 安装失败，请手动运行: pip install pyinstaller
        pause >nul
        exit /b 1
    )
)
echo 正在打包...
pyinstaller --onefile --add-data "manager_ui.html;." --name BlogManager manager.py
if errorlevel 1 (
    echo 打包失败！
    pause >nul
    exit /b 1
)
echo.
echo 打包成功！文件位于: dist\BlogManager.exe
echo.
echo 双击 BlogManager.exe 启动，浏览器自动打开 http://localhost:8080
pause >nul
