from flask import Flask, jsonify
import requests

# ساخت اپلیکیشن وب
app = Flask(__name__)

# آدرس API اصلی نوبیتکس
NOBITEX_API_URL = "https://api.nobitex.ir/market/orderbook/BTCUSDT"

@app.route("/")
def index():
    """صفحه اصلی برای اطمینان از بالا بودن سرویس"""
    return "Nobitex Personal Mirror is running. Use /api/orderbook/BTCUSDT endpoint.", 200

@app.route("/api/orderbook/BTCUSDT")
def get_orderbook():
    """
    این تابع به عنوان پروکسی عمل کرده، داده را از نوبیتکس می‌گیرد
    و به ربات شما برمی‌گرداند.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        # ارسال درخواست به API اصلی نوبیتکس
        response = requests.get(NOBITEX_API_URL, headers=headers, timeout=10)
        
        # اگر درخواست موفق بود، داده JSON را برگردان
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            # در صورت بروز خطا در سمت نوبیتکس، همان خطا را برگردان
            return jsonify({"error": "Failed to fetch from Nobitex API", "status": response.status_code}), response.status_code

    except Exception as e:
        # در صورت بروز خطای شبکه یا تایم‌اوت
        return jsonify({"error": str(e), "status": 500}), 500

# این بخش برای اجرای محلی است و روی سرور استفاده نمی‌شود
if __name__ == "__main__":
    app.run(debug=True)
