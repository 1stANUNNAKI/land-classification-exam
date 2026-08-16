# Emotion Detector — المتطلبات

مشروع التخرج النهائي: تطبيق ويب لكشف العواطف بـ **Watson NLP + Flask**.
التقييم: 8 مهام × أنشطة = **16 نقطة** — النجاح ≥ 12 (75%).

| المهمة | النقاط | ما يُرفع لكل نشاط |
|---|---|---|
| Task 1: مستودع GitHub العام | 1 | رابط README.md (اسم المشروع) |
| Task 2: تطبيق Watson NLP (emotion_detection.py) | 2 | كود الدالة + مخرجات طرفية (استيراد/تطبيق بلا أخطاء) |
| Task 3: تنسيق المخرجات | 2 | كود `emotion_detector` المعدّل + مخرجات تؤكد التنسيق |
| Task 4: حزمة EmotionDetection (`__init__.py`) | 2 | رابط ملف `__init__.py` + مخرجات صلاحية الحزمة |
| Task 5: اختبارات الوحدة (test_emotion_detection.py) | 2 | كود الاختبارات + مخرجات كل الاختبارات نجحت |
| Task 6: نشر Flask (server.py) | 2 | كود `server.py` + لقطة `6b_deployment_test.png` |
| Task 7: معالجة الأخطاء | 3 | كود status 400 + كود الإدخال الفارغ + لقطة `7c_error_handling_interface.png` |
| Task 8: تحليل كود ثابت (pylint) | 2 | كود `server.py` (تحليل) + مخرجات علامة كاملة 10/10 |

## هيكل المجلدات (وضع كل متطلب هنا)

```
emotion-detector/
├── Task_1_repository/        # رابط المستودع + README
├── Task_2_watson_app/        # emotion_detection.py + مخرجات test.py
├── Task_3_output_format/     # الدالة المعدّلة + مخرجات التنسيق
├── Task_4_package/           # EmotionDetection/__init__.py + مخرجات الحزمة
├── Task_5_unit_tests/        # test_emotion_detection.py + مخرجات unittest
├── Task_6_flask_deployment/  # server.py + 6b_deployment_test.png
├── Task_7_error_handling/    # status 400 + blank input + 7c_error_handling_interface.png
└── Task_8_static_analysis/   # pylint على server.py + علامة 10/10
```

## التبعيات
- IBM Cloud مجاني → خدمة Watson NLU: **API Key + URL** (تُملأ في `credentials.env` — لا تُرفع)
- `watson-developer-cloud`, `flask`, `pylint`, `unittest`

## متطلبات استخراج العواطف المتوقعة (ناتج API)
`anger, disgust, fear, joy, sadness` — التنسيق المطلوب:
```
return {'anger': ..., 'disgust': ..., 'fear': ..., 'joy': ..., 'sadness': ...,
        'dominant_emotion': <الأعلى>}
```