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