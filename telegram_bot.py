import telebot
import json
import random
from datetime import datetime

# 1. إعدادات البوت (التوكن الجديد الخاص بكِ)
TOKEN = '8205570396:AAG4MrweCMWWBakSQw_z-FN-Ofp83YAFswM'
bot = telebot.TeleBot(TOKEN)

# 2. دالة تنظيف النص (لتوحيد الإملاء: أ، إ، آ، ة، هـ)
def normalize_text(text):
    if not text: return ""
    text = text.strip().lower()
    replacements = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
        'ة': 'ه', 'ى': 'ي', 'ؤ': 'و', 'ئ': 'ي'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

# 3. دالة تسجيل الأسئلة التي لم يفهمها البوت للتعلم لاحقاً
def log_unknown(question):
    try:
        with open('unanswered_questions.txt', 'a', encoding='utf-8') as f:
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{time_str}] السؤال الجديد: {question}\n")
    except:
        pass

# 4. محرك البحث الذكي (يبحث عن التطابق التام ثم التشابه)
def get_bot_response(user_msg):
    user_msg_clean = normalize_text(user_msg)
    
    try:
        # فتح ملف الـ 10,000 سؤال
        with open('qa_data.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
            
        # المرحلة الأولى: البحث عن تطابق "كامل" (لضمان الدقة في الترحيب وغيره)
        for category in database:
            for item in database[category]:
                if user_msg_clean == normalize_text(item['question']):
                    return random.choice(item['answers'])
        
        # المرحلة الثانية: البحث عن "تشابه جزئي" (إذا كان السؤال جزء من جملة)
        for category in database:
            for item in database[category]:
                db_q_clean = normalize_text(item['question'])
                if user_msg_clean in db_q_clean or db_q_clean in user_msg_clean:
                    return random.choice(item['answers'])
                    
    except Exception as e:
        return f"⚠️ خطأ في قراءة ملف qa_data.json: {str(e)}"

    # المرحلة الثالثة: إذا لم يجد إجابة في كل الملف
    log_unknown(user_msg)
    return "عذراً، لم أفهم سؤالك تماماً.. ولكن تم حفظه في ذاكرتي لأتعلمه قريباً! 🤖"

# 5. التعامل مع الرسائل القادمة من تليجرام
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    response = get_bot_response(message.text)
    bot.reply_to(message, response)

# 6. تشغيل البوت
if __name__ == "__main__":
    print("---")
    print("🚀 بوت IntelliGhadeer شغال الآن بنجاح!")
    print("🤖 جربي مراسلته بـ 'مرحبا' أو 'ما هو الذكاء الاصطناعي'")
    print("---")
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"❌ حدث خطأ في الاتصال: {e}")