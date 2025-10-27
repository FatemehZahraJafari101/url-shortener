from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import string, random, json, os

app = FastAPI(title="🔗 URL Shortener API", version="1.0")

DB_FILE = "database.json"

# اگر فایل دیتابیس وجود ندارد، بسازش
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.get("/")
def home():
    return {"message": "Welcome to the URL Shortener API!"}

@app.post("/shorten")
def shorten_url(url: str):
    """دریافت لینک بلند و ساخت لینک کوتاه"""
    data = load_db()

    # چک کن که آیا لینک قبلاً کوتاه شده
    for short, long in data.items():
        if long == url:
            return {"short_url": f"http://localhost:8000/{short}"}

    short_code = generate_short_code()
    data[short_code] = url
    save_db(data)
    return {"short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    """هدایت به لینک اصلی"""
    data = load_db()
    if short_code not in data:
        raise HTTPException(status_code=404, detail="Short link not found")
    return RedirectResponse(data[short_code])
