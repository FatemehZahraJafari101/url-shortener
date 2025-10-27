from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import string, random, json, os

app = FastAPI(title="🔗 URL Shortener Web")

DB_FILE = "database.json"

# مسیر قالب‌ها
templates = Jinja2Templates(directory="templates")

# ایجاد فایل دیتابیس اگر وجود ندارد
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

# -----------------------------
# مسیر صفحه اصلی
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "short_url": None})

# -----------------------------
# پردازش فرم لینک کوتاه
# -----------------------------
@app.post("/", response_class=HTMLResponse)
def shorten_url(request: Request, url: str = Form(...)):
    data = load_db()

    # بررسی اینکه لینک قبلاً کوتاه شده
    for short, long in data.items():
        if long == url:
            short_url = f"http://localhost:8000/{short}"
            return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url})

    short_code = generate_short_code()
    data[short_code] = url
    save_db(data)
    short_url = f"http://localhost:8000/{short_code}"

    return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url})

# -----------------------------
# هدایت به لینک اصلی
# -----------------------------
@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    data = load_db()
    if short_code not in data:
        return HTMLResponse("<h2>❌ لینک کوتاه پیدا نشد!</h2>", status_code=404)
    return RedirectResponse(data[short_code])
