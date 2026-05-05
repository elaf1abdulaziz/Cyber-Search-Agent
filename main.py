# ---------------------------------------------------------
# Project: Cyber Intelligence Assistant
# Developer: ايلاف عبدالعزيز ال حمد
# Field: Cybersecurity 
# ---------------------------------------------------------

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# تحميل المفتاح السري من ملف .env (تطبيق معايير حماية البيانات الحساسة)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# إعداد الوكيل الذكي (Model: GPT-4o)
chat = ChatOpenAI(model="gpt-4o", api_key=api_key)

# واجهة النظام الترحيبية
print(f"--- Elaf Cyber AI System is Online ---")
print("مرحباً بك في منصة التحليل الأمني الذكية.")

# جعل البرنامج تفاعلياً لاستقبال الاستفسارات التقنية
user_query = input("ما هو موضوع بحثنا الأمني اليوم؟ ")

# معالجة الطلب عبر الوكيل الذكي
response = chat.invoke(user_query)

print("-" * 30)
print(f"نتائج التحليل التقني: \n{response.content}")