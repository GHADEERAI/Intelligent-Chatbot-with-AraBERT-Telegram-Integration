import json
import os

def update_database():
    database_file = 'qa_data.json'
    log_file = 'unanswered_questions.txt'

    if not os.path.exists(log_file):
        print("❌ لا توجد أسئلة جديدة بانتظار الإجابة حالياً.")
        return

    # تحميل قاعدة البيانات الحقيقية
    with open(database_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(log_file, 'r', encoding='utf-8') as f:
        unknown_questions = f.readlines()

    if not unknown_questions:
        print("✅ تم معالجة جميع الأسئلة سابقاً.")
        return

    print(f"📌 لديك {len(unknown_questions)} أسئلة لم يفهمها البوت:")
    
    remaining_questions = []
    for line in unknown_questions:
        # استخراج السؤال من السطر (بعد التاريخ)
        if "السؤال: " in line:
            question = line.split("السؤال: ")[1].strip()
            print(f"\n--- السؤال الحالي: {question} ---")
            answer = input("اكتب الإجابة (أو اضغط Enter لتجاوز السؤال): ")

            if answer:
                print("اختر القسم المناسب للإضافة:")
                print("1: ذكاء اصطناعي | 2: برمجة | 3: دراسة | 4: دين | 5: ترحيب | 6: منوعات")
                choice = input("رقم القسم: ")
                
                categories = {
                    "1": "AI_Science", "2": "Programming", "3": "Education",
                    "4": "Religion", "5": "Greetings", "6": "General"
                }
                
                category_name = categories.get(choice, "General")
                
                # إضافة السؤال والجواب لقاعدة البيانات
                data[category_name].append({
                    "question": question,
                    "answers": [answer]
                })
                print(f"✅ تمت إضافة السؤال إلى قسم {category_name}")
            else:
                remaining_questions.append(line)

    # حفظ التحديثات في الملف الأساسي
    with open(database_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # تحديث ملف الأسئلة المتبقية (التي لم تجب عليها)
    with open(log_file, 'w', encoding='utf-8') as f:
        f.writelines(remaining_questions)

    print("\n🎉 تم تحديث قاعدة البيانات بنجاح!")

if __name__ == "__main__":
    update_database()