# Emotion Detector

**Emotion Detector** — تطبيق ويب لاكتشاف العواطف في النصوص باستخدام
**IBM Watson Natural Language Understanding (NLP)** و **Flask**.

يقوم التطبيق بتحليل أي عبارة نصية ويرجع درجات المشاعر الخمس
(**anger, disgust, fear, joy, sadness**) مع تحديد **المشاعر السائدة (dominant emotion)**.

## المتطلبات / المهام (16 نقطة — النجاح ≥ 12)

| المهمة | النشاطات | ملف التسليم |
|---|---|---|
| Task 1: المستودع العام | نشاط 1 | رابط `README.md` (هذا الملف) |
| Task 2: تطبيق Watson NLP | نشاطان | `emotion_detection.py` + `2b_application_creation` |
| Task 3: تنسيق المخرجات | نشاطان | `3a_output_formatting` + `3b_formatted_output_test` |
| Task 4: حزمة EmotionDetection | نشاطان | `EmotionDetection/__init__.py` + `4b_packaging_test` |
| Task 5: اختبارات الوحدة | نشاطان | `test_emotion_detection.py` + `5b_unit_testing_result` |
| Task 6: نشر Flask | نشاطان | `server.py` + `6b_deployment_test.png` |
| Task 7: معالجة الأخطاء | 3 أنشطة | `7a_error_handling_function` + `7b_error_handling_server` + `7c_error_handling_interface.png` |
| Task 8: تحليل كود ثابت | نشاطان | `8a_server_modified` + `8b_static_code_analysis` (pylint 10.00/10) |

## هيكل المشروع

```
emotion-detector/
├── README.md
├── requirements.txt
├── test_emotion_detection.py
├── EmotionDetection/
│   ├── __init__.py
│   ├── emotion_detection.py
│   ├── server.py
│   ├── templates/index.html
│   └── static/mywebscript.js
├── scripts/                    (أدوات تطوير: مخرجات تجريبية + لقطات)
└── Task_1_repository/ ... Task_8_static_analysis/   (ملفات التسليم)
```

## التشغيل

```bash
pip install -r requirements.txt

# ضع بيانات IBM Cloud (حساب مجاني → خدمة Natural Language Understanding):
export WATSON_API_KEY="<API_KEY>"
export WATSON_URL="<SERVICE_URL>"

# اختبارات الوحدة
python -m unittest -v test_emotion_detection

# تشغيل الخادم (مع تشغيل pylint تلقائياً على server.py)
python EmotionDetection/server.py
# ثم افتح: http://127.0.0.1:5000/
```

## تنسيق المخرجات

```
emotion_detector("I am so glad this happened")
-> {'anger': 0.012, 'disgust': 0.008, 'fear': 0.012,
    'joy': 0.902, 'sadness': 0.066, 'dominant_emotion': 'joy'}
```

- الإدخال الفارغ أو استجابة Watson **400** → كل القيم `None`
- `server.py` يعالج الإدخال الفارغ ويرجع: `Invalid text! Please try again!`
- تشغيل الخادم ينفذ **التحليل الساكن** عبر pylint ويعرض العلامة (10.00/10)