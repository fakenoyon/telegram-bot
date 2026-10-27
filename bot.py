from datetime import datetime, timedelta
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

TOKEN = "8864206014:AAHr0J3I7zMbPr87nKyupQnvgtXcXcseemM"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
      [InlineKeyboardButton("⚡ Get Signal", callback_data="get_signal")]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  welcome_text = (
      "👋 Hello! Trading Signal Bot-এ আপনাকে স্বাগতম।\n\nনিচের **Get Signal**"
      " বাটনে ক্লিক করে পরবর্তী ক্যান্ডেলের সিগন্যাল নিন।"
  )

  if update.message:
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
  elif update.callback_query:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(welcome_text, reply_markup=reply_markup)


async def send_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/CAD", "EUR/GBP", "USD/MXN"]
  selected_pair = random.choice(pairs)

  signal_type = random.choice(["🟢 CALL (BUY) 📈", "🔴 PUT (SELL) 📉"])

  # বর্তমান মিনিটের সাথে ১ মিনিট যোগ করে পরবর্তী মিনিটের টাইম সেট করা
  now = datetime.now()
  next_min = now + timedelta(minutes=1)

  entry_time = next_min.strftime("%H:%M")
  expiry_time = (next_min + timedelta(minutes=1)).strftime("%H:%M")

  risk_level = random.choice(["🟢 Low", "🟢 Medium-Low"])
  confidence = random.choice(["88%", "90%", "92%", "95%"])

  signal_message = (
      f"━━━━━━━━━━━━━━━━━━━\n"
      f"   {signal_type}\n"
      f"━━━━━━━━━━━━━━━━━━━\n\n"
      f"🌐 Pair: {selected_pair}\n"
      f"📊 Market: OTC Market • 24/7\n"
      f"⏱️ Entry Minute: {entry_time}\n"
      f"⏰ Expiry Minute: {expiry_time} (1 Min)\n\n"
      f"⭐ NEXT CANDLE SETUP\n"
      f"🛡️ Risk: {risk_level}\n"
      f"📊 Confidence: {'█' * 8} {confidence}\n\n"
      f"⚡ ENTER ON {entry_time} ⚡\n"
      f"━━━━━━━━━━━━━━━━━━━"
  )

  keyboard = [
      [InlineKeyboardButton("⚡ Get Signal", callback_data="get_signal")]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  await query.message.reply_text(signal_message, reply_markup=reply_markup)


if __name__ == "__main__":
  app = ApplicationBuilder().token(TOKEN).build()

  app.add_handler(CommandHandler("start", start))
  app.add_handler(CallbackQueryHandler(send_signal, pattern="get_signal"))

  print("বটটি নিখুঁত টাইম আপডেটে চালু হয়েছে...")
  app.run_polling()