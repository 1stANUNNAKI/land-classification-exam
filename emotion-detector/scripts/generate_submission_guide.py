#!/usr/bin/env python3
"""Generates SUBMISSION_GUIDE.md - the organized, paste-ready answers for the
16 Emotion Detector questions. Content is inlined from the actual deliverable
files so it always matches the real submission files."""
import os

ROOT = r"D:\امتحان\emotion-detector"
OUT = os.path.join(ROOT, "SUBMISSION_GUIDE.md")

GITHUB_BASE = "https://github.com/basharalameed/land-classification-exam/blob/main/emotion-detector"


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read().rstrip("\n")


Q1_URL = "https://github.com/basharalameed/land-classification-exam/blob/main/emotion-detector/README.md"
Q6_URL = "https://github.com/basharalameed/land-classification-exam/blob/main/emotion-detector/EmotionDetection/__init__.py"

blocks = []
blocks.append("""# دليل إجابات الواجب — Emotion Detector (16 سؤالاً)

> **قاعدة ذهبية للمتعلمين:** كل سؤال "نص" يجب أن تَنسخ فيه **محتوى الملف** (الكود أو
> المخرجات) ثم تَلصقه في خانة الإجابة. **ممنوع منعاً باتاً لصق مسار الملف**
> (مثل `Task_2_watson_app\\2b_application_creation`) — المصحح يرفض هذا ويسجّله خللاً.
> المحتوى الجاهز كاملاً موجود في هذا الدليل وفي الملفات المسمّاة داخل كل مجلد Task.

---

## السؤال 1 — (URL) رابط README.md
**التعليمات:** انسخ الرابط التالي والصقه في خانة "Enter website URL":
```
%s
```

---

## السؤال 2 — (نص) كود تطبيق Watson NLP
**التعليمات:** انسخ الكود التالي **كاملاً** والصقه (نفس محتوى الملف `2a_emotion_detection`):
```python
%s
```

---

## السؤال 3 — (نص) مخرجات الاستيراد والاختبار
**التعليمات:** انسخ المخرجات التالية كما هي (نفس محتوى `2b_application_creation`):
```
%s
```

---

## السؤال 4 — (نص) كود تنسيق المخرجات
**التعليمات:** انسخ كود `emotion_detection.py` **كاملاً** (نفس محتوى `3a_output_formatting`).
ملاحظة فنية: السؤال يسأل عن الصيغة المعدّلة، والدالة `emotion_detector(text_to_analyze)`
الموجودة بالأسفل هي الصيغة النهائية التي تُرجع القاموس المطلوب:
```python
%s
```

---

## السؤال 5 — (نص) مخرجات تنسيق التطبيق
**التعليمات:** انسخ المخرجات التالية (نفس محتوى `3b_formatted_output_test`) — تُظهر
القاموس بالعواطف الخمس + `dominant_emotion`:
```
%s
```

---

## السؤال 6 — (URL) رابط __init__.py
**التعليمات:** انسخ الرابط والصقه في خانة "Enter website URL":
```
%s
```

---

## السؤال 7 — (نص) صلاحية حزمة EmotionDetection
**التعليمات:** انسخ المخرجات التالية (نفس محتوى `4b_packaging_test`) — تتضمن جملة
الاستيراد `from EmotionDetection.emotion_detection import emotion_detector` ودرجات المشاعر:
```
%s
```

---

## السؤال 8 — (نص) كود اختبارات الوحدة
**التعليمات:** انسخ محتوى `test_emotion_detection.py` **كاملاً** (نفس محتوى `5a_unit_testing`):
```python
%s
```

---

## السؤال 9 — (نص) مخرجات نجاح اختبارات الوحدة
**التعليمات:** انسخ المخرجات التالية كاملة (نفس محتوى `5b_unit_testing_result`) —
تُظهر الخمسة اختبارات `ok` والنتيجة `OK`:
```
%s
```

---

## السؤال 10 — (نص) كود نشر Flask
**التعليمات:** انسخ محتوى `server.py` **كاملاً** (نفس محتوى `6a_server`):
```python
%s
```

---

## السؤال 11 — (ملف صورة) لقطة النشر
**التعليمات:** استخدم زر **Upload** وارفع الملف التالي من حاسوبك (هو صورة فعلية، لا تنسخ
نصاً):
```
%%D:\امتحان\emotion-detector\Task_6_flask_deployment\6b_deployment_test.png
```

---

## السؤال 12 — (نص) كود معالجة الخطأ (status 400)
**التعليمات:** انسخ محتوى `7a_error_handling_function` **كاملاً** (وهو `emotion_detection.py`
بنهاية محدّثة تلتقط `ApiException` رمزها 400 وتُرجِع قيماً `None`):
```python
%s
```

---

## السؤال 13 — (نص) كود معالجة الإدخال الفارغ في الخادم
**التعليمات:** انسخ محتوى `7b_error_handling_server` (وهو `server.py` — لاحظ الجزء:
`if not text_to_analyze or not text_to_analyze.strip(): return "Invalid text! Please try again!"`):
```python
%s
```

---

## السؤال 14 — (ملف صورة) لقطة معالجة الأخطاء
**التعليمات:** استخدم زر **Upload** وارفع الملف التالي من حاسوبك:
```
%%D:\امتحان\emotion-detector\Task_7_error_handling\7c_error_handling_interface.png
```

---

## السؤال 15 — (نص) كود التحليل الساكن
**التعليمات:** انسخ محتوى `8a_server_modified` **كاملاً** (نفس `server.py` — لاحظ دالة
`run_static_code_analysis()` التي تنفّذ pylint عند التشغيل):
```python
%s
```

---

## السؤال 16 — (نص) نتيجة pylint
**التعليمات:** انسخ مخرجات pylint التالية كاملة (نفس محتوى `8b_static_code_analysis`) —
تُظهر العلامة **10.00/10**:
```
%s
```

---

## ملاحظات أخيرة للمتعلمين
1. لا تقلّل أو تختصر أي كود — المصحح يطلب **المحتوى الكامل** للملف.
2. الأسئلة 11 و14 ترفع **صوراً** (زر Upload) وليس نصاً.
3. الأسئلة 1 و6 **روابط** (خانة Enter website URL).
4. باقي الأسئلة (نص): انسخ من هذا الدليل أو من الملفات مباشرةً، والصق دون تعديل.
""")

parts = [
    Q1_URL,
    read(r"Task_2_watson_app\2a_emotion_detection"),
    read(r"Task_2_watson_app\2b_application_creation"),
    read(r"Task_3_output_format\3a_output_formatting"),
    read(r"Task_3_output_format\3b_formatted_output_test"),
    Q6_URL,
    read(r"Task_4_package\4b_packaging_test"),
    read(r"Task_5_unit_tests\5a_unit_testing"),
    read(r"Task_5_unit_tests\5b_unit_testing_result"),
    read(r"Task_6_flask_deployment\6a_server"),
    read(r"Task_7_error_handling\7a_error_handling_function"),
    read(r"Task_7_error_handling\7b_error_handling_server"),
    read(r"Task_8_static_analysis\8a_server_modified"),
    read(r"Task_8_static_analysis\8b_static_code_analysis"),
]

with open(OUT, "w", encoding="utf-8") as f:
    f.write(blocks[0] % tuple(parts))

print("written:", OUT)