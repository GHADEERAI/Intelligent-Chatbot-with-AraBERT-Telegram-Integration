import json
import random
from difflib import SequenceMatcher

# تحميل البيانات مع معالجة الخطأ في حال لم يكن الملف موجوداً
def load_data():
    try:
        with open("qa_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

data = load_data()

def get_similarity(a, b):
    # وظيفة هذه الدالة هي حساب نسبة التشابه بين جملة المستخدم وقاعدة البيانات
    return SequenceMatcher(None, a, b).ratio()

def save_new_question(question):
    # حفظ أي سؤال لم يعرفه البوت ليتعلمه لاحقاً
    new_entry = {"question": question, "answer": "هذا سؤال جديد 🤖 سأتعلمه لاحقاً."}
    data.append(new_entry)
    with open("qa_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_answer(user_text):
    text = user_text.lower().strip()
    
    # ردود سريعة جداً للترحيب
    if any(word in text for word in ["مرحبا", "اهلا", "هلا", "هاي"]):
        return random.choice(["أهلاً بك! 😊", "يا هلا والله نورت", "مرحباً، كيف أقدر أساعدك؟"])

    best_match = None
    highest_ratio = 0
    
    # البحث في أول 10 آلاف جملة لضمان السرعة (أو ابحث في الكل)
    for item in data[:10000]: 
        ratio = get_similarity(text, item["question"].lower())
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = item["answer"]
        
        # إذا وجدنا تطابق ممتاز (أكثر من 90%) نكتفي به فوراً للسرعة
        if highest_ratio > 0.9: 
            break

    # إذا كانت نسبة التشابه أكثر من 60% نعتبر الجواب صحيحاً (يغطي الأخطاء الإملائية)
    if highest_ratio > 0.6: 
        return best_match
    else:
        save_new_question(user_text) # يحفظ السؤال الجديد
        return "لم أفهم السؤال تماماً.. ولكن تم حفظه في ذاكرتي لأتعلمه قريباً! 🤖"