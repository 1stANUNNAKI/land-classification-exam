# PROJECT_MAP — مشروع امتحان (D:\امتحان)

## [TECH_STACK]
- Python 3.11.15 (uv) — بيئة افتراضية وحيدة: `D:\امتحان\.venv`
- TensorFlow 2.21.0 (CPU) + Keras 3
- PyTorch 2.13.0 (CPU) + torchvision 0.27
- Numpy 2.4, scikit-learn 1.9, matplotlib, opencv, scikit-image, pandas, pillow
- Jupyter (ipykernel مسجل باسم `exam-env`) + nbconvert (تنفيذ/تحقق)

## [DATA]
- المصدر: EuroSAT RGB (Zenodo, مؤرشفة في `data/EuroSAT_RGB.zip`)
- فئات الزراعة: AnnualCrop, PermanentCrop, Pasture
- فئات غير الزراعة: Forest, HerbaceousVegetation, Highway, Industrial, Residential, River, SeaLake
- الإخراج: `images_dataSAT/class_0_non_agri/` و `images_dataSAT/class_1_agri/` (3000 صورة لكل فئة)
- السكربت: `scripts/prepare_data.py` (إعادة البناء قابلة للتكرار; التحميل عبر curl بسبب 403/SSL في urllib)

## [SYSTEM_FLOW]
```
prepare_data.py → images_dataSAT
   │
   ├─ Q1: Memory vs Generator (تحميل كامل vs كسول) + shape/عرض/عدّ
   ├─ Q2: Keras paths+zip+custom_data_generator(batch 8) + augmentation
   ├─ Q3: PyTorch custom_transform + ImageFolder + loaders + عرض
   ├─ Q4: Keras CNN (4 Conv + 5 Dense) + generators + checkpoint + loss plot  → cnn_model.keras
   ├─ Q5: PyTorch CNN + 8 أسئلة نظرية + loss plot + all_preds/all_labels    → pytorch_cnn.pth
   ├─ Q6: print_metrics لكلا النموذجين + ROC + FN + F1
   ├─ Q7: Keras CNN-ViT hybrid (feature maps → ViT)                          → vit_hybrid.keras
   ├─ Q8: PyTorch CNN-ViT model & model_test (768/12/12, pre-LN) + مقارنة   → pytorch_vit_test.pth
   └─ Q9: تقييم نهائي print_metrics لكلا الـ CNN-ViT
```

## [ARCHITECTURE]
- كل Notebook مستقل بذاته (يعيد تعريف ما يحتاجه، ويحدد PROJECT_ROOT تلقائياً)
- أسماء المتغيرات مطابقة تماماً لمتطلبات الواجب (image_data, agri_images_paths, all_image_paths, temp,
  custom_data_generator, imagefolder_dataset, fnames, validation_generator, test_model, checkpoint,
  train_transform, val_transform, val_loader, all_preds, all_labels, cnn_model, feature_layer_name,
  build_cnn_vit_hybrid, hybrid_model, model_test, print_metrics ...)
- النماذج المحفوظة في `models/` (مشتركة بين Q4/Q6/Q7 و Q5/Q6 و Q8/Q9)
- ViT في PyTorch يستخدم **norm_first=True (pre-LN)** — ضروري لاستقرار عمق 12 (post-LN لا يتقارب)
- ViT في Keras: 16 توكن من خريطة الميزات (4x4x256) + position embedding + 4 blocks

## [ORPHANS & PENDING]
- (فارغ — كل شيء مكتمل ومتحقق)
- ملاحظة: مجلد `data/EuroSAT_RGB_extracted/` يحتفظ بالمصدر لإعادة البناء عند الحاجة

## [VERIFIED RESULTS] (CPU, 20 threads)
| Lab | متغير | النتيجة |
|-----|-------|---------|
| Q1 | shape صورة مفردة | (64,64,3) |
| Q4 | Keras CNN val | Acc 0.9158, F1 0.9123 |
| Q5 | PyTorch CNN val | Acc 0.9317, F1 0.9327 |
| Q7 | Keras CNN-ViT | فقدان متقارب، محفوظ |
| Q8 | base ViT / model_test (768-12-12) | val_acc 0.8525 / 0.8300، 9s / 86s |
| Q9 | Keras ViT / PyTorch ViT | Acc 0.9247 / 0.8300 |

## [CHANGELOG]
- 2026-08-16: إنشاء المشروع، البيانات، 9 notebooks منفذة بلا أخطاء، kernel exam-env