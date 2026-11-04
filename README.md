<p align="center">
  <img src="docs/assets/homepage-preview.png" alt="land-classification-exam — Home Page Preview" width="100%" />
</p>

# مشروع امتحان — تصنيف الأراضي الزراعية باستخدام CNN و Vision Transformer

واجب تقييمي مكوّن من **9 Labs** (Keras + PyTorch) حول التحميل الكفؤ للصور، الأغmentation،
تدريب CNN، وتكامل CNN-Transformer على بيانات الأقمار الصناعية (EuroSAT).

## البنية

```
D:\امتحان\
├── Question_1\Lab1_Comparison_Memory_Generator.ipynb          (10 نقاط)
├── Question_2\Lab2_Keras_Data_Loading_Augmentation.ipynb      (8 نقاط)
├── Question_3\Lab3_PyTorch_Data_Loading_Augmentation.ipynb    (10 نقاط)
├── Question_4\Lab4_Keras_Classifier.ipynb                     (12 نقاط)
├── Question_5\Lab5_PyTorch_Classifier.ipynb                   (20 نقاط)
├── Question_6\Lab6_Comparative_Analysis.ipynb                 (10 نقاط)
├── Question_7\Lab7_Vision_Transformers_Keras.ipynb            (10 نقاط)
├── Question_8\Lab8_Vision_Transformers_PyTorch.ipynb          (12 نقاط)
├── Question_9\Lab9_CNN_Transformer_Evaluation.ipynb           (8 نقاط)
├── images_dataSAT\class_0_non_agri\  و class_1_agri\          (البيانات)
├── models\                                                    (النماذج والرسوم)
├── scripts\prepare_data.py  +  build_notebooks.py
└── .venv                                                     (البيئة الكاملة)
```

## التشغيل

```powershell
D:\امتحان\.venv\Scripts\activate          # أو:
jupyter notebook                          # من مجلد المشروع، Kernel: Python (Exam 3.11)
```

كل notebook منفذ بالكامل ومخرجاتها محفوظة (صفر أخطاء). يمكن إعادة تنفيذ أي notebook كاملاً.

## إعادة البناء من الصفر

```powershell
# البيانات (إن حُذفت): تنزيل EuroSAT وبناء images_dataSAT
curl.exe -L -o D:\امتحان\data\EuroSAT_RGB.zip https://zenodo.org/records/7711810/files/EuroSAT_RGB.zip
D:\امتحان\.venv\Scripts\python.exe D:\امتحان\scripts\prepare_data.py

# إعادة توليد الـ notebooks (نادراً — يحتاج تعديل السكربت أولاً)
D:\امتحان\.venv\Scripts\python.exe D:\امتحان\scripts\build_notebooks.py
```

## ملاحظات جودة

- أسماء المتغيرات مطابقة حرفياً لمتطلبات الواجب (يسهّل التصحيح الآلي)
- نماذج Module 3 (Q7/Q9) محفوظة ومحمّلة من `models/` — لا حاجة لإعادة التدريب
- تدريب كامل يعمل على CPU فقط (20 خيطاً) — زمن Q8 الأقصى ~86 ثانية
- ViT العميق (768/12/12) يعمل بـ pre-LN (`norm_first=True`) لضمان التقارب