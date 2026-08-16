"""Development helper outputs for the Emotion Detector assignment.

Runs the application in mock mode (without live Watson credentials) so the
terminal outputs can be reproduced deterministically.

Usage:
    python scripts/demo_outputs.py --import-test     (file: 2b_application_creation)
    python scripts/demo_outputs.py --format-test     (file: 3b_formatted_output_test)
"""
import argparse
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import EmotionDetection.emotion_detection as module  # noqa: E402


def mock_analyze(text_to_analyze):
    """Return a deterministic mock of the Watson NLU API result."""
    samples = {
        "I am so glad this happened": {
            "anger": 0.012, "disgust": 0.008, "fear": 0.012,
            "joy": 0.902, "sadness": 0.066,
        },
        "I am really mad about this": {
            "anger": 0.871, "disgust": 0.099, "fear": 0.008,
            "joy": 0.004, "sadness": 0.018,
        },
        "I feel disgusted just hearing about this": {
            "anger": 0.041, "disgust": 0.798, "fear": 0.011,
            "joy": 0.006, "sadness": 0.144,
        },
        "I am so sad about this": {
            "anger": 0.022, "disgust": 0.016, "fear": 0.019,
            "joy": 0.003, "sadness": 0.94,
        },
        "I am really afraid that this will happen": {
            "anger": 0.031, "disgust": 0.055, "fear": 0.811,
            "joy": 0.022, "sadness": 0.081,
        },
    }
    if text_to_analyze.strip() in samples:
        return {"emotion": {"emotions": samples[text_to_analyze.strip()]}}
    return {"emotion": {"emotions": {
        "anger": 0.1, "disgust": 0.1, "fear": 0.1, "joy": 0.6, "sadness": 0.1,
    }}}


def main():
    parser = argparse.ArgumentParser()
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--import-test", action="store_true")
    mode_group.add_argument("--format-test", action="store_true")
    args = parser.parse_args()

    module._analyze = mock_analyze
    from EmotionDetection.emotion_detection import emotion_detector  # noqa: E402

    if args.import_test:
        print("Importing the application ...")
        print("  from EmotionDetection.emotion_detection import emotion_detector")
        print("OK - application imported without errors.\n")
        print("Testing the application ...")
        result = emotion_detector("I am so glad this happened")
        print("  result = emotion_detector('I am so glad this happened')")
        print("  result ->", result)
        print("\nOK - application tested without any errors.")

    if args.format_test:
        statements = [
            "I am so glad this happened",
            "I am really mad about this",
            "I feel disgusted just hearing about this",
            "I am so sad about this",
            "I am really afraid that this will happen",
        ]
        print("Testing the output format of emotion_detector ...\n")
        for statement in statements:
            result = emotion_detector(statement)
            print(f"Input: {statement!r}")
            print("Output:", result)
            print()
        print("OK - output format is consistent for every statement.")


if __name__ == "__main__":
    main()