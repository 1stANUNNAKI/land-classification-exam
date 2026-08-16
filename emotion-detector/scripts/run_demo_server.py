"""Development server with a mocked Watson response (screenshots only).

Runs the real Flask application but replaces the Watson call with a
deterministic mock so the web interface can be captured without live
credentials. The production code in EmotionDetection/ is untouched.

Usage:
    python scripts/run_demo_server.py
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import EmotionDetection.emotion_detection as module  # noqa: E402


def mock_analyze(text_to_analyze):
    """Return a deterministic mock of the Watson NLU API result."""
    return {"emotion": {"emotions": {
        "anger": 0.012, "disgust": 0.008, "fear": 0.012,
        "joy": 0.902, "sadness": 0.066,
    }}}


module._analyze = mock_analyze

from EmotionDetection.server import app  # noqa: E402

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)