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