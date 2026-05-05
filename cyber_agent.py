# ---------------------------------------------------------------
# Project: Cyber Intelligence Agent
# Developer: إيلاف عبدالعزيز آل حمد
# Field: Cybersecurity
# Features: Tools + Memory + ReAct Loop (Full AI Agent)
# ---------------------------------------------------------------

import os
import json
import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

# ---------------------------------------------------------------
# (1) تحميل المفتاح السري من ملف .env
# ---------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ---------------------------------------------------------------
# (2) إعداد النموذج الذكي
# ---------------------------------------------------------------
llm = ChatOpenAI(model="gpt-4o", api_key=api_key, temperature=0)

# ---------------------------------------------------------------
# (3) تعريف الأدوات (Tools) — هذا ما يجعله Agent حقيقي
# ---------------------------------------------------------------

@tool
def analyze_threat(threat_description: str) -> str:
    """
    تحليل التهديد الأمني وتصنيفه حسب درجة الخطورة.
    استخدم هذه الأداة عندما يصف المستخدم هجوماً أو تهديداً أمنياً.
    """
    threat_lower = threat_description.lower()
    
    # تصنيف التهديدات
    if any(word in threat_lower for word in ["ransomware", "فدية", "encrypt", "تشفير"]):
        category = "Ransomware Attack"
        severity = "CRITICAL 🔴"
        action = "افصل الجهاز عن الشبكة فوراً وتواصل مع فريق الاستجابة"
    elif any(word in threat_lower for word in ["phishing", "تصيد", "email", "بريد"]):
        category = "Phishing Attack"
        severity = "HIGH 🟠"
        action = "لا تضغط على أي رابط، أبلغ فريق IT، غيّر كلمات المرور"
    elif any(word in threat_lower for word in ["ddos", "flood", "حجب", "denial"]):
        category = "DDoS Attack"
        severity = "HIGH 🟠"
        action = "فعّل حماية DDoS، تواصل مع مزود الخدمة"
    elif any(word in threat_lower for word in ["sql", "injection", "حقن"]):
        category = "SQL Injection"
        severity = "HIGH 🟠"
        action = "أوقف الخدمة المتأثرة، راجع logs قاعدة البيانات"
    elif any(word in threat_lower for word in ["malware", "virus", "فيروس", "trojan"]):
        category = "Malware Infection"
        severity = "MEDIUM 🟡"
        action = "شغّل برنامج مكافحة الفيروسات، عزل الجهاز المصاب"
    else:
        category = "Unknown Threat"
        severity = "MEDIUM 🟡"
        action = "تحليل إضافي مطلوب، راجع مع خبير أمني"
    
    result = {
        "threat_type": category,
        "severity": severity,
        "recommended_action": action,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def check_password_strength(password: str) -> str:
    """
    فحص قوة كلمة المرور وإعطاء توصيات لتحسينها.
    استخدم هذه الأداة عندما يطلب المستخدم فحص كلمة مرور.
    """
    score = 0
    feedback = []
    
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        feedback.append("زد طول كلمة المرور إلى 12 حرف على الأقل")
    else:
        feedback.append("⚠️ كلمة المرور قصيرة جداً")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("أضف أحرف كبيرة (A-Z)")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("أضف أحرف صغيرة (a-z)")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("أضف أرقام (0-9)")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 2
    else:
        feedback.append("أضف رموز خاصة (!@#$%)")
    
    common_passwords = ["password", "123456", "admin", "qwerty", "letmein"]
    if password.lower() in common_passwords:
        score = 0
        feedback = ["❌ هذه كلمة مرور شائعة جداً وسهلة التخمين!"]
    
    if score >= 6:
        strength = "قوية جداً 💚"
    elif score >= 4:
        strength = "متوسطة 🟡"
    elif score >= 2:
        strength = "ضعيفة 🟠"
    else:
        strength = "خطيرة جداً 🔴"
    
    result = {
        "strength": strength,
        "score": f"{score}/7",
        "improvements": feedback if feedback else ["✅ كلمة المرور ممتازة!"]
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def get_security_tips(topic: str) -> str:
    """
    الحصول على نصائح أمنية حول موضوع معين.
    استخدم هذه الأداة عندما يسأل المستخدم عن نصائح أمنية عامة.
    """
    tips_database = {
        "network": [
            "🔒 استخدم VPN عند الاتصال بشبكات WiFi عامة",
            "🛡️ فعّل جدار الحماية (Firewall) دائماً",
            "📡 غيّر كلمة مرور الراوتر الافتراضية",
            "🔍 راقب الأجهزة المتصلة بشبكتك بانتظام",
            "⚡ حدّث firmware الراوتر بانتظام"
        ],
        "email": [
            "📧 لا تفتح مرفقات من مصادر مجهولة",
            "🔗 تحقق من الروابط قبل الضغط عليها",
            "✉️ فعّل المصادقة الثنائية للبريد",
            "🚨 تعلّم كيف تميّز رسائل التصيد",
            "🔐 لا تشارك كلمة مرور بريدك مع أحد"
        ],
        "password": [
            "🔑 استخدم كلمات مرور مختلفة لكل حساب",
            "📱 استخدم تطبيق Password Manager",
            "🔄 غيّر كلمات المرور كل 3 أشهر",
            "❌ لا تستخدم معلوماتك الشخصية في كلمة المرور",
            "✅ فعّل المصادقة الثنائية (2FA) دائماً"
        ],
        "general": [
            "💻 حدّث نظام التشغيل والتطبيقات باستمرار",
            "💾 احتفظ بنسخ احتياطية منتظمة لبياناتك",
            "🔒 لا تشارك معلوماتك الشخصية على الإنترنت",
            "📱 قفّل شاشة جهازك دائماً",
            "🎓 تعلّم أساسيات الأمن السيبراني"
        ]
    }
    
    topic_lower = topic.lower()
    if any(word in topic_lower for word in ["network", "شبكة", "wifi", "واي فاي"]):
        tips = tips_database["network"]
        category = "أمان الشبكة"
    elif any(word in topic_lower for word in ["email", "بريد", "phishing", "تصيد"]):
        tips = tips_database["email"]
        category = "أمان البريد الإلكتروني"
    elif any(word in topic_lower for word in ["password", "كلمة مرور", "باسورد"]):
        tips = tips_database["password"]
        category = "أمان كلمات المرور"
    else:
        tips = tips_database["general"]
        category = "نصائح عامة"
    
    result = {
        "category": category,
        "tips": tips
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------
# (4) System Prompt — هوية الـ Agent
# ---------------------------------------------------------------
SYSTEM_PROMPT = """أنت Elaf Cyber AI — وكيل ذكاء اصطناعي متخصص في الأمن السيبراني.

## دورك:
مساعدة المستخدمين في تحليل التهديدات الأمنية وحماية أنظمتهم.

## الأدوات المتاحة لك:
- analyze_threat: تحليل أي تهديد أمني وتصنيفه
- check_password_strength: فحص قوة كلمة المرور
- get_security_tips: تقديم نصائح أمنية حسب الموضوع

## تعليمات مهمة:
- استخدم الأدوات المناسبة تلقائياً حسب سؤال المستخدم
- أجب دائماً باللغة العربية
- كن دقيقاً وعملياً في توصياتك
- إذا لم تكن متأكداً، اطلب توضيحاً

## حدودك:
- لا تقدم معلومات يمكن استخدامها للهجوم على أنظمة
- ركّز على الدفاع والحماية فقط"""

# ---------------------------------------------------------------
# (5) إنشاء الـ Agent مع الذاكرة (Memory)
# ---------------------------------------------------------------
memory = MemorySaver()

agent = create_react_agent(
    model=llm,
    tools=[analyze_threat, check_password_strength, get_security_tips],
    prompt=SYSTEM_PROMPT,
    checkpointer=memory
)

# ---------------------------------------------------------------
# (6) واجهة المستخدم التفاعلية
# ---------------------------------------------------------------
def run_cyber_agent():
    print("=" * 60)
    print("🛡️  Elaf Cyber AI System is Online")
    print("   مرحباً بك في منصة التحليل الأمني الذكية")
    print("=" * 60)
    print("💡 يمكنك:")
    print("   • تحليل تهديدات: 'تعرضت لهجوم ransomware'")
    print("   • فحص كلمة مرور: 'افحص كلمة المرور: MyPass123'")
    print("   • نصائح أمنية: 'نصائح لأمان الشبكة'")
    print("   • اكتب 'خروج' للإنهاء")
    print("=" * 60)
    
    session_id = "cyber-session-001"
    config = {"configurable": {"thread_id": session_id}}
    
    while True:
        print()
        user_query = input("🔍 سؤالك الأمني: ").strip()
        
        if not user_query:
            continue
        
        if user_query.lower() in ["خروج", "exit", "quit"]:
            print("\n✅ شكراً لاستخدام Elaf Cyber AI. ابقَ آمناً! 🛡️")
            break
        
        print("\n⚙️  الوكيل يعمل...")
        print("-" * 40)
        
        try:
            result = agent.invoke(
                {"messages": [("user", user_query)]},
                config=config
            )
            
            final_response = result["messages"][-1].content
            print(f"\n🤖 التحليل الأمني:\n{final_response}")
            
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
        
        print("-" * 40)


# ---------------------------------------------------------------
# (7) تشغيل البرنامج
# ---------------------------------------------------------------
if __name__ == "__main__":
    run_cyber_agent()