import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters

# ตั้งค่าระบบ Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# สร้างเว็บเซิร์ฟเวอร์จำลองสำหรับ Render (ป้องกันระบบสลีป)
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Discord Bot Controller is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# คำสั่งเริ่มต้น /start ใน Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 ยินดีต้อนรับสู่ระบบควบคุมบอท Discord!\n\n"
        "คำสั่งที่ใช้งานได้:\n"
        "/status - ตรวจสอบสถานะบอท 24 ชม.\n"
        "/help - ดูวิธีใช้งานคำสั่งต่างๆ"
    )

# คำสั่งเช็คสถานะ /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 สถานะระบบ: บอทออนไลน์และทำงานอยู่บน Render ตลอด 24 ชั่วโมงแล้วครับ!")

def main():
    # ใช้ Token เดิมของคุณจากโปรเจกต์บอท @c1_ipa_bot
    TOKEN = "9179167213:AAHyJgbGjyDQc6pRNxJbKJuutAmOJA53f7s"
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    # ลงทะเบียนคำสั่งต่างๆ
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    
    print("Telegram Controller Bot กำลังทำงาน...")
    application.run_polling()

if __name__ == '__main__':
    # เปิดเว็บเซิร์ฟเวอร์ใน Background Thread
    t = threading.Thread(target=run_flask)
    t.start()
    
    # รันบอท Telegram
    main()
