@echo off
cd /d %~dp0
call venv\Scripts\activate
pyinstaller --noconfirm --onedir --noconsole --name EasyBGRemover ^
  --icon app.ico ^
  --add-data "models;models" ^
  --add-data "app.ico;." ^
  --add-data "demo_before_1.png;." ^
  --add-data "demo_after_1.png;." ^
  --add-data "demo_before_2.png;." ^
  --add-data "demo_after_2.png;." ^
  --add-data "demo_before_3.png;." ^
  --add-data "demo_after_3.png;." ^
  --collect-all onnxruntime ^
  --exclude-module rembg ^
  --exclude-module pymatting ^
  --exclude-module numba ^
  --exclude-module llvmlite ^
  --exclude-module scipy ^
  --exclude-module skimage ^
  --exclude-module matplotlib ^
  --exclude-module pooch ^
  main.py
echo === BUILD FINISHED ===
