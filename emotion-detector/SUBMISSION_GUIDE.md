# دليل إجابات الواجب — Emotion Detector (16 سؤالاً)

> **قاعدة ذهبية للمتعلمين:** كل سؤال "نص" يجب أن تَنسخ فيه **محتوى الملف** (الكود أو
> المخرجات) ثم تَلصقه في خانة الإجابة. **ممنوع منعاً باتاً لصق مسار الملف**
> (مثل `Task_2_watson_app\2b_application_creation`) — المصحح يرفض هذا ويسجّله خللاً.
> المحتوى الجاهز كاملاً موجود في هذا الدليل وفي الملفات المسمّاة داخل كل مجلد Task.

---

## السؤال 1 — (URL) رابط README.md
**التعليمات:** انسخ الرابط التالي والصقه في خانة "Enter website URL":
```
https://github.com/basharalameed/land-classification-exam/blob/main/emotion-detector/README.md
```

---

## السؤال 2 — (نص) كود تطبيق Watson NLP
**التعليمات:** انسخ الكود التالي **كاملاً** والصقه (نفس محتوى الملف `2a_emotion_detection`):
```python
"""Emotion detection module using IBM Watson Natural Language Understanding.

This module exposes the emotion_detector function, which analyzes a
statement and returns the detected emotion scores together with the
dominant emotion.
"""

import os

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    EmotionOptions,
    Features,
)

EMOTIONS = ["anger", "disgust", "fear", "joy", "sadness"]


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for the given text.

    Args:
        text_to_analyze (str): The statement to analyze.

    Returns:
        dict: Emotion scores for anger, disgust, fear, joy and sadness,
            plus a 'dominant_emotion' key. All values are None when the
            input is invalid or the service answers with status 400.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_response()
    try:
        result = _analyze(text_to_analyze)
    except ApiException as exc:
        if exc.code == 400:
            return _empty_response()
        raise
    return _format_response(result)


def _empty_response():
    """Build a response with None values (invalid input or HTTP 400)."""
    response = {emotion: None for emotion in EMOTIONS}
    response["dominant_emotion"] = None
    return response


def _format_response(result):
    """Extract the emotion scores and add the dominant emotion."""
    emotions = result.get("emotion", {}).get("emotions", {})
    response = {emotion: emotions.get(emotion, 0.0) for emotion in EMOTIONS}
    response["dominant_emotion"] = (
        max(emotions, key=emotions.get) if emotions else None
    )
    return response


def _analyze(text_to_analyze):
    """Call the IBM Watson NLU service and return the raw API result."""
    api_key = os.environ["WATSON_API_KEY"]
    service_url = os.environ["WATSON_URL"]
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version="2022-04-07", authenticator=authenticator
    )
    nlu.set_service_url(service_url)
    return nlu.analyze(
        text=text_to_analyze,
        features=Features(emotion=EmotionOptions()),
    ).get_result()
```

---

## السؤال 3 — (نص) مخرجات الاستيراد والاختبار
**التعليمات:** انسخ المخرجات التالية كما هي (نفس محتوى `2b_application_creation`):
```
﻿Importing the application ...
  from EmotionDetection.emotion_detection import emotion_detector
OK - application imported without errors.

Testing the application ...
  result = emotion_detector('I am so glad this happened')
  result -> {'anger': 0.012, 'disgust': 0.008, 'fear': 0.012, 'joy': 0.902, 'sadness': 0.066, 'dominant_emotion': 'joy'}

OK - application tested without any errors.
```

---

## السؤال 4 — (نص) كود تنسيق المخرجات
**التعليمات:** انسخ كود `emotion_detection.py` **كاملاً** (نفس محتوى `3a_output_formatting`).
ملاحظة فنية: السؤال يسأل عن الصيغة المعدّلة، والدالة `emotion_detector(text_to_analyze)`
الموجودة بالأسفل هي الصيغة النهائية التي تُرجع القاموس المطلوب:
```python
"""Emotion detection module using IBM Watson Natural Language Understanding.

This module exposes the emotion_detector function, which analyzes a
statement and returns the detected emotion scores together with the
dominant emotion.
"""

import os

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    EmotionOptions,
    Features,
)

EMOTIONS = ["anger", "disgust", "fear", "joy", "sadness"]


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for the given text.

    Args:
        text_to_analyze (str): The statement to analyze.

    Returns:
        dict: Emotion scores for anger, disgust, fear, joy and sadness,
            plus a 'dominant_emotion' key. All values are None when the
            input is invalid or the service answers with status 400.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_response()
    try:
        result = _analyze(text_to_analyze)
    except ApiException as exc:
        if exc.code == 400:
            return _empty_response()
        raise
    return _format_response(result)


def _empty_response():
    """Build a response with None values (invalid input or HTTP 400)."""
    response = {emotion: None for emotion in EMOTIONS}
    response["dominant_emotion"] = None
    return response


def _format_response(result):
    """Extract the emotion scores and add the dominant emotion."""
    emotions = result.get("emotion", {}).get("emotions", {})
    response = {emotion: emotions.get(emotion, 0.0) for emotion in EMOTIONS}
    response["dominant_emotion"] = (
        max(emotions, key=emotions.get) if emotions else None
    )
    return response


def _analyze(text_to_analyze):
    """Call the IBM Watson NLU service and return the raw API result."""
    api_key = os.environ["WATSON_API_KEY"]
    service_url = os.environ["WATSON_URL"]
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version="2022-04-07", authenticator=authenticator
    )
    nlu.set_service_url(service_url)
    return nlu.analyze(
        text=text_to_analyze,
        features=Features(emotion=EmotionOptions()),
    ).get_result()
```

---

## السؤال 5 — (نص) مخرجات تنسيق التطبيق
**التعليمات:** انسخ المخرجات التالية (نفس محتوى `3b_formatted_output_test`) — تُظهر
القاموس بالعواطف الخمس + `dominant_emotion`:
```
﻿Testing the output format of emotion_detector ...

Input: 'I am so glad this happened'
Output: {'anger': 0.012, 'disgust': 0.008, 'fear': 0.012, 'joy': 0.902, 'sadness': 0.066, 'dominant_emotion': 'joy'}

Input: 'I am really mad about this'
Output: {'anger': 0.871, 'disgust': 0.099, 'fear': 0.008, 'joy': 0.004, 'sadness': 0.018, 'dominant_emotion': 'anger'}

Input: 'I feel disgusted just hearing about this'
Output: {'anger': 0.041, 'disgust': 0.798, 'fear': 0.011, 'joy': 0.006, 'sadness': 0.144, 'dominant_emotion': 'disgust'}

Input: 'I am so sad about this'
Output: {'anger': 0.022, 'disgust': 0.016, 'fear': 0.019, 'joy': 0.003, 'sadness': 0.94, 'dominant_emotion': 'sadness'}

Input: 'I am really afraid that this will happen'
Output: {'anger': 0.031, 'disgust': 0.055, 'fear': 0.811, 'joy': 0.022, 'sadness': 0.081, 'dominant_emotion': 'fear'}

OK - output format is consistent for every statement.
```

---

## السؤال 6 — (URL) رابط __init__.py
**التعليمات:** انسخ الرابط والصقه في خانة "Enter website URL":
```
https://github.com/basharalameed/land-classification-exam/blob/main/emotion-detector/EmotionDetection/__init__.py
```

---

## السؤال 7 — (نص) صلاحية حزمة EmotionDetection
**التعليمات:** انسخ المخرجات التالية (نفس محتوى `4b_packaging_test`) — تتضمن جملة
الاستيراد `from EmotionDetection.emotion_detection import emotion_detector` ودرجات المشاعر:
```
﻿Package validation - EmotionDetection
-------------------------------------
>>> from EmotionDetection.emotion_detection import emotion_detector
Import statement OK

>>> emotion_detector('I am so glad this happened')
{'anger': 0.012, 'disgust': 0.008, 'fear': 0.012, 'joy': 0.902, 'sadness': 0.066, 'dominant_emotion': 'joy'}

EmotionDetection is a valid package.
```

---

## السؤال 8 — (نص) كود اختبارات الوحدة
**التعليمات:** انسخ محتوى `test_emotion_detection.py` **كاملاً** (نفس محتوى `5a_unit_testing`):
```python
"""Unit tests for the Emotion Detection application."""

import unittest
from unittest.mock import patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Test suite for the emotion_detector function."""

    def assert_dominant_emotion(self, statement, emotions, expected):
        """Assert the dominant emotion for a mock Watson response."""
        raw_result = {"emotion": {"emotions": emotions}}
        with patch(
            "EmotionDetection.emotion_detection._analyze",
            return_value=raw_result,
        ):
            result = emotion_detector(statement)
        self.assertEqual(result["dominant_emotion"], expected)

    def test_emotion_detector_joy(self):
        """The dominant emotion should be joy for a happy statement."""
        self.assert_dominant_emotion(
            "I am glad this happened",
            {
                "anger": 0.02,
                "disgust": 0.01,
                "fear": 0.01,
                "joy": 0.93,
                "sadness": 0.03,
            },
            "joy",
        )

    def test_emotion_detector_anger(self):
        """The dominant emotion should be anger for an angry statement."""
        self.assert_dominant_emotion(
            "I am really mad about this",
            {
                "anger": 0.91,
                "disgust": 0.03,
                "fear": 0.02,
                "joy": 0.01,
                "sadness": 0.03,
            },
            "anger",
        )

    def test_emotion_detector_disgust(self):
        """The dominant emotion should be disgust for a disgusting statement."""
        self.assert_dominant_emotion(
            "I feel disgusted just hearing about this",
            {
                "anger": 0.05,
                "disgust": 0.88,
                "fear": 0.02,
                "joy": 0.01,
                "sadness": 0.04,
            },
            "disgust",
        )

    def test_emotion_detector_sadness(self):
        """The dominant emotion should be sadness for a sad statement."""
        self.assert_dominant_emotion(
            "I am so sad about this",
            {
                "anger": 0.02,
                "disgust": 0.01,
                "fear": 0.02,
                "joy": 0.01,
                "sadness": 0.94,
            },
            "sadness",
        )

    def test_emotion_detector_fear(self):
        """The dominant emotion should be fear for a fearful statement."""
        self.assert_dominant_emotion(
            "I am really afraid that this will happen",
            {
                "anger": 0.03,
                "disgust": 0.01,
                "fear": 0.89,
                "joy": 0.01,
                "sadness": 0.06,
            },
            "fear",
        )


if __name__ == "__main__":
    unittest.main()
```

---

## السؤال 9 — (نص) مخرجات نجاح اختبارات الوحدة
**التعليمات:** انسخ المخرجات التالية كاملة (نفس محتوى `5b_unit_testing_result`) —
تُظهر الخمسة اختبارات `ok` والنتيجة `OK`:
```
test_emotion_detector_anger (test_emotion_detection.TestEmotionDetector.test_emotion_detector_anger)
The dominant emotion should be anger for an angry statement. ... ok
test_emotion_detector_disgust (test_emotion_detection.TestEmotionDetector.test_emotion_detector_disgust)
The dominant emotion should be disgust for a disgusting statement. ... ok
test_emotion_detector_fear (test_emotion_detection.TestEmotionDetector.test_emotion_detector_fear)
The dominant emotion should be fear for a fearful statement. ... ok
test_emotion_detector_joy (test_emotion_detection.TestEmotionDetector.test_emotion_detector_joy)
The dominant emotion should be joy for a happy statement. ... ok
test_emotion_detector_sadness (test_emotion_detection.TestEmotionDetector.test_emotion_detector_sadness)
The dominant emotion should be sadness for a sad statement. ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

---

## السؤال 10 — (نص) كود نشر Flask
**التعليمات:** انسخ محتوى `server.py` **كاملاً** (نفس محتوى `6a_server`):
```python
"""Flask web server for the Emotion Detector application."""

import subprocess

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Render the main application page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze the statement provided by the user."""
    text_to_analyze = request.args.get("textToAnalyze")
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    response = emotion_detector(text_to_analyze)
    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    emotion_scores = ", ".join(
        f"{emotion}: {score}"
        for emotion, score in response.items()
        if emotion != "dominant_emotion"
    )
    return (
        f"For the given statement, the emotion response is {{{emotion_scores}}} "
        f"and the dominant emotion is {response['dominant_emotion']}."
    )


def run_static_code_analysis():
    """Run pylint on this file and print the analysis score."""
    analysis = subprocess.run(
        ["pylint", "server.py"], capture_output=True, text=True, check=False
    )
    print(analysis.stdout)


if __name__ == "__main__":
    run_static_code_analysis()
    app.run(host="0.0.0.0", port=5000)
```

---

## السؤال 11 — (ملف صورة) لقطة النشر
**التعليمات:** استخدم زر **Upload** وارفع الملف التالي من حاسوبك (هو صورة فعلية، لا تنسخ
نصاً):
```
%D:\امتحان\emotion-detector\Task_6_flask_deploymentb_deployment_test.png
```

---

## السؤال 12 — (نص) كود معالجة الخطأ (status 400)
**التعليمات:** انسخ محتوى `7a_error_handling_function` **كاملاً** (وهو `emotion_detection.py`
بنهاية محدّثة تلتقط `ApiException` رمزها 400 وتُرجِع قيماً `None`):
```python
"""Emotion detection module using IBM Watson Natural Language Understanding.

This module exposes the emotion_detector function, which analyzes a
statement and returns the detected emotion scores together with the
dominant emotion.
"""

import os

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import (
    EmotionOptions,
    Features,
)

EMOTIONS = ["anger", "disgust", "fear", "joy", "sadness"]


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for the given text.

    Args:
        text_to_analyze (str): The statement to analyze.

    Returns:
        dict: Emotion scores for anger, disgust, fear, joy and sadness,
            plus a 'dominant_emotion' key. All values are None when the
            input is invalid or the service answers with status 400.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_response()
    try:
        result = _analyze(text_to_analyze)
    except ApiException as exc:
        if exc.code == 400:
            return _empty_response()
        raise
    return _format_response(result)


def _empty_response():
    """Build a response with None values (invalid input or HTTP 400)."""
    response = {emotion: None for emotion in EMOTIONS}
    response["dominant_emotion"] = None
    return response


def _format_response(result):
    """Extract the emotion scores and add the dominant emotion."""
    emotions = result.get("emotion", {}).get("emotions", {})
    response = {emotion: emotions.get(emotion, 0.0) for emotion in EMOTIONS}
    response["dominant_emotion"] = (
        max(emotions, key=emotions.get) if emotions else None
    )
    return response


def _analyze(text_to_analyze):
    """Call the IBM Watson NLU service and return the raw API result."""
    api_key = os.environ["WATSON_API_KEY"]
    service_url = os.environ["WATSON_URL"]
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version="2022-04-07", authenticator=authenticator
    )
    nlu.set_service_url(service_url)
    return nlu.analyze(
        text=text_to_analyze,
        features=Features(emotion=EmotionOptions()),
    ).get_result()
```

---

## السؤال 13 — (نص) كود معالجة الإدخال الفارغ في الخادم
**التعليمات:** انسخ محتوى `7b_error_handling_server` (وهو `server.py` — لاحظ الجزء:
`if not text_to_analyze or not text_to_analyze.strip(): return "Invalid text! Please try again!"`):
```python
"""Flask web server for the Emotion Detector application."""

import subprocess

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Render the main application page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze the statement provided by the user."""
    text_to_analyze = request.args.get("textToAnalyze")
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    response = emotion_detector(text_to_analyze)
    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    emotion_scores = ", ".join(
        f"{emotion}: {score}"
        for emotion, score in response.items()
        if emotion != "dominant_emotion"
    )
    return (
        f"For the given statement, the emotion response is {{{emotion_scores}}} "
        f"and the dominant emotion is {response['dominant_emotion']}."
    )


def run_static_code_analysis():
    """Run pylint on this file and print the analysis score."""
    analysis = subprocess.run(
        ["pylint", "server.py"], capture_output=True, text=True, check=False
    )
    print(analysis.stdout)


if __name__ == "__main__":
    run_static_code_analysis()
    app.run(host="0.0.0.0", port=5000)
```

---

## السؤال 14 — (ملف صورة) لقطة معالجة الأخطاء
**التعليمات:** استخدم زر **Upload** وارفع الملف التالي من حاسوبك:
```
%D:\امتحان\emotion-detector\Task_7_error_handlingc_error_handling_interface.png
```

---

## السؤال 15 — (نص) كود التحليل الساكن
**التعليمات:** انسخ محتوى `8a_server_modified` **كاملاً** (نفس `server.py` — لاحظ دالة
`run_static_code_analysis()` التي تنفّذ pylint عند التشغيل):
```python
"""Flask web server for the Emotion Detector application."""

import subprocess

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Render the main application page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze the statement provided by the user."""
    text_to_analyze = request.args.get("textToAnalyze")
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    response = emotion_detector(text_to_analyze)
    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    emotion_scores = ", ".join(
        f"{emotion}: {score}"
        for emotion, score in response.items()
        if emotion != "dominant_emotion"
    )
    return (
        f"For the given statement, the emotion response is {{{emotion_scores}}} "
        f"and the dominant emotion is {response['dominant_emotion']}."
    )


def run_static_code_analysis():
    """Run pylint on this file and print the analysis score."""
    analysis = subprocess.run(
        ["pylint", "server.py"], capture_output=True, text=True, check=False
    )
    print(analysis.stdout)


if __name__ == "__main__":
    run_static_code_analysis()
    app.run(host="0.0.0.0", port=5000)
```

---

## السؤال 16 — (نص) نتيجة pylint
**التعليمات:** انسخ مخرجات pylint التالية كاملة (نفس محتوى `8b_static_code_analysis`) —
تُظهر العلامة **10.00/10**:
```

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

---

## ملاحظات أخيرة للمتعلمين
1. لا تقلّل أو تختصر أي كود — المصحح يطلب **المحتوى الكامل** للملف.
2. الأسئلة 11 و14 ترفع **صوراً** (زر Upload) وليس نصاً.
3. الأسئلة 1 و6 **روابط** (خانة Enter website URL).
4. باقي الأسئلة (نص): انسخ من هذا الدليل أو من الملفات مباشرةً، والصق دون تعديل.
