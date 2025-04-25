from flask import Flask, render_template, request
import requests
import re
import os

app = Flask(__name__)
GATEWAY_URL = os.getenv("GATEWAY_URL", "http://gateway:5000/analyze") 

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            if 'file' in request.files and request.files['file'].filename != '':
                file = request.files['file']
                response = requests.post(GATEWAY_URL, files={"file": file})
            else:
                text = request.form.get("text", "").strip()
                if text:
                    response = requests.post(GATEWAY_URL, json={"text": text})
                else:
                    error = "Please enter text or upload an image."

            if response and response.status_code == 200:
                result = response.json()
                if result.get("interaction_result"):
                    # Preprocess interaction_result
                    result["interaction_result"] = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", result["interaction_result"])
                    result["interaction_result"] = result["interaction_result"].replace("\n", "<br>")
                if result.get("drugs_list") and len(result["drugs_list"]) < 2:
                    result["interaction_message"] = "At least 2 drugs should be added to check for interactions."
                else:
                    result["interaction_message"] = None
            elif response:
                error = f"Gateway error: {response.status_code}, {response.text}"
            else:
                error = "No response from the gateway service."

        except Exception as e:
            error = str(e)

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5004)
