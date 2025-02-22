@echo off
cd /d "disi dengan folder patch dimana tempat penyimpanan hasil extract milik user"

:: Cek apakah Python sudah terinstall
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python tidak ditemukan! Pastikan Python sudah terinstall dan ditambahkan ke PATH.
    pause
    exit /b
)

:: Cek apakah virtual environment sudah dibuat
if not exist venv (
    echo Membuat virtual environment...
    python -m venv venv
)

:: Aktifkan virtual environment
call venv\Scripts\activate

:: Install dependensi jika belum ada
pip install --upgrade pip
pip install flask pypdf2

:: Jalankan aplikasi Flask
start "Flask App" cmd /c "python app.py"

:: Tunggu sebentar sebelum membuka browser
timeout /t 3 /nobreak >nul

:: Buka browser secara otomatis
start http://127.0.0.1:5000

pause
