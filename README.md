# 🤖 Internship Application Bot

Aiogram 3.x yordamida yaratilgan Telegram bot. Foydalanuvchilardan amaliyot arizasi qabul qiladi va Telegram kanalga yuboradi.

## 📁 Loyiha tuzilmasi

```
intern_bot/
├── bot.py              # Asosiy entry point
├── config.py           # Konfiguratsiya
├── database.py         # SQLite CRUD
├── keyboards.py        # Barcha klaviaturalar
├── states.py           # FSM holatlari
├── handlers/
│   ├── user.py         # Foydalanuvchi handlerlari
│   └── admin.py        # Admin panel handlerlari
├── .env                # 🔑 Muhit o'zgaruvchilari (BU FAYLNI TO'LDIRING)
├── requirements.txt
└── README.md
```

---

## ⚙️ O'rnatish

### 1. Python virtual muhit yarating (tavsiya etiladi)
```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 2. Kutubxonalarni o'rnating
```bash
pip install -r requirements.txt
```

### 3. `.env` faylini to'ldiring
```env
BOT_TOKEN=7123456789:AAF...       # @BotFather dan olingan token
CHANNEL_ID=@my_channel            # Kanal username yoki -100xxxxxxxxxx
ADMIN_IDS=123456789               # Sizning Telegram user ID (vergul bilan bir nechta)
```

> **Bot token olish:** [@BotFather](https://t.me/BotFather) ga /newbot yuboring  
> **User ID olish:** [@userinfobot](https://t.me/userinfobot) ga /start yuboring  
> **Channel ID:** Bot kanalga admin sifatida qo'shilgan bo'lishi kerak!

### 4. Botni ishga tushiring
```bash
python bot.py
```

---

## 🚀 Deploy (Railway yoki VPS)

### Railway.app (Bepul, eng oson)
1. [railway.app](https://railway.app) ga kiring
2. "New Project" → "Deploy from GitHub repo"
3. Environment variables qo'shing (BOT_TOKEN, CHANNEL_ID, ADMIN_IDS)
4. Deploy!

### Systemd service (VPS uchun)
```bash
# /etc/systemd/system/intern_bot.service
[Unit]
Description=Intern Application Bot
After=network.target

[Service]
WorkingDirectory=/path/to/intern_bot
ExecStart=/path/to/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable intern_bot
sudo systemctl start intern_bot
```

---

## 📋 Bot buyruqlari

| Buyruq | Tavsif |
|--------|--------|
| `/start` | Botni ishga tushirish |
| `/admin` | Admin panel (faqat adminlar) |

---

## ✅ Funksiyalar

- [x] Ariza boshlash (`/start` → tugma)
- [x] Ism/familiya yig'ish
- [x] Telefon raqam (kontakt ulashish yoki qo'lda)
- [x] Yo'nalish tanlash (inline klaviatura)
- [x] Texnologiyalar
- [x] Portfolio/GitHub
- [x] Ariza tasdiqlash
- [x] Kanalga yuborish
- [x] **Bonus:** SQLite database ga saqlash
- [x] **Bonus:** Admin panel (arizalar ro'yxati, statistika)
