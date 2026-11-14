import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ตั้งค่า Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. สร้างเว็บเซิร์ฟเวอร์จำลองสำหรับ Render (ป้องกันระบบสลีป)
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "C1 Cloud Station Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# 2. โค้ดหลักของบอท Telegram
TARGET_APP_ID = "6808957385"  # ID ของแอป C1 Cloud Station

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # ตรวจสอบลิงก์ App Store และ ID แอป
    if "apps.apple.com" in text and TARGET_APP_ID in text:
        await update.message.reply_text("⏳ กำลังเตรียมไฟล์ .ipa ของ C1 Cloud Station ส่งให้คุณ...")
        
        ipa_filename = "c1_cloud_station.ipa"
        
        try:
            if os.path.exists(ipa_filename):
                with open(ipa_filename, 'rb') as ipa_file:
                    await update.message.reply_document(
                        document=ipa_file,
                        caption="📲 นี่คือไฟล์ .ipa ของ C1 Cloud Station พร้อมติดตั้งครับ!"
                    )
            else:
                await update.message.reply_text("⚠️ ไม่พบไฟล์ `c1_cloud_station.ipa` ในระบบเซิร์ฟเวอร์")
        except Exception as e:
            await update.message.reply_text(f"⚠️ เกิดข้อผิดพลาด: {str(e)}")
    else:
        await update.message.reply_text("บอทนี้รองรับเฉพาะลิงก์แอป C1 Cloud Station เท่านั้นครับ")

def main():
    # ดึง Token จาก Environment Variable บน Render
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:9179167213:AAHyJgbGjyDQc6pRNxJbKJuutAmOJA53f7s
        print("Error: BOT_TOKEN environment variable not set!")
        return
        
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Telegram Bot เริ่มทำงานแล้ว...")
    application.run_polling()

if __name__ == '__main__':
    # เปิด Flask ใน Background Thread
    t = threading.Thread(target=run_flask)
    t.start()
    
    # รันบอท Telegram
    main()
