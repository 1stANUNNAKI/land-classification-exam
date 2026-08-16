/**
 * Sends the statement to the /emotionDetector endpoint and shows the
 * response returned by the server inside the system_response container.
 * Error responses are displayed in red.
 */
function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const responseDiv = document.getElementById("system_response");
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            responseDiv.innerHTML = this.responseText;
            if (this.responseText.startsWith("Invalid text")) {
                responseDiv.style.color = "#dc3545";
            } else {
                responseDiv.style.color = "#212529";
            }
        }
    };
    xhttp.open(
        "GET",
        "emotionDetector?textToAnalyze=" + encodeURIComponent(textToAnalyze),
        true
    );
    xhttp.send();
}