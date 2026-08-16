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
