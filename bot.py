import os
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ตั้งค่า Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. เว็บเซิร์ฟเวอร์จำลองสำหรับ Render (ป้องกันระบบสลีป)
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "C1 Cloud Station Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# 2. โค้ดบอท Telegram สำหรับส่งลิงก์ดาวน์โหลด
TARGET_APP_ID = "6808957385"  # ID ของแอป C1 Cloud Station

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # ตรวจสอบลิงก์ App Store และ ID แอป
    if "apps.apple.com" in text and TARGET_APP_ID in text:
        # สร้างปุ่มลิงก์ดาวน์โหลดไฟล์ .ipa จากแหล่งภายนอก (คุณสามารถเปลี่ยน URL ด้านล่างเป็นลิงก์ไฟล์ .ipa จริงๆ ของคุณได้)
        download_url = "https://example.com/c1_cloud_station.ipa"  # <-- เปลี่ยนเป็นลิงก์ไฟล์ .ipa ของคุณ
        
        keyboard = [
            [InlineKeyboardButton("📥 ดาวน์โหลดไฟล์ .ipa", url=download_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📲 พบบัตรคิวแอป C1 Cloud Station แล้ว! สามารถกดดาวน์โหลดไฟล์ .ipa ได้จากปุ่มด้านล่างนี้เลยครับ:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("บอทนี้รองรับเฉพาะลิงก์แอป C1 Cloud Station เท่านั้นครับ")

def main():
    TOKEN = "9179167213:AAHyJgbGjyDQc6pRNxJbKJuutAmOJA53f7s"
        
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Telegram Bot เริ่มทำงานแล้ว...")
    application.run_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_flask)
    t.start()
    main()
